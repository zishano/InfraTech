import importlib.util
import itertools
import json
from pathlib import Path
import unittest

BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
def load(name):
 s=importlib.util.spec_from_file_location(name,BASE/(name+'.py'))
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
a=load('model_architecture');p=load('png_export')

class DeepseekV4WorkflowTests(unittest.TestCase):
    def test_class_defaults_are_parsed_without_executing_any_code(self):
        raw=b'''raise RuntimeError("must never execute")
class Fixture:
    hidden_size: int = 4096
    num_hidden_layers: int = 43
    layer_types = None
    q_lora_rank = dangerous_function()
    def __post_init__(self):
        raise RuntimeError("must never execute")
'''
        f=a.class_defaults(raw,'config_code')
        self.assertEqual({v['name'] for v in f},{'hidden_size','layers','layer_types'})
        self.assertTrue(all(v['verification_scope']=='source_class_default_not_checkpoint' for v in f))
        self.assertTrue(all('line ' in v['evidence']['locator'] for v in f))
        scaffold=a.draft(dict(model='fixture',facts=f,sources={'config_code':'https://example.org/config.py'}))
        labels=[n['label'] for n in scaffold['nodes'] if n['id'].startswith('fact_')]
        self.assertTrue(all('SOURCE DEFAULT; checkpoint unverified' in label for label in labels))

    def test_target_checkpoint_and_framework_defaults_remain_distinct(self):
        folder=REPO/'models/deepseek_v4/flash'
        facts=a.read(folder/'facts.json')['facts']
        self.assertTrue(facts)
        checkpoint=[f for f in facts if f['evidence']['source']=='config']
        defaults=[f for f in facts if f['evidence']['source']=='transformers_config']
        self.assertTrue(checkpoint)
        self.assertTrue(all(f.get('verification_scope')!='source_class_default_not_checkpoint' for f in checkpoint))
        self.assertTrue(all(f['verification_scope']=='source_class_default_not_checkpoint' for f in defaults))
        self.assertEqual(next(f['value'] for f in facts if f['name']=='layers'),43)
        inventory=a.read(folder/'source_inventory.json')['sources']
        self.assertTrue(all(s['status']=='downloaded' for s in inventory))
        self.assertEqual(next(s['resolved_revision'] for s in inventory if s['id']=='config'),'60d8d70770c6776ff598c94bb586a859a38244f1')
        self.assertEqual(next(s['status'] for s in inventory if s['id']=='transformers_config'),'downloaded')

    def test_compressor_value_paths_and_model_specific_branches(self):
        g=a.read(BASE/'examples/deepseek_v4_flash.graph.json');a.validate(g)
        nodes={n['id']:{**n,'label':n.get('description',n['label'])} for n in g['nodes']};edges={(e['source'],e['target']) for e in g['edges']}
        for kind in ['csa','hca']:
            self.assertIn((kind+'_window',kind+'_sum'),edges)
            self.assertIn((kind+'_bias',kind+'_sum'),edges)
        self.assertIn('NO indexer',nodes['hca_out']['label'])
        self.assertIn('K and V are the SAME',nodes['attn_local']['label'])
        for k in ['hc_pre','hc_post','hc_sink','hc_residual','attn_inverse','idx_qproj','idx_kcache','idx_score']:
            self.assertIn(k,nodes)
        self.assertIn(('expert_x','expert_gate'),edges)
        self.assertIn(('expert_x','expert_up'),edges)
        self.assertNotIn(('expert_up','expert_gate'),edges)
        self.assertIn(('expert_mul','expert_weight'),edges)
        self.assertIn(('expert_weight','expert_down'),edges)
        self.assertIn('L2–41: [CSA 4, HCA 128] × 20',nodes['schedule']['label'])
        self.assertIn(('attn_kvrope','attn_kvquant'),edges)
        for k in ['idx_qproj','idx_kcache']:self.assertIn('Hadamard',nodes[k]['label'])
        for k in ['mtp_h','mtp_e','mtp_hp','mtp_ep','mtp_sum','mtp_block','mtp_head']:self.assertIn(k,nodes)
        operations=[n for n in nodes.values() if n.get('kind')!='decoration']
        for left,right in itertools.combinations(operations,2):
            x,y,w,h=left['box'];xx,yy,ww,hh=right['box']
            overlap_x=min(x+w,xx+ww)-max(x,xx)
            overlap_y=min(y+h,yy+hh)-max(y,yy)
            self.assertFalse(overlap_x>1 and overlap_y>1,(left['id'],right['id']))

    def test_new_model_png_is_a_direct_checked_xml_export(self):
        folder=REPO/'models/deepseek_v4/flash'
        m=p.verify(folder/'deepseek_v4_flash.drawio',folder/'deepseek_v4_flash.png',folder/'deepseek_v4_flash.export.json')
        _,nv,ne=p.inspect_drawio(folder/'deepseek_v4_flash.drawio')
        self.assertEqual((m['vertices'],m['edges']),(nv,ne))
        self.assertEqual((nv,ne),(128,112))
        p.validate_layout(a.read(folder/'deepseek_v4_flash.layout.json'))

    def test_checkpoint_schedule_matches_weight_index_module_presence(self):
        folder=REPO/'models/deepseek_v4/flash'
        c=a.read(folder/'official_config.json');infer=a.read(folder/'official_inference_config.json');s=a.read(folder/'checkpoint_summary.json')
        self.assertEqual(c['compress_ratios'],infer['compress_ratios'])
        self.assertEqual(len(c['compress_ratios']),c['num_hidden_layers']+c['num_nextn_predict_layers'])
        self.assertEqual(s['main_schedule_counts'],{'0':2,'4':21,'128':20})
        self.assertEqual(s['auxiliary_compress_ratios'],[0])
        self.assertEqual(len(s['per_layer_checks']),43)
        for layer in s['per_layer_checks']:
            self.assertEqual(layer['indexer_present'],layer['compress_ratio']==4)
            self.assertEqual(layer['compressor_present'],layer['compress_ratio']!=0)
            self.assertEqual(layer['hash_lookup_present'],layer['layer']<3)
        inv=a.read(folder/'source_inventory.json')['sources']
        index=next(item for item in inv if item['id']=='weight_index')
        self.assertEqual(index['sha256'],s['weight_index']['sha256'])
        self.assertEqual(s['weight_index']['tensor_names'],69187)
        self.assertEqual(s['weight_index']['shards'],46)

if __name__=='__main__':unittest.main()
