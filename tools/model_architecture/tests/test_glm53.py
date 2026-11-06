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
  expected=[(e['source'],e['target'],[.5,0,.5,1] if e.get('role')=='index_share_illustration' else e.get('ports')) for e in old['edges'] if 'main_repeat' not in (e['source'],e['target'])]
  expected.append(('main_add2','main_norm',[.5,0,.5,1]))
  self.assertEqual(sorted((e['source'],e['target'],e.get('ports')) for e in g['edges']),sorted(expected))
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
 def test_white_canvas_and_unambiguous_fills(self):
  root=ET.parse(REPO/'models/glm_5_3/glm_5_3_architecture.drawio')
  self.assertEqual(root.find('.//mxGraphModel').get('background'),'#ffffff')
  cells={x.get('id'):x for x in root.iter('mxCell')}
  for cell in cells.values():
   keys=[part.split('=',1)[0] for part in cell.get('style','').split(';') if '=' in part]
   self.assertEqual(len(keys),len(set(keys)),cell.get('id'))
  for key in ['backbone','attention','indexer','moe','mlp','aux','sharing','title']:
   self.assertEqual(a.parse_style(cells[key].get('style'))['fillColor'],'none')
  self.assertEqual(a.parse_style(cells['attn_qa'].get('style'))['fillColor'],'#eaf2ff')
  self.assertEqual(a.parse_style(cells['share_stage_0'].get('style'))['fillColor'],'#eaf6ed')
 def test_repetition_frame_contains_only_decoder_template(self):
  g=a.read(BASE/'examples/glm53.graph.json');ns={n['id']:n for n in g['nodes']}
  self.assertNotIn('main_repeat',ns)
  group=g['repetition_groups'][0];self.assertEqual(group['count'],78)
  self.assertEqual(ns[group['count_label']]['label'],'×78')
  x,y,w,h=ns[group['frame']]['box']
  for key in group['members']:
   xx,yy,ww,hh=ns[key]['box'];self.assertTrue(x<=xx and y<=yy and xx+ww<=x+w and yy+hh<=y+h,key)
  for key in ['main_embed','main_norm','main_head']:
   xx,yy,ww,hh=ns[key]['box'];self.assertTrue(yy+hh<y or yy>y+h,key)
  self.assertTrue(any(e['source']=='main_add2' and e['target']=='main_norm' for e in g['edges']))
 def test_kimi_reference_layout_and_module_palette(self):
  g=a.read(BASE/'examples/glm53.graph.json');ns={n['id']:n for n in g['nodes']}
  x,y,w,h=ns['attention']['box'];bx,by,bw,bh=ns['backbone']['box'];ix,iy,iw,ih=ns['indexer']['box']
  self.assertLess(x+w,bx);self.assertLess(bx+bw,ix)
  for key,color in {'attention_title':'#a7773e','backbone_title':'#59718f','indexer_title':'#527d5d','moe_title':'#3f7e78','sharing_title':'#527d5d'}.items():
   style=a.parse_style(ns[key]['style']);self.assertEqual(style['fillColor'],color);self.assertEqual(style['fontColor'],'#ffffff')
  for n in g['nodes']:
   if n.get('kind')!='decoration':
    role=n['functional_role'];self.assertEqual(a.parse_style(n['style'])['fillColor'],g['presentation_policy']['functional_palette'][role]['fill'])
  self.assertNotEqual(a.parse_style(ns['attn_qa']['style'])['fillColor'],a.parse_style(ns['attn_qnorm']['style'])['fillColor'])
  self.assertEqual(ns['attn_cache']['functional_role'],ns['idx_cache']['functional_role'])
  self.assertEqual(ns['attn_qnorm']['functional_role'],ns['idx_kn']['functional_role'])
  for n in g['nodes']:
   if 'operator_layout' in n:
    xx,yy,ww,hh=n['box'];cx,cy=n['operator_layout']['lane_center']
    self.assertAlmostEqual(xx+ww/2,cx);self.assertAlmostEqual(yy+hh/2,cy)
 def test_indexshare_is_inside_compact_backbone(self):
  g=a.read(BASE/'examples/glm53.graph.json');ns={n['id']:n for n in g['nodes']}
  x,y,w,h=ns['backbone']['box']
  for key in ['sharing','sharing_title','sharing_note']+[f'share_stage_{i}' for i in range(4)]:
   xx,yy,ww,hh=ns[key]['box'];self.assertTrue(x<=xx and y<=yy and xx+ww<=x+w and yy+hh<=y+h,key)
  self.assertLess(ns['main_tokens']['box'][1],ns['sharing']['box'][1])
  self.assertLess(ns['main_tokens']['box'][1]-ns['main_out']['box'][1],1050)
  for i in range(3):self.assertGreater(ns[f'share_stage_{i}']['box'][1],ns[f'share_stage_{i+1}']['box'][1])
  self.assertLess(g['height'],2850)
 def test_native_pair_and_layout(self):
  f=REPO/'models/glm_5_3';s='glm_5_3_architecture'
  m=p.verify(f/(s+'.drawio'),f/(s+'.png'),f/(s+'.export.json'))
  self.assertEqual((m['vertices'],m['edges']),(110,70));p.validate_layout(a.read(f/(s+'.layout.json')))
  layout=a.read(f/(s+'.layout.json'));self.assertGreaterEqual(len(layout['edge_labels']),45)
  self.assertEqual(layout['edge_label_node_overlaps'],[]);self.assertEqual(layout['edge_label_overlaps'],[])
if __name__=='__main__':unittest.main()
