"""GLM-5.1 checkpoint-reviewed operator diagram; no remote model code execution."""
from pathlib import Path
import json,sys,textwrap
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/model_architecture'))
from routing import simplify_connections
from operator_layout import fit_operators
REV='26e1bd6e011feb778d25ae34b09b07074139d92d'
TF='f262c71703eb138381d65ced86b3aaa496be0196'
HF=f'https://huggingface.co/zai-org/GLM-5.1/blob/{REV}/'
BASE=f'https://github.com/huggingface/transformers/blob/{TF}/src/transformers/models/glm_moe_dsa/'
COLORS={'blue':('#526ab8','#f0f4ff'),'orange':('#cf861d','#fff6e8'),'green':('#679336','#f3f8ec'),'teal':('#298c87','#edf8f6'),'gray':('#75869d','#f4f6fa'),'red':('#bf5b66','#fff2f3')}

def build():
 c=json.loads((ROOT/'models/glm_5_1/official_config.json').read_text());summary=json.loads((ROOT/'models/glm_5_1/checkpoint_summary.json').read_text())
 assert (c['num_hidden_layers'],c['hidden_size'],c['first_k_dense_replace'])==(78,6144,3)
 assert all(r['indexer'] for r in summary['per_layer'])
 g=dict(version=1,title='GLM-5.1 — checkpoint-reviewed architecture',width=2400,height=2360,
   sources=dict(config=HF+'config.json',card=HF+'README.md',index=HF+'model.safetensors.index.json',model=BASE+'modeling_glm_moe_dsa.py',framework_config=BASE+'configuration_glm_moe_dsa.py'),
   nodes=[],edges=[],limitations=['Native module-level operator diagram, not an executed trace.','Transformers unabsorbed MLA view; eager/SDPA uses a sparse mask, optimized flash-mla consumes sparse indices.','BF16 checkpoint selected; FP8 distribution is a separate variant, not assumed here.','Weight-index names/shards checked; tensor headers/values, GPU inference and Feishu import were not tested.','MTP index78 is shown as auxiliary checkpoint modules; this Transformers main forward does not execute it.'])
 ns={}
 def n(key,label,x,y,w=280,h=60,color='gray',loc='config.json',source='model',kind='operation',font=20):
  if key in ns:raise ValueError(key)
  while True:
   lines=[s for l in label.split('\n') for s in (textwrap.wrap(l,max(3,int((w-20)/(font*.55))),break_long_words=False) or [''])]
   if len(lines)*font*1.18+16<=h or font<=12:break
   font-=1
  if len(lines)*font*1.18+16>h:raise ValueError((key,label))
  stroke,fill=COLORS[color]
  obj=dict(id=key,label='\n'.join(lines),description=label,box=[x,y,w,h],kind=kind,status='verified',evidence=[dict(source=source,locator=loc),dict(source='config',locator='Pinned official GLM-5.1 config; see official_config.json')],
   style=f'rounded=1;arcSize=10;absoluteArcSize=1;html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={font};fontColor=#25384f;align=center;verticalAlign=middle;spacing=6;fillColor={fill};strokeColor={stroke};strokeWidth=1.2;')
  if label in ['+','×']:obj['style']+='shape=ellipse;perimeter=ellipsePerimeter;fontSize=24;'
  g['nodes'].append(obj);ns[key]=obj;return obj
 def note(key,label,x,y,w,h,font=20,color='gray'):
  o=n(key,label,x,y,w,h,color,kind='decoration',font=font);o['style']+='fillColor=none;strokeColor=none;';return o
 def panel(key,title,x,y,w,h,color):
  o=n(key,'',x,y,w,h,color,kind='decoration');o['style']+='fillColor=none;strokeColor=#c3cedb;dashed=1;dashPattern=6 4;'
  o=note(key+'_title',title,x+14,y+10,w-28,50,28,color);o['style']+=f'fontStyle=1;fontColor={COLORS[color][0]};'
 def e(a,b,ports=None,points=None):
  obj=dict(id='e_'+a+'__'+b,source=a,target=b)
  if ports:obj['ports']=ports
  if points:obj['points']=points
  g['edges'].append(obj)
 def chain(*keys):
  for a,b in zip(keys,keys[1:]):e(a,b)
 note('title','GLM-5.1  |  DSA + Mixture of Experts',30,10,2340,65,42,'blue')
 note('facts','78 layers · hidden 6144 · 64 Q heads · 256 routed / top-8 + 1 shared · context 202752',30,85,2340,50,26)
 note('scope','BF16 checkpoint @26e1bd6 · config + implementation + weight-index checked · bottom-up flow',30,140,2340,32,18)
 panel('backbone','Decoder backbone',30,180,400,1600,'blue')
 panel('attention','DSA / MLA — unabsorbed operator view',460,180,950,1600,'orange')
 panel('indexer','DSA Indexer — independent Q / K / weights',1450,180,920,930,'green')
 panel('moe','MoE — layers 3…77 (0-based)',1450,1140,920,640,'teal')
 panel('mlp','SwiGLU — dense / routed / shared expert',30,1830,1000,470,'green')
 panel('aux','Auxiliary MTP and source scope',1070,1830,1300,470,'gray')
 note('main_config','L0–2: Dense FFN\nL3–77: MoE FFN\nEvery main layer: DSA\nMTP: separate index78',65,280,330,250,22,'blue')
 for key,label,y,h in [('tokens','Token IDs',1730,40),('embed','Embedding [154880,6144]',1650,60),('x','Layer input h',1560,50),('n1','RMSNorm',1480,50),('attn','DSA',1400,60),('n2','RMSNorm',1240,50),('ffn','Dense FFN / MoE',1160,60),('repeat','Repeat 78 layers',960,70),('norm','RMSNorm',840,60),('head','LM head →154880',740,60),('out','Logits',640,60)]:
  n('main_'+key,label,90,y,280,h,'blue',loc='GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM')
 n('main_add1','+',208,1320,44,44,'blue',loc='Decoder residual add after attention, 607–609')
 n('main_add2','+',208,1080,44,44,'blue',loc='Decoder residual add after MLP, 612–616')
 chain('main_tokens','main_embed','main_x','main_n1','main_attn','main_add1','main_n2','main_ffn','main_add2','main_repeat','main_norm','main_head','main_out')
 e('main_x','main_add1',[0,.5,0,.5],[[70,1585],[70,1342]])
 e('main_add1','main_add2',[1,.5,1,.5],[[390,1342],[390,1102]])
 A='GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450'
 note('attn_dims','Q rank2048 · KV rank512 · Q/K head256 =192+RoPE64 · V head256\nInterleaved RoPE64, theta1e6 · no attention output gate',490,260,890,100,21,'orange')
 n('attn_h','h [6144]',650,1650,550,65,'orange',loc=A)
 n('attn_qa','Linear Q down\n6144 →2048',520,1540,300,70,'orange',loc=A)
 n('attn_qnorm','RMSNorm → Qr [2048]',520,1430,300,60,'orange',loc=A)
 n('attn_qup','Linear Q up\n2048 →64×256',520,1320,300,70,'orange',loc=A)
 n('attn_qsplit','Split Q: 192 |64',520,1210,300,60,'orange',loc=A)
 n('attn_qnope','Q content192',500,1100,170,60,'orange',loc=A)
 n('attn_qrope','RoPE64',710,1100,150,60,'orange',loc=A)
 n('attn_qcat','Concat Q [64,256]',520,980,340,60,'orange',loc=A)
 n('attn_kvdown','Linear KV down\n6144 →512+64',990,1540,360,70,'orange',loc=A)
 n('attn_kvsplit','Split c512 | k64',990,1430,360,60,'orange',loc=A)
 n('attn_kvnorm','RMSNorm512',990,1320,170,60,'orange',loc=A)
 n('attn_kvrope','RoPE64',1200,1320,150,60,'orange',loc=A)
 n('attn_cache','Latent KV cache\nc512 + positional key64',990,1210,360,70,'red',loc=A)
 n('attn_expand','Linear KV up: 512 →64×448\nK192 + kPE64 bypass; V256',990,1100,360,75,'orange',loc=A)
 n('attn_k','K [64,256]',990,980,170,60,'orange',loc=A)
 n('attn_v','V [64,256]',1200,980,170,60,'orange',loc=A)
 n('attn_indices','J: selected indices',490,820,230,60,'green',loc=A)
 n('attn_core','Sparse attention\nQKᵀ / sqrt(256) → Softmax → ×V',610,700,740,80,'orange',loc=A)
 n('attn_o','Linear O\n64×256 →6144',850,580,360,70,'orange',loc=A)
 n('attn_out','Attention output [6144]',850,470,360,60,'orange',loc=A)
 chain('attn_h','attn_qa','attn_qnorm','attn_qup','attn_qsplit')
 e('attn_qsplit','attn_qnope');e('attn_qsplit','attn_qrope');e('attn_qnope','attn_qcat');e('attn_qrope','attn_qcat')
 chain('attn_h','attn_kvdown','attn_kvsplit')
 for k in ['attn_kvnorm','attn_kvrope']:e('attn_kvsplit',k);e(k,'attn_cache')
 chain('attn_cache','attn_expand');e('attn_expand','attn_k');e('attn_expand','attn_v')
 for k in ['attn_qcat','attn_k','attn_v']:e(k,'attn_core')
 e('attn_indices','attn_core');chain('attn_core','attn_o','attn_out')
 I='GlmMoeDsaIndexer.__init__/forward, lines 153–242'
 note('index_scope','32 heads ×128 · interleaved RoPE64 · LayerNorm on K\nEach checkpoint layer owns indexer weights; no sharing assumed',1480,245,860,48,18,'green')
 defs=[('qr','Qr [2048]',1490,1030,220,60),('h','h [6144]',1790,1030,520,60),
 ('qp','Linear Qᵢ\n2048 →32×128',1490,950,220,60),('qrpe','RoPE64 + Concat',1490,870,220,55),('q','Qᵢ [32,128]',1490,790,220,55),
 ('kp','Linear Kᵢ\n6144 →128',1790,950,220,60),('kn','LayerNorm128',1790,870,220,55),('krpe','RoPE64 + Concat',1790,790,220,55),('cache','Index key cache [T,128]',1790,710,220,55),
 ('wp','Linear (weights)\n6144 →32',2090,950,220,60),('scale','Scale: 32^-0.5',2090,870,220,55),('w','w [32]',2090,790,220,55),
 ('dot','Matmul (Qᵢ,Kᵢᵀ) / sqrt(128)',1500,610,510,60),('relu','ReLU',1500,530,510,55),('sum','Weighted sum (heads)',1500,450,510,55),('mask','Causal mask',1500,370,510,55),('topk','TopK ≤2048 → J (int32)',1500,300,510,50)]
 for key,label,x,y,w,h in defs:n('idx_'+key,label,x,y,w,h,'red' if key=='cache' else 'green',loc=I,font=19)
 chain('idx_qr','idx_qp','idx_qrpe','idx_q');chain('idx_h','idx_kp','idx_kn','idx_krpe','idx_cache');chain('idx_h','idx_wp','idx_scale','idx_w')
 e('idx_q','idx_dot');e('idx_cache','idx_dot');chain('idx_dot','idx_relu','idx_sum','idx_mask','idx_topk')
 e('idx_w','idx_sum',[1,.5,1,.5],[[2330,817.5],[2330,477.5]])
 M='GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572'
 for key,label,y in [('h','h [6144]',1720),('router','FP32 Linear → Sigmoid',1640),('choice','+ correction bias → Top8',1560),('weights','Gather original scores\nNormalize → ×2.5',1480),('experts','256 routed experts /8 active\nSwiGLU: 6144→2048→6144',1400),('weighted','Weight outputs → Sum',1320)]:
  n('moe_'+key,label,1500,y,420 if key!='h' else 800,60,'teal',loc=M,font=19)
 n('moe_shared','Shared expert ×1\n6144→2048→6144',2100,1400,230,90,'teal',loc=M,font=19)
 n('moe_add','+',1688,1240,44,44,'teal',loc=M)
 chain('moe_h','moe_router','moe_choice','moe_weights','moe_experts','moe_weighted','moe_add');chain('moe_h','moe_shared','moe_add')
 L='GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547'
 n('mlp_x','x [6144]',350,2220,400,50,'green',loc=L)
 n('mlp_gate','Linear (gate)\n6144 →m',200,2140,240,60,'green',loc=L)
 n('mlp_up','Linear (up)\n6144 →m',700,2140,240,60,'green',loc=L)
 n('mlp_silu','SiLU',200,2060,240,50,'green',loc=L)
 n('mlp_mul','×',528,1980,44,44,'green',loc=L)
 n('mlp_down','Linear (down): m →6144',380,1900,350,55,'green',loc=L)
 chain('mlp_x','mlp_gate','mlp_silu','mlp_mul','mlp_down');chain('mlp_x','mlp_up','mlp_mul')
 note('mlp_width','m=12288 for first3 dense layers; m=2048 for routed/shared experts',70,2275,920,38,17)
 note('aux_modules','MTP ×1 — auxiliary checkpoint index78',1100,1910,560,60,22)
 for key,label,x,w in [('norms','enorm / hnorm',1110,170),('projection','eh_proj',1300,150),('block','DSA / MoE',1470,170)]:
  n('mtp_'+key,label,x,2010,w,75,'gray',source='index',loc='model.layers.78 auxiliary parameter names in official weight index',kind='decoration',font=19)
 n('mtp_headnorm','shared_head.norm',1200,2140,360,55,'gray',source='index',loc='model.layers.78.shared_head.norm.weight',kind='decoration',font=20)
 note('mtp_scope','Checkpoint modules only; outside main forward',1100,2230,560,45,18)
 note('aux_scope','Checkpoint config and weight names verified\n59,870 tensor names · 282 shards\nNo tensor-header or GPU inference test\nOptimized sparse-kernel / absorbed layouts are backend-specific',1710,1930,620,260,21)
 note('footer','Sources: official zai-org/GLM-5.1 @26e1bd6 · Transformers @f262c71 · explicit evidence and limitations in README / evidence.md',40,2318,2320,38,18)
 g['port_bindings']={'Qr':dict(source='attn_qnorm',target='idx_qr',shape=['B','T',2048]),'h_index':dict(source='attn_h',target='idx_h',shape=['B','T',6144]),'J':dict(source='idx_topk',target='attn_indices',shape=['B','T','min(2048,context)']),'attention':dict(source='main_n1',target='attn_h',shape=['B','T',6144]),'ffn':dict(source='main_n2',target='moe_h',shape=['B','T',6144])}
 g['checkpoint']=dict(revision=REV,main_layers=78,dense_ffn_layers=list(range(3)),moe_layers=list(range(3,78)),auxiliary_layer_index=78,indexer_mode='independent per checkpoint layer; all79 indexer prefixes present')
 # Model-specific visual roles; topology and provenance are not changed.
 short={'main_embed':'Embedding\n[154880,6144]','main_head':'LM head\n6144 →154880',
        'attn_qnorm':'RMSNorm\nQr [2048]','attn_core':'Sparse attention\nSoftmax(QKᵀ / sqrt(256)) V',
        'moe_router':'Linear → Sigmoid\nFP32 routing'}
 for key,label in short.items():ns[key]['label']=label
 roles={key:'composite' for key in ['main_attn','main_ffn','main_repeat','attn_core','attn_expand','moe_experts','moe_shared']}
 roles.update(main_embed='projection',main_head='projection',moe_weights='aggregation')
 # A shared tensor input reserves a fan-out span, not a uniform operator box.
 ns['mlp_x']['box']=[230,2220,640,50]
 fit_operators(g,roles,font=20)
 simplify_connections(g)
 return g

if __name__=='__main__':
 g=build();p=Path(__file__).with_name('glm51.graph.json');p.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
