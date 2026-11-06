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
 def test_native_pair_and_layout(self):
  f=REPO/'models/glm_5_3';s='glm_5_3_architecture'
  m=p.verify(f/(s+'.drawio'),f/(s+'.png'),f/(s+'.export.json'))
  self.assertEqual((m['vertices'],m['edges']),(98,71));p.validate_layout(a.read(f/(s+'.layout.json')))
if __name__=='__main__':unittest.main()
