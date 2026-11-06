# GLM-5.1 节点证据

## title

GLM-5.1  |  DSA + Mixture of Experts

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## facts

78 layers · hidden 6144 · 64 Q heads · 256 routed / top-8 + 1 shared · context 202752

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## scope

BF16 checkpoint @26e1bd6 · config + implementation + weight-index checked · bottom-up flow

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## backbone_title

Decoder backbone

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attention_title

DSA / MLA — unabsorbed operator view

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## indexer_title

DSA Indexer — independent Q / K / weights

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_title

MoE — layers 3…77 (0-based)

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_title

SwiGLU — dense / routed / shared expert

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## aux_title

Auxiliary MTP and source scope

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_config

L0–2: Dense FFN
L3–77: MoE FFN
Every main layer: DSA
MTP: separate index78

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_tokens

Token IDs

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_embed

Embedding
[154880,6144]

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_x

Layer input h

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_n1

RMSNorm

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_attn

DSA

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_n2

RMSNorm

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_ffn

Dense FFN / MoE

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_repeat

Repeat 78 layers

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_norm

RMSNorm

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_head

LM head
6144 →154880

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_out

Logits

- [GlmMoeDsaDecoderLayer.forward 585–616; GlmMoeDsaModel / ForCausalLM](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_add1

+

- [Decoder residual add after attention, 607–609](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## main_add2

+

- [Decoder residual add after MLP, 612–616](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_dims

Q rank2048 · KV rank512 · Q/K head256 =192+RoPE64 · V head256
Interleaved RoPE64, theta1e6 · no attention output gate

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_h

h [6144]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_qa

Linear Q down
6144 →2048

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_qnorm

RMSNorm
Qr [2048]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_qup

Linear Q up
2048 →64×256

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_qsplit

Split Q: 192 |64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_qnope

Q content192

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_qrope

RoPE64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_qcat

Concat Q [64,256]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_kvdown

Linear KV down
6144 →512+64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_kvsplit

Split c512 | k64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_kvnorm

RMSNorm512

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_kvrope

RoPE64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_cache

Latent KV cache
c512 + positional key64

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_expand

Linear KV up: 512 →64×448
K192 + kPE64 bypass; V256

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_k

K [64,256]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_v

V [64,256]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_indices

J: selected indices

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_core

Sparse attention
Softmax(QKᵀ / sqrt(256)) V

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_o

Linear O
64×256 →6144

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## attn_out

Attention output [6144]

- [GlmMoeDsaAttention.__init__/forward/expand_kv, lines 297–450](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## index_scope

32 heads ×128 · interleaved RoPE64 · LayerNorm on K
Each checkpoint layer owns indexer weights; no sharing assumed

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_qr

Qr [2048]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_h

h [6144]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_qp

Linear Qᵢ
2048 →32×128

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_qrpe

RoPE64 + Concat

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_q

Qᵢ [32,128]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_kp

Linear Kᵢ
6144 →128

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_kn

LayerNorm128

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_krpe

RoPE64 + Concat

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_cache

Index key cache
[T,128]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_wp

Linear (weights)
6144 →32

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_scale

Scale: 32^-0.5

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_w

w [32]

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_dot

Matmul (Qᵢ,Kᵢᵀ) / sqrt(128)

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_relu

ReLU

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_sum

Weighted sum (heads)

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_mask

Causal mask

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## idx_topk

TopK ≤2048 → J (int32)

- [GlmMoeDsaIndexer.__init__/forward, lines 153–242](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_h

h [6144]

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_router

Linear → Sigmoid
FP32 routing

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_choice

+ correction bias → Top8

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_weights

Gather original scores
Normalize → ×2.5

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_experts

256 routed experts /8 active
SwiGLU: 6144→2048→6144

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_weighted

Weight outputs → Sum

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_shared

Shared expert ×1
6144→2048→6144

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## moe_add

+

- [GlmMoeDsaTopkRouter 469–508; Experts 511–547; MoE 550–572](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_x

x [6144]

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_gate

Linear (gate)
6144 →m

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_up

Linear (up)
6144 →m

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_silu

SiLU

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_mul

×

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_down

Linear (down): m →6144

- [GlmMoeDsaMLP.forward 453–466; Experts.forward 523–547](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mlp_width

m=12288 for first3 dense layers; m=2048 for routed/shared experts

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## aux_modules

MTP ×1 — auxiliary checkpoint index78

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mtp_norms

enorm / hnorm

- [model.layers.78 auxiliary parameter names in official weight index](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/model.safetensors.index.json)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mtp_projection

eh_proj

- [model.layers.78 auxiliary parameter names in official weight index](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/model.safetensors.index.json)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mtp_block

DSA / MoE

- [model.layers.78 auxiliary parameter names in official weight index](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/model.safetensors.index.json)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mtp_headnorm

shared_head.norm

- [model.layers.78.shared_head.norm.weight](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/model.safetensors.index.json)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## mtp_scope

Checkpoint modules only; outside main forward

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## aux_scope

Checkpoint config and weight names verified
59,870 tensor names · 282 shards
No tensor-header or GPU inference test
Optimized sparse-kernel / absorbed layouts are
backend-specific

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## footer

Sources: official zai-org/GLM-5.1 @26e1bd6 · Transformers @f262c71 · explicit evidence and limitations in README / evidence.md

- [config.json](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)

- [Pinned official GLM-5.1 config; see official_config.json](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)

## 限制

Native module-level operator diagram, not an executed trace.
Transformers unabsorbed MLA view; eager/SDPA uses a sparse mask, optimized flash-mla consumes sparse indices.
BF16 checkpoint selected; FP8 distribution is a separate variant, not assumed here.
Weight-index names/shards checked; tensor headers/values, GPU inference and Feishu import were not tested.
MTP index78 is shown as auxiliary checkpoint modules; this Transformers main forward does not execute it.
