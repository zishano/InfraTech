"""K3.1-Pro source-reviewed delta, preserving the approved K3 diagram geometry."""
from pathlib import Path
import copy,json,sys,textwrap
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/model_architecture'))
from model_diff import mark,compare_configs

OUT=ROOT/'models/kimi_k_3_1_pro'
K3REV='f831ab66814297da540d832a5235f8e904f29d06'
REV='d9e99b0792a5e93b78ea9bea62a68167e36ddd9e'
SG='b09bda75c89a88263811a49e13adeef7a7aa8bf7'
HF=f'https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/{REV}/'
SGBASE=f'https://github.com/sgl-project/sglang/blob/{SG}/'
CARD='Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA'
CFG='/text_config/dsa_config; dsa_layers equal full_attn_layers (1-based)'
IDX='Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320'

def build():
 baseline=json.loads((OUT/'baseline_k3_config.json').read_text())
 target=json.loads((OUT/'official_config.json').read_text())
 reviewed=json.loads((OUT/'config_diff.json').read_text())['changes']
 assert compare_configs(baseline,target)==reviewed, 'Re-review changed configs before coloring the architecture'
 tc=target['text_config'];dc=tc['dsa_config']
 assert tc['num_hidden_layers']==93 and tc['hidden_size']==7168
 assert dc['dsa_layers']==tc['linear_attn_config']['full_attn_layers']==list(range(4,93,4))+[93]
 assert (dc['index_num_heads'],dc['index_head_dim'],dc['index_topk'],dc['index_rope_dim'])==(32,128,2048,0)
 assert baseline['vision_config']==target['vision_config']
 g=copy.deepcopy(json.loads((ROOT/'tools/model_architecture/examples/kimi_k3.graph.json').read_text()))
 g.update(title='Kimi-K3.1-Pro — architecture delta vs Kimi-K3',width=2920,height=2896)
 g['sources'].update(config=HF+'config.json',card=HF+'README.md',
   baseline_config=f'https://huggingface.co/moonshotai/Kimi-K3/blob/{K3REV}/config.json',
   baseline_code=f'https://huggingface.co/moonshotai/Kimi-K3/blob/{K3REV}/modeling_kimi_linear.py',
   engine=SGBASE+'python/sglang/srt/models/kimi_k3.py',
   engine_config=SGBASE+'python/sglang/srt/configs/kimi_linear.py',
   indexer=SGBASE+'python/sglang/srt/layers/attention/dsa/dsa_indexer.py',
   kernel=SGBASE+'python/sglang/kernels/ops/attention/dsa/cutedsl_fp8_paged_mqa_logits.py',
   metadata='https://huggingface.co/api/models/moonshotai/Kimi-K3.1-Pro/revision/'+REV)
 nodes={n['id']:n for n in g['nodes']}
 for n in g['nodes']:
  n['change']='unchanged';n['description']=n['label']
  n.setdefault('evidence',[]).append(dict(source='config',locator='Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json'))
 def edit(key,label,change=None,source='card',locator=CARD):
  n=nodes[key];n['label']=label
  if change:mark(n,change,locator=locator,source=source)
  return n
 def add(key,label,box,change=None,source='indexer',locator=IDX,kind='operation',font=22):
  if key in nodes:raise ValueError(key)
  x,y,w,h=box
  while True:
   lines=[s for l in label.split('\n') for s in (textwrap.wrap(l,max(3,int((w-24)/(font*.57))),break_long_words=False) or [''])]
   if len(lines)*font*1.18+20<=h or font<=14:break
   font-=1
  if len(lines)*font*1.18+20>h:raise ValueError((key,label,box))
  n=dict(id=key,label='\n'.join(lines),description=label,box=box,change='unchanged',kind=kind,status='verified',evidence=[dict(source=source,locator=locator)],
    style=f'rounded=1;arcSize=12;absoluteArcSize=1;whiteSpace=wrap;html=0;fontFamily=Arial;fontSize={font};fontColor=#26384c;align=center;verticalAlign=middle;spacing=8;strokeColor=#718096;strokeWidth=1;fillColor=#f4f7fb;')
  if change:mark(n,change,locator=locator,source=source)
  g['nodes'].append(n);nodes[key]=n;return n
 def edge(a,b,ports=None,points=None,role=None):
  e=dict(id='k31_link_'+a+'__'+b,source=a,target=b)
  if ports:e['ports']=ports
  if points:e['points']=points
  if role:e['role']=role
  g['edges'].append(e)
 def chain(*items):
  for a,b in zip(items,items[1:]):edge(a,b)
 def panel(key,label,box,change=None):
  n=add(key,'',box,change,kind='decoration',source='card',locator=CARD)
  n['style']+='fillColor=none;dashed=1;dashPattern=6 4;'
  x,y,w,h=box
  head=add(key+'_title',label,[x+10,y+10,w-20,46],change,kind='decoration',source='card',locator=CARD,font=26)
  head['style']+='fontStyle=1;'
 edit('title','Kimi-K3.1-Pro — Architecture Diff vs Kimi-K3')['box']=[10,0,2900,78]
 edit('subtitle','RED: added  |  GREEN: retired  |  YELLOW: parameter / config only')['box']=[40,80,2840,50]
 edit('params','2.8T / 104B active (card) · 93 layers · hidden 7168 · 96 heads · context 1M')['box']=[40,140,2840,66]
 edit('hybrid_outline','Hybrid backbone\n(93 layers)')
 for key,label in {
  'lm_repeat':'23 × [3 KDA + FFN, then\n1 Gated DSA + FFN]\n= 92 attention layers',
  'lm_final':'Final Gated DSA + FFN\n= 1 attention layer',
  'lm_counts':'69 KDA + 24 Gated DSA = 93\nL1 dense FFN; L2–93 MoE\nSame layer positions as K3',
  'm_title':'Gated DSA + FFN (×24)',
  'm_attn':'Gated DSA (NoPE)',
  'mla_title':'Gated DSA (NoPE) — sparse read',
  'mla_attention':'Sparse causal attention (NoPE)\nselected token positions',
 }.items():edit(key,label,'added')
 nodes['m_title']['label']=''
 nodes['m_title']['style']+='fillColor=none;strokeColor=none;'
 mark(nodes['mla'],'added',locator=CARD,source='card');nodes['mla']['style']+='fillColor=none;dashed=1;'
 edit('mla_note','Q rank 1536 · KV rank 512 · output gate retained\nConceptual unabsorbed view; no rotary operation')
 # Clarifications from newly accessible K3 config/code: neutral, not model deltas.
 edit('mla_q','Linear Q down\n7168 → 1536')
 add('mla_qnorm','RMSNorm\nQr [1536]',[1364,2020,172,70],source='baseline_code',locator='KimiMLAAttention.__init__/forward, lines 335–474',font=19)
 add('mla_qup','Linear Q up\n1536 → 96 × 192',[1364,1910,172,76],source='baseline_code',locator='KimiMLAAttention.forward, 419–424',font=18)
 g['edges']=[e for e in g['edges'] if (e['source'],e['target'])!=('mla_q','mla_port_q')]
 chain('mla_q','mla_qnorm','mla_qup','mla_port_q')
 nodes['mla_compress']['box']=[1544,2200,412,78]
 edit('mla_compress','Linear KV down + Split\n7168 → (512 + 64)')
 add('mla_kvnorm','RMSNorm (512)',[1554,2110,242,60],source='baseline_code',locator='KimiMLAAttention.forward, 426–443',font=20)
 add('mla_k64','k64\nNoPE',[1820,2110,136,60],source='baseline_code',locator='KimiMLAAttention.forward: unrotated shared k_rot channels, 426–450',font=18)
 nodes['mla_cache']['box']=[1549,2010,402,78]
 edit('mla_cache','Latent KV cache\n[512 + 64, NoPE]')
 edit('mla_reconstruct','Linear KV up / Split K,V\nK128 + k64; V128')
 g['edges']=[e for e in g['edges'] if (e['source'],e['target'])!=('mla_compress','mla_cache')]
 edge('mla_compress','mla_kvnorm',[.3,0,.5,1]);edge('mla_compress','mla_k64',[.84,0,.5,1])
 edge('mla_kvnorm','mla_cache',[.5,0,.32,1]);edge('mla_k64','mla_cache',[.5,0,.84,1])
 edit('vision_encoder','27 × MoonViT-V2\nhidden 1024 · QKV 1536')
 edit('vision_caveat','Vision config unchanged; projector type patchmergerv2')
 edit('sources','K3.1-Pro config / card @ d9e99b0 · K3 @ f831ab6 · SGLang @ b09bda7 · weight index / full weights not read')['box']=[20,2858,2880,34]
 # Diff register: removed all-token read is inactive and not connected to inference.
 panel('diff_register','CHANGE REGISTER / K3 → K3.1-Pro',[2220,232,670,1090])
 add('diff_added','ADDED\nGated DSA ×24\nIndexer + per-query TopK ≤2048',[2240,330,630,180],'added',source='card',locator=CARD,font=25)
 add('retired_dense_attention','RETIRED / K3 ONLY\nDense all-token attention\nMLA latent projections are retained',[2240,550,630,170],'removed',source='card',locator=CARD,font=24)
 add('diff_quant','PARAMETER / CONFIG ONLY\nQuantization ignore patterns: 6 → 8',[2240,760,630,120],'parameter_changed',source='config',locator='/text_config/quantization_config/ignore; two additional regex patterns',font=24)
 add('diff_count','HF BF16 tensor-elements\n57,179,884,544 → 57,358,410,752\n+178,526,208 (matches new indexer)',[2240,910,630,160],'parameter_changed',source='metadata',locator='safetensors.parameters.BF16; compare pinned baseline metadata; derived indexer count in checkpoint_summary.json',font=22)
 add('diff_unchanged','UNCHANGED\n93 layers · KDA69 · hidden7168\n896 experts / top16 · latent3584\nMoonViT-V2 · context1M',[2240,1110,630,175],source='config',locator='Shared fields equal across both pinned configs; see config_diff.json',kind='decoration',font=21)['style']+='fillColor=none;strokeColor=none;'
 # Added indexer, independently projected Q / K / head weights.
 panel('dsa_indexer','ADDED · DSA Indexer (per DSA layer)',[2220,1336,670,1096],'added')
 add('idx_scope','32 heads ×128 · NoPE · no Hadamard',[2240,1392,630,40],'added',source='engine_config',locator='_init_dsa, lines 137–174',kind='decoration',font=19)['style']+='fillColor=none;strokeColor=none;'
 defs=[
 ('idx_qr','Qr [1536]',[2250,2320,170,50]),
 ('idx_h','h [7168]',[2490,2320,350,50]),
 ('idx_qproj','Linear Wq\n1536 → 32×128',[2250,2200,170,70]),
 ('idx_qquant','FP8 Quant',[2250,2070,170,60]),
 ('idx_q','Qᵢ [32,128]',[2250,1950,170,60]),
 ('idx_kproj','Linear Wk\n7168 →128',[2470,2200,170,70]),
 ('idx_knorm','LayerNorm',[2470,2100,170,60]),
 ('idx_kquant','FP8 Quant',[2470,2000,170,60]),
 ('idx_cache','Index key cache\n[T,128]',[2470,1890,170,70]),
 ('idx_wproj','Linear Wweights\n7168 →32',[2680,2200,180,70]),
 ('idx_scale','Scale\n32^-0.5 ×128^-0.5',[2680,2070,180,70]),
 ('idx_weights','Head weights [32]',[2680,1940,180,60]),
 ('idx_dot','Matmul (Qᵢ, Kᵢᵀ)',[2260,1760,420,70]),
 ('idx_relu','ReLU',[2260,1680,420,54]),
 ('idx_sum','Scale by head weights → Sum (heads)',[2260,1600,420,60]),
 ('idx_mask','Causal mask',[2260,1520,420,54]),
 ('idx_topk','TopK (≤2048) → token indices',[2260,1440,420,60]),
 ]
 for key,label,box in defs:
  source='kernel' if key in ['idx_relu','idx_sum'] else 'indexer'
  locator='relu2_fma_f32x2 and epilogue weighted head reduction, 180–190 / 1416–1542' if source=='kernel' else IDX
  add(key,label,box,'added',source=source,locator=locator,font=21)
 chain('idx_qr','idx_qproj','idx_qquant','idx_q')
 edge('idx_h','idx_kproj',[(2555-2490)/350,0,.5,1]);edge('idx_h','idx_wproj',[(2770-2490)/350,0,.5,1])
 chain('idx_kproj','idx_knorm','idx_kquant','idx_cache');chain('idx_wproj','idx_scale','idx_weights')
 edge('idx_q','idx_dot',[.5,0,(2335-2260)/420,1]);edge('idx_cache','idx_dot',[.5,0,(2555-2260)/420,1])
 chain('idx_dot','idx_relu','idx_sum','idx_mask','idx_topk')
 edge('idx_weights','idx_sum',[1,.5,1,.5],[[2875,1970],[2875,1630]])
 edge('idx_topk','mla_attention',[0,.5,1,.5],[[2185,1470],[2185,1713]],role='added_sparse_selection')
 g['edges'][-1]['diff_change']='added'
 # Evidence/scope area, aligned to unchanged vision block.
 panel('scope_panel','READING THIS DIFF',[2220,2452,670,402])
 add('scope_text','Color = model delta, not a claim\nof changed hidden/expert dimensions.\nGreen nodes are historical only.\nIndex Q/K quantization is engine-specific.',[2240,2530,630,150],source='config',locator='config_diff.json + pinned SGLang Indexer backend',kind='decoration',font=21)['style']+='fillColor=none;strokeColor=none;'
 add('scope_limits','Config + model card + engine checked.\nNo full weights or tensor headers read.\nNo GPU inference executed.',[2240,2710,630,120],source='card',locator='Source inventory and checkpoint_summary.json',kind='decoration',font=20)['style']+='fillColor=none;strokeColor=none;'
 # Reserve green/yellow exclusively for requested diff meanings. The old KDA
 # palette was green, so shared modules become neutral while geometry is kept.
 for n in g['nodes']:
  if n.get('change')!='unchanged':continue
  if n['id']=='ar_source':n['style']+='fillColor=#66768b;strokeColor=#66768b;'
  elif n['id'].endswith('_title') and n['label']:
   n['style']+='fillColor=#59718f;strokeColor=none;fontColor=#ffffff;'
  elif n.get('kind')=='decoration':
   n['style']+='fillColor=none;fontColor=#435671;'
   n['style']+='strokeColor=#b5c1d0;' if not n['label'] or n['id']=='hybrid_outline' else 'strokeColor=none;'
  else:n['style']+='fillColor=#f3f6fb;strokeColor=#8e9db0;fontColor=#26384c;'
 for e in g['edges']:
  if (e['source'].startswith('idx_') and e['target'].startswith('idx_')) or e.get('role')=='added_sparse_selection':
   e['color']='#c62828';e['change']='added'
 g['port_bindings']={'Qr':dict(source='mla_qnorm',target='idx_qr',shape=['T',1536]),'h':dict(source='mla_x',target='idx_h',shape=['T',7168])}
 g['comparison']=dict(baseline='moonshotai/Kimi-K3',baseline_revision=K3REV,target='moonshotai/Kimi-K3.1-Pro',target_revision=REV,
   baseline_graph='tools/model_architecture/examples/kimi_k3.graph.json',layer_numbering='Config lists are 1-based; Python layer_idx is 0-based',themes=dict(added='red',removed='green',parameter_changed='yellow'),
   active_attention_counts=dict(kda=69,dsa=24),retired_nodes=['retired_dense_attention'],unchanged=['KDA five-path topology','AttnRes','Stable LatentMoE','MoonViT-V2','Output gate and NoPE','93-layer positions'],
   clarified_not_model_deltas=['Dense FFN is first layer in BOTH configs','Q rank1536 / KV rank512 available in BOTH configs','num_nextn_predict_layers=0 in BOTH released configs; do not invent an MTP deletion','Model-card 2.8T /104B are rounded; old report2.78T /104.2B are not evidence of changed model scale'])
 g['limitations']=['No K3.1 forward implementation is bundled in its pinned HF file list; DSA details are read from pinned model-card-recommended SGLang.',
   'Weight index downloads redirect to a host denied by active policy; no index/tensor-header/full-weight verification.',
   'HF safetensors metadata element counts are provider metadata, not an independent logical parameter recount.',
   'Q/K FP8 index-cache path is backend-specific; no NoPE RoPE or Hadamard operations are drawn.',
   'Shared K3 modules retain the reviewed report topology and are cross-checked against equal released config fields.','No GPU model execution or Feishu-client import test.']
 from kimi_k31_presentation import present
 return present(g)

if __name__=='__main__':
 g=build();path=Path(__file__).with_name('kimi_k31_pro.graph.json');path.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');print(path,len(g['nodes']),'nodes',len(g['edges']),'edges')
