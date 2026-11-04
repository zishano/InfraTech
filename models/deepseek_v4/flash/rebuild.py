"""Rebuild overview and detailed native pages; export PNG from each XML."""
from pathlib import Path
import sys
import copy
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/model_architecture'))
from model_architecture import read,drawio

def rebuild():
    folder=Path(__file__).parent
    names=['deepseek_v4_flash','deepseek_v4_flash_csa','deepseek_v4_flash_hca']
    notes=['# 算子图详细说明','', '图上仅保留算子；下列说明来自相同 graph JSON，保留完整语义与来源。','']
    for name in names:
        graph=read(ROOT/'tools/model_architecture/examples'/f'{name}.graph.json')
        drawio(graph,folder/f'{name}.drawio')
        notes.extend(['## '+name,''])
        for node in graph['nodes']:
            if not node.get('description'):continue
            notes.extend(['### '+node['id']+' — '+node['label'].replace('\n',' / '),'',node['description'],''])
            for item in node.get('evidence',[]):
                notes.extend(['- ['+item['locator']+']('+graph['sources'][item['source']]+')',''])
    (folder/'operator_notes.md').write_text('\n'.join(notes)+'\n')
    target=folder/f'{names[0]}.drawio'
    root=ET.parse(target).getroot()
    root.find('diagram').set('name','Overview')
    for name,label in zip(names[1:],['CSA detail','HCA detail']):
        page=copy.deepcopy(ET.parse(folder/f'{name}.drawio').getroot().find('diagram'))
        page.set('id',name);page.set('name',label);root.append(page)
    ET.ElementTree(root).write(target,encoding='utf-8',xml_declaration=True)

if __name__=='__main__':rebuild()
