# DeepSeek-V4.1-Flash 节点证据

# DeepSeek-V4.1-Flash — CED + CSA2 + Engram + vision

## title

DeepSeek-V4.1-Flash  |  CED · CSA2 · Engram · native vision

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## facts

40 layers =20 encoder +20 decoder · hidden5120 · 384 experts /top6 +1 shared · context1M

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## symbols

B=batch · S=query length · T=history length · Tg=floor(T/r) · N=B×S · all layer IDs are 0-based

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## attention_title

CSA2 — local SWA + shared global K=V

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## backbone_title

Causal encoder → decoder

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## indexer_title

CSA2 Indexer — Full / Reindex layers

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## moe_title

Mixture of Experts — every main layer

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## engram_title

Engram — token-conditioned memory

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## mhc_title

Single-pass mHC — pre / post / comb

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## vision_title

DeepSeek-ViT + image projector

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## dspark_title

DSpark — auxiliary draft path

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## tokens

Text / image token IDs

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## embedding

Embedding

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## merge

Merge image spans ← V

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## expand

Broadcast 4 HC streams

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## enc_engram

Engram only at L1 /L14

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## enc_attn

mHC pre → Norm
SWA / CSA2 (r=2)

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## enc_ffn

mHC post / pre → Norm
MoE

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## enc_post

mHC post
4 residual streams

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## encoder_output

Encoder boundary H20

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## dec_attn

mHC pre → Norm
CSA2 (r=1)

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## dec_ffn

mHC post / pre → Norm
MoE

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## dec_post

mHC post
4 residual streams

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## collapse

mHC collapse + RMSNorm

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## lm_head

LM head · 5120→129280

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## logits

Logits / sample

- [Transformer.forward 1240–1276; Block.forward 967–996; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## encoder_repeat_count

×20

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## decoder_repeat_count

×20

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## backbone_params

checkpoint config
num_hidden_layers = 40
hidden_size = 5120
max_position_embeddings = 1048576

- [/text_config/num_hidden_layers; /text_config/hidden_size; /text_config/max_position_embeddings](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## mode_title

CSA2 layer modes · shared runtime

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## full_modes

Full: L2,L8,L14,L20
new KV + index K + TopK

- [Attention.__init__; SharedAttentionRuntime; config source lists](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## reindex_modes

Reindex: L24,L28,L32,L36
shared KV/K; refresh Q, weights, TopK

- [Attention.__init__; SharedAttentionRuntime; config source lists](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## reuse_modes

Reuse: other L2–39 · share KV/K/TopK
L0–1: SWA only · no global cache

- [Attention.__init__; SharedAttentionRuntime; config source lists](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_h

h [5120]

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_qa

Linear Q↓
5120→1280

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_qn

RMSNorm1280

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_qb

Linear Q↑
1280→64×512

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_qr

RoPE tail64

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_kv

Linear KV
5120→512

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_kn

RMSNorm512

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_kr

RoPE tail64

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_fp8

FP8 Q/DQ
all512 incl. RoPE

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_ring

Local SWA ring
128 ×512

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_global

Global KV · source
r=2 encoder /1 decoder

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_concat

Concat SWA + global KV

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_j

Window IDs + J

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_core

Sparse gather → Attention
shared K=V · attention sink

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_inverse

Inverse RoPE tail64

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_oa

Grouped Oa
8 ×(4096→1024)

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_ob

Linear Ob
8192→5120

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## a_output

Attention output

- [Attention 614–791; sparse_attn kernel 311–404](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## attention_params

HF text_config
q_lora_rank = 1280
head_dim = 512
qk_rope_head_dim = 64
o_groups = 8
o_lora_rank = 1024
sliding_window = 128
compress_rope_theta = 160000

- [/text_config/q_lora_rank; /text_config/head_dim; /text_config/qk_rope_head_dim; /text_config/o_groups; /text_config/o_lora_rank; /text_config/sliding_window; /text_config/compress_rope_theta](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## i_qr

Qr [1280]

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_latent

RoPE-free latent512
Full owners only

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_h

h [5120]

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_qp

Linear Qi
1280→32×128

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_kp

Linear Ki
512→128

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_qrot

RoPE64 → FP4 Q/DQ

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_krot

RMSNorm → RoPE64
FP4 Q/DQ

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_wp

Linear weights
5120→32; scale1/64

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_q

Qi [32,128]

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_cache

Shared index K cache

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_dot

Matmul(Qi,Kiᵀ) → ReLU

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_sum

Weighted head sum + TP reduce

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_mask

Causal visibility mask

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_candidates

L20: select candidate blocks
Later Reindex: apply candidate mask

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_topk

TopK≤512 → position sort
offset / invalid=-1

- [Indexer 488–581; select_candidate_blocks 584–611](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## index_params

HF text_config
index_n_heads = 32
index_head_dim = 128
index_topk = 512
candidate_topk_blocks = 2048
candidate_block_size = 8

- [/text_config/index_n_heads; /text_config/index_head_dim; /text_config/index_topk; /text_config/candidate_topk_blocks; /text_config/candidate_block_size](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## m_h

h [5120]

- [Gate 794–829; Expert 832–853; MoE 856–906](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## m_router

Linear → sqrt(Softplus)
FP32 router

- [Gate 794–829; Expert 832–853; MoE 856–906](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## m_select

+ text / VL bias → Top6

- [Gate 794–829; Expert 832–853; MoE 856–906](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## m_weights

Gather raw scores
normalize → ×1.5

- [Gate 794–829; Expert 832–853; MoE 856–906](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## m_experts

384 experts /6 active
clipped SwiGLU · ×w before Down

- [Gate 794–829; Expert 832–853; MoE 856–906](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## m_sum

Scatter / sum expert outputs

- [Gate 794–829; Expert 832–853; MoE 856–906](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## m_shared

Shared expert ×1
5120→2304→5120

- [Gate 794–829; Expert 832–853; MoE 856–906](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## m_add

+

- [Attention / Block / Transformer.forward](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## moe_params

HF text_config
n_routed_experts = 384
num_experts_per_tok = 6
n_shared_experts = 1
moe_intermediate_size = 2304
scoring_func = sqrtsoftplus
routed_scaling_factor = 1.5
swiglu_limit = 10.0

- [/text_config/n_routed_experts; /text_config/num_experts_per_tok; /text_config/n_shared_experts; /text_config/moe_intermediate_size; /text_config/scoring_func; /text_config/routed_scaling_factor; /text_config/swiglu_limit](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## e_tokens

Text IDs / compressed map

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_hash

2 /3 /4-gram ×8 heads
hash / modulo buckets

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_lookup

Embedding lookup + flatten
24×256 =6144

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_kv

Linear Wkv → split K / V
6144→4×5120 +5120

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_stream

HC stream x

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_dot

Normalized stream·key
per-copy weighted dot

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_gate

Signed sqrt → Sigmoid

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_value

gate × shared value V

- [Engram 328–366; EngramLayout / NgramHashState](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## e_add

+

- [Attention / Block / Transformer.forward](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## engram_params

HF text_config
engram_layer_ids = [1,14]
engram_max_ngram_size = 4
engram_n_heads = 8
engram_head_dim = 256

- [/text_config/engram_layer_ids; /text_config/engram_max_ngram_size; /text_config/engram_n_heads; /text_config/engram_head_dim](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## hc_x

HC stream x

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_flat

Flatten + RMS statistic

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_linear

FP32 Linear
20480→24

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_split

Split pre4 / post4 / comb16

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_pre_new

Sigmoid + eps
new pre

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_post_new

2 × Sigmoid
post

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_comb

Softmax matrix

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_sink

Sinkhorn ×20

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_next

pre → next sublayer

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_prev

Incoming pre
from previous sublayer

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_collapse

Weighted stream sum

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_norm

RMSNorm5120

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_sublayer

Attention / MoE

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_expand

post × output
expand to4 streams

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_resmix

combᵀ × residual

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_out

Updated HC stream

- [Block.hc_mixes/pre/post/forward 909–996; hc_split_sinkhorn kernel](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## hc_add

+

- [Attention / Block / Transformer.forward](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## mhc_params

HF text_config
hc_mult = 4
hc_sinkhorn_iters = 20
hc_eps = 1e-06
rms_norm_eps = 1e-20

- [/text_config/hc_mult; /text_config/hc_sinkhorn_iters; /text_config/hc_eps; /text_config/rms_norm_eps](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## v_patches

Image patches

- [PatchEmbed / ViT / Block / Aligner](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/vision.py)

## v_patch

Linear patch embedding
3×14×14→1024

- [PatchEmbed / ViT / Block / Aligner](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/vision.py)

## v_attn

Norm → 2D-RoPE attention
+ residual

- [PatchEmbed / ViT / Block / Aligner](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/vision.py)

## v_ffn

Norm → SwiGLU
+ residual

- [PatchEmbed / ViT / Block / Aligner](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/vision.py)

## v_norm

RMSNorm1024

- [PatchEmbed / ViT / Block / Aligner](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/vision.py)

## v_unshuffle

3×3 pixel-unshuffle
1024→9216

- [PatchEmbed / ViT / Block / Aligner](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/vision.py)

## v_project

Linear9216→5120
GELU → Linear5120→5120

- [PatchEmbed / ViT / Block / Aligner](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/vision.py)

## vit_repeat_count

×32

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## vision_params

HF vision_config
num_hidden_layers = 32
hidden_size = 1024
num_attention_heads = 16
intermediate_size = 2816
downsample_ratio = 3
max_image_tokens = 1024

- [/vision_config/num_hidden_layers; /vision_config/hidden_size; /vision_config/num_attention_heads; /vision_config/intermediate_size; /vision_config/downsample_ratio; /vision_config/max_image_tokens](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## ds_taps

Mean over HC streams
concat inputs at L37 /38 /39

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_proj

Linear15360→5120
RMSNorm → main_x

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_seed

Seed + noise token embeddings
5 draft positions · broadcast HC4

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_stage

DSpark SWA + single-pass mHC
MoE128 /top3 +1 shared

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_collapse

HC collapse

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_norm

RMSNorm5120

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_head

LM head + Markov rank256
5-position sequential sampling

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_confidence

Confidence Linear
(5120+256)→1

- [DSparkBlock / DSparkAttention / MarkovHead / ConfidenceHead 1023–1159](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## dspark_repeat_count

×3

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## ds_params

dspark_block_size=5 · noise_token_id=128799
dspark_n_routed_experts=128 · top3

- [/text_config/dspark_*](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## footer

Official HF @314113f · 96,085 tensor names /48 shards checked · implementation and deployment limits in README

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/model.safetensors.index.json)

## 核验边界

Official unsuffixed checkpoint, not -1017.
Shapes are logical global dimensions; tensor-parallel ranks may shard heads/experts.
Official minimal implementation loops through all 40 layers; optimized CED prefill, bounded replay and DSpark verification scheduler are model-card designs, not locally executed paths.
Reference quantizers simulate quantize/dequantize in floating cache buffers; packed cache bytes are official claims.
Weight index verifies names, not tensor shapes/values. No full weights, GPU inference, benchmark, numerical equivalence or Feishu import test.
Technical-report PDF download blocked by proxy; card and pinned reference sources were read.

# DeepSeek-V4.1-Flash — CSA2 detailed dataflow

## title

DeepSeek-V4.1-Flash  |  CSA2: compressor · hierarchical indexer · cross-layer reuse

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## symbols

B=batch · S=query length · Tg=floor(T/r) · r=2 at sources2/8/14, r=1 at source20 · I=shared index K · C=candidates

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## compressor_title

Full mode — main KV compressor

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## indexer_title

Full / Reindex — three-path indexer

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## modes_title

Source ownership / reuse

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## candidates_title

Hierarchical candidate blocks — decoder L20 → L24 /28 /32 /36

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_input

Source-layer attention input h

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_wkv

Linear Wkv
5120→512

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_wgate

Linear Wgate · r=2 only
5120→512

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_values

Group values: r=2 slots

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_scores

Group gate scores: r=2 slots

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_softmax

Softmax over token slots
independent per channel

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_product

gate × KV values

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_sum

Sum over2 token slots

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_norm

RMSNorm512

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_latent

Pre-RoPE latent L
index K is generated first

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_rope

RoPE tail64
group position = j×r

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_fp4

FP4 Q/DQ · E2M1
block16, E4M3 scale

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## c_cache

Shared global KV cache
[B,Tg,512]

- [Compressor 429–485; Attention._compress_kv 741–768](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## compressor_params

HF text_config
kv_source_layer_ids = [2,8,14,20]
head_dim = 512
rms_norm_eps = 1e-20
compress_rope_theta = 160000

- [/text_config/kv_source_layer_ids; /text_config/head_dim; /text_config/rms_norm_eps; /text_config/compress_rope_theta](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## compressor_state

r=2 decode: keep partial group; emit only on completion
r=1: no Wgate / pooling · plain projection + RMSNorm

- [Compressor.forward 459–485](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_qr

Qr [1280]

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_latent

L [512] · Full only

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_h

h [5120]

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_wq

Linear Qi
1280→32×128

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_wk

Linear Ki
512→128

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_ww

Linear head weights
5120→32

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_ropeq

RoPE tail64

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_normk

RMSNorm128

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_scale

Scale 1 /sqrt(32×128)
=1/64

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_fp4q

FP4 Q/DQ
block32, E8M0 scale

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_ropek

RoPE tail64
group position = j×r

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_fp4k

FP4 Q/DQ
block32, E8M0 scale

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_q

Qi [B,S,32,128]

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_cache

Shared index K cache I
[B,Tg,128]

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_dot

Dot(Qi,Iᵀ)

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_relu

ReLU

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_sum

Multiply head weights → sum
TP all-reduce

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_causal

Causal mask: completed groups only

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_candidate

L20: create C
Later Reindex: apply shared C mask

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_top

TopK ≤512

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_sort

Sort positions → add KV offset
unreachable positions → -1

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## i_j

Publish J for Reuse layers

- [Indexer 488–581; attention runtime sharing](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## source_params

HF text_config
kv_source_layer_ids = [2,8,14,20]
index_source_layer_ids = [2,8,14,20,24,28,32,36]
index_topk = 512

- [/text_config/kv_source_layer_ids; /text_config/index_source_layer_ids; /text_config/index_topk](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## mode_full

L20 · Full
new global KV, index K and J

- [Attention.__init__; _compress_topk_idxs; SharedAttentionRuntime](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## mode_reindex

L24 · Reindex
reuse KV/K; new Qi, weights and J

- [Attention.__init__; _compress_topk_idxs; SharedAttentionRuntime](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## mode_reuse

L25 · Reuse
no compressor / indexer; reuse KV,K,J

- [Attention.__init__; _compress_topk_idxs; SharedAttentionRuntime](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## mode_scope

L0–1: pure SWA
Encoder: Full L2/L8/L14, r=2
Decoder: Full L20, r=1
All40 layers keep independent SWA128

- [/text_config/compress_ratios; kv/index source lists](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## kv_scope

Global decoder KV is projected from
the final encoder state at L20 input.
SWA KV remains layer-specific.
TopK limits reads, not stored history.

- [Attention._window_kv / _compress_kv; model card CED](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## b_scores

L20 index scores

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## b_max

Pad -inf → blocks of8
block score = max(position scores)

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## b_newest

Pin newest visible block
score = +inf

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## b_top

Top ≤2048 reachable blocks
expand to position mask C

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## r_score

Current Reindex scores
from own Qi / head weights

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## r_mask

Apply shared C + causal mask

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## r_top

Top ≤512 positions → sort → J

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## r_output

Fresh J for following Reuse layers

- [select_candidate_blocks 584–611; Indexer.forward 549–581](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## candidate_params

HF text_config
candidate_source_layer_id = 20
candidate_topk_blocks = 2048
candidate_block_size = 8
index_topk = 512

- [/text_config/candidate_source_layer_id; /text_config/candidate_topk_blocks; /text_config/candidate_block_size; /text_config/index_topk](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)

## candidate_scope

Candidate cap ≤2048×8 =16384 positions
Causal / partial blocks handled before selection
Reference: dense scoring → candidate mask

- [select_candidate_blocks; Indexer.forward: global einsum before mask](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## footer

Official HF @314113f · FP4 cache/index operations shown as reference Q/DQ · no executed GPU inference / packed cache benchmark

- [Reviewed module semantics](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)

## 核验边界

Official unsuffixed checkpoint, not -1017.
Shapes are logical global dimensions; tensor-parallel ranks may shard heads/experts.
Official minimal implementation loops through all 40 layers; optimized CED prefill, bounded replay and DSpark verification scheduler are model-card designs, not locally executed paths.
Reference quantizers simulate quantize/dequantize in floating cache buffers; packed cache bytes are official claims.
Weight index verifies names, not tensor shapes/values. No full weights, GPU inference, benchmark, numerical equivalence or Feishu import test.
Technical-report PDF download blocked by proxy; card and pinned reference sources were read.

