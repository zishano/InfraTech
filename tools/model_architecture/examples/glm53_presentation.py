"""Kimi-K3.1-Pro visual reference, applied only to reviewed GLM-5.3 topology."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model_architecture import parse_style
PALETTE=dict(header='#59718f',fill='#f3f6fb',stroke='#8e9db0',text='#26384c',title='#435671')

def present(g):
    ns={n['id']:n for n in g['nodes']}
    def lane(key):
        if key.startswith('main_') or key.startswith('decoder_repeat_') or key in ('backbone','backbone_title'):return 990
        if key.startswith('attn_') or key in ('attention','attention_title'):return -430
        if key.startswith(('idx_','moe_')) or key in ('indexer','indexer_title','index_scope','moe'):return 10
        return 0
    for n in g['nodes']:
        dx=lane(n['id']);n['box'][0]+=dx
        if 'operator_layout' in n:
            n['operator_layout']['lane_center'][0]+=dx
            n['operator_layout']['reserved_slot'][0]+=dx
        s=parse_style(n['style'])
        filled=s.get('fillColor','none')!='none'
        s.update(fontColor=PALETTE['text'],fontFamily='Arial')
        if filled:s.update(fillColor=PALETTE['fill'],strokeColor=PALETTE['stroke'],strokeWidth='1')
        elif s.get('strokeColor','none')!='none':s['strokeColor']='#c3cedb'
        if n['id']=='title':s['fontColor']=PALETTE['title']
        if n['id']=='facts':s.update(fillColor=PALETTE['fill'],strokeColor=PALETTE['stroke'])
        if n['id']=='decoder_repeat_frame':s.update(strokeColor=PALETTE['header'],strokeWidth='1.5',rounded='0')
        if n['id']=='decoder_repeat_count':s['fontColor']=PALETTE['header']
        n['style']=';'.join(f'{k}={v}' for k,v in s.items())+';'
    for edge in g['edges']:
        dx=lane(edge['source'])
        assert dx==lane(edge['target']), 'Cross-lane edge requires explicit review'
        if 'points' in edge:edge['points']=[[x+dx,y] for x,y in edge['points']]
        if edge.get('color'):edge['color']=PALETTE['header']
    # Full-width dark title strips sit within unfilled panel frames.
    headers={'backbone_title':'backbone','attention_title':'attention','indexer_title':'indexer',
             'moe_title':'moe','mlp_title':'mlp','aux_title':'aux','sharing_title':'sharing'}
    for heading,panel in headers.items():
        n=ns[heading];x,y,w,h=ns[panel]['box'];n['box']=[x+10,y+10,w-20,48]
        s=parse_style(n['style']);s.update(fillColor=PALETTE['header'],strokeColor='none',fontColor='#ffffff',fontStyle='1',fontSize='26',rounded='1')
        n['style']=';'.join(f'{k}={v}' for k,v in s.items())+';'
    # Shorten the central forward chain and embed IndexShare beneath it.
    def place(key,box):
        n=ns[key];n['box']=box
        if 'operator_layout' in n:
            n['operator_layout']['lane_center']=[box[0]+box[2]/2,box[1]+box[3]/2]
            n['operator_layout']['reserved_slot']=list(box)
    for key,y in {'main_out':310,'main_head':390,'main_norm':495,
                  'main_add2':600,'main_ffn':685,'main_n2':780,'main_add1':855,
                  'main_attn':935,'main_n1':1030,'main_x':1100,
                  'main_embed':1195,'main_tokens':1300}.items():
        x,_,w,h=ns[key]['box'];place(key,[x,y,w,h])
    place('decoder_repeat_frame',[1040,575,360,595])
    place('decoder_repeat_count',[1050,579,100,42])
    place('main_config',[1050,1360,340,90])
    ns['main_config']['style']+='fontSize=17;'
    place('sharing',[1030,1465,380,510])
    place('sharing_title',[1040,1475,360,40])
    ns['sharing_title']['label']='IndexShare · 21 FULL /57 SHARED'
    ns['sharing_title']['style']+='fontSize=18;'
    for i,y in enumerate([1740,1670,1600,1530]):
        n=ns[f'share_stage_{i}'];place(n['id'],[1050,y,340,44])
        n['label']=f'L{i+2} '+('FULL · compute J₂' if i==0 else 'SHARED · reuse J₂')
        n['style']+='fontSize=18;'
    place('sharing_note',[1040,1810,360,110])
    ns['sharing_note']['label']='FULL: L0,L1,L2,L6,…,L74\nSame query; share positions J\nEach layer keeps its own KV'
    ns['sharing_note']['style']+='fontSize=16;'
    for e in g['edges']:
        if e['id']=='e_main_x__main_add1':e['points']=[[1060,1122],[1060,877]]
        if e['id']=='e_main_add1__main_add2':e['points']=[[1380,877],[1380,622]]
        if e.get('role')=='index_share_illustration':e['ports']=[.5,0,.5,1]
    # The former full-width sharing strip is gone; bring the bottom panels up.
    for n in g['nodes']:
        if n['box'][1]>=2400:
            n['box'][1]-=390
            if 'operator_layout' in n:
                n['operator_layout']['lane_center'][1]-=390
                n['operator_layout']['reserved_slot'][1]-=390
    for e in g['edges']:
        if 'points' in e:e['points']=[[x,y-390 if y>=2400 else y] for x,y in e['points']]
    g['height']-=390
    g['presentation_policy'].update(reference='Kimi-K3.1-Pro architecture layout and neutral module palette',
        layout='DSA detail left; compact decoder + integrated IndexShare center; Indexer / MoE right; FFN and auxiliary details below',
        palette=PALETTE,scope='Presentation only: no Kimi operators, dimensions or version-diff claims imported.')
    return g
