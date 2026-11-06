"""Source-pair checks are offline; actual mxGraph export is exercised separately."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
spec=importlib.util.spec_from_file_location('png_export',BASE/'png_export.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class ExportTests(unittest.TestCase):
    def test_native_reconstruction_is_not_embedded_image(self):
        p=REPO/'models/kimi_k_3/architecture_study/kimi_k3_design_preview_v2.drawio'
        model,vertices,edges=a.inspect_drawio(p)
        self.assertGreater(vertices,140)
        self.assertGreater(edges,120)
        cells={c.get('id'):c for c in model.findall('./root/mxCell')}
        # The five KDA inputs and sixth output gate remain distinct native paths.
        for name in ['q','k','v','alpha','beta']:
            self.assertIn('kda_port_'+name,cells)
        graph_edges=[(c.get('source'),c.get('target')) for c in cells.values() if c.get('edge')=='1']
        self.assertIn(('kda_gate_sigmoid','kda_product'),graph_edges)
        self.assertNotIn(('k_out','m_ar1'),graph_edges)
        self.assertNotIn(('m_out','lm_repeat'),graph_edges)
        self.assertIn(('lm_fused','lm_repeat'),graph_edges)

    def test_reject_embedded_raster_and_compressed_pages(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.drawio'
            p.write_text('<mxfile><diagram><mxGraphModel><root><mxCell id="image" vertex="1" style="shape=image;image=data:png;base64,AA"/></root></mxGraphModel></diagram></mxfile>')
            with self.assertRaisesRegex(ValueError,'image'):a.inspect_drawio(p)
            p.write_text('<mxfile><diagram>compressed-data</diagram></mxfile>')
            with self.assertRaisesRegex(ValueError,'uncompressed'):a.inspect_drawio(p)

    def test_pair_verification_detects_changes_on_either_side(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);xml=d/'diagram.drawio';png=d/'diagram.png';meta=d/'diagram.export.json'
            xml.write_bytes(b'original xml');png.write_bytes(b'original png')
            meta.write_text(json.dumps(dict(version=1,drawio_sha256=a.digest(xml),png_sha256=a.digest(png))))
            a.verify(xml,png,meta)
            xml.write_bytes(b'changed xml')
            with self.assertRaisesRegex(ValueError,'draw.io changed'):a.verify(xml,png,meta)
            xml.write_bytes(b'original xml');png.write_bytes(b'changed png')
            with self.assertRaisesRegex(ValueError,'PNG changed'):a.verify(xml,png,meta)

    def test_committed_png_and_xml_are_one_export_pair(self):
        p=REPO/'models/kimi_k_3/architecture_study'
        xml=p/'kimi_k3_design_preview_v2.drawio'
        for name in ['kimi_k3_design_preview_v2','kimi_k3_design_preview']:
            m=a.verify(xml,p/(name+'.png'),p/(name+'.export.json'))
            self.assertEqual(m['renderer'],'mxGraph 4.2.2 / Chromium')
            _,nv,ne=a.inspect_drawio(xml)
            self.assertEqual((m['vertices'],m['edges']),(nv,ne))

    def test_measured_layout_failures_are_rejected(self):
        clean=dict(text_overflow=[],tight_text=[],nonorthogonal_segments=[],edge_node_crossings=[])
        a.validate_layout(clean)
        for key in clean:
            broken=dict(clean);broken[key]=[dict(id='bad-node-or-edge')]
            with self.assertRaisesRegex(ValueError,key):a.validate_layout(broken)
        for key in ('edge_label_node_overlaps','edge_label_overlaps'):
            broken=dict(clean);broken[key]=[dict(id='shape-label',node='projection')]
            with self.assertRaisesRegex(ValueError,key):a.validate_layout(broken)
        with self.assertRaisesRegex(ValueError,'Missing'):a.validate_layout({})

    def test_branch_centers_and_explicit_ports_stay_aligned(self):
        g=json.loads((BASE/'examples/kimi_k3.graph.json').read_text())
        nodes={n['id']:n for n in g['nodes']}
        def center(key):
            x,y,w,h=nodes[key]['box'];return x+w/2
        for group in [
            ['kda_alpha_down','kda_alpha_up','kda_alpha_bias','kda_alpha_scale','kda_alpha_sigmoid','kda_alpha_exp','kda_port_alpha'],
            ['kda_beta_linear','kda_beta_sigmoid','kda_port_beta'],
            ['kda_norm','kda_product','kda_wo'],
            ['mla_compress','mla_cache','mla_reconstruct'],
            ['mla_gate','mla_sigmoid'],
            ['mla_mul','mla_wo'],
            ['moe_down','moe_bank','moe_weighted','moe_norm','moe_up','moe_sum','moe_y'],
            ['mini_images','mini_pool','mini_projector','mini_visvec']]:
            self.assertEqual(len({round(center(k),4) for k in group}),1,group)
        for edge in g['edges']:
            if edge['target']=='kda_core' and edge['source'].startswith('kda_port_') or edge['target']=='mla_attention' and edge['source'].startswith('mla_port_'):
                src=nodes[edge['source']]['box'];dst=nodes[edge['target']]['box']
                self.assertAlmostEqual(src[0]+src[2]*edge['ports'][0],dst[0]+dst[2]*edge['ports'][2])
        # Native fonts must stay readable without relying on 6.5px imported text.
        import re
        for n in g['nodes']:
            match=re.search(r'fontSize=([\d.]+)',n.get('style',''))
            if match and n['label']:self.assertGreaterEqual(float(match.group(1)),13,n['id'])

    def test_published_layout_report_has_no_overflow_or_diagonal(self):
        p=REPO/'models/kimi_k_3/architecture_study'
        report=json.loads((p/'kimi_k3_design_preview_v2.layout.json').read_text())
        a.validate_layout(report)
        self.assertEqual(len(report['routes']),131)

if __name__=='__main__':unittest.main()
