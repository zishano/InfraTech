# GLM-5.2：IndexShare DSA 架构图

- [PNG 架构图](glm_5_2_architecture.png) / [同源原生 draw.io](glm_5_2_architecture.drawio)
- [布局检查](glm_5_2_architecture.layout.json) / [配对记录](glm_5_2_architecture.export.json)
- [逐节点证据](evidence.md) / [官方配置](official_config.json)
- [相对5.1的配置差异](config_diff.json) / [权重索引与参数核对](checkpoint_summary.json)
- [审阅记录](review.json) / [来源清单](sources.json) / [获取结果与哈希](source_inventory.json)

使用官方 **`zai-org/GLM-5.2` BF16** checkpoint `cf457fa734ab149ffef225f80893eb38c6ff5cdc`，不是FP8或第三方量化版本。对应Transformers固定提交 `bbe484b5680f9cdf4d51bafc6b775b136558ab43`；其GLM-MoE-DSA模型与配置文件内容哈希和前次GLM-5.1审阅版本相同，但5.2 checkpoint显式启用IndexShare。

图沿用用户认可的GLM-5.1自适应算子框布局：短算子与维度、按角色和文本定尺寸、主轴／分支对齐、直线优先。新增独立IndexShare说明带，没有把GLM-5.1每层独立Indexer照搬为5.2实际结构。共98个原生图元、71条连接，PNG直接从同名XML导出。

## 核心配置

| 项目 | GLM-5.2 |
| --- | --- |
| 主干 | 78层，hidden6144，词表154880 |
| FFN（0-based） | L0–2 Dense；L3–77 MoE；宽度分别12288／2048 |
| MoE | 256路由专家，top8；1共享专家；路由归一化×2.5 |
| 主注意力 | 64 Q heads；Q rank2048；KV rank512；Q/K每头256=192+RoPE64；V每头256 |
| FULL Indexer | 32heads×128、LayerNorm、interleaved RoPE64、TopK2048 |
| IndexShare | 21个FULL主干层、57个SHARED主干层；index_topk_freq4、offset3；显式indexer_types优先 |
| 上下文 | 202752→1048576（1M） |
| RoPE | theta1000000→8000000；仍是default类型，旋转维度64 |
| MTP | 配置1层，checkpoint辅助index78；有独立Indexer；index_share_for_mtp_iteration=true |

**不要把`head_dim`字段64→192误画为Q/K总维度或RoPE维度变化。** 物理Q/K维度仍由qk_nope_head_dim192 +qk_rope_head_dim64组成；所读框架配置派生会将其RoPE使用的head_dim设为64，Attention也显式使用192+64。

## IndexShare 的真实排布

根据checkpoint显式78项`indexer_types`，主干FULL层为：

```
0, 1, 2, 6, 10, 14, 18, 22, 26, 30, 34,
38, 42, 46, 50, 54, 58, 62, 66, 70, 74
```

其余57层为SHARED。不能简单画作从L0开始重复“1 full +3 shared”，开头L0和L1是额外FULL层。

图中说明带展示：

```
L2 FULL：计算 J₂ → L3 SHARED：复用 J₂ → L4 SHARED：复用 J₂ → L5 SHARED：复用 J₂
L6 FULL：计算 J₆ → L7–9 SHARED：复用 J₆
…
L74 FULL：计算 J₇₄ → L75–77 SHARED：复用 J₇₄
```

- FULL层运行独立Q/K/head-weight索引三路、打分和因果TopK。
- SHARED层没有自己的Indexer，直接接收`prev_topk_indices`，但仍计算自己的主Q/K/V、RoPE、注意力和FFN。
- 共享的是**同一次forward中同一查询的token位置列表**，不是上一个decode token的选择，也不是共享hidden、索引分数或主KV内容。
- 每个主注意力层的潜变量KV缓存仍独立。只有FULL层计算并写入自己的索引Key，SHARED层不运行自身Indexer；不能将缓存容量画作2048，TopK限制的是读取位置。
- 图中四个示例框是索引传播说明，不是在78层以外增加的层。命名J端口表示来源可为本层新索引或前方FULL层共享索引。

所读Transformers实现：`self.indexer=None`用于shared层，`Attention.forward`在无Indexer时要求`prev_topk_indices`，并在所有层分别执行本层缓存更新；Decoder返回位置列表供后续层使用。

## 保留的主结构

DSA仍为低秩Q、512维压缩KV加64维位置key、未吸收的KV上投影视图；无额外attention输出门。Indexer的K为LayerNorm，而不是RMSNorm；主路径与Indexer都执行interleaved RoPE，不套用Kimi的NoPE／无旋转配置，也不凭相似模型添加Hadamard或量化算子。

MoE路由仍以FP32线性→sigmoid取分数，选择时加correction bias，权重从原始分数gather后归一化×2.5。共享专家绕过路由加权。SwiGLU仍为并行gate/up、SiLU(gate)×up、down；路由权重在所读实现中乘在专家down输出之后。

## 权重索引交叉核对

已读取权重索引：**59,585个tensor名称、282个shard**。逐层核对显示：

- 主干21个FULL层有Indexer的wq_b、wk、weights_proj、LayerNorm weight/bias。
- 57个SHARED主干层没有这些Indexer前缀，但仍有各层主注意力与对应FFN权重。
- Dense仍只有0–2层；其余主干层均为路由MoE。
- 辅助index78仍有独立Indexer及enorm、hnorm、eh_proj、DSA、MoE、shared_head.norm，共791个名称。MTP不并入主干78层。

相对5.1少了285个tensor名称，恰为57×5；HF报告的BF16元素数减少534,198,528，也与57个独立索引器的参数量推导一致：

```
每个Indexer：2048×32×128 + 6144×128 + 6144×32 + 2×128 =9,371,904
57 ×9,371,904 =534,198,528
```

这是源码维度推导、索引模块存在性和提供方元数据的交叉一致性，不是独立读取全部tensor headers或权重数值后的参数重计数。HF总元素元数据从753,864,139,008变为753,329,940,480；不能把它直接当成单独主干的精确逻辑参数量。

## MTP 与效率声明的边界

模型卡声明改善MTP用于推测解码，acceptance length最高提升20%；config中`index_share_for_mtp_iteration=true`。图只展示该标志及checkpoint中确认存在的辅助模块，不猜接未核对的MTP迭代forward，也不声称MTP必然复用主干L74的索引；辅助78层有自己的Indexer权重。

模型卡还报告IndexShare在1M长度下降低每token FLOPs 2.9倍。它是**官方计算量声明**，不是本地实测吞吐／延迟加速比。主注意力稀疏、索引共享和后训练能力改进也不能互相替代解释。

当前只审阅模块级结构：eager/SDPA可用稀疏mask，优化后端可直接消费索引或采用absorbed布局；图不声明所有后端物理执行完全相同。未读取tensor headers、下载完整权重、运行GPU推理／基准或实测飞书导入。

## 固定来源与复现

- [官方config](https://huggingface.co/zai-org/GLM-5.2/blob/cf457fa734ab149ffef225f80893eb38c6ff5cdc/config.json)
- [官方模型卡](https://huggingface.co/zai-org/GLM-5.2/blob/cf457fa734ab149ffef225f80893eb38c6ff5cdc/README.md)
- [官方权重索引](https://huggingface.co/zai-org/GLM-5.2/blob/cf457fa734ab149ffef225f80893eb38c6ff5cdc/model.safetensors.index.json)
- [对应模型实现](https://github.com/huggingface/transformers/blob/bbe484b5680f9cdf4d51bafc6b775b136558ab43/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py)
- [配置派生代码](https://github.com/huggingface/transformers/blob/bbe484b5680f9cdf4d51bafc6b775b136558ab43/src/transformers/models/glm_moe_dsa/configuration_glm_moe_dsa.py)

原始文件在本次运行缓存`/workspace/glm52-research/`，可按sources.json重取并对照哈希。构造器复用5.1已审阅的共同算子和认可版式，先断言共同结构字段，再显式加入5.2的索引共享和配置变化；不会独立生成另一套PNG结构。

```bash
python tools/model_architecture/examples/build_glm52.py
python models/glm_5_2/rebuild.py
python tools/model_architecture/model_architecture.py export-png \
  models/glm_5_2/glm_5_2_architecture.drawio \
  --out models/glm_5_2/glm_5_2_architecture.png --scale 2
python tools/model_architecture/model_architecture.py verify-png \
  models/glm_5_2/glm_5_2_architecture.drawio \
  models/glm_5_2/glm_5_2_architecture.png \
  models/glm_5_2/glm_5_2_architecture.export.json
```
