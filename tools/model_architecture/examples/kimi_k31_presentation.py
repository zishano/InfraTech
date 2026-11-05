"""Typography, alignment and simpler routing; model delta semantics unchanged."""
import re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from routing import simplify_connections

def present(g):
    ns={n['id']:n for n in g['nodes']}
    # Align the attention-residual main chain to one vertical axis.
    for key in ['ar_logits','ar_softmax','ar_sum','ar_out']:
        n=ns[key];x,y,w,h=n['box'];n['box']=[200,y,420,h]
    ns['ar_keys']['box']=[270,868,280,94]
    ns['ar_query']['box']=[610,868,190,108]
    labels={'ar_query':'Pseudo-query w','ar_values':'Values V\n(original)',
            'ar_sum':'Weighted sum','ar_out':'Output to next sublayer',
            'ar_logits':'wᵀ RMSNorm(K)','ar_softmax':'Softmax (depth)',
            'idx_qproj':'Linear Wq\n1536 →4096','idx_cache':'Index K cache\n[T,128]',
            'idx_wproj':'Linear (weights)\n7168 →32','idx_scale':'Scale\n1 / sqrt(32×128)',
            'idx_weights':'w [32]','idx_sum':'Weighted sum (heads)',
            'vision_title':'MoonViT-V2 · 27 layers · hidden 1024',
            'diff_quant':'CONFIG ONLY\nMXFP4 exclusions: 6 →8 rules',
            'diff_count':'ADDED INDEXER PARAMETERS\n+178.53M BF16 elements\n(provider metadata; source-derived match)'}
    for key,label in labels.items():ns[key]['label']=label
    ns['idx_wproj']['box']=[2670,2200,190,70]
    ns['ex_mul']['box'][1]=650
    # More breathing room and readable type in the six-step vision inset.
    def yy(y):return y if y<=2508 else 2508+(y-2508)*1.3
    for n in g['nodes']:
        x,y,w,h=n['box']
        if y>=2452:n['box']=[x,round(yy(y),1),w,round(yy(y+h)-yy(y),1)]
    for e in g['edges']:
        if 'points' in e:e['points']=[[x,round(yy(y),1)] for x,y in e['points']]
    ns['vision_encoder']['label']=''
    g['height']=3014
    # A small set of type sizes; fit by changing line breaks before shrinking.
    for n in g['nodes']:
        key=n['id'];text=n['label'];x,y,w,h=n['box'];dec=n.get('kind')=='decoration'
        if not text:continue
        if key=='title':font=44
        elif key.endswith('_title'):font=28
        elif key=='params':font=28
        elif key=='subtitle':font=24
        elif key in ['sources','vision_caveat']:font=16
        elif key.startswith(('mini_','vit','vision_enc_')):font=16
        elif key.startswith(('k_','m_')):font=18
        elif key.startswith(('ar_','lm_','diff_')) or key=='retired_dense_attention':font=22
        else:font=20
        if text in ['+','×']:font=28
        # Keep existing safety margins on small labels and tiny tensor ports.
        lines=text.split('\n')
        sizes=[s for s in [44,28,24,22,20,18,16,14,12] if s<=font]
        for size in sizes:
            if len(lines)*size*1.18+10<=h and max(len(line) for line in lines)*size*.56+12<=w:
                font=size;break
        else:font=sizes[-1]
        n['style']=re.sub(r'fontSize=[^;]+;','',n['style'])+f'fontSize={font};fontFamily=Arial;spacing=4;'
        if dec and not key.endswith('_title') and key not in ['hybrid_outline','title']:
            n['style']+='fontStyle=0;'
    # Explicit three-segment bypass for original values around the pseudo-query.
    for e in g['edges']:
        if (e['source'],e['target'])==('ar_source','ar_values'):
            e['ports']=[1,.5,1,.5];e['points']=[[866,1041],[866,670]]
    # Connect the vision output directly around the pooling column in one bend.
    for e in g['edges']:
        if (e['source'],e['target'])==('vision_out','vision_merge'):
            x,y,w,h=ns['vision_out']['box'];tx,ty,tw,th=ns['vision_merge']['box']
            e['ports']=[.95,1,0,.5];e['points']=[[x+w*.95,ty+th/2]];e['routing']='straight'
    simplify_connections(g)
    g['presentation']={'base':'Kimi-K3 reviewed layout','typography':'Arial / uniform heading, operator and detail levels',
                       'routing':'clear aligned straight segments first; one bend second; detour only around obstacles',
                       'notes':'Full annotations and model-diff classifications are preserved.'}
    return g
