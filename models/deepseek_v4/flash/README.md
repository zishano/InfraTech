# DeepSeek-V4-Flash：官方配置与推理实现核对版

当前模型资料已可正常访问。本目录现依据官方 checkpoint **`60d8d70770c6776ff598c94bb586a859a38244f1`** 的 `config.json`、`inference/config.json`、`inference/model.py`、`inference/kernel.py`、模型卡和权重索引生成，不再仅依赖 Transformers 的 Flash-Base 类默认值。

## 配对交付

- [PNG 架构图](deepseek_v4_flash.png)：从同名 draw.io XML 直接通过 mxGraph 4.2.2 / Chromium 导出。
- [原生可编辑 draw.io](deepseek_v4_flash.drawio)：128 个原生图元、112 条连接，无整图位图节点。
- [布局检查](deepseek_v4_flash.layout.json)、[配对记录](deepseek_v4_flash.export.json)：文字边界、留白、正交性、穿框和文件哈希。
- [官方 checkpoint 配置快照](official_config.json)、[官方推理配置快照](official_inference_config.json)。
- [逐层与权重索引核对摘要](checkpoint_summary.json)、[逐节点证据](evidence.md)。
- [来源清单](sources.json)、[文件获取结果 / SHA-256](source_inventory.json)、[参数提取结果](facts.json)。

完整源码及 5.3 MB 权重索引下载到运行缓存，不在此重复提交；通过来源清单可重取并校验 SHA-256。所有来源 URL 均为公开链接，不保存重定向中的查询参数。Transformers 固定提交资料仍留作对照，其类默认值在 facts.json 中继续单独标注，不能与实际 checkpoint 配置混淆。

## 官方配置确定的结构

| 项目 | 本次核对结果 |
| --- | --- |
| 主干 | 43 层；hidden 4096；64 个 Q heads、1 个共享 KV head；head dim 512 |
| 注意力排布（0-based） | L0–1：纯 SWA；L2–41：`[CSA4, HCA128] ×20`；L42：CSA4 |
| 统计 | 2 层纯 SWA + 21 层 CSA + 20 层 HCA；CSA/HCA 层也保留滑窗分支 |
| MTP | 独立 MTP0 的 layer_id=43，ratio=0；不是主干第 44 层。`compress_ratios` 总共 44 项包含它 |
| MoE | 256 routed experts，每 token 选 6 个；1 shared expert；intermediate 2048 |
| Hash 路由 | L0–2 由 token ID 查表选择专家，但激活权重仍由 learned score 计算；L3–42 使用 learned top-k |
| mHC | 4 个流，pre / post / comb 三组映射，Sinkhorn 20 iterations；残差采用 comb 转置方向 |
| 精度与规模 | 官方模型卡报告 284B total / 13B active / 1M context；routed expert 参数 FP4、其他多数参数 FP8。不是独立参数重计数或 1M 运行测试 |

**不能直接使用 `ModelArgs` 演示默认值。** 官方 `inference/model.py` 的类体含 7 层、8 routed experts、top-2 等演示默认值；真实 Flash 的两个配置文件为 43 层、256 routed experts、top-6。本版优先使用已读取的 checkpoint 配置和配套推理配置。

## 本次补全的图中细节

- Q 低秩投影及逐头归一化、尾部 64 维 RoPE；共享 K=V；局部非 RoPE 448 维的 FP8 模拟，RoPE 64 维保持 BF16；attention sink、输出逆 RoPE、grouped O_a/O_b。
- CSA 与 HCA 的独立 KV/gate 投影、窗口／缓存状态、gate softmax 及 KV 值旁路；压缩条目归一化、RoPE、FP8 模拟和缓存写入。
- CSA Indexer 的独立 Q、压缩 key、head scoring-weight 路径；**Hadamard 旋转和 FP4 QAT 模拟**；因果可见性与 top-k。HCA 无 Indexer。
- mHC 的 pre-collapse、post-expand、combᵀ residual mixing；注意力和 FFN 两处独立使用。
- Expert FFN 的并行 gate/up、不同 clipping 规则、SiLU；routed expert 在 down projection 之前乘 routing weight，shared expert 不乘该权重。
- 独立 MTP 分支：共享 embedding、enorm/hnorm、e_proj/h_proj、流广播相加、layer 43 Block、MTP 专有 HC-head 参数与 norm、共享 LM head。主干 `Transformer.forward` 不会自动执行 MTP。

官方 `Attention` 类的注释沿用 MLA 名称；图中按实际 `forward` 绘制共享 K=V 的单 KV 头路径，不添加旧式 KV-up/reconstruction 分支。

## 权重索引交叉核对

已读取 **69,187 个 tensor 名称与 46 个 shard 的映射**。索引实际使用 `layers.<id>.*` 和 `mtp.0.*` 前缀，不是先前猜测的 `model.layers.*`。

逐层核对结果见 checkpoint_summary.json：ratio=4 层存在 Indexer 与 compressor；ratio=128 层存在 compressor、没有 Indexer；ratio=0 层没有两者。Hash 查表权重出现在主干 L0–2。独立 `mtp.0.*` 有 1,575 个条目。这些是**模块名和分片关系**核对，不是张量形状或权重数值核验。

## 可复现步骤

从仓库根目录执行：

```bash
python tools/model_architecture/model_architecture.py collect \
  models/deepseek_v4/flash/sources.json --out /workspace/deepseek-v4-flash-sources
python tools/model_architecture/model_architecture.py extract \
  /workspace/deepseek-v4-flash-sources --out /workspace/deepseek-v4-flash-facts.json

# 已审阅图数据 → 原生 XML → PNG；不独立生成另一张结构图。
python models/deepseek_v4/flash/rebuild.py
python tools/model_architecture/model_architecture.py export-png \
  models/deepseek_v4/flash/deepseek_v4_flash.drawio \
  --out models/deepseek_v4/flash/deepseek_v4_flash.png --scale 1.5
python tools/model_architecture/model_architecture.py verify-png \
  models/deepseek_v4/flash/deepseek_v4_flash.drawio \
  models/deepseek_v4/flash/deepseek_v4_flash.png \
  models/deepseek_v4/flash/deepseek_v4_flash.export.json
```

图数据位于 `tools/model_architecture/examples/deepseek_v4_flash.graph.json`；同目录 `build_deepseek_v4_flash.py` 读取已提交的官方配置快照并构造布局。直接改 XML 后应先同步需要保留的修改，再重生成，避免覆盖。渲染依赖安装见通用工具 README。

## 信息源与边界

- [官方 config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json)
- [官方 inference/config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/config.json)
- [官方 inference/model.py](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/model.py)
- [官方 inference/kernel.py](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/inference/kernel.py)
- [官方模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/README.md)
- [官方权重索引](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/model.safetensors.index.json)

下载的 Python / GPU kernel 未导入执行；没有下载完整模型权重或读取 safetensors tensor headers，因此未校验形状、数值、完整参数总量或数值推理等价性。1M context 和 284B/13B 是官方资料声明。原生 XML、布局和配对 PNG 在当前 mxGraph 流程验证；飞书客户端导入效果仍未实际测试。
