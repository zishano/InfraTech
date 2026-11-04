"""Compact visual hierarchy for the source-verified operator graphs."""

PALETTE={
 'blue':('#536bd9','#f1f4ff'), 'green':('#63962e','#f4f8ed'),
 'orange':('#ce8220','#fff7e9'), 'teal':('#258b82','#eef8f6'),
 'red':('#cd545d','#fff1f2'), 'neutral':('#64748b','#f8fafc')}

def polish(g,kind):
    scale=.6
    g['width']=round(g['width']*scale);g['height']=round(g['height']*scale)
    nodes={n['id']:n for n in g['nodes']}
    original_boxes={k:list(n['box']) for k,n in nodes.items()}
    for e in g['edges']:
        if 'points' in e:e['points']=[[round(x*scale,2),round(y*scale,2)] for x,y in e['points']]
    for n in g['nodes']:
        key=n['id'];label=n['label'];x,y,w,h=n['box']
        if kind=='overview' and key in ['attn_oa','attn_ob']:
            label=label.split('\n')[0];n['label']=label
        x,y,w,h=[v*scale for v in [x,y,w,h]]
        decorative=n.get('kind')=='decoration'
        frame=decorative and not label
        if kind=='overview':
            hue=('blue' if key.startswith(('hc_','main_','mtp_')) else
                 'green' if key.startswith(('idx_','expert_')) else
                 'orange' if key.startswith(('attn_','csa_')) else
                 'teal' if key.startswith(('hca_','moe_')) else 'neutral')
        else:
            hue=('green' if key.startswith(('idx_','hist_')) or key=='port_I' else
                 ('orange' if kind=='csa' else 'teal') if key.startswith('attn_') else 'blue')
        if key in ['middle_title','indexer_heading']:hue='green'
        if key=='attention_heading':hue='orange'
        if key=='moe_heading':hue='teal'
        if key in ['mhc_heading','main_heading','compress_heading','mtp_heading']:hue='blue'
        if key=='attention_title':hue='orange' if kind=='csa' else 'teal'
        if 'cache' in label.lower() and key!='comp_write':hue='red'
        stroke,fill=PALETTE[hue]
        font=15 if kind!='overview' else 14
        # Compact blocks: retain center/branch positions, remove oversized bars.
        if not decorative:
            lines=label.split('\n')
            ideal=max(len(s) for s in lines)*font*.55+28
            nw=round(min(w,max(92,ideal))/2)*2;nh=round(max(30,len(lines)*font*1.15+14)/2)*2
            while font>10 and max(len(s) for s in lines)*font*.64+16>nw:font-=1
            if label in ['+','×']:nw=nh=30
            n['box']=[round(x+(w-nw)/2,2),round(y+(h-nh)/2,2),round(nw,2),round(nh,2)]
            n['style']=(f'rounded=1;arcSize=12;absoluteArcSize=1;whiteSpace=wrap;html=0;'
              f'fontFamily=Arial;fontSize={font};fontColor=#203148;align=center;verticalAlign=middle;'
              f'spacing=5;strokeColor={stroke};strokeWidth=1.2;fillColor={fill};')
            if label in ['+','×']:n['style']+=f'shape=ellipse;perimeter=ellipsePerimeter;fontSize=18;fontStyle=1;fillColor={fill};'
            if key.startswith('port_') or key in ['attn_A','attn_I','idx_q_input']:
                n['style']+='dashed=1;dashPattern=3 3;'
        else:
            n['box']=[round(v,2) for v in [x,y,w,h]]
            if frame:
                n['style']='rounded=1;arcSize=18;absoluteArcSize=1;fillColor=none;strokeColor=#cbd5e1;strokeWidth=1;dashed=1;dashPattern=5 4;'
            else:
                font=22 if key=='title' else 14 if key.endswith(('_title','_heading')) else 12
                while font>9 and font*1.25+8>h:font-=1
                bold=1 if key=='title' or key.endswith(('_title','_heading')) else 0
                n['style']=(f'rounded=0;whiteSpace=wrap;html=0;fontFamily=Arial;fontSize={font};'
                  f'fontColor={stroke if bold else "#64748b"};fontStyle={bold};align=center;verticalAlign=middle;'
                  f'spacing=2;strokeColor=none;fillColor=none;')
                if key=='title':n['style']+='fontColor=#18273e;'
        if key=='hc_note':n['label']=''
        if key in ['attn_core','attn_gather','idx_topk','comp_sum']:
            n['style']+=f'fillColor={stroke};fontColor=#ffffff;fontStyle=1;'
        # Overview statistics are annotations, not network operations.
        if key in ['defaults','facts']:
            n['kind']='decoration'
            n['style']='html=0;whiteSpace=wrap;fontFamily=Arial;fontSize=14;fontColor=#64748b;align=center;verticalAlign=middle;spacing=3;fillColor=none;strokeColor=none;'
            n['box']=[x,y,w,h]
    # Waypoints on the original side center remain on the new center. Fix roundoff.
    for e in g['edges']:
        if 'points' not in e:continue
        for endpoint,which in [('source',0),('target',-1)]:
            old=original_boxes[e[endpoint]];new=nodes[e[endpoint]]['box']
            ox,oy,ow,oh=old
            px,py=e['points'][which]
            if abs(py-(oy+oh/2)*scale)<.2:e['points'][which][1]=round(new[1]+new[3]/2,2)
    for e in g['edges']:
        if (e['source'],e['target']) in [('idx_q_ready','idx_dot'),('moe_x','moe_shared')]:
            a=nodes[e['source']]['box'];b=nodes[e['target']]['box']
            sx=a[0]+a[2]/2;tx=b[0]+b[2]/2
            bus=b[1]+b[3]+16 if e['source']=='idx_q_ready' else a[1]-14
            e['ports']=[.5,0,.5,1]
            e['points']=[[sx,bus],[tx,bus]]
    if kind!='overview':tensor_inset(g,kind,nodes)
    g['presentation']['style']='compact operator chains; restrained module accents; tensor/state insets; bottom-up'
    from deepseek_page_reflow import reflow
    return reflow(g,kind)


def tensor_inset(g,kind,nodes):
    """Native tensor cells, not a raster; illustrative temporal-buffer view."""
    def annotation(key,label,box,font=13):
        n=nodes[key];n['label']=label;n['box']=box;n['kind']='decoration'
        n['style']=f'html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={font};fontColor=#536580;align=center;verticalAlign=middle;spacing=3;fillColor=none;strokeColor=none;'
    def cell(key,x,y,w,h,fill,stroke='#8d9cbb',label=''):
        g['nodes'].append(dict(id=key,label=label,box=[x,y,w,h],kind='decoration',status='inferred',
          style=f'rounded=0;html=0;fontFamily=Arial;fontSize=12;fontColor=#43536b;align=center;verticalAlign=middle;spacing=2;fillColor={fill};strokeColor={stroke};strokeWidth=1;'))
    annotation('state_shapes','kv_state / score_state\n'+('[8,1024]' if kind=='csa' else '[128,512]'),[60,1670,350,48])
    annotation('state_prefill','Prefill → keep partial window',[60,1850,350,34])
    annotation('state_decode','Decode → emit every '+('4' if kind=='csa' else '128')+' tokens',[1790,1670,490,34])
    annotation('state_window1','Previous raw window [4,1024]' if kind=='csa' else 'Window j: tokens 0…127',[610,1665,410,34])
    annotation('state_window2','Current raw window [4,1024]' if kind=='csa' else 'Window j+1: tokens 128…255',[1110,1665,410,34])
    annotation('state_move','Cat (previous Ca, current Cb)' if kind=='csa' else 'Separate 128-token windows',[820,1910,500,34])
    # Buffer strip and decode cadence.
    for i in range(8):cell(f'buffer_cell_{i}',105+30*i,1750,26,28,'#e3e9ff')
    for i in range(4):
        cell(f'decode_cell_{i}',1820+105*i,1750,85,40,'#eef2ff' if i<3 else '#e6f3e3',label=str(i) if kind=='csa' else str([31,63,95,127][i]))
    cell('decode_caption',1810,1820,440,40,'none','none','update → update → update → emit')
    if kind=='csa':
        for group,x in [('previous',700),('current',1200)]:
            for row in range(2):
                for col in range(4):
                    active=(group=='previous' and row==0) or (group=='current' and row==1)
                    color=('#dce4ff' if row==0 else '#f6dce1') if active else '#f5f7fa'
                    cell(f'{group}_{row}_{col}',x+45*col,1720+38*row,40,32,color)
            cell(group+'_ca',x-65,1720,58,32,'none','none','Ca')
            cell(group+'_cb',x-65,1758,58,32,'none','none','Cb')
        for i in range(8):cell(f'cat_cell_{i}',870+45*i,1850,40,32,'#dce4ff' if i<4 else '#f6dce1')
        cell('previous_connector',750,1810,100,20,'none','none','select Ca')
        cell('current_connector',1230,1810,100,20,'none','none','select Cb')
        g['edges'].extend([
          dict(id='state_select_ca',source='previous_0_3',target='cat_cell_1',ports=[1,.5,.5,0],points=[[930,1736],[930,1825],[935,1825]],dashed=True,role='state_illustration'),
          dict(id='state_select_cb',source='current_1_0',target='cat_cell_6',ports=[0,.5,.5,0],points=[[1170,1774],[1170,1825],[1160,1825]],dashed=True,role='state_illustration')])
    else:
        for group,x in [('previous',650),('current',1150)]:
            for i in range(8):cell(f'{group}_slot_{i}',x+42*i,1730,36,48,'#e1f2ef')
            cell(group+'_ellipsis',x+125,1800,120,32,'none','none','… 128 slots …')
        cell('hca_overlap_caption',830,1850,480,34,'none','none','No overlap · one KV vector per window')
