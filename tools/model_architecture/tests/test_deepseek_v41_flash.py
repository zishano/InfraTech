"""V4.1 must not inherit V4 CSA/HCA assumptions or move control-path inputs."""
from pathlib import Path
import sys,unittest,itertools,xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parents[1];REPO=BASE.parents[1]
sys.path.insert(0,str(BASE))
import model_architecture as a
import png_export as p
class DeepseekV41Tests(unittest.TestCase):
 folder=REPO/'models/deepseek_v4_1/flash'
 def graph(self,detail=False):return a.read(BASE/'examples'/('deepseek_v41_flash_csa2.graph.json' if detail else 'deepseek_v41_flash.graph.json'))
 def test_checkpoint_sources_and_three_modes(self):
  c=a.read(self.folder/'official_config.json')['text_config'];s=a.read(self.folder/'checkpoint_summary.json')
  self.assertEqual(c['compress_ratios'],[0,0]+[2]*18+[1]*20+[0]*3)
  self.assertEqual(s['kv_source_layers'],c['kv_source_layer_ids']);self.assertEqual(s['index_source_layers'],c['index_source_layer_ids'])
  self.assertEqual(s['mode_counts'],{'SWA':2,'Full':4,'Reuse':30,'Reindex':4})
  for row in s['per_layer']:
   self.assertEqual(row['kv_source'],row['layer'] in [2,8,14,20])
   self.assertEqual(row['index_source'],row['layer'] in [2,8,14,20,24,28,32,36])
   self.assertEqual(row['index_key_owner'],row['kv_source'])
  self.assertEqual((s['tensor_names'],s['shards'],s['vision_blocks']),(96085,48,32))
  self.assertEqual(s['engram_layers'],[1,14]);self.assertEqual([x['experts'] for x in s['mtp']],[128]*3)
 def test_checkpoint_fields_in_parameter_notes_are_literal(self):
  c=a.read(self.folder/'official_config.json');count=0
  for detail in [False,True]:
   g=self.graph(detail);a.validate(g)
   for n in g['nodes']:
    for row in n.get('config_parameters',[]):
     value=c
     for key in row['path'].strip('/').split('/'):value=value[key]
     self.assertEqual(value,row['value']);count+=1
  self.assertGreater(count,40)
 def test_repetition_and_geometry(self):
  for detail in [False,True]:
   g=self.graph(detail);ns={n['id']:n for n in g['nodes']}
   self.assertFalse(any('legend' in n['id'] for n in g['nodes']))
   self.assertEqual(g['background'],'#ffffff')
   for group in g.get('repetition_groups',[]):
    x,y,w,h=ns[group['frame']]['box']
    for key in group['members']:
     xx,yy,ww,hh=ns[key]['box'];self.assertTrue(x<=xx and y<=yy and xx+ww<=x+w and yy+hh<=y+h,key)
   ops=[n for n in g['nodes'] if n.get('kind')!='decoration']
   for l,r in itertools.combinations(ops,2):
    x,y,w,h=l['box'];xx,yy,ww,hh=r['box']
    self.assertFalse(min(x+w,xx+ww)-max(x,xx)>1 and min(y+h,yy+hh)-max(y,yy)>1,(l['id'],r['id']))
  self.assertEqual([x['count'] for x in self.graph()['repetition_groups']],[20,20,32,3])
 def test_single_pass_mhc_and_dspark_confidence_use_correct_inputs(self):
  g=self.graph();pairs={(e['source'],e['target']) for e in g['edges']};ns={n['id']:n for n in g['nodes']}
  self.assertIn(('hc_pre_new','hc_next'),pairs);self.assertNotIn(('hc_pre_new','hc_collapse'),pairs)
  self.assertIn(('hc_prev','hc_collapse'),pairs)
  self.assertIn(('ds_collapse','ds_confidence'),pairs);self.assertNotIn(('ds_norm','ds_confidence'),pairs)
  self.assertIn(('ds_collapse','ds_norm'),pairs)
  self.assertIn('inputs at L37 /38 /39',ns['ds_taps']['label'])
  self.assertIn('before Down',ns['m_experts']['label'])
  self.assertEqual(g['port_bindings']['V']['meaning'],'replace image-token spans; learned delimiters separately')
 def test_compressor_keeps_value_bypass_and_ratio_one_bypass(self):
  g=self.graph(True);pairs={(e['source'],e['target']) for e in g['edges']};ns={n['id']:n for n in g['nodes']}
  self.assertIn(('c_wkv','c_norm'),pairs);self.assertIn(('c_values','c_product'),pairs)
  self.assertIn(('c_softmax','c_product'),pairs);self.assertNotIn(('c_values','c_softmax'),pairs)
  self.assertIn('block16, E4M3',ns['c_fp4']['label']);self.assertIn('block32, E8M0',ns['i_fp4k']['label'])
  self.assertEqual(g['port_bindings']['L']['source'],'c_latent')
  self.assertIn('generated first',ns['c_latent']['label'])
 def test_candidate_mask_after_scoring_and_block_selection(self):
  g=self.graph(True);pairs={(e['source'],e['target']) for e in g['edges']};ns={n['id']:n for n in g['nodes']}
  for pair in [('i_dot','i_relu'),('i_sum','i_causal'),('i_causal','i_candidate'),('i_candidate','i_top'),('b_max','b_newest'),('b_newest','b_top'),('r_score','r_mask'),('r_mask','r_top')]:self.assertIn(pair,pairs)
  self.assertIn('16384',ns['candidate_scope']['label']);self.assertIn('dense scoring',ns['candidate_scope']['label'])
  self.assertFalse(any('Hadamard' in n['label'] for n in g['nodes']))
 def test_native_pairs_and_actual_layout(self):
  for stem,detail in [('deepseek_v41_flash_architecture',False),('deepseek_v41_flash_csa2',True)]:
   f=self.folder;m=p.verify(f/(stem+'.drawio'),f/(stem+'.png'),f/(stem+'.export.json'));g=self.graph(detail)
   self.assertEqual((m['vertices'],m['edges']),(len(g['nodes']),len(g['edges'])))
   layout=a.read(f/(stem+'.layout.json'));p.validate_layout(layout)
   self.assertIn('edge_label_node_overlaps',layout);self.assertEqual(layout['edge_label_node_overlaps'],[])
   root=ET.parse(f/(stem+'.drawio'));self.assertEqual(root.find('.//mxGraphModel').get('background'),'#ffffff')
   self.assertNotIn('data:image',(f/(stem+'.drawio')).read_text())
if __name__=='__main__':unittest.main()
