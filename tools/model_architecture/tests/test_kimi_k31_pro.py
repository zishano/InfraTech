"""Verify source-supported K3→K3.1 deltas and their visual meaning."""
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
import model_diff as d
import png_export as p

class KimiK31DiffTests(unittest.TestCase):
    folder=REPO/'models/kimi_k_3_1_pro'
    def graph(self):return a.read(BASE/'examples/kimi_k31_pro.graph.json')

    def test_recursive_config_comparison_does_not_invent_topology(self):
        old=a.read(self.folder/'baseline_k3_config.json');new=a.read(self.folder/'official_config.json')
        actual=d.compare_configs(old,new)
        self.assertEqual(actual,a.read(self.folder/'config_diff.json')['changes'])
        changes={x['path']:x for x in actual}
        self.assertEqual(changes['/text_config/dsa_config']['kind'],'added')
        self.assertEqual(changes['/auto_map/AutoModel']['kind'],'removed')
        for field in ['hidden_size','num_hidden_layers','num_experts','num_experts_per_token','routed_expert_hidden_size','q_lora_rank','kv_lora_rank','num_nextn_predict_layers']:
            self.assertEqual(old['text_config'][field],new['text_config'][field])
        self.assertEqual(old['vision_config'],new['vision_config'])
        self.assertEqual(new['text_config']['num_nextn_predict_layers'],0)
        self.assertEqual(d.compare_configs({'a/b':1},{'a/b':2})[0]['path'],'/a~1b')

    def test_dsa_positions_and_indexer_specific_geometry_are_real_config(self):
        c=a.read(self.folder/'official_config.json')['text_config'];idx=c['dsa_config']
        self.assertEqual(idx['dsa_layers'],c['linear_attn_config']['full_attn_layers'])
        self.assertEqual(idx['dsa_layers'],list(range(4,93,4))+[93])
        self.assertEqual((len(c['linear_attn_config']['kda_layers']),len(idx['dsa_layers'])),(69,24))
        self.assertEqual((idx['index_num_heads'],idx['index_head_dim'],idx['index_topk']),(32,128,2048))
        self.assertEqual(idx['index_rope_dim'],0)
        self.assertEqual(idx['index_k_norm_type'],'layernorm')
        self.assertEqual(idx['index_topk_freq'],1)
        graph=self.graph();nodes={n['id']:n for n in graph['nodes']};edges={(e['source'],e['target']) for e in graph['edges']}
        self.assertEqual(nodes['idx_knorm']['label'],'LayerNorm')
        self.assertIn(('idx_qr','idx_qproj'),edges)
        self.assertIn(('idx_h','idx_kproj'),edges)
        self.assertIn(('idx_h','idx_wproj'),edges)
        self.assertIn(('idx_weights','idx_sum'),edges)
        self.assertNotIn(('idx_weights','idx_mask'),edges)
        self.assertIn(('idx_topk','mla_attention'),edges)
        self.assertEqual(graph['port_bindings']['Qr']['source'],'mla_qnorm')
        ops=[n for n in nodes.values() if n.get('kind')!='decoration' and n['id'].startswith('idx_')]
        self.assertFalse(any('RoPE' in n['label'] or 'Hadamard' in n['label'] for n in ops))

    def test_colors_are_exclusive_and_retired_attention_is_inactive(self):
        graph=self.graph();nodes={n['id']:n for n in graph['nodes']}
        for n in nodes.values():
            change=n.get('change')
            style=a.parse_style(n['style'])
            if change in d.DIFF_THEMES:
                theme=d.DIFF_THEMES[change]
                self.assertEqual(style['fontColor'],theme['text'],n['id'])
                if n.get('kind')!='decoration':
                    self.assertEqual(style['strokeColor'],theme['stroke'],n['id'])
            if change=='unchanged':
                self.assertNotIn(style.get('fontColor'),[t['text'] for t in d.DIFF_THEMES.values()])
        retired=set(graph['comparison']['retired_nodes'])
        self.assertEqual(retired,{'retired_dense_attention'})
        for e in graph['edges']:
            self.assertFalse(retired.intersection([e['source'],e['target']]))
        self.assertEqual(nodes['mla_compress']['change'],'unchanged')
        self.assertEqual(nodes['mla_gate']['change'],'unchanged')
        self.assertEqual(nodes['mla_attention']['change'],'added')
        self.assertEqual(nodes['diff_quant']['change'],'parameter_changed')

    def test_metadata_delta_matches_source_derived_new_parameters(self):
        s=a.read(self.folder/'checkpoint_summary.json')
        expected=24*(1536*32*128+7168*128+7168*32+2*128)
        self.assertEqual(expected,178526208)
        self.assertEqual(s['bf16_metadata_delta'],expected)
        self.assertEqual(s['indexer_expected_parameter_delta']['total'],expected)
        self.assertFalse(s['weight_index_verified'])

    def test_original_k3_layout_is_reused_and_operations_do_not_overlap(self):
        old=a.read(BASE/'examples/kimi_k3.graph.json');g=self.graph();a.validate(g)
        nodes={n['id']:n for n in g['nodes']}
        for n in old['nodes']:
            if n['id'].startswith(('kda_','ar_','moe_','ex_','vision_')):
                self.assertEqual(nodes[n['id']]['box'],n['box'],n['id'])
        ops=[n for n in g['nodes'] if n.get('kind')!='decoration']
        for l,r in itertools.combinations(ops,2):
            x,y,w,h=l['box'];xx,yy,ww,hh=r['box']
            self.assertFalse(min(x+w,xx+ww)-max(x,xx)>1 and min(y+h,yy+hh)-max(y,yy)>1,(l['id'],r['id']))

    def test_png_native_xml_and_diff_edge_colors_match(self):
        folder=self.folder;stem='kimi_k31_pro_architecture';g=self.graph()
        manifest=p.verify(folder/(stem+'.drawio'),folder/(stem+'.png'),folder/(stem+'.export.json'))
        self.assertEqual((manifest['vertices'],manifest['edges']),(len(g['nodes']),len(g['edges'])))
        p.validate_layout(a.read(folder/(stem+'.layout.json')))
        root=ET.parse(folder/(stem+'.drawio')).getroot();cells={c.get('id'):c for c in root.iter('mxCell')}
        for edge in g['edges']:
            if edge.get('change')=='added':self.assertEqual(a.parse_style(cells[edge['id']].get('style'))['strokeColor'],'#c62828')
        self.assertNotIn('data:image',ET.tostring(root).decode())

if __name__=='__main__':unittest.main()
