"""Page composition: compact lanes, adjacent attention/indexer, aligned header."""
import re

def reflow(g,kind):
    nodes={n['id']:n for n in g['nodes']}
    old={k:list(n['box']) for k,n in nodes.items()}
    if kind=='overview':
        sx=.94
        def yy(y):return y
        g['width']=1700
        g['height']=1649
    else:
        sx=.8
        def yy(y):
            if y<162:return y*.8
            if y<=1588:return 130+(y-162)*.64
            if y<1609:return 1043+(y-1588)
            return 1090+(y-1609)*.75
        g['width']=1920;g['height']=1440
    # Transform node centers, retaining readable operator sizes.
    for key,n in nodes.items():
        x,y,w,h=n['box'];dec=n.get('kind')=='decoration'
        if key in ['attn_oa','attn_ob']:n['label']=n['label'].split('\n')[0]
        if dec:
            n['box']=[round(x*sx,1),round(yy(y),1),round(w*sx,1),round(yy(y+h)-yy(y),1)]
        else:
            cx=(x+w/2)*sx;cy=yy(y+h/2)
            n['style']=re.sub(r'fontSize=\d+(?:\.\d+)?;', 'fontSize=13;',n['style'])
            if n['label'] in ['+','×']:nw=nh=28
            else:
                lines=n['label'].split('\n')
                nw=max(78,max(len(s) for s in lines)*7.5+22)
                # Avoid growing the tiny split / linear pair in the Indexer.
                nw=round(min(nw,max(w,78))/2)*2
                nh=30 if len(lines)==1 else 42
            cx=round(cx,1);cy=round(cy,1)
            n['box']=[round(cx-nw/2,1),round(cy-nh/2,1),round(nw,1),nh]
            size=max(10,min(13,int((nw-16)/(max(len(s) for s in n['label'].split('\n'))*.55))))
            n['style']+=f'fontSize={size};'
    for key,n in nodes.items():
        if n.get('kind')=='decoration' and n['label']:
            x,y,w,h=n['box'];height=max(h,24 if len(n['label'].splitlines())==1 else 42)
            n['box']=[x,round(y+(h-height)/2,1),w,height]
        if key=='attn_output':n['label']=''
    # Apply the same continuous map to all existing routes, then snap side centers.
    for e in g['edges']:
        if 'points' not in e:continue
        e['points']=[[round(x*sx,1),round(yy(y),1)] for x,y in e['points']]
        for endpoint,index in [('source',0),('target',-1)]:
            x,y,w,h=old[e[endpoint]];nx,ny,nw,nh=nodes[e[endpoint]]['box']
            if abs(e['points'][index][1]-yy(y+h/2))<.2:
                e['points'][index][1]=round(ny+nh/2,1)
    if kind!='overview':
        # Put Attention between the compressor and Indexer, following tensor flow.
        # The modules use named tensor ports, so the move does not create long wires.
        groups={}
        for key in nodes:
            if key.startswith(('idx_','hist_')) or key in ['middle','middle_title','port_I','hca_no_indexer']:
                groups[key]='index'
            elif key.startswith('attn_') or key in ['attention','attention_title']:
                groups[key]='attention'
        dx={'index':664,'attention':-620}
        for key,group in groups.items():nodes[key]['box'][0]+=dx[group]
        for e in g['edges']:
            a=groups.get(e['source']);b=groups.get(e['target'])
            if a and a==b and 'points' in e:
                for point in e['points']:point[0]+=dx[a]
        nodes['attn_ob']['box'][1]-=6
        nodes['attn_sink']['box'][0]=1140
        nodes['attn_sink']['box'][2]=64
        # Breathing room for the header; the model name is left-aligned.
        for key,box in [('title',[32,14,1400,38]),('source',[32,58,1400,25]),
                        ('facts',[32,86,1400,25]),('ports',[32,111,1840,20])]:
            nodes[key]['box']=box
            nodes[key]['style']+='align=left;'
        # Make each module header follow the same left margin.
        for key in ['compressor_title','middle_title','attention_title']:
            nodes[key]['style']+='align=left;spacingLeft=14;'
    if kind=='overview':overview_composition(g,nodes)
    # Native descriptions and graph edges remain authoritative.
    g['presentation']['layout']=('central backbone; mHC/MoE left; attention/compressors right' if kind=='overview' else 'compact columns: compressor → attention ← indexer; aligned lanes; independent state strip')
    return g


def overview_composition(g,nodes):
    """Attention/compressor on the right; mHC/MoE on the left of backbone."""
    a=nodes['compress']['box'];b=nodes['moe']['box']
    transforms={'compress':(list(a),list(b)),'moe':(list(b),list(a))}
    groups={}
    for key in nodes:
        if key.startswith(('csa_','hca_')) or key in ['compress','compress_heading']:groups[key]='compress'
        if key.startswith(('moe_','expert_')) or key in ['moe','moe_heading']:groups[key]='moe'
    def point(group,x,y):
        (ax,ay,aw,ah),(bx,by,bw,bh)=transforms[group]
        return bx+(x-ax)*bw/aw,by+(y-ay)*bh/ah
    for key,group in groups.items():
        n=nodes[key];x,y,w,h=n['box']
        if n.get('kind')=='decoration':
            xx,yy=point(group,x,y);rx,ry=point(group,x+w,y+h)
            n['box']=[round(xx,1),round(yy,1),round(rx-xx,1),round(ry-yy,1)]
        else:
            cx,cy=point(group,x+w/2,y+h/2)
            n['box']=[round(cx-w/2,1),round(cy-h/2,1),w,h]
    for e in g['edges']:
        group=groups.get(e['source'])
        if group and group==groups.get(e['target']) and 'points' in e:
            e['points']=[[round(v,1) for v in point(group,x,y)] for x,y in e['points']]
    for key in ['title','subtitle','defaults']:
        nodes[key]['style']+='align=left;spacingLeft=8;'
