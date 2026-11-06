"""Size operator boxes by text and visual role while preserving lane centers.

Roles affect presentation only; they do not establish model semantics. Model
builders may explicitly mark composite operations instead of inferring them
from name length. Actual font/layout measurements remain the exporter's job.
"""
import math
import re

PROFILES={
 'primitive':(108,44,12),
 'projection':(180,60,16),
 'aggregation':(170,52,16),
 'cache':(190,64,18),
 'composite':(260,60,20),
 'interface':(100,42,12),
}

def text_width(text,font):
    """Conservative Arial-like estimate; never replaces browser measurement."""
    units=0
    for char in text:
        if ord(char)>0x2e7f:units+=1
        elif char in 'ilI.,:;!| ':units+=.3
        elif char in 'MW@%':units+=.9
        elif ord(char)>127:units+=.65
        elif char.isupper():units+=.66
        else:units+=.55
    return units*font

def infer_role(label):
    low=label.lower()
    if 'cache' in low:return 'cache'
    if 'linear' in low:return 'projection'
    if any(word in low for word in ['matmul','sum','concat','topk','split']):return 'aggregation'
    if any(word in low for word in ['norm','relu','silu','sigmoid','rope','mask']):return 'primitive'
    return 'interface'

def fit_operators(graph,roles=None,font=20):
    roles=roles or {}
    centers={n['id']:n['box'][0]+n['box'][2]/2 for n in graph['nodes']}
    children={}
    for edge in graph['edges']:children.setdefault(edge['source'],[]).append(edge['target'])
    for node in graph['nodes']:
        if node.get('kind')=='decoration' or not node.get('label'):continue
        if node['label'] in ['+','×']:continue
        x,y,w,h=node['box'];cx=x+w/2;cy=y+h/2
        role=roles.get(node['id'],infer_role(node['label']))
        if role not in PROFILES:raise ValueError('Unknown visual operator role: '+role)
        minimum,base_height,pad=PROFILES[role]
        lines=node['label'].split('\n')
        size=font
        # First adapt width to content. The builder's reserved lane limits growth.
        desired=max(minimum,max(text_width(line,size) for line in lines)+2*pad)
        branch=children.get(node['id'],[])
        if len(branch)>1 and role in ['interface','aggregation','composite']:
            spread=max(abs(centers[k]-cx) for k in branch)
            desired=max(desired,2*spread+2*pad)
        new_width=min(w,math.ceil(min(w,desired)/4)*4)
        # Break at explicit spaces before reducing type size in a narrow lane.
        expanded=[]
        for line in lines:
            words=line.split(' ')
            current=''
            for word in words:
                candidate=(current+' '+word).strip()
                if current and text_width(candidate,size)+2*pad>new_width:
                    expanded.append(current);current=word
                else:current=candidate
            expanded.append(current)
        lines=expanded
        while size>16 and max(text_width(line,size) for line in lines)+2*pad>new_width:size-=2
        new_height=math.ceil(max(base_height,len(lines)*size*1.2+20)/4)*4
        node['label']='\n'.join(lines)
        node['box']=[cx-new_width/2,cy-new_height/2,new_width,new_height]
        node['style']=re.sub(r'fontSize=[^;]+;','',node.get('style',''))+f'fontSize={size};spacing=6;'
        node['operator_layout']=dict(role=role,reserved_slot=[x,y,w,h],lane_center=[cx,cy],
             text_lines=len(lines),sizing='content + visual role + branch span + readable font')
    graph['presentation_policy']=dict(operator_sizing='text length and visual complexity',alignment='preserve lane centers and branch rows',font='consistent body size; wrap before shrinking')
    return graph
