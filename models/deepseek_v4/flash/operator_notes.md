# 算子图详细说明

图上仅保留算子；下列说明来自相同 graph JSON，保留完整语义与来源。

## deepseek_v4_flash

### title — DeepSeek-V4-Flash (284B / 13B active)

DeepSeek-V4-Flash | Official architecture study

### subtitle — 43 layers · hidden 4096 · Q 64 / KV 1 · context 1M

OFFICIAL CHECKPOINT 60d8d707 · config, inference implementation, kernel and weight index checked

### defaults — 256 experts · top-6 + 1 shared · head dim 512 · window 128

284B total / 13B active (official card) · 43 layers · hidden 4096 · 64 Q / 1 KV head · 256 experts, top-6 + 1 shared · 1M context

- [/num_hidden_layers, /compress_ratios, /num_hash_layers; index 43 is separate MTP](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [layers.0–42 attention compressors/indexers and mtp.0.*](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/model.safetensors.index.json)

- [Introduction and Model Downloads: 284B total / 13B active / 1M context](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/README.md)

### mhc_heading — mHC

mHC: one attention or FFN wrapper ↑

### compress_heading — Compressor — CSA / HCA

Layer-selected compressors: CSA OR HCA ↑

### main_heading — Transformer ×43

Language backbone / repeat layer ↑

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attention_heading — CSA / HCA / SWA

Official Attention: shared K=V + compressed history ↑

### moe_heading — MoE / MLP

Hash-MoE / routed MoE + shared expert ↑

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### indexer_heading — Lightning Indexer (CSA only)

CSA Lightning Indexer — separate query, key and scoring-weight paths ↑

### hc_x — X [4,4096]

X: four streams [B,T,4,4096]

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_flat — RMSNorm

Flatten streams → unweighted
RMSNorm

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_linear — Linear → Scale + Bias

Linear fn: 16384 → 24 coefficients
Scale + bias; split pre / post /
comb

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_pre — Sigmoid / + ε

pre =
sigmoid(·)
+ eps

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_post — 2 × Sigmoid

post = 2
sigmoid(·)

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_comb — Reshape / [4,4]

comb
logits
[4 × 4]

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_soft — Softmax

Row softmax
+ eps

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_sink — Sinkhorn / ×20

Sinkhorn: 20
iterations
Doubly
stochastic comb

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_collapse — Σ preᵢXᵢ

Collapse input streams
h = sum(pre_i × X_i)

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_norm — RMSNorm

RMSNorm of h

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_fun — Attention / MoE

Attention OR MoE FFN
F(h) [B,T,4096]

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_expand — post × F(h)

Expand block output
post × F(h)

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_residual — combᵀ × X

Residual stream mixing
combᵀ × X

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_sum — +

+

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_y — X′ [4,4096]

Updated streams
[B,T,4,4096]

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### hc_note — pre / post / comb ← X

Residual uses comb transpose; all coefficients are computed from X.

- [Block.hc_pre/hc_post, model.py lines 673–701; hc_split_sinkhorn, kernel.py lines 372–439](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [hc_split_sinkhorn_kernel, lines 372–425](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

### main_tokens — Token IDs

Input token IDs

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_embed — Embedding

Token embedding [B,T,4096]

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_streams — Repeat ×4

Repeat embedding into 4 streams

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_layer_x — X [4,4096]

Layer input X [B,T,4,4096]

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_attn_pre — hc_pre

Attention mHC: pre-collapse; compute post, comb

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_attn_norm — RMSNorm

RMSNorm [4096]

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_attn_core — CSA / HCA / SWA

Layer-selected attention
SWA + layer-selected CSA / HCA; see exact schedule

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_attn_mix — hc_post + Residual

post × attention output + combᵀ × X

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_ffn_pre — hc_pre

FFN mHC: pre-collapse; compute post, comb

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_ffn_norm — RMSNorm

RMSNorm [4096]

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_ffn — Hash-MoE / MoE

Hash-MoE or learned top-k MoE

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_ffn_mix — hc_post + Residual

post × FFN output + combᵀ × residual

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_layer_y — Decoder ×43

Layer output streams
Repeat decoder layer 43× (official checkpoint)

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_hyperhead — HC-head

HyperHead: learned sigmoid-weighted
collapse 4 streams → one hidden state

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_norm — RMSNorm

Final RMSNorm [4096]

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_head — LM-head

LM head: 4096 → vocabulary 129280

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### main_output — Logits [129280]

Last-token logits (official inference)

- [Transformer.__init__/forward, model.py lines 769–811; Block.forward, 688–701; ParallelHead, 703–735](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### schedule — L0–1: SWA / L2–41: [CSA4, HCA128] ×20 / L42: CSA4 / Hash-MoE: L0–2

CHECKPOINT main layers 0–42 (43 total)
L0–1: SWA only (ratio 0)
L2–41: [CSA 4, HCA 128] × 20
L42: CSA 4
MTP0 / L43: SWA only; separate auxiliary path
Hash-MoE L0–2; learned routing L3–42

- [/num_hidden_layers, /compress_ratios, /num_hash_layers; index 43 is separate MTP](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

- [layers.0–42 attention compressors/indexers and mtp.0.*](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/model.safetensors.index.json)

- [Introduction and Model Downloads: 284B total / 13B active / 1M context](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/README.md)

### attn_x — h [4096]

h [B,T,4096]

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qa — Linear (Q down)

Q Linear 4096 → 1024

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qan — RMSNorm

RMSNorm → q_residual

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qb — Linear (Q up)

Q up: 1024 → 64 × 512

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qn — Q head Norm

Per-head unweighted
RMSNorm

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qrope — RoPE₆₄

Partial RoPE:
trailing 64 dims

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kv — Linear (KV down)

KV Linear: 4096 → 512

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvn — RMSNorm

RMSNorm [512]

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvrope — RoPE₆₄

Partial RoPE (64
dims)

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvquant — Quant (FP8 sim)

FP8 simulate non-RoPE
448
RoPE 64 stays BF16

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_local — KV cache (window) / K and V are the SAME

Sliding cache: window 128
K and V are the SAME
tensor

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_compressor — Compressor / C4 / C128

Layer-selected CSA
(4) OR HCA (128)
None for sliding-only

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_entries — KV cache (compress)

Compressed historical
entries
Single shared KV head

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_mask — CSA: TopK + Mask / HCA: Causal Mask

CSA: causal + top-512
mask
HCA: causal mask; no
indexer

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_concat — Concat (KV)

Concatenate local KV and compressed history
Per-query mask; K = V

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_core — Attention (MQA)

Scaled dot-product attention
Softmax over KV logits + learnable sink
Discard sink probability; multiply shared V

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_sink — sink

Learned
sink
per Q
head

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_inverse — RoPE (inverse)

Inverse partial RoPE on attention output
Use conjugate rotation at query position

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_oa — Linear (O down) / 8 × [4096→1024]

Grouped O_a: 8 groups
Per-group 4096 → 1024

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_ob — Linear (O up) / 8192→4096

Flatten 8 × 1024 → O_b → 4096

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_y — h′ [4096]

Attention output [B,T,4096]

- [Attention.__init__/forward, model.py lines 436–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_label — CSA (C4)

CSA | compression stride 4

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_x — h [4096]

Hidden states h [4096]

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_kv — Linear (KV proj)

Linear KV:
4096 → 2 × 512

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_gate — Linear (Gate proj)

Linear gates:
4096 → 2 × 512

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_window — Cat (prev Ca, cur Cb) / window 8 / stride 4

Overlap Ca / Cb: effective width
8, stride 4
Buffer previous Ca across calls

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_bias — + APE → Softmax

GATE PATH: + position bias
FP32 softmax within compression
window

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_sum — × → Sum

Weighted sum of projected KV
One vector [512] per completed
window

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_norm — RMSNorm

RMSNorm [512]

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_rope — RoPE₆₄

Partial RoPE at window position

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_out — Indexer → TopK

Lightning Indexer → top-512
validity mask
Only chosen entries are visible
to each query

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### csa_quant — Quant → KV cache

FP8 simulation on non-RoPE 448
RoPE 64 BF16; write compressed
cache

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_label — HCA (C128)

HCA | compression stride 128

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_x — h [4096]

Hidden states h [4096]

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_kv — Linear (KV proj)

Linear KV:
4096 → 512

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_gate — Linear (Gate proj)

Linear gates:
4096 → 512

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_window — Window 128 / stride 128

Non-overlapping 128-token
windows
Buffer partial window across
calls

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_bias — + APE → Softmax

GATE PATH: + position bias
FP32 softmax within compression
window

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_sum — × → Sum

Weighted sum of projected KV
One vector [512] per completed
window

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_norm — RMSNorm

RMSNorm [512]

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_rope — RoPE₆₄

Partial RoPE at window position

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_out — Causal Mask / NO indexer

Causal visibility mask
All completed compressed
entries; NO indexer

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hca_quant — Quant → KV cache

FP8 simulation on non-RoPE 448
RoPE 64 BF16; write compressed
cache

- [Compressor.__init__/forward, model.py lines 279–377; ratio 4 overlaps, ratio 128 does not](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_x — h [4096]

h [4096] and token IDs (hash route)

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_shared — Shared MLP ×1

One shared expert
4096 → 2048 → 4096

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_router — Linear → √Softplus / Hash / Top6

Learned score: Linear → sqrtsoftplus
Hash: tid2eid[token IDs] selects
experts
Else: top-6(scores + correction
bias)

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_weights — Gather → Normalize / ×1.5

Gather ORIGINAL scores
Normalize selected weights ×
1.5

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_bank — MLP ×256 / 6 active

256 experts; activate 6
Routed weights FP4;
intermediate 2048
Input / output width 4096

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_sum — Σ weighted experts

Weighted routed output

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_add — +

+

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_y — h′ [4096]

MoE output [4096]

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### expert_x — x [4096]

Expert input x [4096]

- [Expert.forward, model.py lines 596–606](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### expert_up — Linear (up) / Clip [−10,10]

Linear W_up
4096 → 2048
clip to [-10,10]

- [Expert.forward, model.py lines 596–606](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### expert_gate — Linear (gate) / Clip max10 → SiLU

Linear W_gate
4096 → 2048
clip MAX at 10
then SiLU

- [Expert.forward, model.py lines 596–606](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### expert_mul — ×

Elementwise product
SiLU(clipped gate) ×
clipped up

- [Expert.forward, model.py lines 596–606](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### expert_weight — × routing weight

Routed: × weight
Shared: bypass

- [Expert.forward, model.py lines 596–606](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### expert_down — Linear (down)

W_down: 2048 → 4096

- [Expert.forward, model.py lines 596–606](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### expert_y — y [4096]

Expert output [4096]

- [Expert.forward, model.py lines 596–606](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### moe_note — Hash L0–2 · Learned Top6 L3–42

Hash routing freezes WHICH experts, not their activation weights.
Checkpoint: Hash-MoE L0–2; learned top-k L3–42.

- [Gate.__init__/forward, model.py lines 546–584; MoE, 609–644](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_q — Qr [1024]

q_residual [1024]

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_qproj — Linear → RoPE / Hadamard → Quant

Q: 1024 → 64 × 128; RoPE 64
Hadamard rotate → FP4 QAT
simulation

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_key — Compressor C4 / dim 128

h → independent overlapping compressor
Index-head width 128; stride 4

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_kcache — Norm → RoPE → Rotate → Quant / KV cache (index)

RMSNorm 128 → RoPE 64
Hadamard rotate → FP4 QAT simulation
Own KV cache / previous Ca state

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_h — Linear (weights)

h [4096] → Linear W_weights
64 query-head scoring weights

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_score — Matmul → ReLU → Scale → Sum

sum_h w_h ReLU(Q_index · K_comp)
Scale: 128^-0.5 × 64^-0.5
Causal masking before top-k

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_select — Mask → TopK (≤512)

Top min(512, compressed length)
Mark invalid future entries as -1
Build per-query CSA mask

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_note — Q / K quantization: FP4 simulation

CSA only. HCA has no Lightning Indexer. Cache buffer / overlap state persists across prefill and decode.

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254; Compressor with rotate=True](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_heading — MTP (auxiliary)

Independent MTP0 / layer_id 43 — not an extra main layer ↑

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_h — Hidden streams

Main hidden streams [B,T,4,4096]

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_hn — RMSNorm (h)

hnorm [4096]

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_hp — Linear (h)

h_proj: 4096 → 4096

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_e — Shared Embedding

MTP token IDs → shared embedding

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_en — RMSNorm (e)

enorm [4096]

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_ep — Linear (e)

e_proj: 4096 → 4096; unsqueeze stream axis

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_sum — +

+

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_block — Block L43 (SWA)

Same mHC decoder Block, layer 43
SWA only (ratio 0); learned MoE routing

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### mtp_head — HC-head → Norm → LM-head

MTP-specific HC-head weights and norm
Shared LM head → MTP logits

- [MTPBlock, model.py lines 738–766; Transformer.__init__, 790–793](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official config.json at checkpoint 60d8d707; see checked-in official_config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### footer — Official Flash checkpoint 60d8d707 · detailed evidence: README / evidence.md · no GPU inference

Official checkpoint deepseek-ai/DeepSeek-V4-Flash @ 60d8d707 · config + model.py + kernel.py + model card + weight index
43 main layers: 2 SWA-only + 21 CSA + 20 HCA; separate MTP0. Index: 69,187 tensor names / 46 shards; shapes and values not read.
284B / 13B are model-card claims, not an independent parameter recount. No GPU inference executed.

## deepseek_v4_flash_csa

### title — DeepSeek-V4-Flash — CSA

DeepSeek-V4-Flash | CSA — computation, cache and addressing

### source — hidden 4096 · heads 64 · head dim 512 · window 128

OFFICIAL CHECKPOINT 60d8d707 | model.py + kernel.py + config.json | bottom-up computation

### facts — CSA · stride 4 · window 8 · index dim 128 · top-k ≤512

CSA: 21 layers (2,4,…,42) · stride 4 · effective window 8 · index heads64 × dim128 · top-k≤512

- [config.json /compress_ratios; Attention.__init__ 436–482](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### ports — A: compressed KV     I: compressed indices     Qr: normalized low-rank query

Named ports A / I / Qr are tensor aliases across panels, not extra computation or copies. B=batch, T=prefill chunk, p=decode position, Nc=completed compressed windows.

### compressor_title — Compressor

1. MAIN KV COMPRESSOR — values and gates are separate

### middle_title — Indexer

2. LIGHTNING INDEXER — three independent learned paths

### attention_title — Attention (MQA)

3. SHARED K=V ATTENTION — window + compressed history

### comp_h — h [4096]

Hidden states h [B,T,4096]

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_fp32 — Cast FP32

Cast hidden states to FP32
Projection / window score arithmetic stays FP32

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_wkv — Linear (KV proj)

Linear Wkv: 4096 → 1024
C = h Wkv

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_wgate — Linear (Gate proj)

Linear Wgate: 4096 → 1024
Z = h Wgate

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_split — Split (Ca / Cb)

Reshape [B,N,4,1024] → Ca / Cb
Ca = first512; Cb = last512

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_ape — + APE

Add learned APE / position bias
shape [4,1024]
Prefill: slot in window; decode: p
% 4

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_gate_split — Split (Za / Zb)

Split biased gate channels Za / Zb
Same Ca/Cb feature layout as KV

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_value_window — Cat (prev Ca, cur Cb)

VALUE WINDOW: [Ca_(j-1), Cb_j]
[B,N,8,512], stride4, effective
width8
First window: missing Ca values =
0

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_gate_window — Cat (prev Za, cur Zb)

GATE WINDOW: [Za_(j-1), Zb_j]
[B,N,8,512]
Missing first-window gates =
-infinity

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_softmax — Softmax (tokens)

FP32 softmax over 8 TOKEN slots
Independently for each of 512
channels
P = softmax(Z_window, dim=tokens)

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_mul — ×

Elementwise product: P ⊙ C_window
Shape [B,N,8,512]
KV values bypass softmax

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_sum — Sum (tokens)

Sum over 8 token slots
c_j[d] = sum_s P[j,s,d] × C[j,s,d]
Result [B,N,512] — NOT pooling across channels

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_complete — Stride boundary

Emit only a completed 4-token stride
Prefill: cutoff=T−(T%4); decode: (p+1)%4==0
Otherwise return None; keep buffered state

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_norm — RMSNorm

Cast pooled vector back to input dtype
Learned RMSNorm over 512 channels

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_nope — Quant (FP8 sim) / content 448

Content 448 dims
FP8 QAT simulation, block64
Simulated values remain BF16

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_rope — RoPE₆₄

Trailing 64 dims: partial RoPE
Prefill position=4j
Decode position=p+1−4
RoPE values remain BF16

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_concat — Concat

Reassemble content448 | RoPE64
One shared KV vector [512] per complete stride

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_write — Cache Write

Write compressed KV cache
Prefill: slots 0…floor(T/4)−1
Decode: slot floor(p/4)

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_bank — KV cache (compress)

Cache capacity [B,floor(max_seq_len/4),512]
Logical valid entries Nc=floor(end_pos/4)
No query-specific pruning or top-k is stored here

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_alias — View [:,128:]

Storage aliases Attention.kv_cache[:,128:]
Compressed entries are appended after the window region
No copied top-k-only KV cache

- [Attention.forward lines 490–500; Compressor.kv_cache write 369–375](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### port_A — A: KV [Nc,512]

PORT A → right panel
ALL valid compressed KV vectors (K=V)
Shape [B,Nc,512]

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_note — KV / Gate are independent projections

Main compressor rotate=False. Indexer uses its OWN smaller compressor with
rotate=True (CSA only).

### idx_q_input — Qr [1024]

PORT Qr: normalized
q_residual
[B,T,1024], same as
attention rank-normalized
query

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_h — h [4096]

Hidden states h [B,T,4096]
Supplies key compressor AND scoring weights

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_q_proj — Linear (Q up)

Wq_b: 1024 → 64×128

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_q_heads — Reshape / [64,128]

Reshape [B,T,64,128]
TP: split query heads

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_q_rope — RoPE₆₄

Partial RoPE on
last64
At CURRENT query
position t

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_q_hadamard — Rotate (Hadamard)

Hadamard rotation
Scale 1/sqrt(128)

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_q_fp4 — Quant (FP4 sim)

FP4 QAT simulation
block32, in-place
Tensor remains BF16

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_q_ready — Qᵢ [64,128]

Index query Q_I
[B,T,64,128]

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_kv_proj — Linear / (KV)

Wkv_I
4096 → 256

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_gate_proj — Linear / (Gate)

Wgate_I
4096 → 256

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_w_proj — Linear (weights)

W_weights: 4096 → 64
One score weight per
head

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_kv_split — Split / Ca / Cb

Split Ca/Cb
128 + 128

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_gate_ape — + APE / Split Za / Zb

Gate + APE
[4,256]
Split Za/Zb

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_window — Cat (prev, current) / 8 × 128

Independent
overlapping windows
[prev Ca4 | current
Cb4]
KV / gates [B,N,8,128]

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_softmax — Softmax (tokens)

Gate-only FP32 softmax
Across 8 slots per
channel

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_pool — × → Sum

KV bypass × gate
probabilities
Sum8 → [B,N,128]

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_norm — RMSNorm

Learned RMSNorm128

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_key_rope — RoPE₆₄

Partial RoPE64
At compressed position
4j

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_key_hadamard — Rotate (Hadamard)

Hadamard rotation
Same orthogonal basis
as Q_I

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_key_fp4 — Quant (FP4 sim)

FP4 QAT simulation,
block32
Tensor remains BF16

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_key_cache — KV cache (index) / [Nc,128]

Independent index KV
cache
[B,Nc,128]
Own previous-Ca /
partial state

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_w_scale — Scale / 128⁻½ × 64⁻½

Scale head weights
128^-0.5 × 64^-0.5
These weights are NOT
a softmax

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_w_ready — weights [64]

Per-query head
weights w
[B,T,64]

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_dot — Matmul (Qᵢ, Kᵢᵀ)

einsum: Q_I · K_I_cache
Raw scores [B,T,64,Nc]

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_relu — ReLU

ReLU of per-head similarities

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_head_sum — Scale → Sum (heads)

Multiply by learned head weights, then sum heads
S[b,t,j] = sum_h w[b,t,h] × ReLU(dot[b,t,h,j])

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_tp — AllReduce (TP)

If TP > 1: all_reduce index scores
Scores [B,T,Nc] across all 64 global heads

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_causal — Causal Mask

Prefill: j >= floor((t+1)/4) → -infinity
Decode: score only cache prefix j < floor((p+1)/4)

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### idx_topk — TopK (≤512)

Top-k with k=min(512,Nc)
Per-query ranking; may include masked -infinity entries
NOT a cache truncation operation

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### port_I — I: compressed indices

PORT I → right panel
Prefill: invalid future j → -1, valid j → j+T
Decode: j → j+128
Selected compressed positions; integer tensor

- [Indexer.__init__/forward, model.py lines 380–433; rotate_activation, 247–254](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_h — h [4096]

Hidden states h [B,T,4096]

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qa — Linear (Q down) / 4096→1024

Linear Wq_a: 4096 → 1024

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qrank — RMSNorm → Qr

Learned RMSNorm1024 → PORT Qr

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qb — Linear (Q up) / 1024→64×512

Wq_b: 1024 → 64 × 512
Reshape to heads [B,T,64,512]

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qhead — Q head Norm

Unweighted RMSNorm per 512-dim
head

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qrope — RoPE₆₄

RoPE on trailing64 at query t
Content448 untouched
Compressed layer: theta160000 /
YaRN16

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qready — Q [64,512]

Q [B,T,64,512]

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_wkv — Linear (KV down) / 4096→512

Linear Wkv: 4096 → 512

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvnorm — RMSNorm

Learned RMSNorm512

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvrope — RoPE₆₄

Partial RoPE64 at token position t

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvquant — Quant (FP8 sim)

FP8 simulation on content448,
block64
RoPE64 stays BF16; shared K=V
tensor

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_ring — KV cache (window) / 128 × 512

Window ring cache [B,128,512]
Decode write slot p%128
Prefill: store last128 tokens in
ring order

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_positions — Position (t / p)

Position inputs: T, start_pos=p,
window=128
This path computes addresses, not
KV values

- [get_window_topk_idxs, model.py lines 254–265](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_win_indices — Window indices (128)

get_window_topk_idxs
Prefill: causal local window, future
→ -1
Decode: ring order from p%128
Warmup slots not yet valid → -1

- [get_window_topk_idxs, model.py lines 254–265](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_I — I: compressed indices

PORT I from middle panel
Per-query selected compressed
indices

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_A — A: compressed KV

PORT A from main compressor
All compressed KV [B,Nc,512]

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_bank — Concat (window KV, compressed KV)

Physical KV bank (K=V)
Prefill: cat current KV[T] and complete compressed KV[Nc]
Decode: [ring128 | compressed cache]; compressor aliases right slice

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_indices — Concat (window indices, I)

Concatenate [local-window indices | port I]
Prefill offset=T; decode compressed offset=128
Convert to int32; -1 stays invalid

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_gather — Gather (KV) → QKᵀ / √512

sparse_attn kernel: tiles of 64 index entries
If idx!=-1: gather shared kv[idx] (both K and V)
Q·K / sqrt(512), FP32 score accumulators
If idx==-1: zero KV and -infinity score

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_softmax — Softmax (+ sink)

Online stable softmax: update running max and sum
Denominator = sum_j exp(score_j-max) + exp(sink_h-max)
The sink changes normalization ONLY; it has no value vector

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_sink — sink

Learned
sink_h
One per
Q head

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_values — Matmul (P, V)

Numerator: sum_j exp(score_j-max) × kv[idx_j]
Divide by denominator; FP32 accumulator → BF16 output
Result [B,T,64,512]

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_inverse — RoPE (inverse)

Conjugate RoPE (inverse=True) on output trailing64
At the CURRENT query position; content448 unchanged

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_oa — Linear (O down) / 8 groups × (4096→1024)

Group 64×512 heads into 8 groups
W_o_a: per-group 4096 → 1024 (einsum)

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_ob — Linear (O up) / 8192→4096

Flatten 8×1024 → W_o_b → 4096
TP output all-reduce when needed

- [RowParallelLinear.forward 173–179; Attention.forward 533–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_output — h′ [4096]

OUTPUT: attention hidden states [B,T,4096]

### states_title — kv_state / score_state

PREFILL / DECODE STATE + WINDOW LAYOUT — temporal state, not an extra network layer

### state_shapes — kv_state / score_state / [8,1024]

MAIN runtime buffers (not checkpoint)
kv_state / score_state: [B,8,1024]
KV init=0; gate init=-infinity
Indexer owns separate [B,8,256] buffers

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_prefill — Prefill → Buffer remainder

PREFILL (start_pos=0)
cutoff=T−T%4; completed=floor(T/4)
Keep incomplete suffix for decode
Keep last complete raw window; read its Ca half later

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_decode — Update → Emit every 4 tokens

DECODE (position p)
Write raw KV / gate at slot 4+(p%4)
Emit only if (p+1)%4==0
Write cache slot floor(p/4); RoPE pos=p+1−4

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_window1 — prev Ca [4,512]

Compressed j=1 (emitted after token7)
VALUES: [Ca0 Ca1 Ca2 Ca3 | Cb4 Cb5 Cb6 Cb7]
GATES:  [Za0 Za1 Za2 Za3 | Zb4 Zb5 Zb6 Zb7] + per-slot APE
Softmax8 PER CHANNEL; output RoPE position4

- [Compressor.overlap_transform, lines 307–314; forward](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_window2 — cur Cb [4,512]

Compressed j=2 (emitted after token11)
VALUES: [Ca4 Ca5 Ca6 Ca7 | Cb8 Cb9 Cb10 Cb11]
Same token can supply Cb to j and Ca to j+1
First j=0: missing previous half has value0 / gate−infinity

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_move — prev ← current (on stride boundary)

On a completed decode stride: copy current raw window into previous-window state. Read Ca from previous slots and Cb from current slots.
A partial stride does NOT create a new compressed entry. Existing entries remain readable; Indexer top-k does not delete them.

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### footer — Official Flash @ 60d8d707 · FP4 / FP8 = simulation · source details: operator_notes.md

Source: official deepseek-ai/DeepSeek-V4-Flash @ 60d8d707 | model.py Compressor / Indexer / Attention; kernel.py sparse_attn
Detailed static source transcription; no full weights, tensor headers or GPU inference executed. Native draw.io is the PNG source.

## deepseek_v4_flash_hca

### title — DeepSeek-V4-Flash — HCA

DeepSeek-V4-Flash | HCA — computation, cache and addressing

### source — hidden 4096 · heads 64 · head dim 512 · window 128

OFFICIAL CHECKPOINT 60d8d707 | model.py + kernel.py + config.json | bottom-up computation

### facts — HCA · stride 128 · window 128 · all causal compressed entries

HCA: 20 layers (3,5,…,41) · non-overlap window 128 · all completed compressed entries · NO learned Indexer

- [config.json /compress_ratios; Attention.__init__ 436–482](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### ports — A: compressed KV     I: causal compressed indices

Named ports A / I / Qr are tensor aliases across panels, not extra computation or copies. B=batch, T=prefill chunk, p=decode position, Nc=completed compressed windows.

### compressor_title — Compressor

1. MAIN KV COMPRESSOR — values and gates are separate

### middle_title — Causal indices

2. CAUSAL HISTORY INDICES — position arithmetic only

### attention_title — Attention (MQA)

3. SHARED K=V ATTENTION — window + compressed history

### comp_h — h [4096]

Hidden states h [B,T,4096]

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_fp32 — Cast FP32

Cast hidden states to FP32
Projection / window score arithmetic stays FP32

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_wkv — Linear (KV proj)

Linear Wkv: 4096 → 512
C = h Wkv

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_wgate — Linear (Gate proj)

Linear Wgate: 4096 → 512
Z = h Wgate

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_split — Reshape [128,512]

Reshape complete prefix
[B,N,128,512]
One KV vector per token; no Ca/Cb
split

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_ape — + APE

Add learned APE / position bias
shape [128,512]
Prefill: slot in window; decode: p
% 128

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_gate_split — Reshape [128,512]

Reshape biased gates [B,N,128,512]
Align one gate per token and
channel

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_value_window — KV window [128,512]

VALUE WINDOW: C_j[0:128]
[B,N,128,512], stride128
No previous-window overlap

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_gate_window — Gate window [128,512]

GATE WINDOW: Z_j + APE
[B,N,128,512]
No previous-window gate state

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_softmax — Softmax (tokens)

FP32 softmax over 128 TOKEN slots
Independently for each of 512
channels
P = softmax(Z_window, dim=tokens)

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_mul — ×

Elementwise product: P ⊙ C_window
Shape [B,N,128,512]
KV values bypass softmax

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_sum — Sum (tokens)

Sum over 128 token slots
c_j[d] = sum_s P[j,s,d] × C[j,s,d]
Result [B,N,512] — NOT pooling across channels

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_complete — Stride boundary

Emit only a completed 128-token stride
Prefill: cutoff=T−(T%128); decode: (p+1)%128==0
Otherwise return None; keep buffered state

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_norm — RMSNorm

Cast pooled vector back to input dtype
Learned RMSNorm over 512 channels

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_nope — Quant (FP8 sim) / content 448

Content 448 dims
FP8 QAT simulation, block64
Simulated values remain BF16

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_rope — RoPE₆₄

Trailing 64 dims: partial RoPE
Prefill position=128j
Decode position=p+1−128
RoPE values remain BF16

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_concat — Concat

Reassemble content448 | RoPE64
One shared KV vector [512] per complete stride

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_write — Cache Write

Write compressed KV cache
Prefill: slots 0…floor(T/128)−1
Decode: slot floor(p/128)

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_bank — KV cache (compress)

Cache capacity [B,floor(max_seq_len/128),512]
Logical valid entries Nc=floor(end_pos/128)
No query-specific pruning or top-k is stored here

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_alias — View [:,128:]

Storage aliases Attention.kv_cache[:,128:]
Compressed entries are appended after the window region
No copied top-k-only KV cache

- [Attention.forward lines 490–500; Compressor.kv_cache write 369–375](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### port_A — A: KV [Nc,512]

PORT A → right panel
ALL valid compressed KV vectors (K=V)
Shape [B,Nc,512]

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### comp_note — KV / Gate are independent projections

Main compressor rotate=False. Indexer uses its OWN smaller compressor with
rotate=True (CSA only).

### hca_no_indexer — Position indices · NO Indexer

NO Lightning Indexer
No learned Q_I / K_I / W_weights
No top-512 pruning; every causal compressed window is eligible

### hist_prefill_input — Prefill: t ∈ [0,T)

Prefill positions t=0…T−1

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_prefill_nc — Nc = ⌊T/128⌋

Allocate candidate
j=0…floor(T/128)−1

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_prefill_range — Arange (Nc)

arange(floor(T/128)), repeat per
query

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_prefill_threshold — visible = ⌊(t+1)/128⌋

For query t: visible count
floor((t+1)/128)

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_prefill_mask — Causal Mask (−1)

Future j >= visible_count
becomes -1

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_prefill_offset — + T

Valid physical slot = T+j;
preserve -1

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_prefill_expand — Expand [B,T,Nc]

Batch-expand indices
[B,T,Nc_max]

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_decode_input — Decode: position p

Decode position p=start_pos; one
token

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_decode_nc — Nc = ⌊(p+1)/128⌋

Nc=floor((p+1)/128) completed
windows

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_decode_range — Arange (Nc)

arange(Nc); every completed
window

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_decode_threshold — Valid prefix

Current prefix already satisfies
causality

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_decode_mask — All eligible indices

No learned score, no query-
dependent top-k

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_decode_offset — + 128

Physical slot = 128+j (after
ring buffer)

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_decode_expand — Expand [B,1,Nc]

Batch-expand indices [B,1,Nc]

- [get_compress_topk_idxs, official model.py lines 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_mode — Select (prefill / decode)

Select prefill OR decode index list
Controlled only by start_pos, T, window_size and ratio128

- [get_compress_topk_idxs 268–276; Attention.forward 504–520](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_valid — 128(j+1) ≤ t+1

Logical rule: 128(j+1) <= t+1
The current incomplete 128-token window is NEVER emitted

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_no_prune — Nc(t)=floor((t+1)/128)

Eligible historical entries grow with context
Nc(t)=floor((t+1)/128)
This is NOT fixed-k sparse retrieval

- [get_compress_topk_idxs 268–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_examples — t=127 → j0 / t=255 → j0,j1

Examples (0-based token positions)
t=126: 0 entries; t=127: {j0}
t=255: {j0,j1}; t=383: {j0,j1,j2}

- [Derived directly from causal inequality in get_compress_topk_idxs](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_storage — A: KV cache (compress)

Indices refer to MAIN compressed KV bank, port A
There is no second indexer cache
Do not discard old compressed entries after 512

- [Attention.__init__/forward 436–543; no Indexer for ratio128](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### hist_port_type — Cast int32

All eligible compressed indices are forwarded
Attention adds local-window indices separately
Final concatenated list is cast to int32

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### port_I — I: compressed indices

PORT I → right panel
All causal historical compressed locations
Prefill: valid j+T / invalid -1
Decode: j+128

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_h — h [4096]

Hidden states h [B,T,4096]

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qa — Linear (Q down) / 4096→1024

Linear Wq_a: 4096 → 1024

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qrank — RMSNorm

Learned RMSNorm1024 → PORT Qr

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qb — Linear (Q up) / 1024→64×512

Wq_b: 1024 → 64 × 512
Reshape to heads [B,T,64,512]

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qhead — Q head Norm

Unweighted RMSNorm per 512-dim
head

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qrope — RoPE₆₄

RoPE on trailing64 at query t
Content448 untouched
Compressed layer: theta160000 /
YaRN16

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_qready — Q [64,512]

Q [B,T,64,512]

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_wkv — Linear (KV down) / 4096→512

Linear Wkv: 4096 → 512

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvnorm — RMSNorm

Learned RMSNorm512

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvrope — RoPE₆₄

Partial RoPE64 at token position t

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_kvquant — Quant (FP8 sim)

FP8 simulation on content448,
block64
RoPE64 stays BF16; shared K=V
tensor

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_ring — KV cache (window) / 128 × 512

Window ring cache [B,128,512]
Decode write slot p%128
Prefill: store last128 tokens in
ring order

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_positions — Position (t / p)

Position inputs: T, start_pos=p,
window=128
This path computes addresses, not
KV values

- [get_window_topk_idxs, model.py lines 254–265](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_win_indices — Window indices (128)

get_window_topk_idxs
Prefill: causal local window, future
→ -1
Decode: ring order from p%128
Warmup slots not yet valid → -1

- [get_window_topk_idxs, model.py lines 254–265](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_I — I: compressed indices

PORT I from middle panel
ALL causal compressed indices

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_A — A: compressed KV

PORT A from main compressor
All compressed KV [B,Nc,512]

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_bank — Concat (window KV, compressed KV)

Physical KV bank (K=V)
Prefill: cat current KV[T] and complete compressed KV[Nc]
Decode: [ring128 | compressed cache]; compressor aliases right slice

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_indices — Concat (window indices, I)

Concatenate [local-window indices | port I]
Prefill offset=T; decode compressed offset=128
Convert to int32; -1 stays invalid

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_gather — Gather (KV) → QKᵀ / √512

sparse_attn kernel: tiles of 64 index entries
If idx!=-1: gather shared kv[idx] (both K and V)
Q·K / sqrt(512), FP32 score accumulators
If idx==-1: zero KV and -infinity score

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_softmax — Softmax (+ sink)

Online stable softmax: update running max and sum
Denominator = sum_j exp(score_j-max) + exp(sink_h-max)
The sink changes normalization ONLY; it has no value vector

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_sink — sink

Learned
sink_h
One per
Q head

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_values — Matmul (P, V)

Numerator: sum_j exp(score_j-max) × kv[idx_j]
Divide by denominator; FP32 accumulator → BF16 output
Result [B,T,64,512]

- [sparse_attn_kernel, official kernel.py lines 277–367](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_inverse — RoPE (inverse)

Conjugate RoPE (inverse=True) on output trailing64
At the CURRENT query position; content448 unchanged

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_oa — Linear (O down) / 8 groups × (4096→1024)

Group 64×512 heads into 8 groups
W_o_a: per-group 4096 → 1024 (einsum)

- [Attention.forward, model.py lines 484–543; get_window_topk_idxs/get_compress_topk_idxs, 254–276](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_ob — Linear (O up) / 8192→4096

Flatten 8×1024 → W_o_b → 4096
TP output all-reduce when needed

- [RowParallelLinear.forward 173–179; Attention.forward 533–543](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### attn_output — h′ [4096]

OUTPUT: attention hidden states [B,T,4096]

### states_title — kv_state / score_state

PREFILL / DECODE STATE + WINDOW LAYOUT — temporal state, not an extra network layer

### state_shapes — kv_state / score_state / [128,512]

MAIN runtime buffers (not checkpoint)
kv_state / score_state: [B,128,512]
KV init=0; gate init=-infinity
No indexer state or indexer KV bank

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_prefill — Prefill → Buffer remainder

PREFILL (start_pos=0)
cutoff=T−T%128; completed=floor(T/128)
Keep incomplete suffix for decode
Keep only current incomplete 128-token window

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_decode — Update → Emit every 128 tokens

DECODE (position p)
Write raw KV / gate at slot p%128
Emit only if (p+1)%128==0
Write cache slot floor(p/128); RoPE pos=p+1−128

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_window1 — Tokens 0…127 → KV₀

Compressed j=0
Tokens0…127 → one512-dim vector
APE has128 slot rows; softmax is per-channel over128 tokens
Emission p=127; RoPE position0; stored at compressed slot0

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_window2 — Tokens 128…255 → KV₁

Compressed j=1
Tokens128…255 → a DIFFERENT512-dim vector
No token overlap with j0; no previous-window Ca branch
Emission p=255; RoPE position128; stored at compressed slot1

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### state_move — Append one KV every 128 tokens

Before boundary p=127/255/…: update partial-window state only. At boundary: compress128 slots and append one KV entry.
All earlier completed entries remain in cache and are indexed causally. No learned retrieval network and no top-512 cap.

- [Compressor.__init__/overlap_transform/forward, official model.py lines 279–377](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)

- [Official Flash config at 60d8d707; hidden4096/head512/window128/index128/topk512/compress_ratios](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)

### footer — Official Flash @ 60d8d707 · FP4 / FP8 = simulation · source details: operator_notes.md

Source: official deepseek-ai/DeepSeek-V4-Flash @ 60d8d707 | model.py Compressor / Indexer / Attention; kernel.py sparse_attn
Detailed static source transcription; no full weights, tensor headers or GPU inference executed. Native draw.io is the PNG source.

