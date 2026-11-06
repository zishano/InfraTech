"""Rebuild both native diagrams and node evidence; export PNG from each XML next."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/model_architecture/examples'))
from build_deepseek_v41_flash import overview,drawio
from build_deepseek_v41_csa2 import build
if __name__=='__main__':
 out=Path(__file__).parent;lines=['# DeepSeek-V4.1-Flash 节点证据','']
 for stem,name,fn in [('deepseek_v41_flash_architecture','deepseek_v41_flash.graph.json',overview),('deepseek_v41_flash_csa2','deepseek_v41_flash_csa2.graph.json',build)]:
  g=fn();drawio(g,out/(stem+'.drawio'))
  (ROOT/'tools/model_architecture/examples'/name).write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
  lines.extend(['# '+g['title'],''])
  for n in g['nodes']:
   if not n['label']:continue
   lines.extend(['## '+n['id'],'',n['label'],''])
   for e in n.get('evidence',[]):lines.extend(['- ['+e['locator']+']('+g['sources'][e['source']]+')',''])
  lines.extend(['## 核验边界','']+g['limitations']+[''])
 (out/'evidence.md').write_text('\n'.join(lines)+'\n')
