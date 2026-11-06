"""Checkpoint-specific topology and direct-export checks for GLM-5.1."""
import itertools
from pathlib import Path
import sys
import unittest
BASE=Path(__file__).resolve().parents[1];REPO=BASE.parents[1]
sys.path.insert(0,str(BASE))
import model_architecture as a
import png_export as p

class GLM51Tests(unittest.TestCase):
    folder=REPO/'models/glm_5_1'
    def graph(self):return a.read(BASE/'examples/glm51.graph.json')
    def test_checkpoint_schedule_and_index_agree(self):
        c=a.read(self.folder/'official_config.json');s=a.read(self.folder/'checkpoint_summary.json')
        self.assertEqual((c['num_hidden_layers'],c['first_k_dense_replace'],c['num_nextn_predict_layers']),(78,3,1))
        self.assertEqual((s['tensor_names'],s['shards']),(59870,282))
        self.assertEqual(len(s['per_layer']),79)
        for layer in s['per_layer']:
            i=layer['layer_index'];self.assertTrue(layer['indexer'])
            self.assertEqual(layer['dense_ffn'],i<3)
            self.assertEqual(layer['routed_experts'],i>=3)
        self.assertEqual(s['per_layer'][-1]['tensors'],791)
    def test_rope_indexer_experts_and_residual_paths(self):
        g=self.graph();a.validate(g);n={n['id']:n for n in g['nodes']};edges={(e['source'],e['target']) for e in g['edges']}
        for pair in [('idx_qr','idx_qp'),('idx_h','idx_kp'),('idx_h','idx_wp'),('idx_kn','idx_krpe'),('idx_w','idx_sum'),('attn_kvrope','attn_cache'),('main_x','main_add1'),('main_add1','main_add2'),('moe_h','moe_shared'),('moe_shared','moe_add'),('mlp_silu','mlp_mul'),('mlp_up','mlp_mul')]:self.assertIn(pair,edges)
        self.assertIn('LayerNorm',n['idx_kn']['label']);self.assertIn('RoPE',n['idx_qrpe']['label'])
        self.assertFalse(any('hadamard' in x['label'].lower() for x in n.values()))
        self.assertFalse(any('gate' in k for k in n if k.startswith('attn_')))
        self.assertFalse(any(e['source'].startswith('mtp_') or e['target'].startswith('mtp_') for e in g['edges']))
        for binding in g['port_bindings'].values():self.assertIn(binding['source'],n);self.assertIn(binding['target'],n)
        ops=[x for x in n.values() if x.get('kind')!='decoration']
        for l,r in itertools.combinations(ops,2):
            x,y,w,h=l['box'];xx,yy,ww,hh=r['box']
            self.assertFalse(min(x+w,xx+ww)-max(x,xx)>1 and min(y+h,yy+hh)-max(y,yy)>1,(l['id'],r['id']))
    def test_operator_dimensions_reflect_roles_and_preserve_lane_centers(self):
        g=self.graph();nodes={n['id']:n for n in g['nodes']}
        self.assertLess(nodes['idx_relu']['box'][2],nodes['attn_core']['box'][2])
        self.assertEqual(nodes['attn_core']['operator_layout']['role'],'composite')
        self.assertEqual(nodes['attn_qa']['operator_layout']['role'],'projection')
        self.assertEqual(nodes['attn_cache']['operator_layout']['role'],'cache')
        for n in nodes.values():
            layout=n.get('operator_layout')
            if not layout:continue
            x,y,w,h=n['box'];cx,cy=layout['lane_center']
            self.assertAlmostEqual(x+w/2,cx);self.assertAlmostEqual(y+h/2,cy)
            self.assertLessEqual(w,layout['reserved_slot'][2])
            self.assertTrue(n.get('evidence'))

    def test_xml_png_layout_are_one_native_export(self):
        stem='glm_5_1_architecture';m=p.verify(self.folder/(stem+'.drawio'),self.folder/(stem+'.png'),self.folder/(stem+'.export.json'))
        g=self.graph();self.assertEqual((m['vertices'],m['edges']),(len(g['nodes']),len(g['edges'])))
        p.validate_layout(a.read(self.folder/(stem+'.layout.json')))
        self.assertNotIn('data:image',(self.folder/(stem+'.drawio')).read_text())
if __name__=='__main__':unittest.main()
