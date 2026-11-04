"""Generate an editable SVG from report-verified facts. Python standard library only."""
from pathlib import Path
from html import escape
W,H=1800,2300
out=[]
def add(s): out.append(s)
def text(x,y,s,size=20,color='#223047',anchor='start',bold=False):
    add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{700 if bold else 400}">{escape(s)}</text>')
def panel(x,y,w,h,title,color):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="white" stroke="{color}" stroke-width="2" stroke-dasharray="8 5"/>')
    text(x+20,y+34,title,25,color,bold=True)
def box(x,y,w,h,lines,color='#edf2f8',size=19):
    if isinstance(lines,str): lines=[lines]
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{color}" stroke="#bbc7d5"/>')
    for i,s in enumerate(lines):text(x+w/2,y+h/2+(i-(len(lines)-1)/2)*25+7,s,size,anchor='middle')
def arrow(x1,y1,x2,y2,color='#52627a',dash=False):
    add(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" fill="none" stroke-width="2" marker-end="url(#arrow)"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
def lines(x,y,items,size=18,gap=28):
    for i,s in enumerate(items):text(x,y+i*gap,s,size)
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
add('<title id="title">Kimi K3 architecture study</title><desc id="desc">Technical report verified conceptual architecture; config and weight index remain unverified.</desc>')
add('<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#52627a"/></marker></defs>')
add('<rect width="100%" height="100%" fill="#fff"/><g font-family="DejaVu Sans,Arial,sans-serif">')
text(900,62,'Kimi K3 | Architecture Study',40,anchor='middle',bold=True)
text(900,105,'Technical-report verified draft · HF config and weight index not yet verified',21,anchor='middle')
box(45,132,1710,68,'2.78T total · 104.2B active · 93 layers · d_model 7168 · 96 heads · 1M context','#f2f5fb',25)
# Center backbone, bottom to top.
panel(650,230,500,1290,'LANGUAGE BACKBONE','#8056bb')
for y,label in [(310,'Output tokens'),(405,'LM head'),(500,'Final depth aggregation / norm')]:
    box(695,y,410,64,label,'#f0eafa')
arrow(900,405,900,374);arrow(900,500,900,469)
box(695,615,410,100,['Final Gated MLA + FFN','Global attention / NoPE'],'#fff0df')
arrow(900,615,900,564)
panel(680,770,440,455,'23 × HYBRID GROUP','#8056bb')
box(705,835,390,100,['1 × Gated MLA + FFN','Global causal attention / NoPE'],'#fff0df')
box(705,1025,390,100,['3 × KDA + FFN','Recurrent linear attention'],'#eaf6dc')
arrow(900,1025,900,935);arrow(900,835,900,715)
text(900,1180,'69 KDA + 24 Gated MLA = 93',22,anchor='middle',bold=True)
box(695,1280,410,95,['92 MoE FFNs + 1 dense FFN','Dense-layer location not mapped'],'#f1edf9',19)
box(695,1410,410,65,'Fused multimodal embeddings','#e1f5f1')
add('<path d="M900,1410 L670,1410 L670,1235 L900,1235 L900,1225" fill="none" stroke="#52627a" stroke-width="2" marker-end="url(#arrow)"/>')
# A conceptual callout, not a standalone layer in the data path.
text(900,1255,'FFN composition across all 93 layers',17,anchor='middle')
# AttnRes
panel(45,230,555,470,'BLOCK ATTENTION RESIDUALS','#8056bb')
box(80,295,485,65,'Embedding + block sums + partial sum','#f0eafa')
arrow(322,360,322,390)
box(80,390,220,65,'Keys: RMSNorm','#f0eafa');box(345,390,220,65,'Values: unchanged','#f0eafa')
box(80,490,485,65,'Learned pseudo-query w → depth softmax','#f0eafa',18)
arrow(190,455,190,490);arrow(455,455,455,590);arrow(320,555,320,590)
box(80,590,485,65,'Weighted sum → next sublayer','#f0eafa')
text(80,683,'Applied before attention and FFN sublayers',18)
arrow(600,465,650,465,'#8056bb',True)
# KDA
panel(45,735,555,785,'KIMI DELTA ATTENTION (KDA)','#70a73c')
box(80,800,485,60,'Input x [d = 7168]','#eaf6dc')
box(80,900,485,80,['Q, K, V: Linear → ShortConv → Swish','Q and K additionally L2-normalized'],'#eaf6dc',18)
arrow(322,860,322,900)
box(80,1040,485,85,['KDA recurrent state update S_t','Inputs: Q, K, V, decay α, write gate β'],'#eaf6dc',18)
arrow(322,980,322,1040)
box(80,1180,485,65,'Head-wise RMSNorm','#eaf6dc');arrow(322,1125,322,1180)
box(80,1300,485,65,'× sigmoid(W_g x) → W_o → output','#eaf6dc',18);arrow(322,1245,322,1300)
lines(80,1420,['g = −5 · sigmoid(exp(A) · z); α = exp(g)','β = sigmoid(Wβ x)','Fixed-size recurrent state; full-rank output gate'],17)
arrow(600,1090,650,1090,'#70a73c',True)
# MoE
panel(1200,230,555,660,'STABLE LATENT MoE','#2684d5')
box(1230,295,495,60,'Input x [7168]','#e5f2ff')
box(1230,405,230,90,['2 shared experts','7168 → 7168'],'#e5f2ff',18)
box(1490,405,235,90,['Down projection','7168 → 3584'],'#e5f2ff',18)
arrow(1360,355,1360,405);arrow(1605,355,1605,405)
box(1490,535,235,100,['896 routed experts','Top 16 per token','Weighted sum'],'#e5f2ff',17);arrow(1605,495,1605,535)
box(1490,670,235,70,['RMSNorm','3584 → 7168 up'],'#e5f2ff',18);arrow(1605,635,1605,670)
box(1230,780,495,60,'SUM: shared + routed output [7168]','#e5f2ff',18)
arrow(1360,495,1360,780);arrow(1605,740,1605,780)
text(1230,875,'Router: Quantile Balancing · Expert FFN: 3072 / SiTU-GLU',16)
arrow(1150,960,1200,550,'#2684d5',True)
# MLA
panel(1200,925,555,595,'GATED MLA | NoPE','#e58a21')
box(1230,990,495,60,'Input x','#fff0df')
box(1230,1100,225,80,['Query projection','Q'],'#fff0df',18)
box(1485,1100,240,80,['KV compression','Latent cache c'],'#fff0df',18)
arrow(1340,1050,1340,1100);arrow(1605,1050,1605,1100)
box(1230,1240,495,65,'Global causal attention (Q, reconstructed K/V)','#fff0df',17)
arrow(1340,1180,1340,1240);arrow(1605,1180,1605,1240)
box(1230,1360,495,65,'× sigmoid(W_g x) → W_o → output','#fff0df',18);arrow(1475,1305,1475,1360)
text(1477,1470,'NO RoPE / no explicit position encoding',21,'#a85c0c',anchor='middle',bold=True)
text(1477,1500,'Projection ranks pending model configuration',17,anchor='middle')
arrow(1150,670,1200,1160,'#e58a21',True)
# Vision bottom
panel(45,1560,1710,440,'NATIVE MULTIMODAL INPUT | MoonViT-V2','#219a95')
box(80,1630,265,75,['Images / video','Patch embedding (14)'],'#e1f5f1',18)
box(410,1630,430,125,['MoonViT-V2 · 27 layers · 401M','12 heads · RMSNorm','Spatial / temporal attention + FFN'],'#e1f5f1',18)
box(905,1630,305,125,['Temporal pooling','2 × 2 pixel shuffle','4× fewer spatial tokens'],'#e1f5f1',18)
box(1275,1630,430,125,['Lightweight MLP projector','Map vision features to LM width'],'#e1f5f1',18)
arrow(345,1668,410,1668);arrow(840,1668,905,1668);arrow(1210,1668,1275,1668)
box(80,1820,570,65,'Text → Tokenizer → Token embeddings','#edf2f8',20)
box(905,1820,800,65,'Merge visual features with text-token embeddings','#e1f5f1',20)
arrow(650,1852,905,1852);arrow(1490,1755,1490,1820)
add('<path d="M1305,1885 L1305,1940 L625,1940 L625,1487 L900,1487 L900,1475" fill="none" stroke="#52627a" stroke-width="2" marker-end="url(#arrow)"/>')
text(80,1965,'Vision linear and attention projections are bias-free. Vision hidden width is not assumed.',19)
# Footnotes
box(45,2040,1710,65,'Auxiliary: 1 MTP layer reported separately; not counted as another main-backbone layer.','#f2f5fb',21)
lines(55,2150,[
'SOURCES: MoonshotAI/Kimi-K3 technical report §§2.1–2.4 and Table 1; official repository commit 3cb39df.',
'BACKBONE: 23 × (3 KDA + 1 MLA) + final MLA is the reported attention schedule; dense FFN is part of the 93 layers.',
'EVIDENCE LIMIT: Hugging Face config / safetensors index inaccessible under current network policy.',
'Transformers main f275431 has kimi_k25 and kimi_linear, but no direct kimi_k3 implementation was found.',
'Conceptual module topology, not an executable graph. Tensor ranks, exact FFN placement and weight names remain unverified.'
],17,28)
add('</g></svg>')
p=Path(__file__).with_name('kimi_k3_architecture.svg');p.write_text('\n'.join(out));print(p)
