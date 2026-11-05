# Kimi-K3.1-Pro 节点与来源

颜色分类由官方模型卡、配置差异和固定推理源码人工核对；配置项删除不自动表示模型算子删除。

## hybrid_outline [unchanged]

Hybrid backbone
(93 layers)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## title [unchanged]

Kimi-K3.1-Pro — Architecture Diff vs Kimi-K3

K3 图中原注释：Kimi K3 — Architecture Study / Detailed v2

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## subtitle [unchanged]

RED: added  |  GREEN: retired  |  YELLOW: parameter / config only

K3 图中原注释：Native reconstruction · bottom-up flow · technical-report reviewed draft

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## params [unchanged]

2.8T / 104B active (card) · 93 layers · hidden 7168 · 96 heads · context 1M

K3 图中原注释：2.78T total · 104.2B active · 93 layers · hidden 7168 · 96 heads · 1M context

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## attnres_title [unchanged]

Block Attention Residual (AttnRes)    ↑

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_title [unchanged]

Kimi Delta Attention (KDA)    ↑

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_title [unchanged]

Stable LatentMoE    ↑

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_title [added]

Gated DSA (NoPE) — sparse read

K3 图中原注释：Gated MLA (NoPE)    ↑

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## vision_title [unchanged]

MoonViT-V2 · 27 layers · hidden 1024

K3 图中原注释：Native vision: MoonViT-V2    ↑

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_keys [unchanged]

RMSNorm(Keys)

- [§2.2, equations 8–10 (block-level attention residuals)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_query [unchanged]

Pseudo-query w

K3 图中原注释：Learned pseudo-query
w
(independent
parameter)

- [§2.2, equations 8–10 (block-level attention residuals)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_logits [unchanged]

wᵀ RMSNorm(K)

K3 图中原注释：Depth logits: wᵀ RMSNorm(K)

- [§2.2, equations 8–10 (block-level attention residuals)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_softmax [unchanged]

Softmax (depth)

K3 图中原注释：Softmax over DEPTH

- [§2.2, equations 8–10 (block-level attention residuals)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_values [unchanged]

Values V
(original)

K3 图中原注释：Values
(original)
unchanged

- [§2.2, equations 8–10 (block-level attention residuals)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_sum [unchanged]

Weighted sum

K3 图中原注释：Weighted sum of original values

- [§2.2, equations 8–10 (block-level attention residuals)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_out [unchanged]

Output to next sublayer

- [§2.2, equations 8–10 (block-level attention residuals)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_x [unchanged]

Input x [T, 7168]

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_q_linear [unchanged]

Linear Wq

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_q_conv [unchanged]

ShortConv

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_q_swish [unchanged]

Swish /
SiLU

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_q_l2 [unchanged]

L2Norm

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_port_q [unchanged]

Q

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_k_linear [unchanged]

Linear Wk

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_k_conv [unchanged]

ShortConv

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_k_swish [unchanged]

Swish /
SiLU

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_k_l2 [unchanged]

L2Norm

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_port_k [unchanged]

K

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_v_linear [unchanged]

Linear Wv

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_v_conv [unchanged]

ShortConv

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_v_swish [unchanged]

Swish /
SiLU

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_port_v [unchanged]

V

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_alpha_down [unchanged]

Linear Wα↓

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_alpha_up [unchanged]

Linear Wα↑

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_alpha_bias [unchanged]

+ bα = z

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_alpha_scale [unchanged]

× exp(A)

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_alpha_sigmoid [unchanged]

g = −5 sigmoid(·)

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_alpha_exp [unchanged]

α = exp(g)

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_port_alpha [unchanged]

α

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_beta_linear [unchanged]

Linear
Wβ

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_beta_sigmoid [unchanged]

Sigmoid

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_port_beta [unchanged]

β

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_core [unchanged]

Kimi Delta Attention / recurrent state update
Sₜ = (I − βₜ kₜ kₜᵀ) Diag(αₜ) Sₜ₋₁ + βₜ kₜ vₜᵀ
oₜ = Sₜᵀ qₜ

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_norm [unchanged]

Head-wise RMSNorm

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_product [unchanged]

×

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_gate_linear [unchanged]

Linear Wg

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_gate_sigmoid [unchanged]

Sigmoid

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## kda_wo [unchanged]

Linear Wo → output y [T, 7168]

- [§2.1.1, equations 1, 2, 5, 6 (conceptual factorization; ranks not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## lm_fused [unchanged]

Fused sequence (text + visual
tokens)

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## lm_repeat [added]

23 × [3 KDA + FFN, then
1 Gated DSA + FFN]
= 92 attention layers

K3 图中原注释：23 × [3 KDA + FFN, then 1
Gated MLA + FFN]
= 92 attention layers

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## lm_final [added]

Final Gated DSA + FFN
= 1 attention layer

K3 图中原注释：Final Gated MLA + FFN
= 1 attention layer

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## lm_norm [unchanged]

Final depth aggregation /
normalization

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## lm_head [unchanged]

LM head

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## lm_out [unchanged]

Output tokens

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## lm_counts [added]

69 KDA + 24 Gated DSA = 93
L1 dense FFN; L2–93 MoE
Same layer positions as K3

K3 图中原注释：69 KDA + 24 Gated MLA = 93
92 MoE FFNs + 1 dense FFN
Dense FFN location not mapped

- [§2.1 and Table 1 (schedule and counts; exact dense FFN location unmapped)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## k_title [unchanged]

KDA + FFN layer (×69)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_ar1 [unchanged]

Block AttnRes

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_norm1 [unchanged]

RMSNorm

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_attn [unchanged]

KDA recurrent attention

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_ar2 [unchanged]

Block AttnRes / partial update

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_norm2 [unchanged]

RMSNorm

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_ffn [unchanged]

FFN (MoE or dense)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_out [unchanged]

Depth / partial-state update

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## m_ar1 [unchanged]

Block AttnRes

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## m_norm1 [unchanged]

RMSNorm

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## m_attn [added]

Gated DSA (NoPE)

K3 图中原注释：Gated MLA (NoPE)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## m_ar2 [unchanged]

Block AttnRes / partial update

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## m_norm2 [unchanged]

RMSNorm

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## m_ffn [unchanged]

FFN (MoE or dense)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## m_out [unchanged]

Depth / partial-state update

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_x [unchanged]

x [T, 7168]

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_shared [unchanged]

2 shared experts
7168 → 7168

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_down [unchanged]

Linear down
7168 → 3584

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_bank [unchanged]

896 experts, activate 16
FFN: SiTU-GLU, width 3072

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_weighted [unchanged]

Weighted sum

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_norm [unchanged]

RMSNorm (3584)

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_up [unchanged]

Linear up
3584 → 7168

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_router [unchanged]

Router
score / QB /
Top-16

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_sum [unchanged]

+

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_y [unchanged]

y [T, 7168]

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_x [unchanged]

Expert input
3584 or 7168

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_gate [unchanged]

Linear
Wgate
(· → 3072)

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_up [unchanged]

Linear Wup
(· → 3072)

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_capgate [unchanged]

4
tanh(a/4)
×
sigmoid(a)

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_capup [unchanged]

25
tanh(b/25)

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_mul [unchanged]

×

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_down [unchanged]

Linear Wdown
3072 → expert width

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ex_y [unchanged]

Expert output

- [§2.3, equations 11–12; Table 1](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_x [unchanged]

x [T, 7168]

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_q [unchanged]

Linear Q down
7168 → 1536

K3 图中原注释：Linear Wq

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_compress [unchanged]

Linear KV down + Split
7168 → (512 + 64)

K3 图中原注释：Linear KV compression: x → c

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_cache [unchanged]

Latent KV cache
[512 + 64, NoPE]

K3 图中原注释：Latent cache c
(compressed KV, persistent)

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_reconstruct [unchanged]

Linear KV up / Split K,V
K128 + k64; V128

K3 图中原注释：Learned up projection
Split K,V

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_port_q [unchanged]

Q

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_port_k [unchanged]

K

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_port_v [unchanged]

V

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_attention [added]

Sparse causal attention (NoPE)
selected token positions

K3 图中原注释：Global causal attention (NoPE)

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## mla_gate [unchanged]

Linear Wg

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_sigmoid [unchanged]

Sigmoid

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_mul [unchanged]

×

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_wo [unchanged]

Linear Wo → y [T, 7168]

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_note [unchanged]

Q rank 1536 · KV rank 512 · output gate retained
Conceptual unabsorbed view; no rotary operation

K3 图中原注释：Conceptual unabsorbed view; exact projection ranks pending config.

- [§2.1.2, equation 7 (unabsorbed conceptual view)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_input [unchanged]

Images / video

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_processor [unchanged]

ImageProcessor

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_patch [unchanged]

Patch embedding
(patch 14)

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_pool [unchanged]

Temporal pooling
+ 2 × 2 pixel shuffle

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_projector [unchanged]

MLP projector

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## text_input [unchanged]

Text

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## text_tokenizer [unchanged]

Tokenizer

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## text_embedding [unchanged]

Text embedding
[Ttext, 7168]

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_merge [unchanged]

+

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitattn0 [unchanged]

Input
x

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitattn1 [unchanged]

Linear QKV
(bias-free)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitattn2 [unchanged]

Spatial /
temporal
attention

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitattn3 [unchanged]

Linear Wo →
output

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitffn0 [unchanged]

Input
x

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitffn1 [unchanged]

Linear up

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitffn2 [unchanged]

GELU
(schematic)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vitffn3 [unchanged]

Linear down →
output

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_caveat [unchanged]

Vision config unchanged; projector type patchmergerv2

K3 图中原注释：Vision FFN / projector internals not weight verified.

- [§2.4 and Table 1 (vision path; exact FFN implementation not verified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## sources [unchanged]

K3.1-Pro config / card @ d9e99b0 · K3 @ f831ab6 · SGLang @ b09bda7 · weight index / full weights not read

K3 图中原注释：Source: MoonshotAI/Kimi-K3 report §§2.1–2.4, Table 1 · 3cb39df · Config / weights not verified

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## k_input [unchanged]

xₗ

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## m_input [unchanged]

xₗ

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## representative_label [unchanged]

Representative layer detail
(explanatory insets)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## output_gate_note [unchanged]

Output gate
(separate from
five KDA
inputs)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## expert_heading [unchanged]

Expert FFN
(SiTU-GLU)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## moe_notes [unchanged]

Shared experts bypass latent down/up.
Routed experts operate in 3584-dimensional space.

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_out [unchanged]

Visual embedding [Tvis, 7168]

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_enc_norm1 [unchanged]

RMSNorm

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_enc_attn [unchanged]

Spatial / temporal attention

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_enc_add1 [unchanged]

Residual add

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_enc_norm2 [unchanged]

RMSNorm

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_enc_ffn [unchanged]

FFN (schematic)

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_enc_add2 [unchanged]

Residual add

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## vision_fused_detail [unchanged]

Fused sequence
(text + visual tokens)

- [§2.4 (schematic reconstruction; exact implementation unverified)](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_merge [unchanged]

+

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_text [unchanged]

Text

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_tokenizer [unchanged]

Tokenizer

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_embed [unchanged]

Embedding

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_textvec [unchanged]

Text embedding

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_images [unchanged]

Images / video

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_pool [unchanged]

Pool / shuffle

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_projector [unchanged]

MLP projector

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mini_visvec [unchanged]

Visual embedding

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_embedding [unchanged]

Embedding

- [§2.2, equation 10](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_blocks [unchanged]

Completed
block sums

- [§2.2, equation 10](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## ar_partial [unchanged]

Current
partial sum

- [§2.2, equation 10](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)

- [Shared topology/config values checked against pinned K3 config; see baseline_k3_config.json and config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## mla_qnorm [unchanged]

RMSNorm
Qr [1536]

- [KimiMLAAttention.__init__/forward, lines 335–474](https://huggingface.co/moonshotai/Kimi-K3/blob/f831ab66814297da540d832a5235f8e904f29d06/modeling_kimi_linear.py)

## mla_qup [unchanged]

Linear Q up
1536 → 96 × 192

- [KimiMLAAttention.forward, 419–424](https://huggingface.co/moonshotai/Kimi-K3/blob/f831ab66814297da540d832a5235f8e904f29d06/modeling_kimi_linear.py)

## mla_kvnorm [unchanged]

RMSNorm (512)

- [KimiMLAAttention.forward, 426–443](https://huggingface.co/moonshotai/Kimi-K3/blob/f831ab66814297da540d832a5235f8e904f29d06/modeling_kimi_linear.py)

## mla_k64 [unchanged]

k64
NoPE

- [KimiMLAAttention.forward: unrotated shared k_rot channels, 426–450](https://huggingface.co/moonshotai/Kimi-K3/blob/f831ab66814297da540d832a5235f8e904f29d06/modeling_kimi_linear.py)

## diff_register_title [unchanged]

CHANGE REGISTER / K3 → K3.1-Pro

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## diff_added [added]

ADDED
Gated DSA ×24
Indexer + per-query TopK ≤2048

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## retired_dense_attention [removed]

RETIRED / K3 ONLY
Dense all-token attention
MLA latent projections are retained

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## diff_quant [parameter_changed]

CONFIG ONLY
MXFP4 exclusions: 6 →8 rules

K3 图中原注释：PARAMETER / CONFIG ONLY
Quantization ignore patterns: 6 → 8

- [/text_config/quantization_config/ignore; two additional regex patterns](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

- [/text_config/quantization_config/ignore; two additional regex patterns](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## diff_count [parameter_changed]

ADDED INDEXER PARAMETERS
+178.53M BF16 elements
(provider metadata; source-derived match)

K3 图中原注释：HF BF16 tensor-elements
57,179,884,544 → 57,358,410,752
+178,526,208 (matches new indexer)

- [safetensors.parameters.BF16; compare pinned baseline metadata; derived indexer count in checkpoint_summary.json](https://huggingface.co/api/models/moonshotai/Kimi-K3.1-Pro/revision/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e)

- [safetensors.parameters.BF16; compare pinned baseline metadata; derived indexer count in checkpoint_summary.json](https://huggingface.co/api/models/moonshotai/Kimi-K3.1-Pro/revision/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e)

## diff_unchanged [unchanged]

UNCHANGED
93 layers · KDA69 · hidden7168
896 experts / top16 · latent3584
MoonViT-V2 · context1M

- [Shared fields equal across both pinned configs; see config_diff.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## dsa_indexer_title [added]

ADDED · DSA Indexer (per DSA layer)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## idx_scope [added]

32 heads ×128 · NoPE · no Hadamard

- [_init_dsa, lines 137–174](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/configs/kimi_linear.py)

- [_init_dsa, lines 137–174](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/configs/kimi_linear.py)

## idx_qr [added]

Qr [1536]

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_h [added]

h [7168]

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_qproj [added]

Linear Wq
1536 →4096

K3 图中原注释：Linear Wq
1536 → 32×128

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_qquant [added]

FP8 Quant

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_q [added]

Qᵢ [32,128]

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_kproj [added]

Linear Wk
7168 →128

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_knorm [added]

LayerNorm

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_kquant [added]

FP8 Quant

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_cache [added]

Index K cache
[T,128]

K3 图中原注释：Index key cache
[T,128]

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_wproj [added]

Linear (weights)
7168 →32

K3 图中原注释：Linear Wweights
7168 →32

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_scale [added]

Scale
1 / sqrt(32×128)

K3 图中原注释：Scale
32^-0.5 ×128^-0.5

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_weights [added]

w [32]

K3 图中原注释：Head weights [32]

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_dot [added]

Matmul (Qᵢ, Kᵢᵀ)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_relu [added]

ReLU

- [relu2_fma_f32x2 and epilogue weighted head reduction, 180–190 / 1416–1542](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/kernels/ops/attention/dsa/cutedsl_fp8_paged_mqa_logits.py)

- [relu2_fma_f32x2 and epilogue weighted head reduction, 180–190 / 1416–1542](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/kernels/ops/attention/dsa/cutedsl_fp8_paged_mqa_logits.py)

## idx_sum [added]

Weighted sum (heads)

K3 图中原注释：Scale by head weights → Sum (heads)

- [relu2_fma_f32x2 and epilogue weighted head reduction, 180–190 / 1416–1542](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/kernels/ops/attention/dsa/cutedsl_fp8_paged_mqa_logits.py)

- [relu2_fma_f32x2 and epilogue weighted head reduction, 180–190 / 1416–1542](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/kernels/ops/attention/dsa/cutedsl_fp8_paged_mqa_logits.py)

## idx_mask [added]

Causal mask

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## idx_topk [added]

TopK (≤2048) → token indices

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

- [Indexer.__init__, lines 272–410; _get_q_k_bf16, 930–1027; forward_cuda, 1983–2320](https://github.com/sgl-project/sglang/blob/b09bda75c89a88263811a49e13adeef7a7aa8bf7/python/sglang/srt/layers/attention/dsa/dsa_indexer.py)

## scope_panel_title [unchanged]

READING THIS DIFF

- [Model Summary, Attention-Layer Composition and footnote: full-attention Gated MLA replaced by Gated DSA](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

## scope_text [unchanged]

Color = model delta, not a claim
of changed hidden/expert dimensions.
Green nodes are historical only.
Index Q/K quantization is engine-specific.

- [config_diff.json + pinned SGLang Indexer backend](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/config.json)

## scope_limits [unchanged]

Config + model card + engine checked.
No full weights or tensor headers read.
No GPU inference executed.

- [Source inventory and checkpoint_summary.json](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/README.md)

