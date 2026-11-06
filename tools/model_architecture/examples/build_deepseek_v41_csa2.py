"""CSA2 compressor, indexer, source modes and hierarchical block candidates."""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parent))
from build_deepseek_v41_flash import Diagram,OUT,drawio

def build():
 d=Diagram('DeepSeek-V4.1-Flash — CSA2 detailed dataflow',3000,2690)
 d.note('title','DeepSeek-V4.1-Flash  |  CSA2: compressor · hierarchical indexer · cross-layer reuse',30,10,2940,75,36)
 d.note('symbols','B=batch · S=query length · Tg=floor(T/r) · r=2 at sources2/8/14, r=1 at source20 · I=shared index K · C=candidates',30,100,2940,50,20,source='config')
 d.panel('compressor','Full mode — main KV compressor',30,180,880,1760,'#a7773e')
 d.panel('indexer','Full / Reindex — three-path indexer',940,180,1280,1760,'#527d5d')
 d.panel('modes','Source ownership / reuse',2250,180,720,1760)
 d.panel('candidates','Hierarchical candidate blocks — decoder L20 → L24 /28 /32 /36',30,1980,2940,660,'#527d5d')
 # r=2: independent KV values and gates, softmax over the two token slots per channel.
 for key,text,cx,y,w,role in [
 ('c_input','Source-layer attention input h',450,1830,730,'tensor'),
 ('c_wkv','Linear Wkv\n5120→512',240,1710,270,'projection'),('c_wgate','Linear Wgate · r=2 only\n5120→512',660,1710,330,'projection'),
 ('c_values','Group values: r=2 slots',240,1590,300,'tensor'),('c_scores','Group gate scores: r=2 slots',660,1590,350,'tensor'),('c_softmax','Softmax over token slots\nindependent per channel',660,1470,350,'selection'),('c_product','gate × KV values',450,1350,340,'elementwise'),('c_sum','Sum over2 token slots',450,1230,350,'elementwise'),
 ('c_norm','RMSNorm512',450,1110,250,'normalization'),('c_latent','Pre-RoPE latent L\nindex K is generated first',450,990,390,'tensor'),('c_rope','RoPE tail64\ngroup position = j×r',450,870,330,'position'),('c_fp4','FP4 Q/DQ · E2M1\nblock16, E4M3 scale',450,750,350,'cache'),('c_cache','Shared global KV cache\n[B,Tg,512]',450,630,360,'cache')]:
  d.node(key,text,cx,y,w,role=role,locator='Compressor 429–485; Attention._compress_kv 741–768')
 d.edge('c_input','c_wkv','[B,S,5120]');d.edge('c_input','c_wgate','[B,S,5120]')
 d.chain(['c_wkv','c_values','c_product','c_sum','c_norm','c_latent','c_rope','c_fp4','c_cache'],['[B,S,512]','[B,Tg,2,512]','[B,Tg,2,512]','[B,Tg,512]','[B,Tg,512]','[B,Tg,512]','[B,Tg,512]','[B,Tg,512]'])
 d.chain(['c_wgate','c_scores','c_softmax','c_product'],['[B,S,512]','[B,Tg,2,512]','[B,Tg,2,512]'])
 d.edge('c_wkv','c_norm','r=1 bypass',[0,.5,0,.5],[[65,1742],[65,1133]])
 d.params('compressor_params','HF text_config',['/text_config/kv_source_layer_ids','/text_config/head_dim','/text_config/rms_norm_eps','/text_config/compress_rope_theta'],65,270,780,205,18)
 d.note('compressor_state','r=2 decode: keep partial group; emit only on completion\nr=1: no Wgate / pooling · plain projection + RMSNorm',65,490,780,85,18,locator='Compressor.forward 459–485')
 # Indexer only key-owning Full layers derive K; Reindex receives shared I.
 for key,text,cx,y,w,role in [
 ('i_qr','Qr [1280]',1130,1830,260,'tensor'),('i_latent','L [512] · Full only',1570,1830,320,'tensor'),('i_h','h [5120]',2020,1830,280,'tensor'),
 ('i_wq','Linear Qi\n1280→32×128',1130,1710,300,'projection'),('i_wk','Linear Ki\n512→128',1570,1710,300,'projection'),('i_ww','Linear head weights\n5120→32',2020,1710,330,'projection'),
 ('i_ropeq','RoPE tail64',1130,1590,280,'position'),('i_normk','RMSNorm128',1570,1590,270,'normalization'),('i_scale','Scale 1 /sqrt(32×128)\n=1/64',2020,1590,330,'elementwise'),
 ('i_fp4q','FP4 Q/DQ\nblock32, E8M0 scale',1130,1470,310,'cache'),('i_ropek','RoPE tail64\ngroup position = j×r',1570,1470,330,'position'),('i_fp4k','FP4 Q/DQ\nblock32, E8M0 scale',1570,1350,310,'cache'),
 ('i_q','Qi [B,S,32,128]',1130,1350,300,'tensor'),('i_cache','Shared index K cache I\n[B,Tg,128]',1570,1230,360,'cache'),
 ('i_dot','Dot(Qi,Iᵀ)',1510,1110,760,'selection'),('i_relu','ReLU',1510,990,200,'elementwise'),('i_sum','Multiply head weights → sum\nTP all-reduce',1510,870,610,'selection'),('i_causal','Causal mask: completed groups only',1510,750,620,'selection'),
 ('i_candidate','L20: create C\nLater Reindex: apply shared C mask',1510,630,620,'selection'),('i_top','TopK ≤512',1510,510,350,'selection'),('i_sort','Sort positions → add KV offset\nunreachable positions → -1',1510,390,620,'selection'),('i_j','Publish J for Reuse layers',1510,280,500,'selection')]:
  d.node(key,text,cx,y,w,role=role,locator='Indexer 488–581; attention runtime sharing')
 d.chain(['i_qr','i_wq','i_ropeq','i_fp4q','i_q','i_dot','i_relu','i_sum','i_causal','i_candidate','i_top','i_sort','i_j'],['[B,S,1280]','[B,S,32,128]','[B,S,32,128]','','[B,S,32,128]','[B,S,32,Tg]','[B,S,32,Tg]','[B,S,Tg]','[B,S,Tg]','[B,S,Tg]','[B,S,≤512]','[B,S,≤512]'])
 d.chain(['i_latent','i_wk','i_normk','i_ropek','i_fp4k','i_cache','i_dot'],['[B,Tg,512]','[B,Tg,128]','[B,Tg,128]','[B,Tg,128]','[B,Tg,128]','[B,Tg,128]'])
 d.edge('i_h','i_ww','[B,S,5120]');d.edge('i_ww','i_scale','[B,S,32]');d.edge('i_scale','i_sum','w [B,S,32]',[.5,0,1,.5],[[2020,902]])
 # Ownership examples are explicitly explanatory, not extra layers in the main network.
 d.params('source_params','HF text_config',['/text_config/kv_source_layer_ids','/text_config/index_source_layer_ids','/text_config/index_topk'],2290,265,640,260,18)
 for key,text,y,role in [('mode_full','L20 · Full\nnew global KV, index K and J',1450,'cache'),('mode_reindex','L24 · Reindex\nreuse KV/K; new Qi, weights and J',1150,'selection'),('mode_reuse','L25 · Reuse\nno compressor / indexer; reuse KV,K,J',850,'selection')]:
  d.node(key,text,2610,y,610,90,role=role,kind='decoration',locator='Attention.__init__; _compress_topk_idxs; SharedAttentionRuntime')
 d.edge('mode_full','mode_reindex','L21–23 reuse J20',role='mode_illustration')
 d.edge('mode_reindex','mode_reuse','J24',role='mode_illustration')
 d.note('mode_scope','L0–1: pure SWA\nEncoder: Full L2/L8/L14, r=2\nDecoder: Full L20, r=1\nAll40 layers keep independent SWA128',2290,560,640,190,20,source='config',locator='/text_config/compress_ratios; kv/index source lists')
 d.note('kv_scope','Global decoder KV is projected from\nthe final encoder state at L20 input.\nSWA KV remains layer-specific.\nTopK limits reads, not stored history.',2290,1640,640,220,20,locator='Attention._window_kv / _compress_kv; model card CED')
 # Level-one block max and forced newest block; level-two current-score TopK.
 for key,text,cx,y,w,role in [('b_scores','L20 index scores',460,2500,540,'tensor'),('b_max','Pad -inf → blocks of8\nblock score = max(position scores)',460,2375,730,'selection'),('b_newest','Pin newest visible block\nscore = +inf',460,2250,660,'selection'),('b_top','Top ≤2048 reachable blocks\nexpand to position mask C',460,2110,730,'selection'),
 ('r_score','Current Reindex scores\nfrom own Qi / head weights',2470,2500,780,'tensor'),('r_mask','Apply shared C + causal mask',2470,2375,730,'selection'),('r_top','Top ≤512 positions → sort → J',2470,2250,780,'selection'),('r_output','Fresh J for following Reuse layers',2470,2110,780,'selection')]:
  d.node(key,text,cx,y,w,role=role,locator='select_candidate_blocks 584–611; Indexer.forward 549–581')
 d.chain(['b_scores','b_max','b_newest','b_top'],['[B,S,Tg]','[B,S,ceil(Tg/8)]','[B,S,ceil(Tg/8)]'])
 d.chain(['r_score','r_mask','r_top','r_output'],['[B,S,Tg]','[B,S,Tg]','[B,S,≤512]'])
 d.params('candidate_params','HF text_config',['/text_config/candidate_source_layer_id','/text_config/candidate_topk_blocks','/text_config/candidate_block_size','/text_config/index_topk'],1050,2080,760,230,18)
 d.note('candidate_scope','Candidate cap ≤2048×8 =16384 positions\nCausal / partial blocks handled before selection\nReference: dense scoring → candidate mask',1050,2350,760,220,20,locator='select_candidate_blocks; Indexer.forward: global einsum before mask')
 d.note('footer','Official HF @314113f · FP4 cache/index operations shown as reference Q/DQ · no executed GPU inference / packed cache benchmark',40,2640,2920,40,16)
 d.g['port_bindings']={'L':dict(source='c_latent',target='i_latent',shape=['B','Tg',512],condition='Full owners only; index K produced before main latent is rotated/quantized'), 'C':dict(source='b_top',target='r_mask',shape=['B','S','Tg']), 'I':dict(source='i_cache',target='mode_reindex',shape=['B','Tg',128])}
 return d.finish()
if __name__=='__main__':
 g=build();Path(__file__).with_name('deepseek_v41_flash_csa2.graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n');drawio(g,OUT/'deepseek_v41_flash_csa2.drawio');print(len(g['nodes']),'nodes',len(g['edges']),'edges')
