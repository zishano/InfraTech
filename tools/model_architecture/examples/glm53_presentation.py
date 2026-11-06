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
    g['presentation_policy'].update(reference='Kimi-K3.1-Pro architecture layout and neutral module palette',
        layout='DSA detail left; decoder backbone center; Indexer / MoE right; sharing and auxiliary details below',
        palette=PALETTE,scope='Presentation only: no Kimi operators, dimensions or version-diff claims imported.')
    return g
