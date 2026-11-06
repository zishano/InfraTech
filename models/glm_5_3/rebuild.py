"""Build native XML and evidence; PNG must be exported from this XML."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/model_architecture'))
from model_architecture import read,drawio
if __name__=='__main__':
    g=read(ROOT/'tools/model_architecture/examples/glm53.graph.json');out=Path(__file__).parent
    drawio(g,out/'glm_5_3_architecture.drawio')
    text=['# GLM-5.3 节点证据','']
    for n in g['nodes']:
        if not n['label']:continue
        text.extend(['## '+n['id'],'',n['label'],''])
        for e in n.get('evidence',[]):text.extend(['- ['+e['locator']+']('+g['sources'][e['source']]+')',''])
    text.extend(['## 限制','']+g['limitations'])
    (out/'evidence.md').write_text('\n'.join(text)+'\n')
