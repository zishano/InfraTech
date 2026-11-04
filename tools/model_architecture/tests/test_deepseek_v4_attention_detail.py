"""Guard model-specific branch semantics and paired native detail pages."""
import itertools
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
sys.path.insert(0,str(BASE))
import model_architecture as a
import png_export as p

class AttentionDetailTests(unittest.TestCase):
    def graph(self,kind):
        return a.read(BASE/'examples'/f'deepseek_v4_flash_{kind}.graph.json')

    def test_values_bypass_gate_softmax_and_ports_resolve(self):
        for kind in ['csa','hca']:
            g=self.graph(kind);a.validate(g)
            nodes={n['id']:n for n in g['nodes']}
            edges={(e['source'],e['target']) for e in g['edges']}
            self.assertIn(('comp_value_window','comp_mul'),edges)
            self.assertIn(('comp_softmax','comp_mul'),edges)
            self.assertNotIn(('comp_value_window','comp_softmax'),edges)
            for binding in g['port_bindings'].values():
                self.assertIn(binding['source'],nodes);self.assertIn(binding['target'],nodes)
            self.assertIn(('attn_sink','attn_softmax'),edges)
            self.assertNotIn(('attn_sink','attn_values'),edges)
            for key in ['attn_gather','attn_softmax','attn_values','attn_sink']:
                self.assertEqual(nodes[key]['evidence'][0]['source'],'kernel')
            ops=[n for n in nodes.values() if n.get('kind')!='decoration']
            for l,r in itertools.combinations(ops,2):
                x,y,w,h=l['box'];xx,yy,ww,hh=r['box']
                self.assertFalse(min(x+w,xx+ww)-max(x,xx)>1 and min(y+h,yy+hh)-max(y,yy)>1,(kind,l['id'],r['id']))

    def test_overlap_and_indexer_are_csa_specific(self):
        c=self.graph('csa');h=self.graph('hca')
        cn={n['id']:n for n in c['nodes']};hn={n['id']:n for n in h['nodes']}
        edges={(e['source'],e['target']) for e in c['edges']}
        self.assertEqual(c['compression_ratio'],4);self.assertEqual(h['compression_ratio'],128)
        self.assertEqual(c['main_compressor_state_shape'],['B',8,1024])
        self.assertEqual(h['main_compressor_state_shape'],['B',128,512])
        self.assertEqual(c['indexer_state_shape'],['B',8,256])
        self.assertIn(('idx_window','idx_pool'),edges)
        self.assertIn(('idx_w_ready','idx_head_sum'),edges)
        self.assertIn('idx_q_input',cn);self.assertIn('idx_key_cache',cn)
        self.assertFalse(any(k.startswith('idx_') for k in hn))
        self.assertEqual(c['window_examples'][0],dict(j=1,ca_tokens=[0,1,2,3],cb_tokens=[4,5,6,7],rope_position=4))
        self.assertEqual(h['window_examples'][1],dict(j=1,first_token=128,last_token=255,rope_position=128))
        self.assertIn('No query-specific pruning',cn['comp_bank']['description'])
        self.assertIn('floor((t+1)/128)',hn['hist_no_prune']['label'])

    def test_operator_presentation_keeps_annotations_outside_labels(self):
        for kind in ['csa','hca']:
            graph=self.graph(kind)
            self.assertEqual(graph['presentation']['reference'],'models/deepseek_v4/deepseek_v4_architecture.jpg')
            for node in graph['nodes']:
                if node.get('kind')=='decoration':continue
                self.assertLessEqual(len(node['label'].splitlines()),2,node['id'])
                self.assertLessEqual(len(node['label']),80,node['id'])
                self.assertTrue(node['description'])
            root=ET.parse(REPO/'models/deepseek_v4/flash'/f'deepseek_v4_flash_{kind}.drawio').getroot()
            cells={c.get('id'):c for c in root.iter('mxCell')}
            self.assertEqual(cells['comp_bank'].get('tooltip'),next(n['description'] for n in graph['nodes'] if n['id']=='comp_bank'))

    def test_modules_have_separate_lanes_and_attention_is_central(self):
        for kind in ['csa','hca']:
            graph=self.graph(kind);nodes={n['id']:n for n in graph['nodes']}
            left=nodes['compressor']['box'];center=nodes['attention']['box'];right=nodes['middle']['box']
            self.assertLess(left[0]+left[2],center[0])
            self.assertLess(center[0]+center[2],right[0])
            self.assertLess(left[1]+left[3],nodes['states']['box'][1])
            self.assertGreater(graph['width'],graph['height'])

    def test_every_detail_png_matches_native_xml_and_master_page(self):
        folder=REPO/'models/deepseek_v4/flash'
        master=ET.parse(folder/'deepseek_v4_flash.drawio').getroot().findall('diagram')
        self.assertEqual([d.get('name') for d in master],['Overview','CSA detail','HCA detail'])
        for page,kind in zip(master[1:],['csa','hca']):
            stem=f'deepseek_v4_flash_{kind}'
            g=self.graph(kind)
            m=p.verify(folder/(stem+'.drawio'),folder/(stem+'.png'),folder/(stem+'.export.json'))
            self.assertEqual((m['vertices'],m['edges']),(len(g['nodes']),len(g['edges'])))
            p.validate_layout(a.read(folder/(stem+'.layout.json')))
            standalone=ET.parse(folder/(stem+'.drawio')).getroot().find('diagram/mxGraphModel')
            self.assertEqual(ET.tostring(page.find('mxGraphModel')),ET.tostring(standalone))
            self.assertNotIn('data:image',ET.tostring(standalone).decode())

if __name__=='__main__':unittest.main()
