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
 g['height']=3660;ns['footer']['box'][1]=3618
 g['tensor_contracts']={
  'symbols':{'B':'batch','S':'current query length','T':'cached + current key length','K':'min(2048,T)','N':'B*S tokens','m':'12288 dense; 2048 expert'},
  'dsa':{'input':['B','S',6144],'q_residual':['B','S',2048],'q':['B','S',64,256],'cache_latent':['B','T',1,512],'cache_rope':['B','T',1,64],'key_expanded':['B','T',64,256],'value_expanded':['B','T',64,256],'output':['B','S',6144]},
  'indexer':{'q':['B','S',32,128],'key':['B','T',128],'head_weights':['B','S',32],'scores':['B','S',32,'T'],'reduced_scores':['B','S','T'],'indices':['B','S','K']},
  'moe':{'router':['N',256],'selection':['N',8],'expert_input':['N_e',6144],'expert_hidden':['N_e',2048],'expert_output':['N_e',6144],'merged_output':['B','S',6144]},
  'absorbed_mqa_equivalent':{'q':['B','S',64,576],'selected_k':['B','S','K',1,576],'selected_v':['B','S','K',1,512],'latent_output':['B','S',64,512],'value_projected':['B','S',64,256],'output':['B','S',6144],'scope':'algebraic correspondence only; no backend execution or numeric equivalence test'}}
 def note(key,label,box,color='#526983',fill='none',size=22,bold=False,locator='Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward'):
  g['nodes'].append(dict(id=key,label=label,description=label,box=box,kind='decoration',status='verified',evidence=[dict(source='model',locator=locator),dict(source='config',locator='Explicit projection dimensions and model sizes')],style=f'rounded=1;arcSize=12;absoluteArcSize=1;html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={size};fontColor={color};align=center;verticalAlign=middle;spacing=12;fillColor={fill};strokeColor=none;fontStyle={1 if bold else 0};'))
 note('dim_title','Tensor dimensions — transformations within one forward pass',[30,2680,2340,55],size=28,bold=True)
 note('dim_symbols','B=batch · S=query length · T=KV length incl. cache · K=min(2048,T) · N=B×S · head axes shown before channel\nPrefill: S may be many tokens; decode: S=1, T grows. All network dimensions below also apply to GLM-5.2.',[50,2740,2300,85],size=21)
 note('dim_dsa_title','DSA / MLA  |  64 heads',[40,2840,750,45],color='#d78105',size=25,bold=True)
 note('dim_dsa','h [B,S,6144]\nQ down → [B,S,2048]\nQ up / reshape → [B,S,64,256]\nQ split: content192 + RoPE64\nKV down → [B,S,512+64]\nCache: c [B,T,1,512] + kPE [B,T,1,64]\nKV up: 512 → 64×(192+256)\nK [B,T,64,256] · V [B,T,64,256]\nAttention → [B,S,64,256]\nFlatten 16384 → O → [B,S,6144]',[40,2895,750,380],color='#915800',fill='#fff7e9',size=22)
 note('dim_index_title','Indexer  |  32 heads',[825,2840,750,45],color='#698e32',size=25,bold=True)
 note('dim_index','Qr [B,S,2048] → Qi [B,S,32,128]\nh [B,S,6144] → Ki [B,S,128]\nK cache → [B,T,128] (shared by heads)\nh → weights [B,S,32]\nQi × Kiᵀ → scores [B,S,32,T]\nReLU → weighted head sum\nReduced scores [B,S,T]\nCausal mask → TopK → J [B,S,K]\nFULL: compute J; SHARED: reuse J\nK is read selection, not cache capacity',[825,2895,750,380],color='#587a28',fill='#f7faef',size=22)
 note('dim_moe_title','FFN / MoE  |  256 experts, top-8',[1610,2840,750,45],color='#148b8c',size=25,bold=True)
 note('dim_moe','h [B,S,6144] → flatten [N,6144]\nRouter 6144 →256: scores [N,256]\nTop8 IDs / weights [N,8]\nDispatch → each expert input [N_e,6144]\nGate / Up → [N_e,2048] each\nSiLU(gate) × Up → Down → [N_e,6144]\nWeight / scatter-sum → [N,6144]\n+ shared expert → [B,S,6144]\nDense L0–2: m=12288 (no dispatch)\nLM head: [B,S,6144] → [B,S,154880]',[1610,2895,750,380],color='#137578',fill='#effafa',size=22)
 note('dim_mqa_title','Absorbed MQA correspondence — alternative algebraic view, not an additional model branch',[40,3300,2320,50],color='#d78105',size=26,bold=True)
 note('dim_mqa','Q content192 × W_Kᵀ →512; concat RoPE64 → Q_abs [B,S,64,576]\nSelected K_abs [B,S,K,1,576] = latent512 + positional64; selected V_abs [B,S,K,1,512]\nSoftmax(Q_abs K_absᵀ / sqrt(256)) V_abs → [B,S,64,512]\nPer-head W_V: 512 →256 → [B,S,64,256]; flatten → Linear O: 16384 →6144\nMQA uses one shared latent KV head. This is the screenshot’s 512+64 view; the main diagram explicitly expands K/V.\nSelection is query-dependent (S axis); no materialized gather, fused kernel or quantized numerical equivalence is claimed.',[40,3360,2320,240],color='#915800',fill='#fff7e9',size=22,locator='Algebra from Attention.__init__/expand_kv: kv_b_proj splits per-head W_K (512→192) and W_V (512→256); o_proj 64×256→6144')
 g['limitations'].append('Dimension guide uses logical sequence-major axes; absorbed MQA is an algebraic correspondence, not a verified backend or quantized numeric execution graph.')
 return g
if __name__=='__main__':
 g=build();Path(__file__).with_name('glm53.graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
