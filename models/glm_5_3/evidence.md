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

Official FP8 release @ba32f8c · same base as GLM-5.2 · post-training gains · bottom-up flow

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

L0–2: Dense FFN
L3–77: MoE FFN
DSA: 21 FULL +57 SHARED
MTP: separate index78

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

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

## main_repeat

Repeat 78 layers

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

Q rank2048 · KV rank512 · Q/K256 =192+RoPE64 · V256
Interleaved RoPE64, theta8e6 · per-layer KV cache

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

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

TopK ≤2048 → J (int32)

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

m=12288 for first3 dense layers; m=2048 for routed/shared experts

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

FP8 release / deployment config
E4M3 · dynamic activation
Weight blocks 128 ×128
541 exclusions; no extra network branch

- [/quantization_config](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Introduction: same base model as GLM-5.2; gains from post-training](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/README.md)

## footer

Sources: GLM-5.3 @ba32f8c · Transformers @8833c91 · same base as 5.2; target weight-index download blocked (see README)

- [config.json](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.2 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## sharing_title

IndexShare — reuse token positions across layers; keep KV caches independent

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_0

L2: FULL
compute J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_1

L3: SHARED
reuse J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_2

L4: SHARED
reuse J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## share_stage_3

L5: SHARED
reuse J₂

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## sharing_note

0-based: L0 /L1 also FULL. Next groups: L6 FULL →L7–9 SHARED; …; L74 FULL →L75–77 SHARED.
J is reused within the same forward query; it is not the previous decode token’s selection.

- [/indexer_types (0-based), /index_topk_freq=4, /index_skip_topk_offset=3](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

- [Attention.forward, 404–417: shared layers consume prev_topk_indices; KV update remains per layer at 395–398](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

## dim_title

Tensor dimensions — transformations within one forward pass

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_symbols

B=batch · S=query length · T=KV length incl. cache · K=min(2048,T) · N=B×S · head axes shown before channel
Prefill: S may be many tokens; decode: S=1, T grows. All network dimensions below also apply to GLM-5.2.

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_dsa_title

DSA / MLA  |  64 heads

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_dsa

h [B,S,6144]
Q down → [B,S,2048]
Q up / reshape → [B,S,64,256]
Q split: content192 + RoPE64
KV down → [B,S,512+64]
Cache: c [B,T,1,512] + kPE [B,T,1,64]
KV up: 512 → 64×(192+256)
K [B,T,64,256] · V [B,T,64,256]
Attention → [B,S,64,256]
Flatten 16384 → O → [B,S,6144]

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_index_title

Indexer  |  32 heads

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_index

Qr [B,S,2048] → Qi [B,S,32,128]
h [B,S,6144] → Ki [B,S,128]
K cache → [B,T,128] (shared by heads)
h → weights [B,S,32]
Qi × Kiᵀ → scores [B,S,32,T]
ReLU → weighted head sum
Reduced scores [B,S,T]
Causal mask → TopK → J [B,S,K]
FULL: compute J; SHARED: reuse J
K is read selection, not cache capacity

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_moe_title

FFN / MoE  |  256 experts, top-8

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_moe

h [B,S,6144] → flatten [N,6144]
Router 6144 →256: scores [N,256]
Top8 IDs / weights [N,8]
Dispatch → each expert input [N_e,6144]
Gate / Up → [N_e,2048] each
SiLU(gate) × Up → Down → [N_e,6144]
Weight / scatter-sum → [N,6144]
+ shared expert → [B,S,6144]
Dense L0–2: m=12288 (no dispatch)
LM head: [B,S,6144] → [B,S,154880]

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_mqa_title

Absorbed MQA correspondence — alternative algebraic view, not an additional model branch

- [Attention.forward / expand_kv; Indexer.forward; MoE and MLP forward](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## dim_mqa

Q content192 × W_Kᵀ →512; concat RoPE64 → Q_abs [B,S,64,576]
Selected K_abs [B,S,K,1,576] = latent512 + positional64; selected V_abs [B,S,K,1,512]
Softmax(Q_abs K_absᵀ / sqrt(256)) V_abs → [B,S,64,512]
Per-head W_V: 512 →256 → [B,S,64,256]; flatten → Linear O: 16384 →6144
MQA uses one shared latent KV head. This is the screenshot’s 512+64 view; the main diagram explicitly expands K/V.
Selection is query-dependent (S axis); no materialized gather, fused kernel or quantized numerical equivalence is claimed.

- [Algebra from Attention.__init__/expand_kv: kv_b_proj splits per-head W_K (512→192) and W_V (512→256); o_proj 64×256→6144](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Explicit projection dimensions and model sizes](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)

## 限制

Official model card states the same base as GLM-5.2; core configuration and pinned implementation match.
GLM-5.3 weight-index download blocked by proxy at official CDN; baseline weight-index citations are explicitly marked and do not verify target weights.
FP8 overlay describes release configuration, not added model operators or a verified backend execution graph.
MTP auxiliary structure inherited from matching config/base; no target tensor-name or backend-iteration verification.
No tensor headers, full weights, GPU inference, benchmark or Feishu import tested.
Dimension guide uses logical sequence-major axes; absorbed MQA is an algebraic correspondence, not a verified backend or quantized numeric execution graph.
