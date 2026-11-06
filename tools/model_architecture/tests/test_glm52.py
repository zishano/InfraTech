"""GLM-5.2 sharing must follow actual checkpoint schedule and weight presence."""
from pathlib import Path
import itertools,sys,unittest
BASE=Path(__file__).resolve().parents[1];REPO=BASE.parents[1]
sys.path.insert(0,str(BASE))
import model_architecture as a
import png_export as p

class GLM52Tests(unittest.TestCase):
    folder=REPO/'models/glm_5_2'
    def graph(self):return a.read(BASE/'examples/glm52.graph.json')
    def test_explicit_schedule_matches_weight_index_and_parameter_delta(self):
        c=a.read(self.folder/'official_config.json');s=a.read(self.folder/'checkpoint_summary.json')
        full=[0,1]+list(range(2,78,4))
        self.assertEqual([i for i,x in enumerate(c['indexer_types']) if x=='full'],full)
        self.assertEqual((len(full),len(s['shared_indexer_layers'])),(21,57))
        for row in s['per_layer']:
            i=row['layer_index'];self.assertEqual(row['indexer'],i in full or i==78)
            self.assertEqual(row['dense_ffn'],i<3);self.assertEqual(row['routed_experts'],i>=3)
        self.assertEqual((s['tensor_names'],s['shards']),(59585,282))
        d=s['indexer_reduction'];self.assertEqual(d['source_derived_removed_parameters'],534198528)
        self.assertEqual(d['metadata_element_delta'],-534198528);self.assertEqual(d['tensor_name_delta'],-285)
    def test_attention_dimensions_and_sharing_semantics_remain_separate(self):
        c=a.read(self.folder/'official_config.json');g=self.graph();a.validate(g)
        self.assertEqual((c['qk_nope_head_dim'],c['qk_rope_head_dim'],c['qk_head_dim']),(192,64,256))
        self.assertEqual((c['max_position_embeddings'],c['rope_parameters']['rope_theta']),(1048576,8000000))
        self.assertTrue(c['index_share_for_mtp_iteration'])
        self.assertIn('condition',g['port_bindings']['J']);self.assertIn('previous_J',g['port_bindings'])
        nodes={n['id']:n for n in g['nodes']}
        self.assertIn('FULL',nodes['share_stage_0']['label']);self.assertIn('SHARED',nodes['share_stage_3']['label'])
        for e in g['edges']:
            if e.get('role')=='index_share_illustration':
                self.assertTrue(e['source'].startswith('share_stage_'));self.assertTrue(e['target'].startswith('share_stage_'))
        ops=[n for n in g['nodes'] if n.get('kind')!='decoration']
        for l,r in itertools.combinations(ops,2):
            x,y,w,h=l['box'];xx,yy,ww,hh=r['box']
            self.assertFalse(min(x+w,xx+ww)-max(x,xx)>1 and min(y+h,yy+hh)-max(y,yy)>1,(l['id'],r['id']))
        for n in ops:
            if 'operator_layout' in n:
                x,y,w,h=n['box'];cx,cy=n['operator_layout']['lane_center']
                self.assertAlmostEqual(x+w/2,cx);self.assertAlmostEqual(y+h/2,cy)
    def test_native_export_is_the_png_source(self):
        stem='glm_5_2_architecture';m=p.verify(self.folder/(stem+'.drawio'),self.folder/(stem+'.png'),self.folder/(stem+'.export.json'));g=self.graph()
        self.assertEqual((m['vertices'],m['edges']),(len(g['nodes']),len(g['edges'])))
        p.validate_layout(a.read(self.folder/(stem+'.layout.json')))
        self.assertNotIn('data:image',(self.folder/(stem+'.drawio')).read_text())
if __name__=='__main__':unittest.main()
