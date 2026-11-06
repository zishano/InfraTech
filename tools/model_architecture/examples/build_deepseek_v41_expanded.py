"""Operator-level counterpart to the architecture overview; explicit residual/control paths."""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parent))
from build_deepseek_v41_flash import Diagram,OUT,drawio

def build():
 d=Diagram('DeepSeek-V4.1-Flash — expanded Block and expert paths',3000,2500)
 d.note('title','DeepSeek-V4.1-Flash  |  Expanded operators: residuals · normalization · routing',30,10,2940,70,36)
 d.note('symbols','Same40-layer model as the overview · B=batch · S=query length · N=B×S · Ne=tokens dispatched to one expert',30,95,2940,50,20)
 d.panel('architecture_map','Whole-model map',30,180,600,2250)
 d.panel('block','One main Block — explicit single-pass mHC',660,180,1250,2250,'#7a6794')
 d.panel('experts','MoE / routed expert — explicit SwiGLU',1940,180,1030,2250,'#3f7e78')
 # Architecture map links to the single shared expansion, not additional model layers.
 rows=[('map_ids','Text / image IDs',2220,'tensor'),('map_embed','Embedding / image-span merge',2090,'projection'),('map_expand','Broadcast HC4',1960,'tensor'),('map_enc','Encoder Block\nL0–19',1700,'attention'),('map_h20','Encoder boundary H20',1530,'tensor'),('map_dec','Decoder Block\nL20–39',1270,'attention'),('map_collapse','HC weighted collapse',1080,'elementwise'),('map_norm','RMSNorm5120',950,'normalization'),('map_head','LM head',820,'projection'),('map_logits','Logits / sample',690,'tensor')]
 for k,t,y,r in rows:d.node(k,t,330,y,480,role=r,locator='Transformer.forward 1240–1276')
 d.chain([x[0] for x in rows],['[B,S]','[B,S,5120]','[B,S,4,5120]','[B,S,4,5120]','[B,S,4,5120]','[B,S,4,5120]','[B,S,5120]','[B,S,5120]','[B,129280]'])
 d.frame('map_encoder',60,1650,540,160,20,['map_enc']);d.frame('map_decoder',60,1220,540,160,20,['map_dec'])
 d.params('map_params','HF text_config',['/text_config/num_hidden_layers','/text_config/hidden_size','/text_config/engram_layer_ids'],65,275,520,190,18)
 d.note('map_scope','Encoder: SWA L0–1, CSA2 r=2 L2–19\nDecoder: CSA2 r=1 L20–39\nBoth use the Block expansion at right.\nCSA2 internals: separate detailed diagram.',65,475,520,170,18)
 # Main Block, one operator per box along the critical path.
 block_rows=[('b_input','Input HC stream',2280,'tensor'),('b_engram','Conditional Engram · L1 /L14',2160,'selection'),('b_pre_a','mHC pre: weighted sum',2020,'elementwise'),('b_norm_a','RMSNorm5120',1910,'normalization'),('b_attention','SWA / CSA2 attention',1800,'attention'),('b_post_a','post × attention output',1680,'elementwise'),('b_add_a','+',1550,'elementwise'),('b_pre_f','mHC pre: weighted sum',1410,'elementwise'),('b_norm_f','RMSNorm5120',1300,'normalization'),('b_moe','MoE',1190,'expert'),('b_post_f','post × FFN output',1030,'elementwise'),('b_add_f','+',940,'elementwise'),('b_output','Output HC stream',690,'tensor')]
 for k,t,y,r in block_rows:d.node(k,t,1630,y,46 if t=='+' else 350,46,role=r,locator='Block.forward 967–996; Engram at Transformer.forward before Block')
 d.chain([x[0] for x in block_rows],['[B,S,4,5120]','[B,S,4,5120]','[B,S,5120]','[B,S,5120]','[B,S,5120]','[B,S,4,5120]','[B,S,4,5120]','[B,S,5120]','[B,S,5120]','[B,S,5120]','[B,S,4,5120]','[B,S,4,5120]'])
 d.node('incoming_pre','prev pre',1830,2110,140,46,role='tensor',font=17,locator='Block.forward pre_mix argument; previous layer FFN output')
 d.edge('incoming_pre','b_pre_a','[B,S,4]')
 # Each sublayer computes pre for the NEXT sublayer, not itself.
 for prefix,ys in [('a',[2120,2020,1930,1850,1750,1630,1550]),('f',[1460,1360,1270,1190,1090,970,900])]:
  flat,linear,scale,split,branches,sink,mix=ys
  d.node(prefix+'_flat','Flatten HC streams',1000,flat,360,46,locator='Block.hc_mixes: flatten(2)')
  d.node(prefix+'_linear','FP32 Linear\n20480→24',900,linear,290,64,'projection',locator='Block.hc_mixes: F.linear')
  d.node(prefix+'_rstd','RMS statistic: rsqrt',1250,linear,300,46,'normalization',locator='Block.hc_mixes: rsqrt(mean(x²)+eps)')
  d.node(prefix+'_scale','×',1000,scale,46,46,'elementwise')
  d.node(prefix+'_split','Split pre4 / post4 / comb16',1000,split,510,46,locator='hc_split_sinkhorn kernel')
  d.node(prefix+'_pre','Sigmoid + eps',800,branches,220,46,'elementwise',locator='hc_split_sinkhorn pre branch')
  d.node(prefix+'_post','2 × Sigmoid',1040,branches,210,46,'elementwise',locator='hc_split_sinkhorn post branch')
  d.node(prefix+'_comb','Softmax',1280,branches,210,46,'selection',locator='hc_split_sinkhorn comb branch')
  d.node(prefix+'_sink','Sinkhorn ×20',1280,sink,230,46,'normalization',locator='hc_split_sinkhorn comb row/column normalization')
  d.node(prefix+'_residual','combᵀ × residual',1280,mix,270,46,'elementwise',locator='Block.hc_post: sum over input stream axis')
  d.edge(prefix+'_flat',prefix+'_linear','[B,S,20480]');d.edge(prefix+'_flat',prefix+'_rstd','[B,S,20480]')
  d.edge(prefix+'_linear',prefix+'_scale','[B,S,24]');d.edge(prefix+'_rstd',prefix+'_scale','[B,S,1]')
  d.edge(prefix+'_scale',prefix+'_split','[B,S,24]')
  for key,cx in [('pre',800),('post',1040),('comb',1280)]:
   affine=prefix+'_'+key+'_affine'
   d.node(affine,'Scale + bias',cx,branches+55,210,34,'projection',font=17,locator='hc_split_sinkhorn: mixes * learned hc_scale + hc_base')
   d.edge(prefix+'_split',affine);d.edge(affine,prefix+'_'+key)
  d.edge(prefix+'_comb',prefix+'_sink','[B,S,4,4]');d.edge(prefix+'_sink',prefix+'_residual','[B,S,4,4]')
 d.edge('b_engram','a_flat','current x')
 d.edge('b_engram','a_residual','residual',[0,.5,0,.5],[[675,2183],[675,1573]])
 d.edge('a_post','b_post_a','[B,S,4]',[.5,0,0,.5],[[1040,1703]])
 d.edge('a_residual','b_add_a','[B,S,4,5120]',[1,.5,0,.5])
 d.edge('a_pre','b_pre_f','pre for FFN',[.5,0,0,.5],[[800,1433]])
 d.edge('b_add_a','f_flat','current x',[0,.5,1,.5],[[1440,1573],[1440,1483]])
 d.edge('b_add_a','f_residual','residual',[1,.5,1,.5],[[1875,1573],[1875,923]])
 d.edge('f_post','b_post_f','[B,S,4]',[.5,0,0,.5],[[1040,1053]])
 d.edge('f_residual','b_add_f','',[.5,1,0,.5],[[1280,963]])
 d.node('next_pre','pre for next Block',800,740,280,46,locator='Block.forward returns ffn_pre')
 d.edge('f_pre','next_pre','[B,S,4]')
 d.frame('block_repeat',680,880,1210,1375,40,[x[0] for x in block_rows[1:-1]]+[p+'_'+x for p in ['a','f'] for x in ['flat','linear','rstd','scale','split','pre','post','comb','sink','residual','pre_affine','post_affine','comb_affine']])
 d.note('block_scope','×40 is the shared Block template: 20 encoder +20 decoder layers.\nEngram and CSA2 modes vary by layer; parameters are not tied.',700,270,1160,95,20,source='config',locator='/text_config/num_hidden_layers; engram_layer_ids; compress_ratios')
 d.params('block_params','HF text_config',['/text_config/hc_mult','/text_config/hc_sinkhorn_iters','/text_config/hc_eps','/text_config/rms_norm_eps'],720,385,1100,210,18)
 # Explicit expert gates, clipping, route-weight placement, and shared branch.
 right=[('r_h','MoE input',2440,2280,900,'tensor'),('r_linear','FP32 Linear\n5120→384',2170,2160,350,'projection'),('r_scores','sqrt(Softplus)',2170,2040,350,'routing'),('r_bias','+ selection bias (text /image)',2170,1920,370,'routing'),('r_top','Top6 expert IDs',2170,1800,350,'routing'),('r_gather','Gather original scores',2170,1680,370,'routing'),('r_norm','Normalize weights ×1.5',2170,1560,370,'routing'),('r_dispatch','Dispatch selected experts',2210,1440,400,'tensor'),('r_gate','Linear gate\n5120→2304',2140,1320,280,'projection'),('r_up','Linear up\n5120→2304',2760,1320,280,'projection'),('r_gclip','Clamp max10',2140,1200,280,'elementwise'),('r_uclip','Clamp [-10,+10]',2760,1200,280,'elementwise'),('r_silu','SiLU',2140,1080,240,'elementwise'),('r_mul','×',2460,960,46,'elementwise'),('r_route','×',2460,840,46,'elementwise'),('r_down','Linear down\n2304→5120',2460,720,360,'projection'),('r_sum','Scatter / sum routed outputs',2460,610,430,'elementwise'),('r_shared','Shared SwiGLU\nno route weight',2820,1680,240,'expert'),('r_add','+',2460,460,46,'elementwise'),('r_output','MoE output',2460,300,320,'tensor')]
 for k,t,cx,y,w,r in right:d.node(k,t,cx,y,w,role=r,locator='Gate / Expert / MoE 794–906',font=19)
 d.chain(['r_h','r_linear','r_scores','r_bias','r_top','r_gather','r_norm','r_dispatch'],['[N,5120]','[N,384]','[N,384]','[N,384]','IDs [N,6]','w [N,6]','IDs / dispatch'])
 d.edge('r_scores','r_gather','raw scores',[0,.5,0,.5],[[1950,2063],[1950,1703]])
 d.edge('r_h','r_dispatch','x',[0,.5,0,.5],[[1960,2303],[1960,1463]])
 d.edge('r_dispatch','r_gate','[Ne,5120]');d.edge('r_dispatch','r_up','[Ne,5120]')
 d.chain(['r_gate','r_gclip','r_silu','r_mul','r_route','r_down','r_sum','r_add','r_output'],['[Ne,2304]','[Ne,2304]','[Ne,2304]','[Ne,2304]','[Ne,2304]','[Ne,5120]','[N,5120]','[N,5120]'])
 d.edge('r_up','r_uclip','[Ne,2304]');d.edge('r_uclip','r_mul','[Ne,2304]')
 d.edge('r_norm','r_route','dispatch w_e',[1,.5,0,.5],[[2410,1583],[2410,863]])
 d.edge('r_h','r_shared','[N,5120]');d.edge('r_shared','r_add','shared',[1,.5,1,.5],[[2950,1712],[2950,483]])
 expert_members=['r_gate','r_up','r_gclip','r_uclip','r_silu','r_mul','r_route','r_down']
 d.frame('expert_repeat',1970,675,950,760,384,expert_members)
 d.params('expert_params','HF text_config',['/text_config/n_routed_experts','/text_config/num_experts_per_tok','/text_config/moe_intermediate_size'],1960,270,320,170,16)
 d.note('footer','Operator expansion of the same official @314113f model · CSA2 dataflow remains in its separate paired detail figure · no new model layers',40,2450,2920,40,16)
 d.g['port_bindings']={'Block':dict(source='map_enc',target='b_input',meaning='Representative expansion; not an extra layer'), 'DecoderBlock':dict(source='map_dec',target='b_input',meaning='Same template with decoder mode and no Engram'), 'previous_pre':dict(source='next_pre',target='incoming_pre',meaning='Previous Block FFN pre is next Block attention pre; same-Block attention pre feeds FFN'), 'MoE':dict(source='b_moe',target='r_h',shape=['B','S',5120])}
 for edge in d.g['edges']:
  if edge['id'] in ['e_a_post__b_post_a','e_f_post__b_post_f']:edge['label_offset']=[-100,0]
  if edge['id']=='e_a_pre__b_pre_f':edge['label_offset']=[350,0]
 d.g['diagram_level']='operator_expansion'
 return d.finish()
if __name__=='__main__':
 g=build();Path(__file__).with_name('deepseek_v41_flash_expanded.graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');drawio(g,OUT/'deepseek_v41_flash_expanded.drawio');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
