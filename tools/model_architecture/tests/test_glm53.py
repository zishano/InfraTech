"""Do not invent architecture changes from post-training or FP8 storage."""
from pathlib import Path
import sys,unittest
import xml.etree.ElementTree as ET
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
  self.assertEqual([(e['source'],e['target'],e.get('ports')) for e in g['edges']],[(e['source'],e['target'],e.get('ports')) for e in old['edges']])
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
  self.assertFalse(any(n['id'].startswith('dim_') for n in g['nodes']))
  edges={ (e['source'],e['target']):e for e in g['edges'] }
  self.assertEqual(edges['attn_qup','attn_qsplit']['label'],'[B,S,64,256]')
  self.assertIn('[B,S,16384]',edges['attn_core','attn_o']['label'])
  cells={x.get('id'):x for x in ET.parse(REPO/'models/glm_5_3/glm_5_3_architecture.drawio').iter('mxCell')}
  for e in g['edges']:
   if e.get('tensor_shape'):
    self.assertEqual(cells[e['id']].get('value'),e['tensor_shape'])
    self.assertIn('fontSize=17;',cells[e['id']].get('style'))
 def test_transparent_canvas_and_unambiguous_fills(self):
  root=ET.parse(REPO/'models/glm_5_3/glm_5_3_architecture.drawio')
  self.assertEqual(root.find('.//mxGraphModel').get('background'),'none')
  cells={x.get('id'):x for x in root.iter('mxCell')}
  for cell in cells.values():
   keys=[part.split('=',1)[0] for part in cell.get('style','').split(';') if '=' in part]
   self.assertEqual(len(keys),len(set(keys)),cell.get('id'))
  for key in ['backbone','attention','indexer','moe','mlp','aux','sharing','title']:
   self.assertEqual(a.parse_style(cells[key].get('style'))['fillColor'],'none')
  self.assertEqual(a.parse_style(cells['attn_qa'].get('style'))['fillColor'],'#fff6e8')
  self.assertEqual(a.parse_style(cells['share_stage_0'].get('style'))['fillColor'],'#f5f0fc')
 def test_native_pair_and_layout(self):
  f=REPO/'models/glm_5_3';s='glm_5_3_architecture'
  m=p.verify(f/(s+'.drawio'),f/(s+'.png'),f/(s+'.export.json'))
  self.assertEqual((m['vertices'],m['edges']),(98,71));p.validate_layout(a.read(f/(s+'.layout.json')))
  layout=a.read(f/(s+'.layout.json'));self.assertGreaterEqual(len(layout['edge_labels']),45)
  self.assertEqual(layout['edge_label_node_overlaps'],[]);self.assertEqual(layout['edge_label_overlaps'],[])
if __name__=='__main__':unittest.main()
