# 可复用的开源模型架构图工作流

把模型资料、证据、结构描述和绘图分开保存。资料收集、提取及 draw.io/SVG 使用 Python 3.10+ 标准库；正式 PNG 导出另需 Playwright、Chromium 和固定版本 mxGraph。不运行远端模型代码，不下载完整权重，不要求绘图 API key。

## 后续模型从这里开始

先阅读 [绘图规范与经验](WORKFLOW.md)：它将来源核验、具体算子审阅、版本差异、软硬协同口径、字体布局、直线优先及同源交付整理成统一流程。Kimi／DeepSeek 的特定参数与计算不能直接套用到其他模型。

```bash
python tools/model_architecture/model_architecture.py init-study org/NewModel \
  --revision CHECKED_REVISION --out /workspace/new-model-study

# 有旧版基线时：
python tools/model_architecture/model_architecture.py init-study org/NewModel \
  --revision NEW_REVISION --baseline org/OldModel \
  --baseline-revision OLD_REVISION --out /workspace/model-diff-study
```

生成 `sources.json`、`review.json`、`architecture_review.md`；有基线时另生成 `baseline.sources.json`。所有检查均为 `pending`，不会联网、执行模型、自动认定结构或覆盖已有文件。`main` 仅作发现入口，正式证据需要固定版本。

随后按本文的 `collect → extract → draft → validate/render → export-png → verify-png` 流程执行。基线和目标的资料应分别收集到不同目录，防止同名文件／source ID 覆盖。`review.json` 保存结构、缓存、版本差异与新增／沿用／后端优化的审阅记录，不能替代真实源码核对。

## 已支持的自动化

1. `init-study`：创建带来源、拓扑、差异、优化声明及交付检查项的新模型审阅工作区，所有项目保留待核对状态。
2. `init`：根据 Hugging Face `owner/model` 创建资料清单，包含 config、模型卡、safetensors 索引，可附官方 GitHub README。
3. `collect`：下载清单明确指定的公开 HTTPS 资料，保留最终 URL、SHA-256、可用时的 HF commit；每文件上限 32 MiB。失败写入 inventory，不伪造成功。
4. `extract`：从 config 提取嵌套作用域中的参数、JSON Pointer 和来源；保留同名/冲突字段。从权重索引提取张量名数量、模块前缀、分片数量。
5. `draft`：生成明确标注“不完整”的参数摘要与结构审阅骨架。
6. **人工/AI 审阅源码与报告，补全 graph JSON。** 这一环节不能用 config 字段或权重名代替；五路 KDA、输出门、MoE 路由都是此次实际遇到的例子。
7. `validate` / `render`：检查证据、几何及连接引用，输出 `.drawio`、`.svg` 和证据报告。
8. **正式 PNG 只从 draw.io XML 导出**：使用 `export-png`，保存来源/图片 SHA-256、节点数、连线数及渲染版本，再用 `verify-png` 检查配对。禁止独立生成正式 PNG 的计算结构。

**不会声称仅输入模型名就能无误地恢复任意模型完整计算图。** 配置声明、报告结构、实际 `forward()`、部署框架的融合实现可能不同；渲染器不负责替你裁决差异。

## 新模型使用步骤

在仓库根目录执行，工作文件建议放到仓库外：

```bash
python tools/model_architecture/model_architecture.py init org/NewModel \
  --revision main --github org/ModelRepository \
  --out /workspace/new-model/sources.json
```

审阅 `sources.json`：将 `main` 改为已核对的 HF revision / GitHub commit；添加模型的 `configuration_*.py`、`modeling_*.py`、processor、报告等具体文件链接。GitHub raw 形式为 `https://raw.githubusercontent.com/owner/repo/COMMIT/path`。来源种类使用 `config`、`weight_index`、`documentation`、`implementation` 或 `configuration_code`。后者只用 AST 读取 Python 配置类的字面量默认值，不执行 import、类体、函数调用或 `__post_init__`；提取结果标注为 source class default，不能冒充 checkpoint 配置。报告 PDF 可以收集后用 `pdftotext` 阅读。不要将 `.py` 下载后直接 import 或启用 `trust_remote_code`。

首次发现路径可从 HF 模型文件列表、config 的 `auto_map` 和 `architectures` 入手，再查看 Transformers 或官方仓库对应模型目录。路径发现和源码语义分析目前由使用者/AI 执行，不是此脚本的自动搜索能力。不要把相似模型的实现冒充为目标模型实现。

```bash
python tools/model_architecture/model_architecture.py collect \
  /workspace/new-model/sources.json --out /workspace/new-model/sources
python tools/model_architecture/model_architecture.py extract \
  /workspace/new-model/sources --out /workspace/new-model/facts.json
python tools/model_architecture/model_architecture.py draft \
  /workspace/new-model/facts.json --out /workspace/new-model/architecture.graph.json
```

`collect` 返回码 2 表示必需资料获取失败；仍保留成功项和失败记录，先解决具体网络/权限问题。不存在标准 `model.safetensors.index.json` 的单文件模型或其他命名模型，需要调整清单；索引为可选，不应据此认定模型不存在。不得绕过 TLS 验证或网络策略。公开资料收集不需要将密钥放入 JSON；私有模型认证不属于当前下载器功能。

接下来依据源码/报告编辑 `architecture.graph.json`，替换占位符、增加分支及来源。完成审阅后：

```bash
python tools/model_architecture/model_architecture.py validate /workspace/new-model/architecture.graph.json
python tools/model_architecture/model_architecture.py render \
  /workspace/new-model/architecture.graph.json --out /workspace/new-model/output
```

产物：

- `architecture.drawio`：标准未压缩 XML，原生节点和连线，可编辑；可尝试从飞书 draw.io 导入入口导入，尚未做飞书客户端自动化验证。
- `architecture.svg`：矢量结构图，由同一份 graph 生成；使用简单文字换行和正交连线，不承诺像素级还原设计预览。
- `evidence.md`：节点证据状态、定位信息、来源和限制。
- `image_prompt.txt`：现在只保留“正式 PNG 必须从 draw.io 导出”的提示；不再指示图像工具独立生成架构图。旧版生成式图片只能作为单独标注的风格/人工重建参考。

## Kimi-K3 可直接复现示例

```bash
python tools/model_architecture/model_architecture.py render \
  tools/model_architecture/examples/kimi_k3.graph.json \
  --out /workspace/kimi-k3-reproduced
```

示例现按原 preview PNG 的模块位置和可读分支重建为原生图元，保留 KDA 五输入及独立输出门、Block AttnRes、潜空间 MoE、NoPE MLA 和视觉分支。代表性层展开为独立说明框，不再错误串入主干。原生成式 PNG 单独存档；重建不是像素无损恢复。证据基于已读取的固定提交技术报告；HF config/权重索引未读，精确投影维度、dense 层位置、视觉 FFN 细节仍待确认。示例不是新完成的权重核验结果。

无需联网的参数提取演示（合成测试配置，不是实际模型）：

```bash
python tools/model_architecture/model_architecture.py extract \
  tools/model_architecture/tests/fixtures --out /workspace/fixture-facts.json
python tools/model_architecture/model_architecture.py draft \
  /workspace/fixture-facts.json --out /workspace/fixture.graph.json
```

## Graph 数据约定

见 [GRAPH_FORMAT.md](GRAPH_FORMAT.md)。一个 graph 由 `sources`、`nodes`、`edges`、画布尺寸和 `limitations` 组成。节点使用 `verified`、`inferred`、`unverified` 三种证据状态；`verified` 必须指向具体资料和定位。状态代表**人工审阅声明**，校验器只能检查结构，不能证明报告或源码语义正确。

权重索引只有 tensor 名称及 shard 映射，不能提供 tensor shape；也不能用文件字节数直接推出参数量。真正的 shape 检查需后续增加 safetensors header 读取适配器，并明确量化、打包和共享权重规则。当前版本没有实现该功能。

## 验证

```bash
python -m unittest discover -s tools/model_architecture/tests -v
```

覆盖嵌套 config、字段冲突、来源哈希变更、索引与形状的区别、下载失败、路径/完整权重下载拒绝、悬空连线、证据缺失及可编辑产物输出。进一步扩展模型时，优先增加该模型真实资料的脱敏小样例和拓扑不变量测试。

## 正式 PNG 导出：draw.io 是结构源文件

一次性安装渲染依赖（TLS 和 npm 完整性校验保持开启）：

```bash
python -m pip install -r tools/model_architecture/requirements-render.txt
npm install --prefix /workspace/.cache/model-architecture-renderer \
  --ignore-scripts --no-audit --no-fund mxgraph@4.2.2
```

需要一个可用 Chromium。当前环境使用 `/usr/bin/chromium`；其他机器可通过 `--browser` 指定其可执行文件，或先使用 Playwright 支持的浏览器安装方式。`--mxgraph` 可指定 npm 包的 `javascript/src` 目录。

```bash
python tools/model_architecture/model_architecture.py export-png \
  /workspace/new-model/output/architecture.drawio \
  --out /workspace/new-model/output/architecture.png --scale 3
python tools/model_architecture/model_architecture.py verify-png \
  /workspace/new-model/output/architecture.drawio \
  /workspace/new-model/output/architecture.png \
  /workspace/new-model/output/architecture.export.json
```

导出时由 mxGraph 4.2.2 在 Chromium 中**直接解码 draw.io XML**，并检查解码后的节点数与边数。渲染不访问远端图片/字体，不允许用整张图片节点替代架构图。PNG 后缀对应的 `.export.json` 保存两份文件的哈希，任一文件导出后被单独修改，配对检查就会失败。哈希验证检测文件漂移，不证明公式、分支或模型事实正确。

支持原生未压缩 XML 的第一个页面；不支持压缩页、以图片替代图元的文件或任意 diagrams.net 插件。简单图元的显示由 mxGraph 决定；飞书和 diagrams.net 的字体/主题可能略有不同，未宣称与旧生成式位图逐像素相同。

**以后每次更新：改 draw.io → export-png → verify-png → 结构/视觉审阅 → 提交并推送用户指定分支。** 若选择通过 graph JSON 重建 draw.io，应先把 draw.io 中的人工修改同步回 JSON，避免重生成时丢失。

## 导出前的版式检查

`export-png` 现在会测量实际渲染的文字边界和连线，并在以下情况拒绝导出：文字超出节点、文字到边界的最小留白少于 2 个原生坐标单位、正交连线出现斜向错位线段，或连线穿过无关运算节点。诊断保存在 PNG 同名 `.layout.json`；配对 manifest 包含其哈希，`verify-png` 也会校验它。

容器背景、标题、图例等应在 graph JSON 中标记 `kind: "decoration"`，生成器自动写入 `architectureDecoration=1` 样式，避免将合法背景容器误判为运算节点。导入外部原生 XML 时也需标记这类非运算背景。布局检查不能证明架构语义正确，也不保证其他客户端的字体渲染完全相同。

## 第二个模型测试：DeepSeek-V4-Flash

见 [源码核对版交付](../../models/deepseek_v4/flash/README.md) 和 `examples/deepseek_v4_flash.graph.json`。新增 `configuration_code` 收集类型可在 checkpoint config 暂不可读时提取框架配置类默认值；每项保存声明行号和 `source_class_default_not_checkpoint` 标签。不会运行初始化逻辑或自动推断逐层排布。

初版仅有 Transformers 类默认值；网络放行后，现已收集官方 Flash 固定提交的 checkpoint config、推理 config、model.py、kernel.py、模型卡和权重索引，并与框架默认值分开保留。图现包含精确 43 层排布、MTP 和量化模拟路径；权重索引交叉核对覆盖全部主干层，但未读取 tensor shape 或数值。

### Hugging Face 缓存重定向

初始资料 URL 仍要求公开 HTTPS 且不带查询参数或内嵌凭据。响应可能正常跳转到 `api/resolve-cache/...?...etag...`；收集器现在验证重定向的 HTTPS 目标并接受这种响应，但保存最终 URL 时剥离全部查询参数，避免将签名或凭据记录到 inventory。文件 SHA-256 和 resolved_revision 仍保留。不会关闭 TLS、绕过代理或放宽完整权重下载限制。

### DeepSeek CSA / HCA 详细页

`examples/build_deepseek_v4_attention_detail.py` 将固定官方提交的 Compressor、Indexer、Attention、sparse_attn 分拆为原生算子，生成 CSA/HCA graph JSON。`models/deepseek_v4/flash/rebuild.py` 同时构建独立详细 draw.io 和三页总图；独立详细 PNG 必须从对应 XML 使用 `export-png` 导出。总图 PNG 导出首页，详细页各有独立 PNG 和配对检查记录。

大图跨面板的数据通过 `port_bindings` 元数据及可见 A / I / Qr 同名端口关联，分别代表完整压缩 KV、压缩位置索引和归一化低秩 query；端口不是额外网络层。模型专用测试检查端点存在、值旁路、CSA 独立 Indexer、HCA 无 Indexer、窗口实例及总图详细页与独立 XML 一致。通用新模型仍需审阅官方 forward 的真实分支，再配置布局，不能只替换模型名称和参数。

`examples/deepseek_operator_style.py` 是当前 DeepSeek 的算子展示层：参考已有 JPG 的模块配色、虚线边框和算子符号，显示短标签，完整注释保留在 `description`。两个构造器均调用它，rebuild 同步生成详细说明文档；PNG 仍从原生 XML 导出。

`examples/deepseek_visual_layout.py` 负责紧凑布局：短算子块、模块色描边、少量重点强调，以及原生张量格状态示意。它保留原节点描述和计算边，仅重排几何和分支走线；两个模型专用构造器统一使用该展示层。

`examples/deepseek_page_reflow.py` 负责页面编排：总览主干居中、mHC/MoE 在左、注意力/压缩器在右；详细页将注意力放在压缩器和索引器之间，并统一标题、模块间隔及底部状态区。重排后须再次运行严格导出及节点避让测试。


### 版本差异架构图

`model_diff.py` 提供 `compare_configs(before, after)` 的 JSON Pointer 逐字段差异，以及 `mark(node, change, source=..., locator=...)` 的红／绿／黄原生样式：`added`、`removed`、`parameter_changed`。这些是展示语义，不会把配置字段删除自动判成网络层删除。需要结合固定模型卡和实际实现审阅后再给图元分类。

Kimi-K3.1-Pro 的实例为 `examples/build_kimi_k31_pro.py`：继承 `kimi_k3.graph.json` 的模块几何，保留原图；公共部分用中性色，新增 DSA 用红色，旧全注意力用绿色独立退役框，参数／配置统计用黄色。颜色语义及来源随 `architecture_diff.json` 一起保存。`drawio` 支持边的 `color`（六位十六进制）字段，用于让新增路径的连线也遵循相同主题。

```bash
python tools/model_architecture/examples/build_kimi_k31_pro.py
python models/kimi_k_3_1_pro/rebuild.py
python tools/model_architecture/model_architecture.py export-png \
  models/kimi_k_3_1_pro/kimi_k31_pro_architecture.drawio \
  --out models/kimi_k_3_1_pro/kimi_k31_pro_architecture.png --scale 1.5
```


连线简化可调用 `routing.simplify_connections(graph)`，优先对齐端口直连，再寻找无障碍的单折点路径；不会增删模型计算边。图中 `routing: "straight"` 表示让 draw.io 按显式端口及可选 waypoint 绘制，关闭自动增加的绕线。必须继续通过 mxGraph 实测布局检查。Kimi 的展示层示例见 `examples/kimi_k31_presentation.py`。

### GLM-5.1 示例

[GLM-5.1 官方checkpoint核对图](../../models/glm_5_1/README.md) 由 `examples/build_glm51.py` 构建，沿用新的审阅模板与直线优先工具。覆盖78层、3 Dense +75 MoE、带interleaved RoPE的三路DSA Indexer、普通残差与SwiGLU，并将仅核对权重模块存在性的辅助MTP与主forward分开。不能将Kimi索引器的NoPE或DeepSeek压缩器假设套入本例。

节点自适应排版使用 `operator_layout.fit_operators(graph, roles, font=20)`：构造器为Attention/MoE等明确指定composite角色，其余按算子名称选择简单算子／投影／聚合／缓存等视觉类别。在预留lane内调整宽高，保持中心对齐；长标签先换行，再视需要调整字号。它不改变计算边或证据，也不能替代逐图视觉判断和浏览器测量。GLM-5.1已使用该策略。

**已认可的默认排版参考**：GLM-5.1 的 `f4caaa9` 版本。后续绘图优先采用“按算子复杂度与文本定框 → 主链／分支对齐 → 直线优先 → 实测导出检查”，详见 [WORKFLOW.md](WORKFLOW.md) 的“用户认可的排版参考”。通用实现为 `operator_layout.py`，模型构造示例为 `examples/build_glm51.py`。

### GLM-5.2 / IndexShare 示例

[GLM-5.2架构图](../../models/glm_5_2/README.md) 与 `examples/build_glm52.py` 展示同一模型家族的安全复用：先核对共享核心字段与固定实现，再显式加入目标配置的21 FULL /57 SHARED层、首层例外、1M上下文和theta8e6。IndexShare说明带表示同一次查询的位置传递，不是KV共享或额外主干层；MTP迭代共享仅按已核对范围标注。

### GLM-5.3 / 相同基座与量化发布

[GLM-5.3架构图](../../models/glm_5_3/README.md) 与 `examples/build_glm53.py` 示范：用完整核心配置和实现哈希断言复用，区分后训练能力、FP8发布配置与网络结构。目标权重索引获取失败时明确保留边界，基线索引不能改名冒充本版权重证据。
