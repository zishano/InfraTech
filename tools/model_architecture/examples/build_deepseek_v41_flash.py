"""Official DeepSeek-V4.1-Flash: source-reviewed graph, no model code execution."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).parent));sys.path.insert(0,str(Path(__file__).parents[1]))
from glm53_function_colors import FUNCTION_COLORS
from model_architecture import validate,drawio
from routing import simplify_connections
REV='314113f8a7dadb388215396ba5fbee2c610a04d6'
OUT=ROOT/'models/deepseek_v4_1/flash'
C=json.loads((OUT/'official_config.json').read_text());T=C['text_config'];V=C['vision_config']
for key,expected in dict(hidden_size=5120,num_hidden_layers=40,num_attention_heads=64,head_dim=512,q_lora_rank=1280,o_lora_rank=1024,o_groups=8,n_routed_experts=384,num_experts_per_tok=6,n_shared_experts=1,moe_intermediate_size=2304,hc_mult=4,engram_n_heads=8,engram_head_dim=256,engram_max_ngram_size=4,num_nextn_predict_layers=3,index_topk=512,dspark_markov_rank=256,dspark_block_size=5).items():
 assert T[key]==expected, f'Re-review changed checkpoint field: {key}'
assert T['compress_ratios']==[0,0]+[2]*18+[1]*20+[0]*3
assert T['kv_source_layer_ids']==[2,8,14,20]
assert T['index_source_layer_ids']==[2,8,14,20,24,28,32,36]
assert T['engram_layer_ids']==[1,14] and T['dspark_target_layer_ids']==[37,38,39]
HF=f'https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/{REV}/'
SOURCES={k:HF+v for k,v in dict(config='config.json',model='inference/model.py',kernel='inference/kernel.py',engram='inference/engram.py',vision='inference/vision.py',card='README.md',index='model.safetensors.index.json',runtime='inference/README.md').items()}
LIMITS=['Official unsuffixed checkpoint, not -1017.','Shapes are logical global dimensions; tensor-parallel ranks may shard heads/experts.','Official minimal implementation loops through all 40 layers; optimized CED prefill, bounded replay and DSpark verification scheduler are model-card designs, not locally executed paths.','Reference quantizers simulate quantize/dequantize in floating cache buffers; packed cache bytes are official claims.','Weight index verifies names, not tensor shapes/values. No full weights, GPU inference, benchmark, numerical equivalence or Feishu import test.','Technical-report PDF download blocked by proxy; card and pinned reference sources were read.']
class Diagram:
 def __init__(self,title,w,h):
  self.g=dict(version=1,title=title,width=w,height=h,background='#ffffff',sources=SOURCES,nodes=[],edges=[],limitations=LIMITS,checkpoint=dict(revision=REV,text_layers=40,mtp_layers=3,vision_layers=32),repetition_groups=[])
  self.ns={}
 def node(self,key,text,cx,y,w=260,h=None,role='tensor',source='model',locator='Attention / Block / Transformer.forward',kind='operation',font=20):
  if h is None:h=64 if '\n' in text else 46
  p=FUNCTION_COLORS[role];style=f'rounded=1;arcSize=10;absoluteArcSize=1;html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={font};fontColor={p["text"]};align=center;verticalAlign=middle;spacing=6;fillColor={p["fill"]};strokeColor={p["stroke"]};strokeWidth=1;'
  if text in ('+','×'):style+='shape=ellipse;fontSize=27;'
  n=dict(id=key,label=text,box=[cx-w/2,y,w,h],style=style,kind=kind,status='verified',functional_role=role,evidence=[dict(source=source,locator=locator)])
  assert key not in self.ns;self.ns[key]=n;self.g['nodes'].append(n);return key
 def note(self,key,text,x,y,w,h,font=18,source='model',locator='Reviewed module semantics'):
  self.node(key,text,x+w/2,y,w,h,source=source,locator=locator,kind='decoration',font=font)
  self.ns[key]['style']+='fillColor=none;strokeColor=none;fontColor=#526171;'
 def panel(self,key,title,x,y,w,h,color='#59718f'):
  self.note(key,'',x,y,w,h);self.ns[key]['style']+='strokeColor=#c3cedb;dashed=1;dashPattern=6 4;'
  self.note(key+'_title',title,x+10,y+10,w-20,48,26)
  self.ns[key+'_title']['style']+=f'fillColor={color};fontColor=#ffffff;fontStyle=1;'
 def frame(self,key,x,y,w,h,count,members):
  self.note(key,'',x,y,w,h);self.ns[key]['style']+='rounded=0;strokeColor=#59718f;strokeWidth=1.5;'
  self.note(key+'_count','×'+str(count),x+10,y+5,90,40,26);self.ns[key+'_count']['style']+='align=left;fontStyle=1;'
  self.g['repetition_groups'].append(dict(frame=key,count=count,members=members,scope='Layer template; per-layer modes/parameters may differ.'))
 def edge(self,a,b,label='',ports=None,points=None,role=None):
  e=dict(id='e_'+a+'__'+b,source=a,target=b,routing='straight')
  if label:e.update(label=label,tensor_shape=label,label_font_size=17)
  if ports:e['ports']=ports
  if points:e['points']=points
  if role:e['role']=role
  self.g['edges'].append(e)
 def chain(self,keys,labels=None):
  for i,(a,b) in enumerate(zip(keys,keys[1:])):self.edge(a,b,(labels or ['']*(len(keys)-1))[i])
 def params(self,key,title,paths,x,y,w,h,font=17):
  rows=[]
  for path in paths:
   v=C
   for part in path.strip('/').split('/'):v=v[part]
   rows.append(dict(path=path,value=v))
  def fmt(v):return v if isinstance(v,str) else json.dumps(v,separators=(',',':'))
  text=title+'\n'+'\n'.join(r['path'].split('/')[-1]+' = '+fmt(r['value']) for r in rows)
  self.note(key,text,x,y,w,h,font,source='config',locator='; '.join(paths));n=self.ns[key];n['style']+='align=left;';n['config_parameters']=rows
 def finish(self):
  simplify_connections(self.g)
  self.g['presentation_policy']=dict(reference='GLM-5.3 d8dc8ea confirmed workflow',flow='bottom-up',functional_palette=FUNCTION_COLORS,legend=False,parameter_notes='Pinned HF config fields in module whitespace',implementation_view='Official minimal reference, plus separately labeled model-card runtime claims')
  validate(self.g);return self.g

def overview():
 d=Diagram('DeepSeek-V4.1-Flash — CED + CSA2 + Engram + vision',3000,3740)
 d.note('title','DeepSeek-V4.1-Flash  |  CED · CSA2 · Engram · native vision',30,10,2940,70,40)
 d.note('facts','40 layers =20 encoder +20 decoder · hidden5120 · 384 experts /top6 +1 shared · context1M',30,85,2940,52,26,source='config')
 d.note('symbols','B=batch · S=query length · T=history length · Tg=floor(T/r) · N=B×S · all layer IDs are 0-based',30,143,2940,34,17)
 d.panel('attention','CSA2 — local SWA + shared global K=V',30,190,1040,1600,'#a7773e')
 d.panel('backbone','Causal encoder → decoder',1100,190,650,2450)
 d.panel('indexer','CSA2 Indexer — Full / Reindex layers',1780,190,1190,1040,'#527d5d')
 d.panel('moe','Mixture of Experts — every main layer',1780,1260,1190,1020,'#3f7e78')
 d.panel('engram','Engram — token-conditioned memory',30,1820,1040,820,'#7a6794')
 d.panel('mhc','Single-pass mHC — pre / post / comb',1780,2310,1190,1360,'#7a6794')
 d.panel('vision','DeepSeek-ViT + image projector',30,2670,1040,1000,'#59718f')
 d.panel('dspark','DSpark — auxiliary draft path',1100,2670,650,1000,'#59718f')
 # Main CED stream, with complete repeated templates rather than Repeat operators.
 for key,text,y,role in [
 ('tokens','Text / image token IDs',2130,'tensor'),('embedding','Embedding',2040,'projection'),('merge','Merge image spans ← V',1950,'tensor'),('expand','Broadcast 4 HC streams',1840,'tensor'),
 ('enc_engram','Engram only at L1 /L14',1660,'selection'),('enc_attn','mHC pre → Norm\nSWA / CSA2 (r=2)',1545,'attention'),('enc_ffn','mHC post / pre → Norm\nMoE',1420,'expert'),('enc_post','mHC post\n4 residual streams',1295,'elementwise'),
 ('encoder_output','Encoder boundary H20',1130,'tensor'),('dec_attn','mHC pre → Norm\nCSA2 (r=1)',930,'attention'),('dec_ffn','mHC post / pre → Norm\nMoE',805,'expert'),('dec_post','mHC post\n4 residual streams',680,'elementwise'),
 ('collapse','mHC collapse + RMSNorm',490,'normalization'),('lm_head','LM head · 5120→129280',385,'projection'),('logits','Logits / sample',285,'tensor')]:
  d.node(key,text,1425,y,490,role=role,locator='Transformer.forward 1240–1276; Block.forward 967–996; model card CED')
 d.frame('encoder_repeat',1130,1220,590,550,20,['enc_engram','enc_attn','enc_ffn','enc_post'])
 d.frame('decoder_repeat',1130,600,590,460,20,['dec_attn','dec_ffn','dec_post'])
 seq=['tokens','embedding','merge','expand','enc_engram','enc_attn','enc_ffn','enc_post','encoder_output','dec_attn','dec_ffn','dec_post','collapse','lm_head','logits']
 d.chain(seq,['[B,S]','[B,S,5120]','[B,S,5120]']+['[B,S,4,5120]']*9+['[B,S,5120]','[B,129280]'])
 d.params('backbone_params','checkpoint config',['/text_config/num_hidden_layers','/text_config/hidden_size','/text_config/max_position_embeddings'],1130,2190,590,110,17)
 d.note('mode_title','CSA2 layer modes · shared runtime',1130,2310,590,40,22)
 for key,text,y,role in [('full_modes','Full: L2,L8,L14,L20\nnew KV + index K + TopK',2370,'cache'),('reindex_modes','Reindex: L24,L28,L32,L36\nshared KV/K; refresh Q, weights, TopK',2455,'selection'),('reuse_modes','Reuse: other L2–39 · share KV/K/TopK\nL0–1: SWA only · no global cache',2540,'selection')]:
  d.node(key,text,1425,y,570,70,role=role,kind='decoration',font=18,locator='Attention.__init__; SharedAttentionRuntime; config source lists')
 # Main attention, explicitly one shared K=V head (no MLA KV-up reconstruction).
 for key,text,cx,y,w,role in [
 ('a_h','h [5120]',550,1640,920,'tensor'),('a_qa','Linear Q↓\n5120→1280',300,1525,260,'projection'),('a_qn','RMSNorm1280',300,1410,210,'normalization'),('a_qb','Linear Q↑\n1280→64×512',300,1290,270,'projection'),('a_qr','RoPE tail64',300,1160,220,'position'),
 ('a_kv','Linear KV\n5120→512',860,1525,260,'projection'),('a_kn','RMSNorm512',860,1410,210,'normalization'),('a_kr','RoPE tail64',860,1290,220,'position'),('a_fp8','FP8 Q/DQ\nall512 incl. RoPE',860,1170,260,'cache'),('a_ring','Local SWA ring\n128 ×512',860,1045,260,'cache'),
 ('a_global','Global KV · source\nr=2 encoder /1 decoder',520,900,240,'cache'),('a_concat','Concat SWA + global KV',900,900,260,'tensor'),('a_j','Window IDs + J',140,865,190,'selection'),
 ('a_core','Sparse gather → Attention\nshared K=V · attention sink',580,730,600,'attention'),('a_inverse','Inverse RoPE tail64',580,620,310,'position'),('a_oa','Grouped Oa\n8 ×(4096→1024)',580,500,320,'projection'),('a_ob','Linear Ob\n8192→5120',580,390,270,'projection'),('a_output','Attention output',580,290,300,'tensor')]:
  d.node(key,text,cx,y,w,role=role,locator='Attention 614–791; sparse_attn kernel 311–404')
 d.chain(['a_h','a_qa','a_qn','a_qb','a_qr','a_core','a_inverse','a_oa','a_ob','a_output'],['[B,S,5120]','[B,S,1280]','[B,S,1280]','[B,S,64,512]','Q [B,S,64,512]','[B,S,64,512]','[B,S,8,4096]','[B,S,8,1024]','[B,S,5120]'])
 d.chain(['a_h','a_kv','a_kn','a_kr','a_fp8','a_ring','a_concat','a_core'],['[B,S,5120]','[B,S,512]','[B,S,512]','[B,S,512]','','[B,128,512]','KV [B,128+Tg,512]'])
 d.edge('a_global','a_concat','[B,Tg,512]',[1,.5,0,.5]);d.edge('a_j','a_core','[B,S,≤128+512]',[.5,0,0,.5],[[140,770]])
 d.params('attention_params','HF text_config',['/text_config/q_lora_rank','/text_config/head_dim','/text_config/qk_rope_head_dim','/text_config/o_groups','/text_config/o_lora_rank','/text_config/sliding_window','/text_config/compress_rope_theta'],60,300,360,345)
 # Full/Reindex indexer. The reference scores globally and masks candidates afterwards.
 for key,text,cx,y,w,role in [
 ('i_qr','Qr [1280]',1960,1120,230,'tensor'),('i_latent','RoPE-free latent512\nFull owners only',2380,1120,270,'tensor'),('i_h','h [5120]',2800,1120,260,'tensor'),
 ('i_qp','Linear Qi\n1280→32×128',1960,1010,280,'projection'),('i_kp','Linear Ki\n512→128',2380,1010,270,'projection'),('i_qrot','RoPE64 → FP4 Q/DQ',1960,900,300,'position'),('i_krot','RMSNorm → RoPE64\nFP4 Q/DQ',2380,900,300,'normalization'),('i_wp','Linear weights\n5120→32; scale1/64',2800,900,290,'projection'),
 ('i_q','Qi [32,128]',1960,790,230,'tensor'),('i_cache','Shared index K cache',2380,790,300,'cache'),('i_dot','Matmul(Qi,Kiᵀ) → ReLU',2200,680,590,'selection'),('i_sum','Weighted head sum + TP reduce',2200,560,590,'selection'),('i_mask','Causal visibility mask',2200,450,360,'selection'),
 ('i_candidates','L20: select candidate blocks\nLater Reindex: apply candidate mask',2200,350,590,'selection'),('i_topk','TopK≤512 → position sort\noffset / invalid=-1',2200,270,430,'selection')]:
  d.node(key,text,cx,y,w,role=role,locator='Indexer 488–581; select_candidate_blocks 584–611')
 d.chain(['i_qr','i_qp','i_qrot','i_q','i_dot','i_sum','i_mask','i_candidates','i_topk'],['[B,S,1280]','[B,S,32,128]','','[B,S,32,128]','[B,S,32,Tg]','[B,S,Tg]','[B,S,Tg]',''])
 d.chain(['i_latent','i_kp','i_krot','i_cache','i_dot'],['[B,Tg,512]','[B,Tg,128]','','[B,Tg,128]'])
 d.edge('i_h','i_wp','[B,S,5120]');d.edge('i_wp','i_sum','w [B,S,32]',[.5,0,1,.5],[[2800,592]])
 d.params('index_params','HF text_config',['/text_config/index_n_heads','/text_config/index_head_dim','/text_config/index_topk','/text_config/candidate_topk_blocks','/text_config/candidate_block_size'],2535,265,400,260,17)
 # Router and expert result aggregation; weight is applied before expert down projection.
 for key,text,cx,y,w,role in [('m_h','h [5120]',2375,2170,1040,'tensor'),('m_router','Linear → sqrt(Softplus)\nFP32 router',2050,2050,330,'routing'),('m_select','+ text / VL bias → Top6',2050,1930,340,'routing'),('m_weights','Gather raw scores\nnormalize → ×1.5',2050,1810,330,'routing'),('m_experts','384 experts /6 active\nclipped SwiGLU · ×w before Down',2050,1630,370,'expert'),('m_sum','Scatter / sum expert outputs',2050,1470,370,'elementwise'),('m_shared','Shared expert ×1\n5120→2304→5120',2770,1670,330,'expert')]:
  d.node(key,text,cx,y,w,role=role,locator='Gate 794–829; Expert 832–853; MoE 856–906')
 d.node('m_add','+',2320,1360,46,46,'elementwise')
 d.chain(['m_h','m_router','m_select','m_weights','m_experts','m_sum','m_add'],['[N,5120]','[N,384]','IDs [N,6]','w [N,6]','[N,6,5120]','[N,5120]'])
 d.edge('m_h','m_experts','x [N,5120]',[0,.5,0,.5],[[1820,2193],[1820,1662]])
 d.edge('m_h','m_shared','[N,5120]');d.edge('m_shared','m_add','[N,5120]',[.5,0,1,.5],[[2770,1383]])
 d.params('moe_params','HF text_config',['/text_config/n_routed_experts','/text_config/num_experts_per_tok','/text_config/n_shared_experts','/text_config/moe_intermediate_size','/text_config/scoring_func','/text_config/routed_scaling_factor','/text_config/swiglu_limit'],2300,1770,310,345,16)
 # Engram: 24 independent lookups, normalized key match, signed sqrt gate, residual write.
 for key,text,cx,y,w,role in [('e_tokens','Text IDs / compressed map',280,2520,360,'tensor'),('e_hash','2 /3 /4-gram ×8 heads\nhash / modulo buckets',280,2410,360,'selection'),('e_lookup','Embedding lookup + flatten\n24×256 =6144',280,2300,370,'cache'),('e_kv','Linear Wkv → split K / V\n6144→4×5120 +5120',280,2190,370,'projection'),('e_stream','HC stream x',800,2520,350,'tensor'),('e_dot','Normalized stream·key\nper-copy weighted dot',800,2190,350,'normalization'),('e_gate','Signed sqrt → Sigmoid',800,2080,350,'elementwise'),('e_value','gate × shared value V',800,1970,350,'elementwise')]:
  d.node(key,text,cx,y,w,role=role,locator='Engram 328–366; EngramLayout / NgramHashState',source='model')
 d.node('e_add','+',800,1900,46,46,'elementwise')
 d.chain(['e_tokens','e_hash','e_lookup','e_kv'],['[B,S]','[B,S,24]','[B,S,6144]']);d.edge('e_kv','e_dot','K [B,S,4,5120]',[1,.5,0,.5]);d.edge('e_stream','e_dot','[B,S,4,5120]')
 d.chain(['e_dot','e_gate','e_value','e_add'],['[B,S,4]','[B,S,4]','[B,S,4,5120]'])
 d.edge('e_kv','e_value','V [B,S,5120]',[1,.5,0,.5],[[580,2222],[580,2002]])
 d.edge('e_stream','e_add','residual',[1,.5,1,.5],[[1035,2543],[1035,1923]])
 d.params('engram_params','HF text_config',['/text_config/engram_layer_ids','/text_config/engram_max_ngram_size','/text_config/engram_n_heads','/text_config/engram_head_dim'],60,1910,390,230,16)
 # Single-pass mHC: computed pre is forwarded to the NEXT sublayer.
 for key,text,cx,y,w,role in [('hc_x','HC stream x',2375,3550,1020,'tensor'),('hc_flat','Flatten + RMS statistic',2070,3440,350,'normalization'),('hc_linear','FP32 Linear\n20480→24',2070,3320,320,'projection'),('hc_split','Split pre4 / post4 / comb16',2070,3210,450,'tensor'),('hc_pre_new','Sigmoid + eps\nnew pre',1920,3070,220,'elementwise'),('hc_post_new','2 × Sigmoid\npost',2180,3070,220,'elementwise'),('hc_comb','Softmax matrix',2440,3070,220,'elementwise'),('hc_sink','Sinkhorn ×20',2440,2930,260,'normalization'),('hc_next','pre → next sublayer',1920,2930,250,'tensor'),('hc_prev','Incoming pre\nfrom previous sublayer',2780,3330,320,'tensor'),('hc_collapse','Weighted stream sum',2780,3210,320,'elementwise'),('hc_norm','RMSNorm5120',2780,3100,230,'normalization'),('hc_sublayer','Attention / MoE',2780,2990,320,'attention'),('hc_expand','post × output\nexpand to4 streams',2780,2850,330,'elementwise'),('hc_resmix','combᵀ × residual',2440,2710,330,'elementwise'),('hc_out','Updated HC stream',2780,2420,320,'tensor')]:
  d.node(key,text,cx,y,w,role=role,locator='Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel',font=19)
 d.node('hc_add','+',2780,2580,46,46,'elementwise')
 d.chain(['hc_x','hc_flat','hc_linear','hc_split'],['[B,S,4,5120]','[B,S,20480]','[B,S,24]'])
 for key in ['hc_pre_new','hc_post_new','hc_comb']:d.edge('hc_split',key)
 d.edge('hc_pre_new','hc_next','[B,S,4]');d.edge('hc_comb','hc_sink','[B,S,4,4]')
 d.edge('hc_prev','hc_collapse','[B,S,4]');d.edge('hc_x','hc_collapse','x',[1,.5,1,.5],[[2940,3573],[2940,3233]])
 d.chain(['hc_collapse','hc_norm','hc_sublayer','hc_expand','hc_add','hc_out'],['[B,S,5120]','[B,S,5120]','[B,S,5120]','[B,S,4,5120]','[B,S,4,5120]'])
 d.edge('hc_post_new','hc_expand','[B,S,4]',[.5,0,0,.5],[[2180,2882]])
 d.edge('hc_sink','hc_resmix','[B,S,4,4]');d.edge('hc_x','hc_resmix','residual',[0,.5,0,.5],[[1795,3573],[1795,2742]])
 d.edge('hc_resmix','hc_add','[B,S,4,5120]',[.5,0,0,.5],[[2440,2603]])
 d.params('mhc_params','HF text_config',['/text_config/hc_mult','/text_config/hc_sinkhorn_iters','/text_config/hc_eps','/text_config/rms_norm_eps'],1820,2390,650,220,18)
 # Vision uses real image-span replacement, not additive multimodal fusion.
 for key,text,y,role in [('v_patches','Image patches',3560,'tensor'),('v_patch','Linear patch embedding\n3×14×14→1024',3450,'projection'),('v_attn','Norm → 2D-RoPE attention\n+ residual',3270,'attention'),('v_ffn','Norm → SwiGLU\n+ residual',3150,'expert'),('v_norm','RMSNorm1024',2990,'normalization'),('v_unshuffle','3×3 pixel-unshuffle\n1024→9216',2880,'tensor'),('v_project','Linear9216→5120\nGELU → Linear5120→5120',2770,'projection')]:
  d.node(key,text,720,y,520,role=role,source='vision',locator='PatchEmbed / ViT / Block / Aligner')
 d.frame('vit_repeat',440,3090,560,310,32,['v_attn','v_ffn'])
 d.chain(['v_patches','v_patch','v_attn','v_ffn','v_norm','v_unshuffle','v_project'],['[Np,3,14,14]','[Np,1024]','[Np,1024]','[Np,1024]','[Np,1024]','[Nv,9216]'])
 d.params('vision_params','HF vision_config',['/vision_config/num_hidden_layers','/vision_config/hidden_size','/vision_config/num_attention_heads','/vision_config/intermediate_size','/vision_config/downsample_ratio','/vision_config/max_image_tokens'],60,2760,360,290,16)
 # DSpark forward exists, but the reference generation loop does not call it.
 for key,text,y,role in [('ds_taps','Mean over HC streams\nconcat inputs at L37 /38 /39',3550,'tensor'),('ds_proj','Linear15360→5120\nRMSNorm → main_x',3440,'projection'),('ds_seed','Seed + noise token embeddings\n5 draft positions · broadcast HC4',3320,'tensor'),('ds_stage','DSpark SWA + single-pass mHC\nMoE128 /top3 +1 shared',3200,'expert'),('ds_collapse','HC collapse',3070,'elementwise'),('ds_norm','RMSNorm5120',2990,'normalization'),('ds_head','LM head + Markov rank256\n5-position sequential sampling',2880,'projection'),('ds_confidence','Confidence Linear\n(5120+256)→1',2770,'projection')]:
  d.node(key,text,1425,y,550,role=role,font=18,locator='DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159')
 d.frame('dspark_repeat',1120,3120,610,180,3,['ds_stage'])
 d.edge('ds_taps','ds_proj','[B,S,15360]');d.edge('ds_seed','ds_stage','[B,5,4,5120]');d.edge('ds_proj','ds_stage','main_x',[1,.5,1,.5],[[1730,3472],[1730,3232]])
 d.chain(['ds_stage','ds_collapse','ds_norm','ds_head','ds_confidence'],['[B,5,4,5120]','[B,5,5120]','[B,5,5120]','Markov [B,5,256]'])
 d.edge('ds_collapse','ds_confidence','hidden',[1,.5,1,.5],[[1730,3093],[1730,2802]])
 d.note('ds_params','dspark_block_size=5 · noise_token_id=128799\ndspark_n_routed_experts=128 · top3',1120,3620,610,50,16,source='config',locator='/text_config/dspark_*')
 for e in d.g['edges']:
  if e['id']=='e_m_h__m_experts':e['label_offset']=[-50,0]
  if e['id']=='e_hc_resmix__hc_add':e['label_offset']=[-70,0]
 d.note('footer','Official HF @314113f · 96,085 tensor names /48 shards checked · implementation and deployment limits in README',40,3690,2920,40,16,source='index')
 d.g['port_bindings']={'V':dict(source='v_project',target='merge',shape=['Nv',5120],meaning='replace image-token spans; learned delimiters separately'), 'Qr':dict(source='a_qn',target='i_qr',shape=['B','S',1280]),'J':dict(source='i_topk',target='a_j',shape=['B','S','≤512'])}
 return d.finish()

if __name__=='__main__':
 g=overview();p=Path(__file__).with_name('deepseek_v41_flash.graph.json');p.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');drawio(g,OUT/'deepseek_v41_flash_architecture.drawio');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
