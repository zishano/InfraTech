# GLM-5.3 节点证据

## title

GLM-5.3  |  IndexShare DSA + Mixture of Experts

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## facts

78 layers · hidden 6144 · 64 Q heads · 256 routed / top-8 + 1 shared · context 1M

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## scope

FP8 @ba32f8c · B=batch, S=query, T=KV incl. cache, K=min(2048,T), N=B×S · dimensions label the arrows

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## backbone_title

Decoder backbone

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attention_title

DSA / MLA — unabsorbed operator view

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## indexer_title

DSA Indexer — FULL layers only (21 /78)

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_title

MoE — layers 3…77 (0-based)

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_title

SwiGLU — dense / routed / shared expert

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## aux_title

Auxiliary MTP and source scope

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_config

num_hidden_layers = 78
hidden_size = 6144
vocab_size = 154880
max_position_embeddings = 1048576

- [/num_hidden_layers](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/hidden_size](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/vocab_size](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/max_position_embeddings](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_tokens

Token IDs

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_embed

Embedding
[154880,6144]

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_x

Layer input h

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_n1

RMSNorm

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_attn

DSA

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_n2

RMSNorm

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_ffn

Dense FFN / MoE

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_norm

RMSNorm

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_head

LM head
6144 →154880

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_out

Logits

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_add1

+

- [Decoder residual add after attention, 607–609](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## main_add2

+

- [Decoder residual add after MLP, 612–616](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_dims

DSA / MLA · config
num_attention_heads = 64
q_lora_rank = 2048
kv_lora_rank = 512
qk_nope_head_dim = 192
qk_rope_head_dim = 64
qk_head_dim = 256
v_head_dim = 256
rope_theta = 8000000
rope_interleave = true
attention_bias = false

- [/num_attention_heads](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/q_lora_rank](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/kv_lora_rank](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/qk_nope_head_dim](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/qk_rope_head_dim](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/qk_head_dim](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/v_head_dim](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/rope_parameters/rope_theta](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/rope_interleave](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/attention_bias](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_h

h [6144]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_qa

Linear Q down
6144 →2048

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_qnorm

RMSNorm
Qr [2048]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_qup

Linear Q up
2048 →64×256

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_qsplit

Split Q: 192 |64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_qnope

Q content192

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_qrope

RoPE64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_qcat

Concat Q [64,256]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_kvdown

Linear KV down
6144 →512+64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_kvsplit

Split c512 | k64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_kvnorm

RMSNorm512

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_kvrope

RoPE64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_cache

Latent KV cache
c512 + positional key64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_expand

Linear KV up: 512 →64×448
K192 + kPE64 bypass; V256

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_k

K [64,256]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_v

V [64,256]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_indices

J: new / shared

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_core

Sparse attention
Softmax(QKᵀ / sqrt(256)) V

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_o

Linear O
64×256 →6144

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## attn_out

Attention output [6144]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## index_scope

32 heads ×128 · interleaved RoPE64 · LayerNorm on K
SHARED layers reuse previous TopK; no new Q/K/weight projections

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_qr

Qr [2048]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_h

h [6144]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_qp

Linear Qᵢ
2048 →32×128

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_qrpe

RoPE64 + Concat

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_q

Qᵢ [32,128]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_kp

Linear Kᵢ
6144 →128

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_kn

LayerNorm128

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_krpe

RoPE64 + Concat

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_cache

Index key cache
[T,128]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_wp

Linear (weights)
6144 →32

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_scale

Scale: 32^-0.5

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_w

w [32]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_dot

Matmul (Qᵢ,Kᵢᵀ) / sqrt(128)

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_relu

ReLU

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_sum

Weighted sum (heads)

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_mask

Causal mask

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## idx_topk

TopK ≤2048 → J [B,S,K]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_h

h [6144]

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_router

Linear → Sigmoid
FP32 routing

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_choice

+ correction bias → Top8

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_weights

Gather original scores
Normalize → ×2.5

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_experts

256 routed experts /8 active
SwiGLU: 6144→2048→6144

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_weighted

Weight outputs → Sum

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_shared

Shared expert ×1
6144→2048→6144

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_add

+

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_x

x [6144]

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_gate

Linear (gate)
6144 →m

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_up

Linear (up)
6144 →m

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_silu

SiLU

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_mul

×

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_down

Linear (down): m →6144

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_width

m=12288 Dense /2048 expert · N_e=tokens per expert (Dense: N_e=N)

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## aux_modules

MTP ×1 — inherited base view; target config verified

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mtp_norms

enorm / hnorm

- [GLM-5.2 baseline only; target topology supported by matching config + model card: model.layers.78 auxiliary parameter names in official weight index](https://huggingface.co/zai-org/GLM-5.2/blob/cf457fa734ab149ffef225f80893eb38c6ff5cdc/model.safetensors.index.json)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mtp_projection

eh_proj

- [GLM-5.2 baseline only; target topology supported by matching config + model card: model.layers.78 auxiliary parameter names in official weight index](https://huggingface.co/zai-org/GLM-5.2/blob/cf457fa734ab149ffef225f80893eb38c6ff5cdc/model.safetensors.index.json)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mtp_block

DSA / MoE

- [GLM-5.2 baseline only; target topology supported by matching config + model card: model.layers.78 auxiliary parameter names in official weight index](https://huggingface.co/zai-org/GLM-5.2/blob/cf457fa734ab149ffef225f80893eb38c6ff5cdc/model.safetensors.index.json)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mtp_headnorm

shared_head.norm

- [GLM-5.2 baseline only; target topology supported by matching config + model card: model.layers.78.shared_head.norm.weight](https://huggingface.co/zai-org/GLM-5.2/blob/cf457fa734ab149ffef225f80893eb38c6ff5cdc/model.safetensors.index.json)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mtp_scope

Own indexer; MTP-iteration share flag=true (backend)

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## aux_scope

MTP / precision · config
num_nextn_predict_layers = 1
index_share_for_mtp_iteration = true
dtype = bfloat16
quant_method = fp8
fmt = e4m3
weight_block_size = [128,128]
activation_scheme = dynamic

- [/num_nextn_predict_layers](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/index_share_for_mtp_iteration](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/dtype](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/quantization_config/quant_method](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/quantization_config/fmt](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/quantization_config/weight_block_size](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/quantization_config/activation_scheme](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## footer

Sources: GLM-5.3 @ba32f8c · Transformers @8833c91 · same base as 5.2; target weight-index download blocked (see README)

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## sharing_title

IndexShare · 21 FULL /57 SHARED

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_0

L2 FULL · compute J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_1

L3 SHARED · reuse J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_2

L4 SHARED · reuse J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_3

L5 SHARED · reuse J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## sharing_note

index_topk_freq = 4
index_skip_topk_offset = 3
FULL: L0,L1,L2,L6,…,L74
Same query; share positions J
Each layer keeps its own KV

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [/index_topk_freq](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/index_skip_topk_offset](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## decoder_repeat_count

×78

- [/num_hidden_layers=78; /mlp_layer_types; /indexer_types](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## index_config_params

Indexer · config
index_n_heads = 32
index_head_dim = 128
index_topk = 2048
indexer_rope_interleave = true

- [/index_n_heads](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/index_head_dim](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/index_topk](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/indexer_rope_interleave](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## moe_config_params

MoE · config
n_routed_experts = 256
num_experts_per_tok = 8
n_shared_experts = 1
moe_intermediate_size = 2048
routed_scaling_factor = 2.5
scoring_func = sigmoid
norm_topk_prob = true

- [/n_routed_experts](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/num_experts_per_tok](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/n_shared_experts](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/moe_intermediate_size](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/routed_scaling_factor](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/scoring_func](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/norm_topk_prob](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## mlp_config_params

SwiGLU · config
hidden_size = 6144
intermediate_size = 12288
moe_intermediate_size = 2048
hidden_act = silu
first_k_dense_replace = 3

- [/hidden_size](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/intermediate_size](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/moe_intermediate_size](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/hidden_act](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [/first_k_dense_replace](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## 限制

Official model card states the same base as GLM-5.2; core configuration and pinned implementation match.
GLM-5.3 weight-index download blocked by proxy at official CDN; baseline weight-index citations are explicitly marked and do not verify target weights.
FP8 overlay describes release configuration, not added model operators or a verified backend execution graph.
MTP auxiliary structure inherited from matching config/base; no target tensor-name or backend-iteration verification.
No tensor headers, full weights, GPU inference, benchmark or Feishu import tested.
Edge dimensions use logical sequence-major axes; MoE selected-expert results need not be physically materialized. Absorbed MQA correspondence is documentation only.
