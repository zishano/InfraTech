"""GLM-5.3: same reviewed base, post-training gains and FP8 release config."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).parent))
from build_glm52 import build as build_reviewed_core
REV='ba32f8c19c8738e2c57c71798c601d477a7bf844'
TF='8833c9181eec925f1b4e0096db516462044345df'
def build():
 out=ROOT/'models/glm_5_3';c=json.loads((out/'official_config.json').read_text());b=json.loads((out/'baseline_glm52_config.json').read_text())
 assert {k:v for k,v in c.items() if k not in ('quantization_config','transformers_version')}=={k:v for k,v in b.items() if k not in ('quantization_config','transformers_version')},'Re-review changed architecture'
 inv=json.loads((out/'source_inventory.json').read_text())
 assert next(x['sha256'] for x in inv if x['id']=='model')=='226f5a24b6aa15eca90bcc74e6bf1e2e887687ccfeb0d1ae28da4bf4c216038f'
 assert next(x['sha256'] for x in inv if x['id']=='framework_config')=='4e0581bbc950f19b2e9cc6e08f300e592f59564b4a34a57b1af670c8ec5bb4dd'
 q=c['quantization_config'];assert (q['quant_method'],q['fmt'],q['weight_block_size'],len(q['modules_to_not_convert']))==('fp8','e4m3',[128,128],541)
 g=build_reviewed_core();g['title']='GLM-5.3 — IndexShare DSA + MoE'
 g['background']='none'
 # Group frames and text have no fill; preserve colored operator/MTP/share boxes.
 for node in g['nodes']:
  if node['kind']=='decoration' and not node['id'].startswith(('share_stage_','mtp_')):
   node['style']+='fillColor=none;'
 g['sources']['baseline_index']=g['sources']['index'];del g['sources']['index']
 for k in ('config','card'):g['sources'][k]=f'https://huggingface.co/zai-org/GLM-5.3/blob/{REV}/'+('config.json' if k=='config' else 'README.md')
 for k,name in [('model','modeling_glm_moe_dsa.py'),('framework_config','configuration_glm_moe_dsa.py')]:g['sources'][k]=f'https://github.com/huggingface/transformers/blob/{TF}/src/transformers/models/glm_moe_dsa/{name}'
 for n in g['nodes']:
  for e in n.get('evidence',[]):
   if e['source']=='index':e['source']='baseline_index';e['locator']='GLM-5.2 baseline only; target topology supported by matching config + model card: '+e['locator']
 ns={n['id']:n for n in g['nodes']}
 def edit(k,text):ns[k]['label']=text;ns[k]['description']=text
 edit('title','GLM-5.3  |  IndexShare DSA + Mixture of Experts')
 edit('scope','Official FP8 release @ba32f8c · same base as GLM-5.2 · post-training gains · bottom-up flow')
 edit('aux_scope','FP8 release / deployment config\nE4M3 · dynamic activation\nWeight blocks 128 ×128\n541 exclusions; no extra network branch')
 edit('aux_modules','MTP ×1 — inherited base view; target config verified')
 edit('footer','Sources: GLM-5.3 @ba32f8c · Transformers @8833c91 · same base as 5.2; target weight-index download blocked (see README)')
 ns['aux_scope']['evidence']=[dict(source='config',locator='/quantization_config'),dict(source='card',locator='Introduction: same base model as GLM-5.2; gains from post-training')]
 g['checkpoint']=dict(revision=REV,main_layers=78,auxiliary_layers=1,indexer_mode='config: 21 FULL /57 SHARED',context=1048576,weight_index_verified=False,release_quantization=q)
 g['limitations']=['Official model card states the same base as GLM-5.2; core configuration and pinned implementation match.','GLM-5.3 weight-index download blocked by proxy at official CDN; baseline weight-index citations are explicitly marked and do not verify target weights.','FP8 overlay describes release configuration, not added model operators or a verified backend execution graph.','MTP auxiliary structure inherited from matching config/base; no target tensor-name or backend-iteration verification.','No tensor headers, full weights, GPU inference, benchmark or Feishu import tested.']
 # Tensor contracts use sequence-major logical axes; implementations may transpose.
 # These are within-forward dimension transforms, not changes from 5.2 to 5.3.
 g['tensor_contracts']={
  'symbols':{'B':'batch','S':'current query length','T':'cached + current key length','K':'min(2048,T)','N':'B*S tokens','m':'12288 dense; 2048 expert'},
  'dsa':{'input':['B','S',6144],'q_residual':['B','S',2048],'q':['B','S',64,256],'cache_latent':['B','T',1,512],'cache_rope':['B','T',1,64],'key_expanded':['B','T',64,256],'value_expanded':['B','T',64,256],'output':['B','S',6144]},
  'indexer':{'q':['B','S',32,128],'key':['B','T',128],'head_weights':['B','S',32],'scores':['B','S',32,'T'],'reduced_scores':['B','S','T'],'indices':['B','S','K']},
  'moe':{'router':['N',256],'selection':['N',8],'expert_input':['N_e',6144],'expert_hidden':['N_e',2048],'expert_output':['N_e',6144],'merged_output':['B','S',6144]},
  'absorbed_mqa_equivalent':{'q':['B','S',64,576],'selected_k':['B','S','K',1,576],'selected_v':['B','S','K',1,512],'latent_output':['B','S',64,512],'value_projected':['B','S',64,256],'output':['B','S',6144],'scope':'algebraic correspondence only; no backend execution or numeric equivalence test'}}
 # Place dimensions on the actual mxGraph edges, not in a separate legend table.
 # Logical sequence-major shapes; implementation-only transposes are omitted.
 labels={
 ('main_tokens','main_embed'):'[B,S]',
 ('main_embed','main_x'):'[B,S,6144]',
 ('main_n1','main_attn'):'[B,S,6144]',
 ('main_n2','main_ffn'):'[B,S,6144]',
 ('main_norm','main_head'):'[B,S,6144]',
 ('main_head','main_out'):'[B,S,154880]',
 ('attn_h','attn_qa'):'[B,S,6144]',
 ('attn_qa','attn_qnorm'):'[B,S,2048]',
 ('attn_qnorm','attn_qup'):'[B,S,2048]',
 ('attn_qup','attn_qsplit'):'[B,S,64,256]',
 ('attn_qsplit','attn_qnope'):'[B,S,64,192]',
 ('attn_qsplit','attn_qrope'):'[B,S,64,64]',
 ('attn_qcat','attn_core'):'Q [B,S,64,256]',
 ('attn_h','attn_kvdown'):'[B,S,6144]',
 ('attn_kvdown','attn_kvsplit'):'[B,S,576]',
 ('attn_kvsplit','attn_kvnorm'):'[B,S,512]',
 ('attn_kvsplit','attn_kvrope'):'[B,S,64]',
 ('attn_cache','attn_expand'):'c [B,T,1,512]\nkPE [B,T,1,64]',
 ('attn_k','attn_core'):'K [B,T,64,256]',
 ('attn_v','attn_core'):'V [B,T,64,256]',
 ('attn_indices','attn_core'):'J [B,S,K]',
 ('attn_core','attn_o'):'[B,S,64,256]\nreshape → [B,S,16384]',
 ('attn_o','attn_out'):'[B,S,6144]',
 ('idx_qr','idx_qp'):'[B,S,2048]',
 ('idx_qp','idx_qrpe'):'[B,S,32,128]',
 ('idx_q','idx_dot'):'Qi [B,S,32,128]',
 ('idx_h','idx_kp'):'[B,S,6144]',
 ('idx_kp','idx_kn'):'[B,S,128]',
 ('idx_cache','idx_dot'):'Ki [B,T,128]',
 ('idx_h','idx_wp'):'[B,S,6144]',
 ('idx_wp','idx_scale'):'[B,S,32]',
 ('idx_w','idx_sum'):'w [B,S,32]',
 ('idx_dot','idx_relu'):'[B,S,32,T]',
 ('idx_relu','idx_sum'):'[B,S,32,T]',
 ('idx_sum','idx_mask'):'[B,S,T]',
 ('idx_mask','idx_topk'):'[B,S,T]',
 ('moe_h','moe_router'):'[N,6144]',
 ('moe_router','moe_choice'):'[N,256]',
 ('moe_choice','moe_weights'):'IDs [N,8]',
 ('moe_weights','moe_experts'):'weights [N,8]',
 ('moe_experts','moe_weighted'):'[N,8,6144]',
 ('moe_weighted','moe_add'):'[N,6144]',
 ('moe_h','moe_shared'):'[N,6144]',
 ('moe_shared','moe_add'):'[N,6144]',
 ('mlp_x','mlp_gate'):'[N_e,6144]',
 ('mlp_x','mlp_up'):'[N_e,6144]',
 ('mlp_gate','mlp_silu'):'[N_e,m]',
 ('mlp_silu','mlp_mul'):'[N_e,m]',
 ('mlp_up','mlp_mul'):'[N_e,m]',
 ('mlp_mul','mlp_down'):'[N_e,m]',
 }
 for edge in g['edges']:
  pair=(edge['source'],edge['target'])
  if pair in labels:
   edge.update(label=labels[pair],label_font_size=17,tensor_shape=labels[pair],label_offset=[0,0])
 # Compact row spacing while retaining room for native edge dimensions.
 scale=1.12
 for n in g['nodes']:
  x,y,w,h=n['box']
  if n['kind']=='decoration':n['box']=[x,y*scale,w,h*scale]
  else:n['box']=[x,(y+h/2)*scale-h/2,w,h]
  if 'operator_layout' in n:
   n['operator_layout']['lane_center'][1]*=scale
   slot=n['operator_layout']['reserved_slot'];slot[1]*=scale;slot[3]*=scale
 for edge in g['edges']:
  if 'points' in edge:edge['points']=[[x,y*scale] for x,y in edge['points']]
 g['height']=3024
 g['presentation_policy']['spacing']='Compact 1.12× baseline row positions; preserve operator sizes and 17pt edge labels.'
 edit('scope','FP8 @ba32f8c · B=batch, S=query, T=KV incl. cache, K=min(2048,T), N=B×S · dimensions label the arrows')
 edit('mlp_width','m=12288 Dense /2048 expert · N_e=tokens per expert (Dense: N_e=N)')
 edit('idx_topk','TopK ≤2048 → J [B,S,K]')
 # Describe implicit reshapes/dispatch in tooltips, with concise visible operators.
 ns['attn_o']['description']+='\nInput [B,S,64,256] is flattened to [B,S,16384] before Linear O.'
 ns['moe_h']['description']+='\nFlatten token axes to N=B*S before routing / expert execution.'
 ns['moe_experts']['description']+='\nLogical expert results [N,8,6144]; grouped/fused implementations need not materialize this tensor.'
 ns['mlp_down']['description']+='\nOutput [N_e,6144]. Routed/shared expert m=2048; dense m=12288.'
 g['edge_dimension_policy']='Native edge labels on actual computational connections; logical shapes, batch included; no standalone dimension panel.'
 g['limitations'].append('Edge dimensions use logical sequence-major axes; MoE selected-expert results need not be physically materialized. Absorbed MQA correspondence is documentation only.')
 return g
if __name__=='__main__':
 g=build();Path(__file__).with_name('glm53.graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
