"""GLM-5.3: same reviewed base, post-training gains and FP8 release config."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).parent))
from build_glm52 import build as build_reviewed_core
REV='ba32f8c19c8738e2c57c71798c601d477a7bf844'
TF='8833c9181eec925f1b4e0096db516462044345df'
def build():
 out=ROOT/'models/glm_5_3';c=json.loads((out/'official_config.json').read_text());b=json.loads((out/'baseline_glm52_config.json').read_text())
 assert {k:v for k,v in c.items() if k not in ('quantization_config','transformers_version')}=={k:v for k,v in b.items() if k not in ('quantization_config','transformers_version')},'Re-review changed architecture'
 inv=json.loads((out/'source_inventory.json').read_text())
 assert next(x['sha256'] for x in inv if x['id']=='model')=='226f5a24b6aa15eca90bcc74e6bf1e2e887687ccfeb0d1ae28da4bf4c216038f'
 assert next(x['sha256'] for x in inv if x['id']=='framework_config')=='4e0581bbc950f19b2e9cc6e08f300e592f59564b4a34a57b1af670c8ec5bb4dd'
 q=c['quantization_config'];assert (q['quant_method'],q['fmt'],q['weight_block_size'],len(q['modules_to_not_convert']))==('fp8','e4m3',[128,128],541)
 g=build_reviewed_core();g['title']='GLM-5.3 — IndexShare DSA + MoE'
 g['sources']['baseline_index']=g['sources']['index'];del g['sources']['index']
 for k in ('config','card'):g['sources'][k]=f'https://huggingface.co/zai-org/GLM-5.3/blob/{REV}/'+('config.json' if k=='config' else 'README.md')
 for k,name in [('model','modeling_glm_moe_dsa.py'),('framework_config','configuration_glm_moe_dsa.py')]:g['sources'][k]=f'https://github.com/huggingface/transformers/blob/{TF}/src/transformers/models/glm_moe_dsa/{name}'
 for n in g['nodes']:
  for e in n.get('evidence',[]):
   if e['source']=='index':e['source']='baseline_index';e['locator']='GLM-5.2 baseline only; target topology supported by matching config + model card: '+e['locator']
 ns={n['id']:n for n in g['nodes']}
 def edit(k,text):ns[k]['label']=text;ns[k]['description']=text
 edit('title','GLM-5.3  |  IndexShare DSA + Mixture of Experts')
 edit('scope','Official FP8 release @ba32f8c · same base as GLM-5.2 · post-training gains · bottom-up flow')
 edit('aux_scope','FP8 release / deployment config\nE4M3 · dynamic activation\nWeight blocks 128 ×128\n541 exclusions; no extra network branch')
 edit('aux_modules','MTP ×1 — inherited base view; target config verified')
 edit('footer','Sources: GLM-5.3 @ba32f8c · Transformers @8833c91 · same base as 5.2; target weight-index download blocked (see README)')
 ns['aux_scope']['evidence']=[dict(source='config',locator='/quantization_config'),dict(source='card',locator='Introduction: same base model as GLM-5.2; gains from post-training')]
 g['checkpoint']=dict(revision=REV,main_layers=78,auxiliary_layers=1,indexer_mode='config: 21 FULL /57 SHARED',context=1048576,weight_index_verified=False,release_quantization=q)
 g['limitations']=['Official model card states the same base as GLM-5.2; core configuration and pinned implementation match.','GLM-5.3 weight-index download blocked by proxy at official CDN; baseline weight-index citations are explicitly marked and do not verify target weights.','FP8 overlay describes release configuration, not added model operators or a verified backend execution graph.','MTP auxiliary structure inherited from matching config/base; no target tensor-name or backend-iteration verification.','No tensor headers, full weights, GPU inference, benchmark or Feishu import tested.']
 return g
if __name__=='__main__':
 g=build();Path(__file__).with_name('glm53.graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
