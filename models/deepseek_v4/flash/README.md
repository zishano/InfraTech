# DeepSeek-V4-Flash：可复用绘图流程测试

本目录是 **Transformers 实现核对版**，不是完整 checkpoint／权重核验版。数字来自固定提交 `f2754311602414ed561cdf8ed9d852390f514404` 的 `DeepseekV4Config` 类，其文档绑定 `DeepSeek-V4-Flash-Base`。本环境无法访问 Hugging Face，因此没有读取用户目标 `deepseek-ai/DeepSeek-V4-Flash` 的实际 config、模型卡或权重索引。

## 配对交付

- [PNG 架构图](deepseek_v4_flash.png)：由 draw.io XML 直接通过 mxGraph 4.2.2 / Chromium 导出。
- [原生可编辑 draw.io](deepseek_v4_flash.drawio)：无整图位图节点。
- [实际布局检查](deepseek_v4_flash.layout.json)、[配对记录](deepseek_v4_flash.export.json)。
- [来源清单](sources.json)、[收集结果及 SHA-256](source_inventory.json)、[提取的默认值](facts.json)、[逐节点证据](evidence.md)。收集结果中的 `.source` 路径指本次运行缓存；完整第三方源码不随本目录提交，可用 sources.json 重新获取。

## 这次核对的内容

| 模块 | 已读取源码支持的结构 |
| --- | --- |
| 主干 | token embedding → repeat 为 4 个流 → decoder 层 → HyperHead learned sigmoid collapse → RMSNorm → LM head |
| mHC | X 展平／无权 RMSNorm／投影为 pre、post、comb；pre 压缩输入，post 展开子层输出，comb 经 Sinkhorn 后**转置**混合原始流；注意力和 FFN 各有独立 mHC |
| 注意力 | Q 低秩投影、逐头归一化、尾部 64 维 RoPE；单个共享 KV 头，**K 与 V 是同一个张量**；滑动窗口 + 该层选用的压缩分支；learned sink；输出执行 inverse RoPE 后再 grouped O_a / O_b |
| CSA | stride 4、两个 Ca/Cb 序列重叠窗口、独立 KV 与 gate 投影、FP32 softmax gate、KV 值旁路、RMSNorm／RoPE／cache；Lightning Indexer 为每个 query 构建 top-512 可见性 mask |
| HCA | 128-token 非重叠窗口、独立 KV 与 gate 投影、FP32 softmax gate、KV 值旁路、RMSNorm／RoPE／cache；可见历史压缩条目，**没有 Lightning Indexer** |
| Indexer | 独立 Q、压缩 key、head scoring-weight 三条路径；ReLU 相似度、缩放、加权 head 求和、因果屏蔽和 top-k；跨调用保留窗口状态 |
| MoE | 256 routed／top-6／1 shared 是类默认值；HashRouter 用 token ID 表决定专家索引，但仍由 learned score 计算激活权重；普通 router 用 correction bias 选择专家，原始 scores 归一化后 ×1.5 |
| Expert FFN | gate／up 两条并行路径；gate 只 clamp max=10 再 SiLU，up clamp 到 [-10,10]；相乘后 down projection |

**不把 Pro 的回退排布套到 Flash。** 配置源码明确其缺省 `layer_types` 构造是 V4-Pro fallback；实际 checkpoint 可以通过 `layer_types` 或 legacy `compress_ratios` 覆盖。由于 checkpoint 未读，本图不声明 Flash 各层的 CSA/HCA 排布。43 层、4096 hidden、64 heads 等均标注为 Flash-Base 配置类默认值，不能当作本次已读取 checkpoint 的事实。

MTP 在配置中声明但此 Transformers 类没有实例化；未添加到主干。没有独立复核 284B/13B 参数统计，因此未将其作为图中核实结果。本次不运行模型推理，不执行下载的 Python，不下载完整权重，也没有将 Transformers 路径当作 SGLang/vLLM 的全部融合 kernel 实现。

## 可复现步骤

从仓库根目录执行：

```bash
# 重新收集资料。HF 未放行时必需 config 获取失败，返回 2；成功的源码仍保留。
python tools/model_architecture/model_architecture.py collect \
  models/deepseek_v4/flash/sources.json --out /workspace/deepseek-v4-flash-sources
python tools/model_architecture/model_architecture.py extract \
  /workspace/deepseek-v4-flash-sources --out /workspace/deepseek-v4-flash-facts.json

# 用已审阅的结构数据重建 XML；不要从 PNG 另生成一套结构。
python models/deepseek_v4/flash/rebuild.py
python tools/model_architecture/model_architecture.py export-png \
  models/deepseek_v4/flash/deepseek_v4_flash.drawio \
  --out models/deepseek_v4/flash/deepseek_v4_flash.png --scale 1.5
python tools/model_architecture/model_architecture.py verify-png \
  models/deepseek_v4/flash/deepseek_v4_flash.drawio \
  models/deepseek_v4/flash/deepseek_v4_flash.png \
  models/deepseek_v4/flash/deepseek_v4_flash.export.json
```

结构数据在 `tools/model_architecture/examples/deepseek_v4_flash.graph.json`；同目录 `build_deepseek_v4_flash.py` 是布局构造脚本。先同步 JSON／脚本中需要保留的修改，再重生成，避免覆盖人工 XML 修改。渲染依赖安装见通用工具 README。

## 来源

- [固定提交的配置类](https://github.com/huggingface/transformers/blob/f2754311602414ed561cdf8ed9d852390f514404/src/transformers/models/deepseek_v4/configuration_deepseek_v4.py)：类默认值及 `__post_init__` 的排布覆盖逻辑。
- [固定提交的模型实现](https://github.com/huggingface/transformers/blob/f2754311602414ed561cdf8ed9d852390f514404/src/transformers/models/deepseek_v4/modeling_deepseek_v4.py)：图中各模块的类名、方法和行号见 evidence.md。
- [固定提交的 modular 源码](https://github.com/huggingface/transformers/blob/f2754311602414ed561cdf8ed9d852390f514404/src/transformers/models/deepseek_v4/modular_deepseek_v4.py)：已收集，不导入执行。
- [目标 checkpoint](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)：未能读取，等待环境放行后继续核对实际配置与权重索引。

原生 XML 与 PNG 已在当前 mxGraph 渲染流程验证；没有声称完成飞书客户端导入测试。
