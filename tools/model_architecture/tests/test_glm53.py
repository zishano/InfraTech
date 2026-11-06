"""Do not invent architecture changes from post-training or FP8 storage."""
from pathlib import Path
import sys,unittest
BASE=Path(__file__).resolve().parents[1];REPO=BASE.parents[1]
sys.path.insert(0,str(BASE))
import model_architecture as a
import png_export as p
from model_diff import compare_configs
class GLM53Tests(unittest.TestCase):
 def test_same_base_and_separate_quantization(self):
  folder=REPO/'models/glm_5_3';c=a.read(folder/'official_config.json');b=a.read(folder/'baseline_glm52_config.json')
  self.assertEqual({x['path'] for x in compare_configs(b,c)},{'/quantization_config','/transformers_version'})
  self.assertEqual(len(c['quantization_config']['modules_to_not_convert']),541)
  g=a.read(BASE/'examples/glm53.graph.json');a.validate(g)
  old=a.read(BASE/'examples/glm52.graph.json')
  self.assertEqual(g['edges'],old['edges'])
  self.assertFalse(g['checkpoint']['weight_index_verified'])
  self.assertNotIn('index',g['sources']);self.assertIn('baseline_index',g['sources'])
  self.assertTrue(all(e['source']!='index' for n in g['nodes'] for e in n.get('evidence',[])))
 def test_tensor_contracts_match_config_and_absorption(self):
  c=a.read(REPO/'models/glm_5_3/official_config.json');g=a.read(BASE/'examples/glm53.graph.json');t=g['tensor_contracts']
  self.assertEqual(t['dsa']['q'][-2:],[c['num_attention_heads'],c['qk_nope_head_dim']+c['qk_rope_head_dim']])
  self.assertEqual(t['dsa']['cache_latent'][-1],c['kv_lora_rank'])
  self.assertEqual(t['dsa']['output'],['B','S',c['hidden_size']])
  self.assertEqual(t['indexer']['q'][-2:],[c['index_n_heads'],c['index_head_dim']])
  self.assertEqual(t['moe']['selection'][-1],c['num_experts_per_tok'])
  m=t['absorbed_mqa_equivalent'];self.assertEqual(m['q'][-1],c['kv_lora_rank']+c['qk_rope_head_dim'])
  self.assertEqual(m['latent_output'][-1],c['kv_lora_rank']);self.assertEqual(m['value_projected'][-1],c['v_head_dim'])
  self.assertIn('not an additional model branch',next(n['label'] for n in g['nodes'] if n['id']=='dim_mqa_title'))
 def test_native_pair_and_layout(self):
  f=REPO/'models/glm_5_3';s='glm_5_3_architecture'
  m=p.verify(f/(s+'.drawio'),f/(s+'.png'),f/(s+'.export.json'))
  self.assertEqual((m['vertices'],m['edges']),(108,71));p.validate_layout(a.read(f/(s+'.layout.json')))
if __name__=='__main__':unittest.main()
