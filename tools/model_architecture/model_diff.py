"""Reusable config comparison and source-reviewed architecture diff colors.

A config deletion is not automatically a removed neural-network operation.
Topology classifications must cite a model card or implementation.
"""
import copy

DIFF_THEMES={
    'added':dict(stroke='#c62828',text='#b71c1c',fill='#fff1f0'),
    'removed':dict(stroke='#2e7d32',text='#1b5e20',fill='#edf7ee'),
    'parameter_changed':dict(stroke='#d39b12',text='#8a6500',fill='#fff8d9'),
}

def compare_configs(before,after,path=''):
    out=[]
    if isinstance(before,dict) and isinstance(after,dict):
        for key in sorted(before.keys()|after.keys()):
            ptr=path+'/'+str(key).replace('~','~0').replace('/','~1')
            if key not in before:out.append(dict(path=ptr,kind='added',after=copy.deepcopy(after[key])))
            elif key not in after:out.append(dict(path=ptr,kind='removed',before=copy.deepcopy(before[key])))
            else:out.extend(compare_configs(before[key],after[key],ptr))
    elif before!=after:out.append(dict(path=path,kind='changed',before=copy.deepcopy(before),after=copy.deepcopy(after)))
    return out

def mark(node,change,*,locator,source):
    if change not in DIFF_THEMES:raise ValueError('Unknown architecture change: '+change)
    t=DIFF_THEMES[change]
    node['change']=change
    node['style']=node.get('style','')+f"strokeColor={t['stroke']};fontColor={t['text']};fillColor={t['fill']};strokeWidth=2;"
    node['status']='verified'
    node.setdefault('evidence',[]).append(dict(source=source,locator=locator))
    return node
