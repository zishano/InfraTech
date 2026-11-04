"""Detailed CSA/HCA computational pages, transcribed from pinned official code.

No model code is imported/executed. Named tensor ports connect panels without
ambiguous page-spanning wires. Graphs are exported as native draw.io, then PNG.
"""
from pathlib import Path
import json
import textwrap

REV='60d8d70770c6776ff598c94bb586a859a38244f1'
HF=f'https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/{REV}/'
COLORS={'kv':'#e0f4ef','index':'#e8f2df','attn':'#fff0dc','state':'#eee7f7','plain':'#f3f6fa'}

class Page:
    def __init__(self,kind):
        self.kind=kind;self.nodes={}
        self.g=dict(version=1,title=f'DeepSeek-V4-Flash | {kind.upper()} detailed computation',width=4000,height=5700,
          sources={'model':HF+'inference/model.py','kernel':HF+'inference/kernel.py','config':HF+'config.json'},nodes=[],edges=[],
          limitations=['Static official-source transcription; no GPU model execution or numerical equivalence test.',
          'Tensor shapes are global/unsharded; TP splits heads and performs a scoring all-reduce when world_size > 1.',
          'Matching named ports denote the same tensor/storage; they do not imply copies or additional model layers.',
          'QAT simulation in this reference retains BF16 tensors; diagrams do not assert a physically packed FP4/FP8 KV cache.'])
    def node(self,key,label,box,color='plain',font=24,kind='operation',locator=None,shape=None):
        assert key not in self.nodes
        x,y,w,h=box
        while True:
            lines=[p for line in label.split('\n') for p in (textwrap.wrap(line,max(3,int((w-24)/(font*.58))),break_long_words=False) or [''])]
            if len(lines)*font*1.18+20<=h or font<=14:break
            font-=1
        assert len(lines)*font*1.18+20<=h,(key,label,box)
        n=dict(id=key,label='\n'.join(lines),box=box,kind=kind,status='verified' if locator else 'inferred',
               style=f'rounded=1;arcSize=12;absoluteArcSize=1;whiteSpace=wrap;html=0;fontFamily=Arial;fontSize={font};fontColor=#16283d;align=center;verticalAlign=middle;spacing=10;strokeColor=#34465a;fillColor={COLORS[color]};')
        if shape:n['style']+='shape='+shape+';'
        if locator:n['evidence']=[dict(source='kernel' if 'kernel.py' in locator else 'model',locator=locator),dict(source='config',locator='Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios')]
        self.g['nodes'].append(n);self.nodes[key]=n;return key
    def note(self,key,label,box,font=24):
        self.node(key,label,box,font=font,kind='decoration');self.nodes[key]['style']+='fillColor=none;strokeColor=none;'
    def panel(self,key,label,box,color):
        self.node(key,'',box,color,kind='decoration');self.nodes[key]['style']+='fillColor=#ffffff;dashed=1;'
        x,y,w,h=box;self.node(key+'_title',label,[x+15,y+15,w-30,75],color,30,kind='decoration')
    def edge(self,a,b,ports=None,points=None,dashed=False):
        e=dict(id='edge_'+str(len(self.g['edges'])),source=a,target=b)
        if ports:e['ports']=ports
        if points:e['points']=points
        if dashed:e['dashed']=True
        self.g['edges'].append(e)
    def chain(self,*seq):
        for a,b in zip(seq,seq[1:]):self.edge(a,b)
    def mid(self,k):x,y,w,h=self.nodes[k]['box'];return x+w/2,y+h/2
    def fork(self,source,target,bus_y):
        sx,_=self.mid(source);tx,_=self.mid(target);self.edge(source,target,[.5,0,.5,1],[[sx,bus_y],[tx,bus_y]])
    def vertical(self,source,target):
        x,y,w,h=self.nodes[source]['box'];tx,_=self.mid(target);self.edge(source,target,[(tx-x)/w,0,.5,1])

COMP='Compressor.__init__/overlap_transform/forward, official model.py lines 279–377'
IDX='Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254'
ATT='Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276'
KER='sparse_attn_kernel, official kernel.py lines 277–367'

def start(kind):
    p=Page(kind);r=4 if kind=='csa' else 128
    p.note('title',f'DeepSeek-V4-Flash | {kind.upper()} — computation, cache and addressing',[40,15,3920,100],48)
    p.note('source','OFFICIAL CHECKPOINT 60d8d707 | model.py + kernel.py + config.json | bottom-up computation',[40,125,3920,80],28)
    p.node('facts',(f'CSA: 21 layers (2,4,…,42) · stride 4 · effective window 8 · index heads64 × dim128 · top-k≤512' if kind=='csa' else
       'HCA: 20 layers (3,5,…,41) · non-overlap window 128 · all completed compressed entries · NO learned Indexer'),[40,225,3920,90],'state',29,locator='config.json /compress_ratios; Attention.__init__ 436–482')
    p.note('ports','Named ports A / I / Qr are tensor aliases across panels, not extra computation or copies. B=batch, T=prefill chunk, p=decode position, Nc=completed compressed windows.',[40,330,3920,90],24)
    p.panel('compressor','1. MAIN KV COMPRESSOR — values and gates are separate',[30,450,1250,3960],'kv')
    p.panel('middle',('2. LIGHTNING INDEXER — three independent learned paths' if kind=='csa' else '2. CAUSAL HISTORY INDICES — position arithmetic only'),[1320,450,1250,3960],'index')
    p.panel('attention','3. SHARED K=V ATTENTION — window + compressed history',[2610,450,1360,3960],'attn')
    p.g['compression_ratio']=r
    return p

def compressor(p):
    csa=p.kind=='csa';r=4 if csa else 128;coff=2 if csa else 1
    n=p.node;e=p.edge
    n('comp_h','Hidden states h [B,T,4096]',[70,4230,1130,110],'kv',28,locator=COMP)
    n('comp_fp32','Cast hidden states to FP32\nProjection / window score arithmetic stays FP32',[70,4050,1130,110],'kv',27,locator=COMP)
    n('comp_wkv',f'Linear Wkv: 4096 → {coff*512}\nC = h Wkv',[70,3860,500,120],'kv',26,locator=COMP)
    n('comp_wgate',f'Linear Wgate: 4096 → {coff*512}\nZ = h Wgate',[700,3860,500,120],'kv',26,locator=COMP)
    n('comp_split',(f'Reshape [B,N,4,1024] → Ca / Cb\nCa = first512; Cb = last512' if csa else 'Reshape complete prefix [B,N,128,512]\nOne KV vector per token; no Ca/Cb split'),[70,3640,500,160],'kv',24,locator=COMP)
    n('comp_ape',f'Add learned APE / position bias\nshape [{r},{coff*512}]\nPrefill: slot in window; decode: p % {r}',[700,3640,500,160],'kv',24,locator=COMP)
    n('comp_gate_split',('Split biased gate channels Za / Zb\nSame Ca/Cb feature layout as KV' if csa else 'Reshape biased gates [B,N,128,512]\nAlign one gate per token and channel'),[700,3430,500,150],'kv',24,locator=COMP)
    n('comp_value_window',('VALUE WINDOW: [Ca_(j-1), Cb_j]\n[B,N,8,512], stride4, effective width8\nFirst window: missing Ca values = 0' if csa else 'VALUE WINDOW: C_j[0:128]\n[B,N,128,512], stride128\nNo previous-window overlap'),[70,3230,500,190],'kv',24,locator=COMP)
    n('comp_gate_window',('GATE WINDOW: [Za_(j-1), Zb_j]\n[B,N,8,512]\nMissing first-window gates = -infinity' if csa else 'GATE WINDOW: Z_j + APE\n[B,N,128,512]\nNo previous-window gate state'),[700,3200,500,190],'kv',24,locator=COMP)
    n('comp_softmax',f'FP32 softmax over {coff*r} TOKEN slots\nIndependently for each of 512 channels\nP = softmax(Z_window, dim=tokens)',[700,2980,500,160],'kv',24,locator=COMP)
    n('comp_mul',f'Elementwise product: P ⊙ C_window\nShape [B,N,{coff*r},512]\nKV values bypass softmax',[70,2760,1130,150],'kv',28,locator=COMP)
    n('comp_sum',f'Sum over {coff*r} token slots\nc_j[d] = sum_s P[j,s,d] × C[j,s,d]\nResult [B,N,512] — NOT pooling across channels',[70,2550,1130,150],'kv',27,locator=COMP)
    n('comp_complete',f'Emit only a completed {r}-token stride\nPrefill: cutoff=T−(T%{r}); decode: (p+1)%{r}==0\nOtherwise return None; keep buffered state',[70,2350,1130,145],'kv',26,locator=COMP)
    n('comp_norm','Cast pooled vector back to input dtype\nLearned RMSNorm over 512 channels',[70,2160,1130,120],'kv',27,locator=COMP)
    n('comp_nope','Content 448 dims\nFP8 QAT simulation, block64\nSimulated values remain BF16',[70,1940,500,155],'kv',24,locator=COMP)
    n('comp_rope',f'Trailing 64 dims: partial RoPE\nPrefill position={r}j\nDecode position=p+1−{r}\nRoPE values remain BF16',[700,1940,500,155],'kv',24,locator=COMP)
    n('comp_concat','Reassemble content448 | RoPE64\nOne shared KV vector [512] per complete stride',[70,1740,1130,130],'kv',27,locator=COMP)
    n('comp_write',f'Write compressed KV cache\nPrefill: slots 0…floor(T/{r})−1\nDecode: slot floor(p/{r})',[70,1530,1130,145],'kv',27,locator=COMP)
    n('comp_bank',f'Cache capacity [B,floor(max_seq_len/{r}),512]\nLogical valid entries Nc=floor(end_pos/{r})\nNo query-specific pruning or top-k is stored here',[70,1300,1130,160],'kv',26,locator=COMP)
    n('comp_alias','Storage aliases Attention.kv_cache[:,128:]\nCompressed entries are appended after the window region\nNo copied top-k-only KV cache',[70,1080,1130,145],'kv',26,locator='Attention.forward lines 490–500; Compressor.kv_cache write 369–375')
    n('port_A','PORT A → right panel\nALL valid compressed KV vectors (K=V)\nShape [B,Nc,512]',[70,820,1130,170],'kv',30,locator=COMP)
    p.chain('comp_h','comp_fp32');p.fork('comp_fp32','comp_wkv',4010);p.fork('comp_fp32','comp_wgate',4010)
    p.chain('comp_wkv','comp_split','comp_value_window')
    p.chain('comp_wgate','comp_ape','comp_gate_split','comp_gate_window','comp_softmax')
    e('comp_value_window','comp_mul',[.5,0,(320-70)/1130,1]);e('comp_softmax','comp_mul',[.5,0,(950-70)/1130,1])
    p.chain('comp_mul','comp_sum','comp_complete','comp_norm')
    p.vertical('comp_norm','comp_nope');p.vertical('comp_norm','comp_rope')
    for k in ['comp_nope','comp_rope']:
        x,_=p.mid(k);e(k,'comp_concat',[.5,0,(x-70)/1130,1])
    p.chain('comp_concat','comp_write','comp_bank','comp_alias','port_A')
    p.note('comp_note','Main compressor rotate=False. Indexer uses its OWN smaller compressor with rotate=True (CSA only).',[70,590,1130,150],25)
    p.g['main_compressor_state_shape']=['B',coff*r,coff*512]

def indexer(p):
    n=p.node;e=p.edge
    n('idx_q_input','PORT Qr: normalized q_residual\n[B,T,1024], same as attention rank-normalized query',[1360,4230,330,140],'index',24,locator=IDX)
    n('idx_h','Hidden states h [B,T,4096]\nSupplies key compressor AND scoring weights',[1750,4230,720,140],'index',25,locator=IDX)
    qnodes=[('idx_q_proj','Wq_b: 1024 → 64×128',[1360,4020,330,130]),
       ('idx_q_heads','Reshape [B,T,64,128]\nTP: split query heads',[1360,3810,330,145]),
       ('idx_q_rope','Partial RoPE on last64\nAt CURRENT query position t',[1360,3600,330,145]),
       ('idx_q_hadamard','Hadamard rotation\nScale 1/sqrt(128)',[1360,3390,330,145]),
       ('idx_q_fp4','FP4 QAT simulation\nblock32, in-place\nTensor remains BF16',[1360,3170,330,160]),
       ('idx_q_ready','Index query Q_I\n[B,T,64,128]',[1360,2970,330,130])]
    for k,t,b in qnodes:n(k,t,b,'index',24,locator=IDX)
    p.chain('idx_q_input',*[a[0] for a in qnodes])
    n('idx_kv_proj','Wkv_I\n4096 → 256',[1750,4020,150,130],'index',19,locator=IDX)
    n('idx_gate_proj','Wgate_I\n4096 → 256',[1930,4020,150,130],'index',19,locator=IDX)
    n('idx_w_proj','W_weights: 4096 → 64\nOne score weight per head',[2140,4020,330,130],'index',23,locator=IDX)
    for k in ['idx_kv_proj','idx_gate_proj','idx_w_proj']:p.fork('idx_h',k,4190)
    n('idx_kv_split','Split Ca/Cb\n128 + 128',[1750,3810,150,145],'index',19,locator=IDX)
    n('idx_gate_ape','Gate + APE\n[4,256]\nSplit Za/Zb',[1930,3810,150,145],'index',19,locator=IDX)
    n('idx_window','Independent overlapping windows\n[prev Ca4 | current Cb4]\nKV / gates [B,N,8,128]',[1750,3580,330,175],'index',23,locator=IDX)
    n('idx_softmax','Gate-only FP32 softmax\nAcross 8 slots per channel',[1750,3380,330,145],'index',23,locator=IDX)
    n('idx_pool','KV bypass × gate probabilities\nSum8 → [B,N,128]',[1750,3170,330,155],'index',23,locator=IDX)
    n('idx_norm','Learned RMSNorm128',[1750,2970,330,115],'index',24,locator=IDX)
    n('idx_key_rope','Partial RoPE64\nAt compressed position 4j',[1750,2780,330,130],'index',23,locator=IDX)
    n('idx_key_hadamard','Hadamard rotation\nSame orthogonal basis as Q_I',[1750,2590,330,145],'index',23,locator=IDX)
    n('idx_key_fp4','FP4 QAT simulation, block32\nTensor remains BF16',[1750,2390,330,145],'index',23,locator=IDX)
    n('idx_key_cache','Independent index KV cache\n[B,Nc,128]\nOwn previous-Ca / partial state',[1750,2180,330,155],'index',23,locator=IDX)
    p.chain('idx_kv_proj','idx_kv_split');p.chain('idx_gate_proj','idx_gate_ape')
    e('idx_kv_split','idx_window',[.5,0,.23,1]);e('idx_gate_ape','idx_window',[.5,0,.77,1])
    p.chain('idx_window','idx_softmax','idx_pool','idx_norm','idx_key_rope','idx_key_hadamard','idx_key_fp4','idx_key_cache')
    e('idx_window','idx_pool',[1,.5,1,.5],[[2100,3667.5],[2100,3247.5]])
    n('idx_w_scale','Scale head weights\n128^-0.5 × 64^-0.5\nThese weights are NOT a softmax',[2140,3810,330,175],'index',23,locator=IDX)
    n('idx_w_ready','Per-query head weights w\n[B,T,64]',[2140,3590,330,130],'index',24,locator=IDX)
    p.chain('idx_w_proj','idx_w_scale','idx_w_ready')
    n('idx_dot','einsum: Q_I · K_I_cache\nRaw scores [B,T,64,Nc]',[1390,1920,1080,150],'index',29,locator=IDX)
    e('idx_q_ready','idx_dot',[.5,0,(1525-1390)/1080,1]);e('idx_key_cache','idx_dot',[.5,0,(1915-1390)/1080,1])
    n('idx_relu','ReLU of per-head similarities',[1390,1720,1080,110],'index',29,locator=IDX)
    n('idx_head_sum','Multiply by learned head weights, then sum heads\nS[b,t,j] = sum_h w[b,t,h] × ReLU(dot[b,t,h,j])',[1390,1510,1080,150],'index',28,locator=IDX)
    p.chain('idx_dot','idx_relu','idx_head_sum')
    e('idx_w_ready','idx_head_sum',[1,.5,1,.5],[[2530,3655],[2530,1585]])
    n('idx_tp','If TP > 1: all_reduce index scores\nScores [B,T,Nc] across all 64 global heads',[1390,1320,1080,120],'index',28,locator=IDX)
    n('idx_causal','Prefill: j >= floor((t+1)/4) → -infinity\nDecode: score only cache prefix j < floor((p+1)/4)',[1390,1120,1080,145],'index',28,locator=IDX)
    n('idx_topk','Top-k with k=min(512,Nc)\nPer-query ranking; may include masked -infinity entries\nNOT a cache truncation operation',[1390,910,1080,160],'index',28,locator=IDX)
    n('port_I','PORT I → right panel\nPrefill: invalid future j → -1, valid j → j+T\nDecode: j → j+128\nSelected compressed positions; integer tensor',[1390,650,1080,200],'index',29,locator=IDX)
    p.chain('idx_head_sum','idx_tp','idx_causal','idx_topk','port_I')
    p.g['indexer_state_shape']=['B',8,256]
    p.g['indexer_key_shape']=['B','Nc',128]

def hca_indices(p):
    n=p.node;e=p.edge
    p.note('hca_no_indexer','NO Lightning Indexer\nNo learned Q_I / K_I / W_weights\nNo top-512 pruning; every causal compressed window is eligible',[1360,580,1110,165],30)
    for mode,x in [('prefill',1360),('decode',1960)]:
        prefix='hist_'+mode
        labels=[
          ('input','Prefill positions t=0…T−1' if mode=='prefill' else 'Decode position p=start_pos; one token',4230,130),
          ('nc','Allocate candidate j=0…floor(T/128)−1' if mode=='prefill' else 'Nc=floor((p+1)/128) completed windows',4000,150),
          ('range','arange(floor(T/128)), repeat per query' if mode=='prefill' else 'arange(Nc); every completed window',3770,150),
          ('threshold','For query t: visible count floor((t+1)/128)' if mode=='prefill' else 'Current prefix already satisfies causality',3540,150),
          ('mask','Future j >= visible_count becomes -1' if mode=='prefill' else 'No learned score, no query-dependent top-k',3310,150),
          ('offset','Valid physical slot = T+j; preserve -1' if mode=='prefill' else 'Physical slot = 128+j (after ring buffer)',3080,150),
          ('expand','Batch-expand indices [B,T,Nc_max]' if mode=='prefill' else 'Batch-expand indices [B,1,Nc]',2850,150)]
        for k,t,y,h in labels:n(prefix+'_'+k,t,[x,y,510,h],'index',26,locator='get_compress_topk_idxs, official model.py lines 268–276')
        p.chain(*[prefix+'_'+k for k,_,_,_ in labels])
    n('hist_mode','Select prefill OR decode index list\nControlled only by start_pos, T, window_size and ratio128',[1390,2590,1080,150],'index',28,locator='get_compress_topk_idxs 268–276; Attention.forward 504–520')
    e('hist_prefill_expand','hist_mode',[.5,0,.22,1]);e('hist_decode_expand','hist_mode',[.5,0,.78,1])
    n('hist_valid','Logical rule: 128(j+1) <= t+1\nThe current incomplete 128-token window is NEVER emitted',[1390,2340,1080,150],'index',28,locator=COMP)
    n('hist_no_prune','Eligible historical entries grow with context\nNc(t)=floor((t+1)/128)\nThis is NOT fixed-k sparse retrieval',[1390,2080,1080,170],'index',29,locator='get_compress_topk_idxs 268–276')
    n('hist_examples','Examples (0-based token positions)\nt=126: 0 entries; t=127: {j0}\nt=255: {j0,j1}; t=383: {j0,j1,j2}',[1390,1800,1080,180],'index',29,locator='Derived directly from causal inequality in get_compress_topk_idxs')
    n('hist_storage','Indices refer to MAIN compressed KV bank, port A\nThere is no second indexer cache\nDo not discard old compressed entries after 512',[1390,1510,1080,170],'index',29,locator='Attention.__init__/forward 436–543; no Indexer for ratio128')
    n('hist_port_type','All eligible compressed indices are forwarded\nAttention adds local-window indices separately\nFinal concatenated list is cast to int32',[1390,1230,1080,170],'index',29,locator=ATT)
    n('port_I','PORT I → right panel\nAll causal historical compressed locations\nPrefill: valid j+T / invalid -1\nDecode: j+128',[1390,900,1080,210],'index',30,locator=ATT)
    p.chain('hist_mode','hist_valid','hist_no_prune','hist_examples','hist_storage','hist_port_type','port_I')

def attention(p):
    csa=p.kind=='csa';r=4 if csa else 128;n=p.node;e=p.edge
    n('attn_h','Hidden states h [B,T,4096]',[2650,4230,1260,110],'attn',29,locator=ATT)
    q=[('qa','Linear Wq_a: 4096 → 1024',4050,110),('qrank','Learned RMSNorm1024 → PORT Qr',3860,120),
       ('qb','Wq_b: 1024 → 64 × 512\nReshape to heads [B,T,64,512]',3660,140),
       ('qhead','Unweighted RMSNorm per 512-dim head',3460,120),
       ('qrope','RoPE on trailing64 at query t\nContent448 untouched\nCompressed layer: theta160000 / YaRN16',3250,150),
       ('qready','Q [B,T,64,512]',3060,110)]
    for k,t,y,h in q:n('attn_'+k,t,[2650,y,540,h],'attn',26,locator=ATT)
    p.chain('attn_h','attn_qa',*[('attn_'+x[0]) for x in q[1:]])
    # Source h forks into Q and KV, not h→Q→KV.
    first=next(z for z in p.g['edges'] if z['source']=='attn_h');first.update(ports=[.5,0,.5,1],points=[[3280,4200],[2920,4200]])
    kv=[('wkv','Linear Wkv: 4096 → 512',4050,110),('kvnorm','Learned RMSNorm512',3860,120),
        ('kvrope','Partial RoPE64 at token position t',3660,130),
        ('kvquant','FP8 simulation on content448, block64\nRoPE64 stays BF16; shared K=V tensor',3450,150),
        ('ring','Window ring cache [B,128,512]\nDecode write slot p%128\nPrefill: store last128 tokens in ring order',3240,150)]
    for k,t,y,h in kv:n('attn_'+k,t,[3370,y,540,h],'attn',26,locator=ATT)
    p.fork('attn_h','attn_wkv',4200);p.chain(*['attn_'+x[0] for x in kv])
    n('attn_positions','Position inputs: T, start_pos=p, window=128\nThis path computes addresses, not KV values',[2670,2870,540,155],'attn',25,locator='get_window_topk_idxs, model.py lines 254–265')
    n('attn_win_indices','get_window_topk_idxs\nPrefill: causal local window, future → -1\nDecode: ring order from p%128\nWarmup slots not yet valid → -1',[2670,2670,540,165],'attn',24,locator='get_window_topk_idxs, model.py lines 254–265')
    n('attn_I','PORT I from middle panel\n'+('Per-query selected compressed indices' if csa else 'ALL causal compressed indices'),[2670,2470,540,145],'index',25,locator=ATT)
    n('attn_A','PORT A from main compressor\nAll compressed KV [B,Nc,512]',[2670,2330,540,115],'kv',25,locator=COMP)
    n('attn_bank','Physical KV bank (K=V)\nPrefill: cat current KV[T] and complete compressed KV[Nc]\nDecode: [ring128 | compressed cache]; compressor aliases right slice',[2650,2110,1260,170],'attn',27,locator=ATT)
    n('attn_indices','Concatenate [local-window indices | port I]\nPrefill offset=T; decode compressed offset=128\nConvert to int32; -1 stays invalid',[2670,1870,1240,165],'attn',28,locator=ATT)
    p.chain('attn_positions','attn_win_indices')
    e('attn_win_indices','attn_indices',[0,.5,(2940-2670)/1240,1],[[2600,2752.5],[2600,2070],[2940,2070]])
    e('attn_I','attn_indices',[0,.5,(3300-2670)/1240,1],[[2620,2542.5],[2620,2075],[3300,2075]])
    e('attn_A','attn_bank',[.5,0,(2940-2650)/1260,1])
    e('attn_ring','attn_bank',[.5,0,(3640-2650)/1260,1])
    n('attn_gather','sparse_attn kernel: tiles of 64 index entries\nIf idx!=-1: gather shared kv[idx] (both K and V)\nQ·K / sqrt(512), FP32 score accumulators\nIf idx==-1: zero KV and -infinity score',[2730,1550,1100,190],'attn',27,locator=KER)
    n('attn_softmax','Online stable softmax: update running max and sum\nDenominator = sum_j exp(score_j-max) + exp(sink_h-max)\nThe sink changes normalization ONLY; it has no value vector',[2730,1300,1100,190],'attn',27,locator=KER)
    n('attn_sink','Learned sink_h\nOne per Q head',[3850,1300,100,190],'attn',17,locator=KER)
    n('attn_values','Numerator: sum_j exp(score_j-max) × kv[idx_j]\nDivide by denominator; FP32 accumulator → BF16 output\nResult [B,T,64,512]',[2730,1090,1100,150],'attn',27,locator=KER)
    n('attn_inverse','Conjugate RoPE (inverse=True) on output trailing64\nAt the CURRENT query position; content448 unchanged',[2730,900,1100,130],'attn',28,locator=ATT)
    n('attn_oa','Group 64×512 heads into 8 groups\nW_o_a: per-group 4096 → 1024 (einsum)',[2730,740,1100,110],'attn',28,locator=ATT)
    n('attn_ob','Flatten 8×1024 → W_o_b → 4096\nTP output all-reduce when needed',[2730,600,1100,100],'attn',28,locator='RowParallelLinear.forward 173–179; Attention.forward 533–543')
    # Output port is a separate header label; computation exits at O_b.
    p.note('attn_output','OUTPUT: attention hidden states [B,T,4096]',[2670,535,1240,60],26)
    e('attn_qready','attn_gather',[0,.5,0,.5],[[2580,3115],[2580,1645]])
    e('attn_indices','attn_gather',[.25,0,(2980-2730)/1100,1])
    e('attn_bank','attn_gather',[1,.5,(3650-2730)/1100,1],[[3930,2195],[3930,1795],[3650,1795]])
    p.chain('attn_gather','attn_softmax','attn_values','attn_inverse','attn_oa','attn_ob')
    e('attn_sink','attn_softmax',[0,.5,1,.5])
    e('attn_gather','attn_values',[1,.8,1,.5],[[3960,1702],[3960,1165]])
    p.g['port_bindings']={'A':dict(source='port_A',target='attn_A',shape=['B','Nc',512]),
                          'I':dict(source='port_I',target='attn_I',shape=['B','T','Kcomp'],dtype='integer indices, not KV'),
                          'Qr':dict(source='attn_qrank',target='idx_q_input',shape=['B','T',1024])} if csa else {
                          'A':dict(source='port_A',target='attn_A',shape=['B','Nc',512]),
                          'I':dict(source='port_I',target='attn_I',shape=['B','T','Neligible'],dtype='integer indices, not KV')}


def state_panel(p):
    csa=p.kind=='csa';r=4 if csa else 128;coff=2 if csa else 1
    p.panel('states','PREFILL / DECODE STATE + WINDOW LAYOUT — temporal state, not an extra network layer',[30,4470,3940,1050],'state')
    n=p.node
    n('state_shapes',f'MAIN runtime buffers (not checkpoint)\nkv_state / score_state: [B,{coff*r},{coff*512}]\nKV init=0; gate init=-infinity\n'+('Indexer owns separate [B,8,256] buffers' if csa else 'No indexer state or indexer KV bank'),[70,4600,1170,220],'state',27,locator=COMP)
    n('state_prefill',f'PREFILL (start_pos=0)\ncutoff=T−T%{r}; completed=floor(T/{r})\nKeep incomplete suffix for decode\n'+('Keep last complete raw window; read its Ca half later' if csa else 'Keep only current incomplete 128-token window'),[1370,4600,1170,220],'state',27,locator=COMP)
    n('state_decode',f'DECODE (position p)\nWrite raw KV / gate at slot '+(f'{r}+(p%{r})' if csa else f'p%{r}')+f'\nEmit only if (p+1)%{r}==0\nWrite cache slot floor(p/{r}); RoPE pos=p+1−{r}',[2660,4600,1250,220],'state',27,locator=COMP)
    if csa:
        n('state_window1','Compressed j=1 (emitted after token7)\nVALUES: [Ca0 Ca1 Ca2 Ca3 | Cb4 Cb5 Cb6 Cb7]\nGATES:  [Za0 Za1 Za2 Za3 | Zb4 Zb5 Zb6 Zb7] + per-slot APE\nSoftmax8 PER CHANNEL; output RoPE position4',[70,4880,1820,240],'state',29,locator='Compressor.overlap_transform, lines 307–314; forward')
        n('state_window2','Compressed j=2 (emitted after token11)\nVALUES: [Ca4 Ca5 Ca6 Ca7 | Cb8 Cb9 Cb10 Cb11]\nSame token can supply Cb to j and Ca to j+1\nFirst j=0: missing previous half has value0 / gate−infinity',[2010,4880,1900,240],'state',29,locator=COMP)
        n('state_move','On a completed decode stride: copy current raw window into previous-window state. Read Ca from previous slots and Cb from current slots.\nA partial stride does NOT create a new compressed entry. Existing entries remain readable; Indexer top-k does not delete them.',[70,5200,3840,200],'state',29,locator=COMP)
        p.g['window_examples']=[dict(j=1,ca_tokens=[0,1,2,3],cb_tokens=[4,5,6,7],rope_position=4),dict(j=2,ca_tokens=[4,5,6,7],cb_tokens=[8,9,10,11],rope_position=8)]
    else:
        n('state_window1','Compressed j=0\nTokens0…127 → one512-dim vector\nAPE has128 slot rows; softmax is per-channel over128 tokens\nEmission p=127; RoPE position0; stored at compressed slot0',[70,4880,1820,240],'state',29,locator=COMP)
        n('state_window2','Compressed j=1\nTokens128…255 → a DIFFERENT512-dim vector\nNo token overlap with j0; no previous-window Ca branch\nEmission p=255; RoPE position128; stored at compressed slot1',[2010,4880,1900,240],'state',29,locator=COMP)
        n('state_move','Before boundary p=127/255/…: update partial-window state only. At boundary: compress128 slots and append one KV entry.\nAll earlier completed entries remain in cache and are indexed causally. No learned retrieval network and no top-512 cap.',[70,5200,3840,200],'state',29,locator=COMP)
        p.g['window_examples']=[dict(j=0,first_token=0,last_token=127,rope_position=0),dict(j=1,first_token=128,last_token=255,rope_position=128)]
    p.note('footer','Source: official deepseek-ai/DeepSeek-V4-Flash @ 60d8d707 | model.py Compressor / Indexer / Attention; kernel.py sparse_attn\nDetailed static source transcription; no full weights, tensor headers or GPU inference executed. Native draw.io is the PNG source.',[50,5560,3900,110],24)


def build(kind):
    p=start(kind);compressor(p)
    if kind=='csa':indexer(p)
    else:hca_indices(p)
    attention(p);state_panel(p)
    from deepseek_operator_style import apply
    return apply(p.g,kind)

if __name__=='__main__':
    for kind in ['csa','hca']:
        g=build(kind);path=Path(__file__).with_name('deepseek_v4_flash_'+kind+'.graph.json')
        path.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
        print(path.name,len(g['nodes']),'nodes',len(g['edges']),'edges')
