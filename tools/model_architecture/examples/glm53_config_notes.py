"""Place source-cited checkpoint configuration values in clear panel space."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model_architecture import parse_style

def present(g):
    c=json.loads((ROOT/'models/glm_5_3/official_config.json').read_text());ns={n['id']:n for n in g['nodes']}
    def value(path):
        v=c
        for part in path.strip('/').split('/'):v=v[part]
        return v
    def fmt(v):return json.dumps(v,ensure_ascii=False,separators=(',',':')) if not isinstance(v,str) else v
    def params(key,title,paths,box,size=17):
        entries=[dict(path=path,value=value(path)) for path in paths]
        # Full config paths retained in metadata/evidence; leaf keys on the diagram.
        label=title+'\n'+'\n'.join(path.rsplit('/',1)[-1]+' = '+fmt(value(path)) for path in paths)
        node=ns.get(key)
        if node is None:
            node=dict(id=key,kind='decoration',status='verified');g['nodes'].append(node);ns[key]=node
        node.update(label=label,description='Hugging Face checkpoint config, pinned revision '+g['checkpoint']['revision'],box=box,
          evidence=[dict(source='config',locator=path) for path in paths],config_parameters=entries,
          style=f'html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={size};fontColor=#526171;align=left;verticalAlign=middle;spacing=8;fillColor=none;strokeColor=none;')
    params('attn_dims','DSA / MLA · config',[
      '/num_attention_heads','/q_lora_rank','/kv_lora_rank','/qk_nope_head_dim','/qk_rope_head_dim','/qk_head_dim','/v_head_dim',
      '/rope_parameters/rope_theta','/rope_interleave','/attention_bias'],[65,290,370,400])
    params('index_config_params','Indexer · config',[
      '/index_n_heads','/index_head_dim','/index_topk','/indexer_rope_interleave'],[1950,335,400,175])
    params('moe_config_params','MoE · config',[
      '/n_routed_experts','/num_experts_per_tok','/n_shared_experts','/moe_intermediate_size','/routed_scaling_factor','/scoring_func','/norm_topk_prob'],[1895,1680,305,240],16)
    params('mlp_config_params','SwiGLU · config',[
      '/hidden_size','/intermediate_size','/moe_intermediate_size','/hidden_act','/first_k_dense_replace'],[65,2110,350,170],17)
    params('main_config','',[
      '/num_hidden_layers','/hidden_size','/vocab_size','/max_position_embeddings'],[1050,1355,340,100],16)
    # Avoid an empty heading line in this particularly compact backbone note.
    ns['main_config']['label']=ns['main_config']['label'].lstrip('\n')
    params('aux_scope','MTP / precision · config',[
      '/num_nextn_predict_layers','/index_share_for_mtp_iteration','/dtype',
      '/quantization_config/quant_method','/quantization_config/fmt','/quantization_config/weight_block_size','/quantization_config/activation_scheme'],[1710,2140,620,300],20)
    note=ns['sharing_note']
    note['label']=f"index_topk_freq = {c['index_topk_freq']}\nindex_skip_topk_offset = {c['index_skip_topk_offset']}\nFULL: L0,L1,L2,L6,…,L74\nSame query; share positions J\nEach layer keeps its own KV"
    note['evidence']+=[dict(source='config',locator='/index_topk_freq'),dict(source='config',locator='/index_skip_topk_offset')]
    note['config_parameters']=[dict(path=path,value=c[path[1:]]) for path in ['/index_topk_freq','/index_skip_topk_offset']]
    g['presentation_policy']['config_notes']='Pinned HF config values generated into unfilled panel whitespace; full JSON paths in metadata/evidence.'
    g['presentation_policy']['legend']='omitted per user preference; same function retains the same color'
    return g
