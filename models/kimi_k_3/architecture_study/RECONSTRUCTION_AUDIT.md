# Preview v2 重建与配对核对

## 源文件及当前结果

- 转录参考：`kimi_k3_design_preview_v2.imagegen_reference.png`（旧生成式图）。
- 可编辑重建：`kimi_k3_design_preview_v2.drawio`，原生节点/连线，无整图位图节点。
- 正式 PNG：`kimi_k3_design_preview_v2.png`，由该 XML 直接通过 mxGraph / Chromium 渲染。
- 配对记录：`kimi_k3_design_preview_v2.export.json`。

**人工转录不等于像素无损恢复。** 已按旧 PNG 的模块分区、相对位置和可读计算路径重建；字体、曲线、文字换行及部分布局留白与原位图不同，不能宣称与旧 PNG 逐像素一致。当前能够验证的是：新的正式 PNG 完全由配对的原生 draw.io 解码渲染，而不是独立生成另一张结构图。

## 已核对的结构

| 原图区域 | 原生图对应 | 核对点 |
| --- | --- | --- |
| KDA 五条核心输入 | `kda_port_q/k/v/alpha/beta` → `kda_core` | Q/K/V、α、β 均为各自独立路径；Q/K 有 L2Norm，V 无 |
| α | `kda_alpha_down/up/bias/scale/sigmoid/exp` | 两个投影后加 bias、乘 exp(A)、−5 sigmoid、最后 exp(g) |
| 独立输出门 | `kda_gate_linear` → `kda_gate_sigmoid` → `kda_product` | 门控与核心输出的 head-wise RMSNorm 结果相乘，再经 Wo |
| AttnRes | `ar_embedding/ar_blocks/ar_partial`、keys/query/values 路径 | 三路来源、独立 pseudo-query、原值旁路分别可编辑 |
| Stable LatentMoE | `moe_router/moe_down/moe_shared` 三路 | router 不串在 down projection 前；聚合后 RMSNorm，再上投影 |
| Gated MLA | Q / compressed KV / output gate | 单个 KV 压缩分支、独立输出门、NoPE，不添加 RoPE |
| 主干与代表性层说明 | `lm_repeat/lm_final` 和 `k_*/m_*` | 主干只表达 23 组 + final MLA；代表性展开为独立说明，不作为额外执行层串入主干 |
| 视觉区 | `vision_*` / `vitattn*` / `vitffn*` | PatchEmbed、编码器、pool/shuffle、projector 及文字融合路径；具体实现未权重验证，保留 schematic 提示 |

未确认参数仍保持未确认，不因重建变成已知事实。视觉区极小文字、公式的排版细节和图像生成的笔画不作无损还原承诺。

## 后续一致性规则

修改 draw.io 后必须重新导出 PNG。配对校验检测任何单边文件修改；不替代模型语义核验、原图人工转录核验或飞书客户端验证。具体命令见同目录 README。
