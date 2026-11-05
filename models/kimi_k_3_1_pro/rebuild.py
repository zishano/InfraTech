"""Rebuild native draw.io and node evidence; PNG must be a direct XML export."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/model_architecture'))
from model_architecture import drawio,read

def rebuild():
    folder=Path(__file__).parent
    g=read(ROOT/'tools/model_architecture/examples/kimi_k31_pro.graph.json')
    drawio(g,folder/'kimi_k31_pro_architecture.drawio')
    lines=['# Kimi-K3.1-Pro 节点与来源','', '颜色分类由官方模型卡、配置差异和固定推理源码人工核对；配置项删除不自动表示模型算子删除。','']
    for n in g['nodes']:
        if not n['label']:continue
        lines.extend(['## '+n['id']+' ['+n.get('change','unchanged')+']','',n['label'],''])
        if n.get('description') and n['description']!=n['label']:
            lines.extend(['K3 图中原注释：'+n['description'],''])
        for e in n.get('evidence',[]):lines.extend(['- ['+e['locator']+']('+g['sources'][e['source']]+')',''])
    (folder/'evidence.md').write_text('\n'.join(lines)+'\n')
    (folder/'architecture_diff.json').write_text(json.dumps(dict(comparison=g['comparison'],changed_nodes=[dict(id=n['id'],change=n['change'],label=n['label'],active=n['id'] not in g['comparison']['retired_nodes']) for n in g['nodes'] if n.get('change')!='unchanged'],limitations=g['limitations']),ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':rebuild()
