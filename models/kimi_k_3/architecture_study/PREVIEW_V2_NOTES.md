# Preview v2 修订说明

本次以 `kimi_k3_design_preview.png` 的视觉风格为基础修订，不将 SVG 导出版本当作替代品。旧设计稿另存为 v1，v2 为新的设计预览。

## KDA 的五条输入路径

以下来自技术报告 §2.1.1，Eq. 1、2、5、6。箭头按图中要求从下向上连接。

| 路径 | 从输入 x 到 KDA 核心的运算 |
| --- | --- |
| Q | Linear Wq → ShortConv → Swish/SiLU → L2Norm → Q |
| K | Linear Wk → ShortConv → Swish/SiLU → L2Norm → K |
| V | Linear Wv → ShortConv → Swish/SiLU → V；不做 Q/K 的 L2Norm |
| α（通道遗忘系数） | Linear Wα↓ → Linear Wα↑ → head bias bα → z → g = −5 sigmoid(exp(A)z) → α = exp(g) |
| β（写入强度） | Linear Wβ → Sigmoid → β |

KDA 的固定大小状态更新为：

`S_t = (I − β_t k_t k_tᵀ) Diag(α_t) S_(t−1) + β_t k_t v_tᵀ`

`o_t = S_tᵀ q_t`

**输出门是另外一条旁路，不属于上述五个 KDA 核心输入**：

`x → full-rank Linear W_g → Sigmoid`

该旁路与核心输出的 head-wise RMSNorm 结果逐元素相乘，再经 Linear W_o 输出。报告明确 K3 的输出门采用 full-rank projection，不能直接照搬旧模型的低秩输出门。

## 其他修订要求

- AttnRes、MoE、MLA、视觉模块均改为下方输入、上方输出，主干保持从下向上。
- MoE 保留 2 个全维共享专家与 896 选 16 的潜空间路由专家，并明确聚合后 RMSNorm、再上投影。
- MoE 的 router 与 latent down projection 都直接读取原始 x，属于并行分支；router 的选择和权重连接专家与聚合，不能画作 `x → router → down projection`。
- AttnRes 的 learned pseudo-query 是独立参数，与 RMSNorm(keys) 一起进入 depth logits；不能画作 source → pseudo-query → RMSNorm。
- Gated MLA 保留报告确认的 NoPE，不恢复旧参考 JPG 中的 RoPE 分支。
- 原图用于布局、详细程度和阅读顺序参考；不能用来补齐未经核实的 projection ranks 或视觉张量维度。
- 图像生成稿中的连线与公式仍应对照上述文字及报告核查；尚未读取 Hugging Face 配置和权重索引。

来源：[Kimi-K3 技术报告（固定提交）](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)。
