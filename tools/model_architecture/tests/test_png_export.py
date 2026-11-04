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

if __name__=='__main__':unittest.main()
