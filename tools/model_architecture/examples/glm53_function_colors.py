"""Explicit functional palette for the reviewed GLM graph; no topology changes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model_architecture import parse_style
FUNCTION_COLORS={
 'projection':dict(label='Projection',fill='#eaf2ff',stroke='#6c91c9',text='#294f80'),
 'normalization':dict(label='Normalization',fill='#f1eafb',stroke='#9b82be',text='#604780'),
 'position':dict(label='RoPE / position',fill='#e6f6fb',stroke='#6aa6b9',text='#326a7d'),
 'attention':dict(label='Attention',fill='#fff0df',stroke='#c49358',text='#875c26'),
 'selection':dict(label='Index / select',fill='#eaf6ed',stroke='#78a485',text='#426b4e'),
 'cache':dict(label='Cache',fill='#fbecef',stroke='#c28a96',text='#895a67'),
 'routing':dict(label='MoE routing',fill='#fff5d9',stroke='#bda05c',text='#806a31'),
 'expert':dict(label='FFN / experts',fill='#e5f5f3',stroke='#6baba4',text='#386f69'),
 'elementwise':dict(label='Activation / merge',fill='#f8ebf5',stroke='#b18da9',text='#805b77'),
 'tensor':dict(label='Tensor / layout',fill='#f2f4f7',stroke='#9aa6b4',text='#526171'),
}
ROLE_NODES={
 'projection':'main_head attn_qa attn_qup attn_kvdown attn_expand attn_o idx_qp idx_kp idx_wp mlp_gate mlp_up mlp_down mtp_projection',
 'normalization':'main_n1 main_n2 main_norm attn_qnorm attn_kvnorm idx_kn mtp_norms mtp_headnorm',
 'position':'attn_qrope attn_kvrope idx_qrpe idx_krpe',
 'attention':'main_attn attn_core mtp_block',
 'selection':'attn_indices idx_dot idx_sum idx_mask idx_topk share_stage_0 share_stage_1 share_stage_2 share_stage_3',
 'cache':'attn_cache idx_cache',
 'routing':'moe_router moe_choice moe_weights',
 'expert':'main_ffn moe_experts moe_shared',
 'elementwise':'main_add1 main_add2 moe_add moe_weighted mlp_silu mlp_mul idx_relu idx_scale',
}

def present(g):
    ns={n['id']:n for n in g['nodes']}
    roles={key:role for role,keys in ROLE_NODES.items() for key in keys.split()}
    def style(n,**values):
        s=parse_style(n['style']);s.update(values);n['style']=';'.join(f'{k}={v}' for k,v in s.items())+';'
    for n in g['nodes']:
        role=roles.get(n['id'])
        if role is None and n.get('kind')!='decoration':role='tensor'
        if role:
            n['functional_role']=role;c=FUNCTION_COLORS[role]
            style(n,fillColor=c['fill'],strokeColor=c['stroke'],fontColor=c['text'])
    for key,color in {'attention_title':'#a7773e','indexer_title':'#527d5d','sharing_title':'#527d5d',
                       'moe_title':'#3f7e78','mlp_title':'#3f7e78'}.items():
        style(ns[key],fillColor=color,fontColor='#ffffff')
    # A compact legend after the existing panels; no standalone tensor-shape table.
    ns['footer']['box'][1]+=140;g['height']+=140
    base=dict(kind='decoration',status='verified',evidence=[dict(source='config',locator='Presentation legend only; functional categories of reviewed model operators')])
    def legend(key,label,box,fill='none',stroke='none',text='#526171',font=18):
        g['nodes'].append(dict(base,id=key,label=label,box=box,
          style=f'rounded=1;html=0;whiteSpace=wrap;fontFamily=Arial;fontSize={font};align=center;verticalAlign=middle;spacing=6;fillColor={fill};strokeColor={stroke};fontColor={text};'))
    legend('functional_legend_title','Function color key',[40,2590,2320,34],font=21)
    for i,(role,c) in enumerate(FUNCTION_COLORS.items()):
        legend('functional_legend_'+role,c['label'],[50+230*i,2635,220,44],c['fill'],c['stroke'],c['text'])
    g['presentation_policy']['functional_palette']=FUNCTION_COLORS
    g['presentation_policy']['color_meaning']='Operator function; current model overview, not a version-diff classification.'
    return g
