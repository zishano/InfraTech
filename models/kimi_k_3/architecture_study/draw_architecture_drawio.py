"""Build portable, uncompressed diagrams.net XML with editable native shapes."""
from pathlib import Path
import xml.etree.ElementTree as E

BASE = Path(__file__).parent
mxfile = E.Element('mxfile', host='app.diagrams.net', type='device', version='24.7.17')
page = E.SubElement(mxfile, 'diagram', id='kimi-k3-v2', name='Kimi K3 Detailed v2')
model = E.SubElement(page, 'mxGraphModel', dx='2600', dy='3500', grid='1', gridSize='10', guides='1', tooltips='1', connect='1', arrows='1', fold='1', page='1', pageScale='1', pageWidth='2600', pageHeight='3500', math='0', shadow='0')
root = E.SubElement(model, 'root')
E.SubElement(root, 'mxCell', id='0')
E.SubElement(root, 'mxCell', id='1', parent='0')
ids = set(['0','1'])
boxes = {}
colors={'purple':('#f2eafa','#8650b5'),'green':('#edf8df','#659c33'),'blue':('#e9f3ff','#277dc8'),'orange':('#fff0de','#ec8a1a'),'teal':('#e1f5f2','#199c98'),'grey':('#f4f6fa','#738195')}

def node(key,label,x,y,w=180,h=54,color='grey',shape='rounded',font=20):
    assert key not in ids,key
    ids.add(key); boxes[key]=(x,y,w,h)
    fill,stroke=colors[color]
    style=f'rounded=1;whiteSpace=wrap;html=0;fillColor={fill};strokeColor={stroke};fontColor=#152337;fontFamily=Arial;fontSize={font};align=center;verticalAlign=middle;spacing=5;strokeWidth=1.5;'
    if shape=='ellipse':style+='shape=ellipse;aspect=fixed;'
    c=E.SubElement(root,'mxCell',id=key,value=label,style=style,vertex='1',parent='1')
    E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    return key

def label(key,text,x,y,w,h=40,font=20,color='#24344b'):
    assert key not in ids;ids.add(key)
    c=E.SubElement(root,'mxCell',id=key,value=text,style=f'text;html=0;whiteSpace=wrap;align=center;verticalAlign=middle;fontFamily=Arial;fontSize={font};fontColor={color};',vertex='1',parent='1')
    E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})

def panel(key,title,x,y,w,h,color):
    fill,stroke=colors[color]
    assert key not in ids;ids.add(key)
    c=E.SubElement(root,'mxCell',id=key,value='',style=f'rounded=1;fillColor=#ffffff;strokeColor={stroke};dashed=1;dashPattern=8 5;strokeWidth=2;pointerEvents=0;',vertex='1',parent='1',connectable='0')
    E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    label(key+'_title',title+'  ↑',x+10,y+10,w-20,50,26,stroke)

def edge(src,dst,text='',ports=None,dashed=False,points=None):
    key='edge_'+str(len(ids));ids.add(key)
    style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;endArrow=block;endFill=1;strokeColor=#43546b;strokeWidth=1.5;fontFamily=Arial;fontSize=16;labelBackgroundColor=#ffffff;'
    if ports is None:style+='exitX=0.5;exitY=0;entryX=0.5;entryY=1;'
    else:style+='exitX=%s;exitY=%s;entryX=%s;entryY=%s;'%ports
    if dashed:style+='dashed=1;'
    c=E.SubElement(root,'mxCell',id=key,value=text,style=style,edge='1',parent='1',source=src,target=dst)
    g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
    if points:
        arr=E.SubElement(g,'Array',attrib={'as':'points'})
        for x,y in points:E.SubElement(arr,'mxPoint',x=str(x),y=str(y))

def chain(items):
    for a,b in zip(items,items[1:]):edge(a,b)

label('title','Kimi K3 — Architecture Study / Detailed v2',30,20,2540,70,42)
label('subtitle','Bottom-up computational flow · editable diagrams.net / draw.io source',30,95,2540,45,25)
node('params','2.78T total · 104.2B active · 93 layers · hidden 7168 · 96 heads · 1M context',50,155,2500,65,'purple',font=27)
# Background panels first, for correct layering.
panel('attnres','Block Attention Residuals',30,250,820,800,'purple')
panel('kda','Kimi Delta Attention — five inputs + separate output gate',30,1080,820,1380,'green')
panel('backbone','Language Backbone',880,250,650,2210,'purple')
panel('moe','Stable LatentMoE',1560,250,1010,1030,'blue')
panel('mla','Gated MLA — NoPE / no RoPE',1560,1310,1010,1150,'orange')
panel('vision','Native vision / multimodal input',30,2490,2540,760,'teal')
# AttnRes: independent learned query, original-value bypass.
node('ar_source','Stack: embedding + completed block sums\n+ current partial sum',75,935,720,75,'purple')
node('ar_keys','RMSNorm(keys)',80,795,300,65,'purple')
node('ar_query','Learned pseudo-query w\n(independent parameter)',440,795,300,65,'purple')
node('ar_logits','Depth logits: wᵀ RMSNorm(K)',80,665,480,65,'purple')
node('ar_softmax','Softmax over depth',80,555,480,65,'purple')
node('ar_values','Original values V\n(unchanged)',635,540,150,95,'purple',font=18)
node('ar_sum','Weighted sum of original values',95,430,675,65,'purple')
node('ar_out','Output to next attention / FFN sublayer',95,330,675,65,'purple')
chain(['ar_source','ar_keys','ar_logits','ar_softmax','ar_sum','ar_out'])
edge('ar_query','ar_logits',ports=(0.5,0,0.9,1));edge('ar_source','ar_values',ports=(0.9,0,0.5,1));edge('ar_values','ar_sum',ports=(0.5,0,1,0.5))
# KDA: exact five input columns and sixth output gate bypass.
node('kda_x','Input x [T, 7168]',65,2355,745,65,'green')
cols=[80,205,330,455,610]
widths=[105,105,105,140,105]
for name,x,w in zip(['q','k','v','alpha','beta'],cols,widths):
    prev='kda_x'
    if name in ('q','k','v'):
        items=[('linear','Linear W'+name,2240),('conv','ShortConv',2130),('swish','Swish / SiLU',2020)]
        if name!='v':items.append(('l2','L2Norm',1910))
    elif name=='alpha':
        items=[('down','Linear Wα↓',2240),('up','Linear Wα↑',2145),('bias','z = · + bα',2050),('scale','× exp(A)',1955),('sigmoid','g = −5 sigmoid(·)',1860),('exp','α = exp(g)',1765)]
    else:items=[('linear','Linear Wβ',2240),('sigmoid','Sigmoid',2020)]
    for tag,txt,y in items:
        key='kda_'+name+'_'+tag;node(key,txt,x,y,w,62,'green',font=16 if name=='alpha' else 17);edge(prev,key);prev=key
    key='kda_port_'+name;node(key,{'q':'Q','k':'K','v':'V','alpha':'α','beta':'β'}[name],x,1655,w,45,'green',font=23);edge(prev,key)
node('kda_core','Kimi Delta Attention / recurrent state update\nSₜ = (I − βₜ kₜ kₜᵀ) Diag(αₜ) Sₜ₋₁ + βₜ kₜ vₜᵀ\noₜ = Sₜᵀ qₜ',60,1510,665,115,'green',font=18)
for name,x,w in zip(['q','k','v','alpha','beta'],cols,widths):edge('kda_port_'+name,'kda_core',ports=(0.5,0,((x+w/2)-60)/665,1))
node('kda_norm','Head-wise RMSNorm',105,1400,560,60,'green')
node('kda_product','×',355,1305,65,65,'green',shape='ellipse',font=28)
node('kda_gate_linear','Full-rank\nLinear Wg',730,2050,100,85,'green',font=17)
node('kda_gate_sigmoid','Sigmoid',730,1390,100,60,'green',font=17)
node('kda_wo','Linear Wo → output y [T, 7168]',95,1190,585,65,'green')
chain(['kda_core','kda_norm','kda_product','kda_wo'])
chain(['kda_x','kda_gate_linear','kda_gate_sigmoid']);edge('kda_gate_sigmoid','kda_product','output gate',ports=(0.5,0,1,0.5))
# Backbone: representative layer breakdown, no extra dense attention layer.
node('lm_fused','Fused sequence (text + visual tokens)',920,2340,570,65,'purple')
node('lm_repeat','23 × [3 KDA + FFN, then 1 Gated MLA + FFN]\n= 92 attention layers',920,830,570,100,'purple')
node('lm_final','Final Gated MLA + FFN\n= 1 attention layer',920,660,570,90,'orange')
node('lm_norm','Final depth aggregation / normalization',920,530,570,65,'purple')
node('lm_head','LM head',980,430,450,65,'purple')
node('lm_out','Output tokens',980,330,450,65,'purple')
chain(['lm_repeat','lm_final','lm_norm','lm_head','lm_out'])
label('lm_counts','69 KDA + 24 Gated MLA = 93\n92 MoE FFNs + 1 dense FFN\nDense FFN location not mapped',930,970,550,110,23)
prev='lm_fused'
for prefix,y0,title,attn in [('k',2240,'Representative KDA layer','KDA recurrent attention'),('m',1630,'Representative Gated MLA layer','Gated MLA (NoPE)')]:
    label(prefix+'_title',title,935,y0-520,540,35,23)
    seq=[('ar1','Block AttnRes'),('norm1','RMSNorm'),('attn',attn),('ar2','Block AttnRes / partial update'),('norm2','RMSNorm'),('ffn','FFN (MoE or dense)'),('out','Depth / partial-state update')]
    for i,(tag,txt) in enumerate(seq):
        key=prefix+'_'+tag;node(key,txt,965,y0-i*65,480,48,'green' if prefix=='k' else 'orange',font=19);edge(prev,key);prev=key
edge(prev,'lm_repeat')
# MoE: three independent paths from original x.
node('moe_x','Input x [T, 7168]',1600,1170,930,65,'blue')
node('moe_shared','2 shared experts\n7168 → 7168',1590,590,200,90,'blue')
node('moe_down','Linear down\n7168 → 3584',1835,1040,230,75,'blue')
node('moe_bank','896 routed experts\nSelect 16 per token\nFFN intermediate 3072',1835,875,230,110,'blue')
node('moe_weighted','Router-weighted sum',1835,765,230,65,'blue')
node('moe_norm','RMSNorm (3584)',1835,660,230,65,'blue')
node('moe_up','Linear up\n3584 → 7168',1835,550,230,75,'blue')
node('moe_router','Router: score\nQuantile Balancing\nTop-16',2110,1020,190,110,'blue')
node('moe_sum','+',1915,430,65,65,'blue',shape='ellipse',font=30)
node('moe_y','Output y [T, 7168]',1770,330,380,65,'blue')
chain(['moe_x','moe_down','moe_bank','moe_weighted','moe_norm','moe_up','moe_sum','moe_y'])
edge('moe_x','moe_shared',ports=(0.07,0,0.5,1));edge('moe_shared','moe_sum',ports=(0.5,0,0,0.5))
edge('moe_x','moe_router',ports=(0.65,0,0.5,1));edge('moe_router','moe_bank','selection',ports=(0,0.25,1,0.5));edge('moe_router','moe_weighted','weights',ports=(0.5,0,1,0.5))
# Expert inset: SiTU-GLU explicit bounded factors.
node('ex_x','Expert input\n3584 routed / 7168 shared',2320,1120,220,85,'blue',font=17)
node('ex_gate','Linear Wgate\na = Wgate x',2310,950,105,90,'blue',font=16)
node('ex_up','Linear Wup\nb = Wup x',2430,950,105,90,'blue',font=16)
node('ex_capgate','4 tanh(a/4)\n× sigmoid(a)',2310,790,105,100,'blue',font=16)
node('ex_capup','25 tanh(b/25)',2430,790,105,100,'blue',font=16)
node('ex_mul','×',2390,670,60,60,'blue',shape='ellipse',font=28)
node('ex_down','Linear Wdown\n3072 → expert width',2310,520,230,90,'blue',font=17)
node('ex_y','Expert output',2310,395,230,60,'blue',font=19)
chain(['ex_x','ex_gate','ex_capgate','ex_mul','ex_down','ex_y']);edge('ex_x','ex_up');chain(['ex_up','ex_capup','ex_mul'])
# MLA: query, compressed KV, and independent output gate.
node('mla_x','Input x [T, 7168]',1610,2355,900,65,'orange')
node('mla_q','Query projection Wq',1610,2180,230,75,'orange')
node('mla_compress','KV compression: x → c',1870,2180,350,75,'orange')
node('mla_cache','Compressed latent KV cache c',1870,2050,350,75,'orange')
node('mla_reconstruct','Learned up projection / split K,V',1870,1920,350,75,'orange')
node('mla_port_q','Q',1690,1805,80,50,'orange');node('mla_port_k','K',1900,1805,80,50,'orange');node('mla_port_v','V',2100,1805,80,50,'orange')
node('mla_attention','Global causal attention — NoPE',1615,1660,700,90,'orange',font=23)
node('mla_gate','Full-rank Linear Wg',2315,2150,225,75,'orange',font=18)
node('mla_sigmoid','Sigmoid',2330,1640,190,65,'orange')
node('mla_mul','×',1925,1550,65,65,'orange',shape='ellipse',font=30)
node('mla_wo','Linear Wo → output y [T, 7168]',1680,1420,575,65,'orange')
chain(['mla_x','mla_q','mla_port_q','mla_attention','mla_mul','mla_wo'])
chain(['mla_x','mla_compress','mla_cache','mla_reconstruct','mla_port_k']);edge('mla_reconstruct','mla_port_v');edge('mla_port_k','mla_attention',ports=(0.5,0,0.5,1));edge('mla_port_v','mla_attention',ports=(0.5,0,0.8,1))
chain(['mla_x','mla_gate','mla_sigmoid']);edge('mla_sigmoid','mla_mul',ports=(0.5,0,1,0.5))
label('mla_note','No RoPE. Exact projection ranks / head dimensions pending configuration.',1600,2300,930,40,18)
# Vision: full upward input pathway, plus upward internal examples.
node('vision_input','Images / video',80,3150,300,55,'teal')
node('vision_processor','ImageProcessor',80,3060,300,55,'teal')
node('vision_patch','Patch embedding (patch 14)',80,2970,300,55,'teal')
node('vision_encoder','MoonViT-V2: 27 layers / 401M / 12 heads\nRMSNorm / spatial + temporal attention / FFN\nBias-free linear and attention projections',80,2775,650,130,'teal',font=20)
node('vision_pool','Temporal pooling + 2 × 2 pixel shuffle\n4× fewer spatial tokens',80,2640,650,85,'teal')
node('vision_projector','Lightweight MLP projector → visual embeddings',790,2640,700,70,'teal')
chain(['vision_input','vision_processor','vision_patch','vision_encoder','vision_pool']);edge('vision_pool','vision_projector',ports=(1,0.5,0,0.5))
node('text_input','Text',850,3150,400,55,'grey');node('text_tokenizer','Tokenizer',850,3050,400,55,'grey');node('text_embedding','Text embedding [Ttext, 7168]',850,2940,400,65,'grey')
node('vision_merge','Merge text + visual embeddings',850,2820,590,70,'teal')
chain(['text_input','text_tokenizer','text_embedding','vision_merge'])
edge('vision_projector','vision_merge','visual tokens',ports=(1,0.5,1,0.5),points=[(1510,2675),(1510,2855)])
edge('vision_merge','lm_fused','fused sequence',ports=(0.5,0,0.5,1),points=[(1135,2610),(1205,2610)])
for prefix,x,items in [('vitattn',1600,['Input x','Linear QKV (bias-free)','Spatial / temporal attention','Linear Wo → output']),('vitffn',2090,['Input x','Linear up','GELU (schematic)','Linear down → output'])]:
    prev=None
    for i,txt in enumerate(items):
        key=prefix+str(i);node(key,txt,x,3130-i*135,400,75,'teal',font=20)
        if prev:edge(prev,key)
        prev=key
label('vision_caveat','Vision inset is schematic; exact projector / FFN configuration not weight verified.',1550,2580,950,55,18)
node('mtp','Auxiliary: 1 MTP layer reported separately; not added to the 93-layer main backbone.',50,3290,2500,65,'grey',font=24)
label('sources','Source: MoonshotAI/Kimi-K3 technical report §§2.1–2.4 / Table 1 · commit 3cb39df\nReport-based conceptual topology. HF config / weight index not verified; exact ranks and dense-layer location pending.',50,3380,2500,85,21)

# Validate native graph integrity before writing.
cells=root.findall('mxCell');known={c.get('id') for c in cells}
assert len(known)==len(cells)
for c in cells:
    for ref in ['parent','source','target']:
        if c.get(ref):assert c.get(ref) in known,(c.get('id'),ref)
    if c.get('vertex')=='1':
        g=c.find('mxGeometry');x,y,w,h=[float(g.get(a)) for a in ['x','y','width','height']]
        assert x>=0 and y>=0 and x+w<=2600 and y+h<=3500,c.get('id')
E.indent(mxfile,space='  ')
path=BASE/'kimi_k3_design_preview_v2.drawio'
E.ElementTree(mxfile).write(path,encoding='utf-8',xml_declaration=True)
E.parse(path)
print(f'{path}: {sum(c.get("vertex")=="1" for c in cells)} native shapes, {sum(c.get("edge")=="1" for c in cells)} edges; XML and references valid')
