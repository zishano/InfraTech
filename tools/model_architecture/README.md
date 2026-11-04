# 可复用的开源模型架构图工作流

把模型资料、证据、结构描述和绘图分开保存。使用 Python 3.10+ 标准库，无额外依赖；不运行远端模型代码，不下载完整权重，不要求绘图 API key。

## 已支持的自动化

1. `init`：根据 Hugging Face `owner/model` 创建资料清单，包含 config、模型卡、safetensors 索引，可附官方 GitHub README。
2. `collect`：下载清单明确指定的公开 HTTPS 资料，保留最终 URL、SHA-256、可用时的 HF commit；每文件上限 32 MiB。失败写入 inventory，不伪造成功。
3. `extract`：从 config 提取嵌套作用域中的参数、JSON Pointer 和来源；保留同名/冲突字段。从权重索引提取张量名数量、模块前缀、分片数量。
4. `draft`：生成明确标注“不完整”的参数摘要与结构审阅骨架。
5. **人工/AI 审阅源码与报告，补全 graph JSON。** 这一环节不能用 config 字段或权重名代替；五路 KDA、输出门、MoE 路由都是此次实际遇到的例子。
6. `validate` / `render`：检查证据、几何及连接引用，输出同一 graph 驱动的 `.drawio`、`.svg`、证据报告和图像生成提示词。

**不会声称仅输入模型名就能无误地恢复任意模型完整计算图。** 配置声明、报告结构、实际 `forward()`、部署框架的融合实现可能不同；渲染器不负责替你裁决差异。

## 新模型使用步骤

在仓库根目录执行，工作文件建议放到仓库外：

```bash
python tools/model_architecture/model_architecture.py init org/NewModel \
  --revision main --github org/ModelRepository \
  --out /workspace/new-model/sources.json
```

审阅 `sources.json`：将 `main` 改为已核对的 HF revision / GitHub commit；添加模型的 `configuration_*.py`、`modeling_*.py`、processor、报告等具体文件链接。GitHub raw 形式为 `https://raw.githubusercontent.com/owner/repo/COMMIT/path`。来源种类使用 `config`、`weight_index`、`documentation` 或 `implementation`。报告 PDF 可以收集后用 `pdftotext` 阅读。不要将 `.py` 下载后直接 import 或启用 `trust_remote_code`。

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
- `image_prompt.txt`：可交给图像生成工具，配合 SVG 和参考图片制作美观 preview；脚本自身不调用图像服务。**图像稿必须逐项与 graph 核对，不作为反向恢复可编辑结构的来源。**

## Kimi-K3 可直接复现示例

```bash
python tools/model_architecture/model_architecture.py render \
  tools/model_architecture/examples/kimi_k3.graph.json \
  --out /workspace/kimi-k3-reproduced
```

示例由已有 v2 draw.io 的 130 个节点和 113 条边整理而来，保留 KDA 五输入及独立输出门、Block AttnRes、潜空间 MoE、NoPE MLA 和视觉分支。证据基于已读取的固定提交技术报告；HF config/权重索引未读，精确投影维度、dense 层位置、视觉 FFN 细节仍待确认。示例不是新完成的权重核验结果。

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
