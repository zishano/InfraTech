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
    for name in names:
        drawio(read(ROOT/'tools/model_architecture/examples'/f'{name}.graph.json'),folder/f'{name}.drawio')
    target=folder/f'{names[0]}.drawio'
    root=ET.parse(target).getroot()
    root.find('diagram').set('name','Overview')
    for name,label in zip(names[1:],['CSA detail','HCA detail']):
        page=copy.deepcopy(ET.parse(folder/f'{name}.drawio').getroot().find('diagram'))
        page.set('id',name);page.set('name',label);root.append(page)
    ET.ElementTree(root).write(target,encoding='utf-8',xml_declaration=True)

if __name__=='__main__':rebuild()
