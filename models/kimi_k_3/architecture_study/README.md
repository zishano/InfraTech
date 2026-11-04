# Kimi K3 架构图核对试作

此目录保留可编辑 SVG 和生成脚本，不覆盖上一级已有 JPG。图的布局沿用“主干 + 周边模块展开 + 底部视觉分支”的组织方式。

## 文件

- `kimi_k3_design_preview_v2.drawio`：按 v2 模块结构重建的原生可编辑图，使用标准、未压缩的 draw.io XML，供飞书白板的 draw.io 导入入口使用；包含五路 KDA、独立输出门、MoE、MLA、AttnRes 和视觉分支。已检查 XML 与节点引用，未在实际飞书客户端验证导入。布局为原生节点重排，并非 PNG 的逐像素复刻。
- `draw_architecture_drawio.py`：生成上述 `.drawio` 的 Python 标准库脚本。
- `kimi_k3_design_preview.png`：当前视觉设计稿；v2 按用户要求细化 KDA 五路输入，并统一从下向上的数据流。对应说明见 `PREVIEW_V2_NOTES.md`。
- `kimi_k3_design_preview_v1.png`：保留的第一版视觉设计稿。
- `kimi_k3_design_preview_v2.png`：第二版视觉设计稿的独立文件。
- `kimi_k3_architecture.svg`：第一版可编辑文字与矢量模块，尚未同步 v2 细节；本次审阅以设计预览 v2 为准。
- `draw_architecture.py`：仅依赖 Python 标准库的 SVG 生成脚本。运行 `python draw_architecture.py` 可重建。
- `kimi_k3_architecture.png`：SVG 的高清导出（若已生成）。

## 实际核对过的来源

1. [MoonshotAI/Kimi-K3 官方仓库](https://github.com/MoonshotAI/Kimi-K3/tree/3cb39dfd32e51c3328e2e4b4af21341247d06c43)。检查时仅有 README、LICENSE、技术报告和 logo，没有模型实现。
2. [技术报告 PDF](https://github.com/MoonshotAI/Kimi-K3/blob/3cb39dfd32e51c3328e2e4b4af21341247d06c43/k3_tech_report.pdf)：§2.1 / §2.1.1 / §2.1.2 / §2.2 / §2.3 / §2.4 和 Table 1。下面的具体结构均以这份报告为依据。
3. [Transformers 模型目录](https://github.com/huggingface/transformers/tree/f2754311602414ed561cdf8ed9d852390f514404/src/transformers/models)：完整检查该提交的目录树，找到 `kimi_k25`、`kimi_linear`，未找到独立 `kimi_k3` 实现。**没有将 K2.5 或 Kimi Linear 的源码当成 K3 的源码。** 此结论只针对这个提交及所检查的模型目录。
4. 用户指定的 [Hugging Face 模型页](https://huggingface.co/moonshotai/Kimi-K3)：本机访问模型配置、模型卡及文件列表均被代理策略以 403 阻止。因此**尚未读取 config.json、权重索引、权重张量形状或模型自定义实现**；不能称为权重核验版。

## 核对结果与原图差异

| 项目 | 报告支持的内容 | 本图处理 |
| --- | --- | --- |
| 主干 | §2.1：每组 3 KDA + 1 Gated MLA，末尾额外一个 Gated MLA；Table 1：69 KDA、24 MLA、93 层 | 画作 23 组 + 末尾 MLA，不在 93 层之外再添加一层 dense attention |
| FFN | 官方 README / Table 1：1 个 dense layer；其余采用 MoE | 标注 92 MoE FFN + 1 dense FFN；未映射其准确层号，等待 config / 实现确认 |
| MLA 位置编码 | §2.1.2 明确所有 MLA 层采用 NoPE | 删除原 JPG 的 RoPE / PE cache 分支；不沿用原图中未经此次核验的 q/kv rank 和 head dimension |
| MLA 输出门 | §2.1.2 Eq.7：`W_o[sigmoid(W_g x) ⊙ attention_output]`，W_g 为 full-rank | 明确门控发生在输出投影之前 |
| KDA | §2.1.1：Q/K/V 有 ShortConv + Swish；Q/K L2Norm；通道衰减；head-wise RMSNorm；full-rank sigmoid 输出门 | 展开这些处理。衰减采用 Eq.5 的下界 sigmoid 参数化，不沿用旧 Kimi Linear 的输出门结构 |
| Stable LatentMoE | §2.3 Eq.11：路由专家在 3584 潜空间计算，聚合后 RMSNorm，再上投影；2 个共享专家处理全维输入 | 两条支路分开，避免把共享专家误放到潜空间或让其经过共享 down/up 投影 |
| AttnRes | §2.2：block sums + 当前 partial sum；归一化 keys，learned pseudo-query，depth softmax，加权原始 values | 单独画深度聚合；不与 token attention 混淆。没有声称组装出的图等于精确执行图 |
| Vision | §2.4 / Table 1：MoonViT-V2 27 层 / 401M / 12 heads / patch 14；无 bias 的线性和注意力投影；时空注意力；temporal pooling；2×2 pixel shuffle；MLP projector | 画出报告支持的拓扑，不推定视觉 hidden width、具体 head dim 或 projector 的精确张量形状 |
| MTP | Table 1：1 MTP layer | 单独标记辅助模块，不加到主干 93 层中 |

总参数、激活参数分别使用报告 Table 1 的 2.78T、104.2B；官方 README 中的 2.8T、104B 是取整表达。

## 尚未完成的核验

需要环境允许访问 `huggingface.co` 后，读取模型配置和 safetensors 权重索引，必要时只读取张量头部，以确认：模型类 / 自定义实现、精确 layer_types、dense FFN 层号、Q/K/V projection rank、cache tensor shape、视觉 hidden width、参数名称及模块对应关系。无需为此下载全量 2.78T 权重。

网络配置草稿已新增 `huggingface.co` 与 `api.github.com`；草稿保存不等于当前实例网络立即生效。

SVG 是用于结构审阅的可编辑交付；另外生成的图像设计稿应以本 SVG 和本说明的事实为准。此试作未运行模型推理，未校验完整权重，也未修改原 README 或原架构 JPG。
