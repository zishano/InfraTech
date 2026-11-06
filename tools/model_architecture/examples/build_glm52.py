"""GLM-5.2: reviewed shared core plus explicit IndexShare topology."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).parent))
from build_glm51 import build as build_reviewed_core
REV='cf457fa734ab149ffef225f80893eb38c6ff5cdc'
TF='bbe484b5680f9cdf4d51bafc6b775b136558ab43'
HF=f'https://huggingface.co/zai-org/GLM-5.2/blob/{REV}/'
BASE=f'https://github.com/huggingface/transformers/blob/{TF}/src/transformers/models/glm_moe_dsa/'

def build():
 out=ROOT/'models/glm_5_2';c=json.loads((out/'official_config.json').read_text());old=json.loads((out/'baseline_glm51_config.json').read_text());s=json.loads((out/'checkpoint_summary.json').read_text())
 for k in ['num_hidden_layers','first_k_dense_replace','hidden_size','num_attention_heads','q_lora_rank','kv_lora_rank','qk_nope_head_dim','qk_rope_head_dim','v_head_dim','n_routed_experts','n_shared_experts','num_experts_per_tok','intermediate_size','moe_intermediate_size','routed_scaling_factor','index_head_dim','index_n_heads','index_topk','num_key_value_heads','vocab_size','rms_norm_eps','scoring_func','norm_topk_prob','hidden_act','num_nextn_predict_layers','dtype','attention_bias']:
  assert c[k]==old[k],f'Re-review changed shared core: {k}'
 full=[i for i,v in enumerate(c['indexer_types']) if v=='full'];shared=[i for i,v in enumerate(c['indexer_types']) if v=='shared']
 assert full==s['full_indexer_layers']==[0,1]+list(range(2,78,4))
 assert len(shared)==57 and c['max_position_embeddings']==1048576 and c['rope_parameters']['rope_theta']==8000000
 inv=json.loads((out/'source_inventory.json').read_text())
 assert next(r['sha256'] for r in inv if r['id']=='model')=='226f5a24b6aa15eca90bcc74e6bf1e2e887687ccfeb0d1ae28da4bf4c216038f', 'Re-review changed model implementation'
 g=build_reviewed_core();g['title']='GLM-5.2 — IndexShare DSA + MoE';g['height']=2700
 g['sources']=dict(config=HF+'config.json',card=HF+'README.md',index=HF+'model.safetensors.index.json',model=BASE+'modeling_glm_moe_dsa.py',framework_config=BASE+'configuration_glm_moe_dsa.py')
 ns={n['id']:n for n in g['nodes']}
 def edit(key,label):ns[key]['label']=label;ns[key]['description']=label
 edit('title','GLM-5.2  |  IndexShare DSA + Mixture of Experts')
 edit('facts','78 layers · hidden 6144 · 64 Q heads · 256 routed / top-8 + 1 shared · context 1M')
 edit('scope','BF16 checkpoint @cf457fa · explicit IndexShare schedule + weight-index checked · bottom-up flow')
 edit('main_config','L0–2: Dense FFN\nL3–77: MoE FFN\nDSA: 21 FULL +57 SHARED\nMTP: separate index78')
 edit('attn_dims','Q rank2048 · KV rank512 · Q/K256 =192+RoPE64 · V256\nInterleaved RoPE64, theta8e6 · per-layer KV cache')
 edit('indexer_title','DSA Indexer — FULL layers only (21 /78)')
 edit('index_scope','32 heads ×128 · interleaved RoPE64 · LayerNorm on K\nSHARED layers reuse previous TopK; no new Q/K/weight projections')
 ns['index_scope']['style']+='fontSize=16;';ns['index_scope']['box'][3]=52
 edit('attn_indices','J: new / shared')
 edit('aux_scope','Checkpoint config and module names verified\n59,585 tensor names · 282 shards\nNo tensor-header or GPU inference test\nIndexShare reuses positions, not per-layer KV')
 edit('mtp_scope','Own indexer; MTP-iteration share flag=true (backend)')
 edit('footer','Sources: official GLM-5.2 @cf457fa · Transformers @bbe484b · IndexShare evidence and backend limits in README / evidence.md')
 # Keep the approved adaptive layout, inserting a dedicated sharing band.
 for n in g['nodes']:
  if n['box'][1]>=1830:
   n['box'][1]+=340
   if 'operator_layout' in n:
    n['operator_layout']['lane_center'][1]+=340;n['operator_layout']['reserved_slot'][1]+=340
  for e in n.get('evidence',[]):
   e['locator']=e['locator'].replace('GLM-5.1','GLM-5.2')
 for edge in g['edges']:
  if 'points' in edge:edge['points']=[[x,y+340 if y>=1830 else y] for x,y in edge['points']]
 def node(key,label,box,header=False,frame=False,full_mode=False):
  color='#7356a6';fill='#f5f0fc' if full_mode else '#fbfaff'
  style=f'rounded=1;arcSize=12;absoluteArcSize=1;html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={26 if header else 22};fontColor=#493366;align=center;verticalAlign=middle;spacing=8;fillColor={fill};strokeColor={color};strokeWidth=1.2;'
  if header:style+='fillColor=none;strokeColor=none;fontStyle=1;'
  if frame:style+='fillColor=none;strokeColor=#c3cedb;dashed=1;dashPattern=6 4;'
  n=dict(id=key,label=label,description=label,box=box,kind='decoration',status='verified',style=style,
    evidence=[dict(source='config',locator='/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3'),dict(source='model',locator='Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398')])
  g['nodes'].append(n);ns[key]=n
 node('sharing','',[30,1830,2340,300],frame=True)
 node('sharing_title','IndexShare — reuse token positions across layers; keep KV caches independent',[50,1842,2300,50],header=True)
 for i,(label,x) in enumerate([('L2: FULL\ncompute J₂',130),('L3: SHARED\nreuse J₂',680),('L4: SHARED\nreuse J₂',1230),('L5: SHARED\nreuse J₂',1780)]):
  key=f'share_stage_{i}';node(key,label,[x,1940,420,75],full_mode=i==0)
  if i:g['edges'].append(dict(id=f'share_transfer_{i}',source=f'share_stage_{i-1}',target=key,ports=[1,.5,0,.5],routing='straight',color='#7356a6',role='index_share_illustration'))
 node('sharing_note','0-based: L0 /L1 also FULL. Next groups: L6 FULL →L7–9 SHARED; …; L74 FULL →L75–77 SHARED.\nJ is reused within the same forward query; it is not the previous decode token’s selection.',[70,2030,2260,80])
 ns['sharing_note']['style']+='fontSize=19;fillColor=none;strokeColor=none;'
 g['port_bindings']['J']['condition']='FULL layer only: compute fresh indices'
 g['port_bindings']['previous_J']=dict(source='share_stage_0',target='attn_indices',shape=['B','T','min(2048,context)'],condition='SHARED layers consume previous FULL layer indices in the same forward; schedule inset is illustrative')
 g['checkpoint'].update(revision=REV,indexer_mode='explicit full/shared IndexShare',full_indexer_layers=full,shared_indexer_layers=shared,auxiliary_indexer=True,context=1048576,rope_theta=8000000,index_share_for_mtp_iteration=c['index_share_for_mtp_iteration'])
 g['limitations']=[x for x in g['limitations'] if 'GLM-5.1' not in x]+['IndexShare inset illustrates per-query cross-layer propagation, not extra decoder layers.','MTP iteration sharing is declared by checkpoint config; its backend-specific execution was not traced.','Model-card FLOP/acceptance claims are not local throughput or inference measurements.']
 g['routing_summary']['straight']+=3
 g['presentation_policy']['reference']='Approved GLM-5.1 adaptive operator layout; shared core fields and pinned implementation rechecked.'
 return g

if __name__=='__main__':
 g=build();p=Path(__file__).with_name('glm52.graph.json');p.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
