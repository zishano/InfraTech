# GLM-5.3：IndexShare DSA + MoE

[PNG 架构图](glm_5_3_architecture.png) · [可编辑 draw.io](glm_5_3_architecture.drawio) · [节点证据](evidence.md) · [布局实测](glm_5_3_architecture.layout.json) · [配对记录](glm_5_3_architecture.export.json)

**GLM-5.3 沿用 GLM-5.2 的基座，官方明确表示全部能力提升来自后训练。** 本图保留已认可的自下而上、自适应算子框布局，展开 DSA、Indexer 的 Q/K/head-weight 三路、IndexShare、MoE 路由与 SwiGLU。共98个原生图元、71条连接；正式 PNG 直接从同名 draw.io XML 导出。

## 核心结构

| 模块 | GLM-5.3 配置 |
| --- | --- |
| 主干 | 78层，hidden6144，词表154880 |
| FFN | L0–2 Dense12288；L3–77 MoE2048 |
| MoE | 256路由专家选8，1共享专家；sigmoid路由、归一化×2.5 |
| DSA | 64 Q heads；Q rank2048、KV rank512；Q/K256=NoPE192+RoPE64，V256 |
| Indexer | 32heads×128、K LayerNorm、interleaved RoPE、TopK2048 |
| IndexShare | 21 FULL +57 SHARED；FULL为L0、L1、L2及L6、L10…L74 |
| 上下文 | 1048576；RoPE theta8000000 |
| MTP | 配置1辅助层；MTP迭代索引共享标志true，未追踪后端迭代执行 |

IndexShare共享的是**同一次forward、同一查询的位置列表**，不是前一个decode token的索引，也不是KV内容。SHARED层仍计算自己的主Q/K/V与FFN；各层KV缓存独立。详细主结构及继承设计可对照[GLM-5.2说明](../glm_5_2/README.md)。

## 与 GLM-5.2 的区别

逐字段比较官方配置，只有`quantization_config`与`transformers_version`不同；主干尺寸、索引共享排布、上下文、RoPE和专家配置完全一致。固定版本的Transformers模型及配置源码内容哈希也与上次审阅版本一致。不存在可据此画出的新注意力分支或新增专家模块；官方模型卡将能力提升归因于后训练，没有披露足以绘制训练计算图的具体流水线。

本次官方发布包含FP8 E4M3量化配置：动态激活、128×128权重分块、541条`modules_to_not_convert`条目。排除条目列出保留原精度的模块，例如归一化、路由及部分索引相关模块；不是541个新增算子，也不意味着所有权重都变为FP8。`dtype=bfloat16`与FP8量化权重可共存，具体执行精度由量化配置和后端决定。

HF元数据报告 BF16 2,103,729,152、F8_E4M3 751,226,191,872、F32 19,456，共753,329,940,480个元素；总数与5.2提供方元数据一致。它不是本地独立重算的主干逻辑参数量，不能将存储位宽变化解读为模型规模缩小。参见[配置差异](config_diff.json)、[量化与元数据](checkpoint_summary.json)。

## 来源与核验边界

- [官方模型卡](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/README.md)（本地[快照](official_model_card.md)）：明确same base、post-training。
- [官方配置](https://huggingface.co/zai-org/GLM-5.3/blob/ba32f8c19c8738e2c57c71798c601d477a7bf844/config.json)（[快照](official_config.json)）。
- [固定模型实现](https://github.com/huggingface/transformers/blob/8833c9181eec925f1b4e0096db516462044345df/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)及同目录配置类；模块视图采用未吸收MLA布局，不等同于所有优化后端的物理执行。
- [来源清单](sources.json)、[下载记录与哈希](source_inventory.json)、[审阅记录](review.json)。

**本次5.3权重索引未成功下载。** 官方resolve重定向到`us.aws.cdn.hf.co`后被代理403阻断，raw接口只返回Git LFS指针；指针已记录，不能当成索引正文。图中权重存在性引文明确保留为5.2基线，不宣称验证了5.3张量名称、分片数或辅助层权重。本次结构结论来自5.3配置、模型卡与匹配实现。未下载完整权重、读取tensor headers、运行GPU/精度/吞吐测试或实测飞书导入。

## 复现

```bash
python tools/model_architecture/examples/build_glm53.py
python models/glm_5_3/rebuild.py
python tools/model_architecture/model_architecture.py export-png models/glm_5_3/glm_5_3_architecture.drawio --out models/glm_5_3/glm_5_3_architecture.png --scale 2
python tools/model_architecture/model_architecture.py verify-png models/glm_5_3/glm_5_3_architecture.drawio models/glm_5_3/glm_5_3_architecture.png models/glm_5_3/glm_5_3_architecture.export.json
```
