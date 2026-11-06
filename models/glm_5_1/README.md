# GLM-5.1 架构图：官方 checkpoint 核对版

- [PNG 架构图](glm_5_1_architecture.png) / [原生可编辑 draw.io](glm_5_1_architecture.drawio)
- [配对记录](glm_5_1_architecture.export.json) / [实测布局](glm_5_1_architecture.layout.json)
- [逐节点证据](evidence.md) / [参数快照](official_config.json)
- [权重索引核对](checkpoint_summary.json) / [来源与哈希](source_inventory.json) / [可重取来源](sources.json)
- [按通用流程填写的审阅记录](review.json)

目标为官方 **`zai-org/GLM-5.1` BF16 checkpoint**，固定 revision `26e1bd6e011feb778d25ae34b09b07074139d92d`；不是同名 FP8、NVFP4 或第三方量化版本。计算算子按固定 Transformers 提交 `f262c71703eb138381d65ced86b3aaa496be0196` 的 `glm_moe_dsa` 实现审阅，未导入执行远端代码。

图共91个原生图元、68条连接；自下而上，按主干、DSA/MLA、三路Indexer、MoE、SwiGLU与辅助MTP分区。节点保留短算子及必要维度，长说明在本文和证据中。采用模块配色，不是版本差异红绿黄图；缓存单独标色。PNG直接由同名XML经mxGraph/Chromium导出。

## 核对结果

| 项目 | GLM-5.1发布配置 |
| --- | --- |
| 主干 | 78层；hidden6144；词表154880 |
| FFN排布（0-based） | L0–2为Dense，intermediate12288；L3–77为MoE，共75层 |
| 路由专家 | 256个，每token选择8个；1个共享专家；expert intermediate2048 |
| 主注意力 | 64 heads；Q rank2048；KV rank512；Q/K每头256=192+RoPE64；V每头256 |
| 索引器 | 32 heads×128；TopK2048；独立K投影、LayerNorm128、head-weight路径 |
| 位置编码 | 主注意力及Indexer均使用interleaved RoPE64；theta1000000 |
| 上下文配置 | max_position_embeddings202752，不是1M配置 |
| 辅助预测 | num_nextn_predict_layers1；权重位于model.layers.78，不计入主干78层 |
| 精度 | 本次BF16 checkpoint；不把独立FP8发布版本的规则套入此图 |

官方GLM-5家族模型卡报告744B总参数、40B激活参数。GLM-5.1与所核对GLM-5配置除`transformers_version`外相同，未据此虚构新层。HF API的safetensors元数据为753,864,139,008个元素，包含发布文件里的辅助模块；这是提供方统计，不能当成独立重算的主干逻辑参数量，也不能直接与取整的家族模型卡规模相减推断结构变更。

## DSA / MLA：主计算与索引分开

图使用所读Transformers的**未吸收投影视图**：

1. Q经6144→2048低秩投影和RMSNorm，得到Qr；上投影至64×256，再分192维内容和64维RoPE，重组为Q。
2. KV经6144→(512+64)投影。512维潜变量经RMSNorm，64维共享位置key经RoPE，两部分在压缩状态下写入缓存。
3. 潜变量经KV上投影产生每头K192/V256；K拼接绕过该投影的共享kPE64，得到K256。图中“KV up + kPE bypass”是一个明确标注的模块框，不表示kPE也经过同一上投影。
4. Indexer提供因果可见的TopK位置，主注意力按这些位置的稀疏可见性计算QK、softmax和V加权，最后做O投影至6144。
5. 所读实现**没有额外attention sigmoid输出门**，不沿用Kimi的门控结构。

所读eager/SDPA路径会展开KV并构造稀疏mask，优化的`flash-mla`可直接消费索引。图表达的是有来源支持的模块级结构，不表示所有后端都物理gather、融合或以相同方式缓存。没有把某个硬件的absorbed MQA实现当成唯一架构。

## 三路Indexer

- **Q路**：输入取主注意力归一化后的Qr2048，投影成32×128；对其中64维执行interleaved RoPE，再与其余内容拼接。
- **K路**：hidden6144→128，LayerNorm（所读源码eps1e-6），对64维执行RoPE，写入独立逐token索引key缓存。
- **weights路**：hidden6144→32，乘32^-0.5。QK打分先乘128^-0.5并经过ReLU，再乘head weights、跨头求和；因果mask后取TopK并返回int32位置。

这里有RoPE，区别于Kimi-K3.1的NoPE索引器。没有凭其他模型添加Hadamard或FP8量化算子。

框架类支持shared indexer模式，但此checkpoint没有指定共享模式字段；默认freq1派生为全部full，且索引实际包含主干0–77及辅助78的全部Indexer前缀。因此本图不画跨层复用TopK。TopK2048限制当前查询的读取位置，不把所有历史缓存截断到2048。

## MoE / SwiGLU

Router以FP32线性计算后取sigmoid。选择专家时使用`scores + e_score_correction_bias`；权重从**原始sigmoid scores**按选中索引gather，归一化后乘2.5。配置n_group=1/topk_group=1，分组选择没有额外裁剪效果，图中省略恒等的单组选择框。

路由专家FFN为并行gate/up、SiLU(gate)×up、down；所读Experts源码在down输出之后乘routing weight，再聚合。共享专家独立处理相同输入，不乘该路由权重，与路由结果相加。Dense FFN宽12288，路由／共享专家宽2048，均为6144输入／输出；没有Kimi式latent3584下投影路径。

## 权重与MTP边界

已读取5.4MB权重索引，核对59,870个tensor名称及282个shard映射：

- main0–2存在dense FFN；3–77存在routed专家；全部主干层有Indexer。
- 辅助`model.layers.78.*`包含791个名称，包括enorm、hnorm、eh_proj、DSA、MoE和shared_head.norm。
- MTP图元只展示配置声明和这些辅助checkpoint模块的存在，**未用相似模型的MTP实现猜接其完整forward**。所读Transformers主干forward执行78层，不自动执行辅助78层。

没有读取safetensors tensor headers或权重数值，没有下载完整权重，也没有运行GPU推理或性能基准。原生XML及PNG配对通过当前mxGraph流程验证；未实测飞书客户端导入。

## 来源与复现

- [官方config](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/config.json)
- [官方模型卡](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/README.md)
- [官方权重索引](https://huggingface.co/zai-org/GLM-5.1/blob/26e1bd6e011feb778d25ae34b09b07074139d92d/model.safetensors.index.json)
- [Transformers模型实现](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)
- [Transformers配置派生](https://github.com/huggingface/transformers/blob/f262c71703eb138381d65ced86b3aaa496be0196/src/transformers/models/glm_moe_dsa/configuration_glm_moe_dsa.py)
- [GLM-5家族模型卡](https://huggingface.co/zai-org/GLM-5/blob/c183ef8c61faee82855eca1ed9bb3a9a7ce3b0b2/README.md)

完整来源文件保存在本次运行缓存`/workspace/glm51-research/`，可按sources.json重取；构造器只读取已审阅快照与摘要，不执行下载源码。

```bash
python tools/model_architecture/examples/build_glm51.py
python models/glm_5_1/rebuild.py
python tools/model_architecture/model_architecture.py export-png \
  models/glm_5_1/glm_5_1_architecture.drawio \
  --out models/glm_5_1/glm_5_1_architecture.png --scale 2
python tools/model_architecture/model_architecture.py verify-png \
  models/glm_5_1/glm_5_1_architecture.drawio \
  models/glm_5_1/glm_5_1_architecture.png \
  models/glm_5_1/glm_5_1_architecture.export.json
```

## 算子框尺寸与对齐

使用通用 `operator_layout.py` 按名称／维度长度和模型构造器判断的视觉复杂度分配尺寸：简单激活与归一化紧凑显示，投影通常两行，聚合、缓存和复合模块适当放大。保持各lane原有中心轴及并行分支层级，尺寸变化后重新选择端口和直线／必要折线路径，并检查实际文字留白和节点避让。长说明保留在description／证据文档，不通过机械拉宽所有节点或一味缩字解决。
