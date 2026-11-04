"""Build a source-reviewed DeepSeek-V4 Flash study; never imports model code.

Numbers are literal defaults from the pinned Transformers Flash-Base config class.
The unavailable checkpoint's per-layer schedule is deliberately not inferred.
"""
from pathlib import Path
import json
import textwrap

SHA='f2754311602414ed561cdf8ed9d852390f514404'
BASE=f'https://github.com/huggingface/transformers/blob/{SHA}/src/transformers/models/deepseek_v4/'
G=dict(version=1,title='DeepSeek-V4-Flash — Transformers implementation study',width=3000,height=3900,
       sources={'model':BASE+'modeling_deepseek_v4.py','config':BASE+'configuration_deepseek_v4.py'},nodes=[],edges=[],limitations=[
           'Flash-Base class defaults, not downloaded DeepSeek-V4-Flash checkpoint configuration.',
           'HF config/model card/weight index blocked by current network policy; no weights or inference tested.',
           'Exact layer_types/compress_ratios schedule unknown; the Pro fallback schedule is NOT assigned to Flash.',
           'This is the pinned Transformers reference implementation, not an assertion about every serving-engine kernel.',
           'No independently verified parameter recount; 284B/13B headline is deliberately omitted.',
           'MTP is declared in configuration but not instantiated by this Transformers model.'])
D={}
COLORS={'purple':'#f0e9fa','green':'#edf7e3','blue':'#e5f0ff','orange':'#fff0de','teal':'#e2f6f2','grey':'#f1f4f8'}

def node(key,label,x,y,w,h,color='grey',font=20,kind='operation',locator=None,ellipse=False):
    assert key not in D
    while True:
        limit=max(3,int((w-20)/(font*.59)))
        lines=[part for line in label.split('\n') for part in (textwrap.wrap(line,limit,break_long_words=False) or [''])]
        if len(lines)*font*1.18+16<=h or font<=14:break
        font-=1
    assert len(lines)*font*1.18+16<=h,(key,label,h)
    style=f'rounded=1;arcSize=10;absoluteArcSize=1;whiteSpace=wrap;html=0;fontFamily=Arial;fontSize={font};fontColor=#182539;align=center;verticalAlign=middle;spacing=8;strokeColor=#364359;strokeWidth=1;fillColor={COLORS[color]};'
    if ellipse:style+='shape=ellipse;'
    n=dict(id=key,label='\n'.join(lines),box=[x,y,w,h],kind=kind,status='verified' if locator else 'inferred',style=style)
    if locator:
        n['evidence']=[dict(source='model',locator=locator),dict(source='config',locator='DeepseekV4Config literal class defaults, lines 128–175; not checkpoint values')]
    G['nodes'].append(n);D[key]=n
    return key

def note(key,label,x,y,w,h,font=20):
    node(key,label,x,y,w,h,font=font,kind='decoration')
    D[key]['style']+='fillColor=none;strokeColor=none;'

def panel(key,label,x,y,w,h,color):
    node(key,'',x,y,w,h,color,kind='decoration')
    D[key]['style']+='fillColor=#ffffff;dashed=1;'
    node(key+'_heading',label+' ↑',x+12,y+12,w-24,62,color,26,kind='decoration')

def edge(a,b,ports=None,points=None,dashed=False):
    e=dict(id=f'edge_{len(G["edges"])}',source=a,target=b)
    if ports:e['ports']=ports
    if points:e['points']=points
    if dashed:e['dashed']=True
    G['edges'].append(e)

def chain(seq):
    for a,b in zip(seq,seq[1:]):edge(a,b)

def mid(k):x,y,w,h=D[k]['box'];return x+w/2,y+h/2

def vertical_input(a,b):
    # Input side uses the downstream x so the entry is vertically aligned.
    x,y,w,h=D[a]['box'];bx,_=mid(b);edge(a,b,[(bx-x)/w,0,.5,1])

note('title','DeepSeek-V4-Flash | Detailed architecture study',40,15,2920,80,42)
note('subtitle','SOURCE-REVIEWED TRANSFORMERS IMPLEMENTATION · Flash-Base class defaults; checkpoint config not read',40,100,2920,65,25)
node('defaults','DEFAULTS: 43 layers · hidden 4096 · 64 Q heads / 1 KV head · head dim 512 · 256 experts, top-6 + 1 shared · mHC streams 4',40,175,2920,65,'purple',26,locator='DeepseekV4Config defaults / DeepseekV4Attention / DeepseekV4SparseMoeBlock')
panel('mhc','mHC: one attention or FFN wrapper',30,260,940,1450,'purple')
panel('compress','Layer-selected compressors: CSA OR HCA',30,1760,940,1460,'teal')
panel('main','Language backbone / repeat layer',1010,260,850,2960,'purple')
panel('attention','Shared-KV MQA + optional compressed history',1900,260,1070,1590,'orange')
panel('moe','Hash-MoE / routed MoE + shared expert',1900,1900,1070,1320,'blue')
panel('indexer','CSA Lightning Indexer — separate query, key and scoring-weight paths',30,3270,2940,500,'green')
# mHC block. Source: model lines 873–1005, 1161–1187.
loc='DeepseekV4HyperConnection.forward, lines 940–984; DeepseekV4DecoderLayer.forward, 1176–1186'
node('hc_x','X: four streams [B,T,4,4096]',70,1580,850,80,'purple',22,locator=loc)
node('hc_flat','Flatten streams → unweighted RMSNorm',500,1470,400,80,'purple',20,locator=loc)
node('hc_linear','Linear fn: 16384 → 24 coefficients\nScale + bias; split pre / post / comb',500,1370,400,80,'purple',18,locator=loc)
node('hc_pre','pre = sigmoid(·) + eps',500,1260,120,80,'purple',16,locator=loc)
node('hc_post','post = 2 sigmoid(·)',650,1260,120,80,'purple',16,locator=loc)
node('hc_comb','comb logits\n[4 × 4]',800,1260,120,80,'purple',16,locator=loc)
node('hc_soft','Row softmax + eps',800,1160,120,70,'purple',16,locator=loc)
node('hc_sink','Sinkhorn: 20 iterations\nDoubly stochastic comb',780,1030,160,95,'purple',16,locator=loc)
node('hc_collapse','Collapse input streams\nh = sum(pre_i × X_i)',100,1160,300,80,'purple',20,locator=loc)
node('hc_norm','RMSNorm of h',100,1040,300,70,'purple',20,locator='DeepseekV4DecoderLayer.forward, lines 1175–1186')
node('hc_fun','Attention OR MoE FFN\nF(h) [B,T,4096]',100,900,300,100,'purple',22,locator=loc)
node('hc_expand','Expand block output\npost × F(h)',100,730,300,85,'purple',20,locator=loc)
node('hc_residual','Residual stream mixing\ncombᵀ × X',570,730,330,85,'purple',22,locator=loc)
node('hc_sum','+',215,550,70,70,'purple',28,locator=loc,ellipse=True)
node('hc_y','Updated streams\n[B,T,4,4096]',100,400,300,85,'purple',22,locator=loc)
vertical_input('hc_x','hc_flat');chain(['hc_flat','hc_linear'])
for k in ['hc_pre','hc_post','hc_comb']:
    bx,_=mid(k);edge('hc_linear',k,[(bx-500)/400,0,.5,1])
chain(['hc_comb','hc_soft','hc_sink'])
edge('hc_x','hc_collapse',[(250-70)/850,0,.5,1])
edge('hc_pre','hc_collapse',[.5,0,1,.5],[[560,1200]])
chain(['hc_collapse','hc_norm','hc_fun','hc_expand','hc_sum','hc_y'])
edge('hc_post','hc_expand',[.5,0,1,.5],[[710,860],[430,860],[430,772.5]])
edge('hc_x','hc_residual',[1,.5,1,.5],[[950,1620],[950,772.5]])
edge('hc_sink','hc_residual',[.5,0,(860-570)/330,1])
edge('hc_residual','hc_sum',[.5,0,1,.5],[[735,650],[320,650],[320,585]])
note('hc_note','Residual uses comb transpose; all coefficients are computed from X.',65,1670,850,40,17)
# Main inference layer, not two separate representative layers.
loc='DeepseekV4Model.forward, lines 1317–1368; DeepseekV4DecoderLayer.forward, 1161–1187'
for k,txt,y,h in [
('tokens','Input token IDs',3060,70),('embed','Token embedding [B,T,4096]',2940,80),
('streams','Repeat embedding into 4 streams',2810,85),('layer_x','Layer input X [B,T,4,4096]',2600,80),
('attn_pre','Attention mHC: pre-collapse; compute post, comb',2450,90),('attn_norm','RMSNorm [4096]',2300,80),
('attn_core','Layer-selected attention\nSWA + (CSA OR HCA); exact schedule unknown',2130,110),
('attn_mix','post × attention output + combᵀ × X',1980,90),
('ffn_pre','FFN mHC: pre-collapse; compute post, comb',1820,90),('ffn_norm','RMSNorm [4096]',1670,80),
('ffn','Hash-MoE or learned top-k MoE',1520,80),('ffn_mix','post × FFN output + combᵀ × residual',1360,90),
('layer_y','Layer output streams\nRepeat this decoder layer 43× (class default)',1180,100),
('hyperhead','HyperHead: learned sigmoid-weighted\ncollapse 4 streams → one hidden state',690,110),
('norm','Final RMSNorm [4096]',550,80),('head','LM head: 4096 → vocabulary 129280',445,70),('output','Next-token logits',350,60)]:
 node('main_'+k,txt,1100,y,670,h,'purple',22,locator=loc)
chain(['main_'+k for k in ['tokens','embed','streams','layer_x','attn_pre','attn_norm','attn_core','attn_mix','ffn_pre','ffn_norm','ffn','ffn_mix','layer_y','hyperhead','norm','head','output']])
edge('main_layer_x','main_attn_mix',[1,.5,1,.5],[[1825,2640],[1825,2025]])
edge('main_attn_pre','main_attn_mix',[0,.5,0,.5],[[1050,2495],[1050,2025]],True)
edge('main_attn_mix','main_ffn_mix',[1,.5,1,.5],[[1840,2025],[1840,1405]])
edge('main_ffn_pre','main_ffn_mix',[0,.5,0,.5],[[1035,1865],[1035,1405]],True)
note('schedule','IMPORTANT: do not copy Pro fallback layer_types.\nCheckpoint-specific CSA/HCA ordering is unverified.\nMTP: config declares 1; this class does not instantiate it.',1070,875,730,180,23)
# Attention, model lines 752–870.
loc='DeepseekV4Attention.__init__/forward, lines 752–870; apply_rotary_pos_emb, 339–356'
node('attn_x','h [B,T,4096]',1940,1720,990,80,'orange',24,locator=loc)
for key,txt,x,y,w,h in [
('qa','Q Linear 4096 → 1024',1940,1580,270,70),('qan','RMSNorm → q_residual',1940,1470,270,70),
('qb','Q up: 1024 → 64 × 512',1940,1340,270,80),('qn','Per-head unweighted RMSNorm',1940,1210,270,75),
('qrope','Partial RoPE: trailing 64 dims',1940,1090,270,80),
('kv','KV Linear: 4096 → 512',2290,1580,270,70),('kvn','RMSNorm [512]',2290,1470,270,70),
('kvrope','Partial RoPE (64 dims)',2290,1340,270,80),('local','Sliding cache: window 128\nK and V are the SAME tensor',2290,1210,270,85),
('compressor','Layer-selected CSA (4) OR HCA (128)\nNone for sliding-only',2640,1560,270,110),
('entries','Compressed historical entries\nSingle shared KV head',2640,1410,270,95),
('mask','CSA: causal + top-512 mask\nHCA: causal mask; no indexer',2640,1270,270,100),
('concat','Concatenate local KV and compressed history\nPer-query mask; K = V',2290,1050,620,100),
('core','Scaled dot-product attention\nSoftmax over KV logits + learnable sink\nDiscard sink probability; multiply shared V',2050,850,760,120),
('sink','Learned sink\nper Q head',2850,850,90,120),
('inverse','Inverse partial RoPE on attention output\nUse conjugate rotation at query position',2180,710,500,90),
('oa','Grouped O_a: 8 groups\nPer-group 4096 → 1024',2180,560,500,85),
('ob','Flatten 8 × 1024 → O_b → 4096',2180,445,500,75),('y','Attention output [B,T,4096]',2180,340,500,65)]:
 node('attn_'+key,txt,x,y,w,h,'orange',20,locator=loc)
for b in ['attn_qa','attn_kv','attn_compressor']:
    bx,_=mid(b);edge('attn_x',b,[.5,0,.5,1],[[2435,1695],[bx,1695]])
chain(['attn_qa','attn_qan','attn_qb','attn_qn','attn_qrope'])
chain(['attn_kv','attn_kvn','attn_kvrope','attn_local'])
chain(['attn_compressor','attn_entries','attn_mask'])
for a in ['attn_local','attn_mask']:
 bx,_=mid(a);edge(a,'attn_concat',[.5,0,(bx-2290)/620,1])
edge('attn_qrope','attn_core',[.5,0,(2075-2050)/760,1])
edge('attn_concat','attn_core',[.5,0,(2600-2050)/760,1])
edge('attn_sink','attn_core',[0,.5,1,.5])
chain(['attn_core','attn_inverse','attn_oa','attn_ob','attn_y'])
# Align attention output path with its wide attention block's explicit output anchor.
G['edges'][-4]['ports']=[.5,0,.5,1]
# Route around the schedule note; it is not a computational stage.
for e in G['edges']:
    if e['source']=='main_layer_y' and e['target']=='main_hyperhead':e.update(ports=[1,.5,.5,1],points=[[1810,1230],[1810,835],[1435,835]])
# Compressor internals: both paths displayed as alternatives.
for kind,x,ratio in [('csa',65,4),('hca',535,128)]:
 loc=('DeepseekV4CSACompressor.forward, lines 620–700' if kind=='csa' else 'DeepseekV4HCACompressor.forward, lines 391–440')
 note(kind+'_label',kind.upper()+f' | compression stride {ratio}',x,1840,400,65,25)
 node(kind+'_x','Hidden states h [4096]',x,3090,400,75,'teal',22,locator=loc)
 node(kind+'_kv','Linear KV: 4096 → '+('2 × 512' if kind=='csa' else '512'),x,2950,175,95,'teal',18,locator=loc)
 node(kind+'_gate','Linear gates: 4096 → '+('2 × 512' if kind=='csa' else '512'),x+225,2950,175,95,'teal',18,locator=loc)
 node(kind+'_window',('Overlap Ca / Cb: effective width 8, stride 4\nBuffer previous Ca across calls' if kind=='csa' else 'Non-overlapping 128-token windows\nBuffer partial window across calls'),x,2770,400,120,'teal',20,locator=loc)
 node(kind+'_bias','GATE PATH: + position bias\nFP32 softmax within compression window',x,2580,400,120,'teal',20,locator=loc)
 node(kind+'_sum','Weighted sum of projected KV\nOne vector [512] per completed window',x,2410,400,100,'teal',20,locator=loc)
 node(kind+'_norm','RMSNorm [512]',x,2270,400,75,'teal',22,locator=loc)
 node(kind+'_rope','Partial RoPE at window position\nAppend to compressed KV cache',x,2100,400,100,'teal',20,locator=loc)
 node(kind+'_out',('Lightning Indexer → top-512 validity mask\nOnly chosen entries are visible to each query' if kind=='csa' else 'Causal visibility mask\nAll completed compressed entries; NO indexer'),x,1915,400,140,'teal',20,locator=loc)
 for b in [kind+'_kv',kind+'_gate']:vertical_input(kind+'_x',b)
 edge(kind+'_kv',kind+'_window',[.5,0,.22,1]);edge(kind+'_gate',kind+'_window',[.5,0,.78,1])
 chain([kind+'_window',kind+'_bias',kind+'_sum',kind+'_norm',kind+'_rope',kind+'_out'])
 edge(kind+'_window',kind+'_sum',[1,.5,1,.5],[[x+420,2830],[x+420,2460]])
# MoE and explicit FFN inset.
loc='DeepseekV4TopKRouter / HashRouter / SparseMoeBlock, lines 1065–1135; DeepseekV4MLP, 1006–1022'
node('moe_x','h [4096] and token IDs (hash route)',1940,3080,990,80,'blue',22,locator=loc)
node('moe_shared','One shared expert\n4096 → 2048 → 4096',1940,2690,260,100,'blue',22,locator=loc)
node('moe_router','Learned score: Linear → sqrtsoftplus\nHash: tid2eid[token IDs] selects experts\nElse: top-6(scores + correction bias)',2250,2910,360,120,'blue',18,locator=loc)
node('moe_weights','Gather ORIGINAL scores\nNormalize selected weights × 1.5',2250,2740,360,100,'blue',20,locator=loc)
node('moe_bank','256 routed experts; activate 6\nInput / output width 4096\nExpert intermediate width 2048',2250,2540,360,130,'blue',22,locator=loc)
node('moe_sum','Weighted routed output',2250,2370,360,95,'blue',22,locator=loc)
node('moe_add','+',2395,2220,70,70,'blue',30,locator=loc,ellipse=True)
node('moe_y','MoE output [4096]',2250,2070,360,80,'blue',22,locator=loc)
vertical_input('moe_x','moe_router');chain(['moe_router','moe_weights'])
# Original h supplies expert activations; weights only control dispatch/aggregation.
edge('moe_x','moe_bank',[(2220-1940)/990,0,0,.5],[[2220,2605]])
edge('moe_weights','moe_bank',[.5,0,.5,1])
chain(['moe_bank','moe_sum','moe_add','moe_y'])
edge('moe_x','moe_shared',[(2070-1940)/990,0,.5,1])
edge('moe_shared','moe_add',[.5,0,0,.5],[[2070,2255]])
# Narrow FFN column: kept independent, so no causal confusion with router.
for k,txt,y,h in [('x','Expert input x [4096]',2990,70),('up','Linear W_up\n4096 → 2048\nclip to [-10,10]',2850,115),('gate','Linear W_gate\n4096 → 2048\nclip MAX at 10\nthen SiLU',2660,150),('mul','Elementwise product\nSiLU(clipped gate) × clipped up',2440,130),('down','W_down: 2048 → 4096',2260,100),('y','Expert output [4096]',2100,90)]:
 node('expert_'+k,txt,2660,y,280,h,'blue',20,locator='DeepseekV4MLP.forward, lines 1018–1022; DeepseekV4Experts')
# Gate/up are parallel; route up branch alongside gate box.
edge('expert_x','expert_up')
edge('expert_x','expert_gate',[1,.5,1,.5],[[2950,3025],[2950,2735]])
edge('expert_up','expert_mul',[0,.5,0,.5],[[2640,2907.5],[2640,2505]])
chain(['expert_gate','expert_mul','expert_down','expert_y'])
note('moe_note','Hash routing freezes WHICH experts, not their activation weights.\nDefault hash bootstrap count = 3; actual checkpoint schedule not read.',1940,1990,990,70,20)
# CSA indexer (independent auxiliary graph, not another layer in the LM trunk).
loc='DeepseekV4Indexer.forward, lines 504–583; DeepseekV4IndexerScorer.forward, 452–456'
for key,txt,x,y,w,h in [
('q','q_residual [1024]',80,3650,480,70),('qproj','Index Q projection: 64 × 128\nPartial RoPE at query position',80,3510,480,100),
('key','h → independent overlapping compressor\nIndex-head width 128; stride 4',730,3650,600,90),
('kcache','Normalized + partial-RoPE compressed keys\nOwn cache / previous-window Ca state',730,3505,600,100),
('h','h [4096] → Linear W_weights\n64 query-head scoring weights',1500,3650,600,90),
('score','sum_h w_h ReLU(Q_index · K_comp)\nScale: 128^-0.5 × 64^-0.5\nCausal masking before top-k',1500,3500,600,110),
('select','Top min(512, compressed length)\nMark invalid future entries as -1\nBuild per-query CSA mask',2320,3470,580,150)]:
 node('idx_'+key,txt,x,y,w,h,'green',22,locator=loc)
edge('idx_q','idx_qproj');edge('idx_key','idx_kcache');edge('idx_h','idx_score')
# Sideways inter-module wires use dedicated channels above the boxes.
edge('idx_qproj','idx_score',[.5,0,.8,0],[[320,3410],[1980,3410]])
edge('idx_kcache','idx_score',[.5,0,.4,0],[[1030,3450],[1740,3450]])
edge('idx_score','idx_select',[1,.5,0,.5])
note('idx_note','CSA only. HCA has no Lightning Indexer. Cache buffer / overlap state persists across prefill and decode.',65,3350,2860,50,21)
# Evidence footer.
note('footer','Pinned source: huggingface/transformers @ f275431 · configuration_deepseek_v4.py + modeling_deepseek_v4.py\nClass defaults shown; HF checkpoint config / weight index blocked. Exact layer schedule remains UNVERIFIED. No inference or parameter recount performed.',40,3790,2920,90,22)
# Put backgrounds before all foreground nodes, preserving panel/label ordering.
# Existing list order already does this for each independent panel.
path=Path(__file__).with_name('deepseek_v4_flash.graph.json')
path.write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n')
print(path,len(G['nodes']),'nodes',len(G['edges']),'edges')
