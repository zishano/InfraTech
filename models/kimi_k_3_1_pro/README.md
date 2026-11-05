# Kimi-K3.1-Pro：相对 Kimi-K3 的架构差异图

- [PNG 架构差异图](kimi_k31_pro_architecture.png)
- [同源原生可编辑 draw.io](kimi_k31_pro_architecture.drawio)
- [布局检查](kimi_k31_pro_architecture.layout.json) / [XML–PNG 配对记录](kimi_k31_pro_architecture.export.json)
- [结构差异分类](architecture_diff.json) / [逐字段配置差异](config_diff.json)
- [逐节点来源](evidence.md) / [来源 URL](sources.json) / [获取结果与 SHA-256](source_inventory.json)
- [参数及元数据核对摘要](checkpoint_summary.json)

以之前 `kimi_k3_design_preview_v2` 的原生图数据为布局底稿，沿用主干、AttnRes、KDA 五路输入、Stable LatentMoE 和 MoonViT-V2 的模块分区，统一字号并对齐主链后，在原 MLA 位置绘制 Gated DSA，并在右侧展开新增 Indexer。正式 PNG 直接从同名 draw.io 渲染，没有独立生成另一套连线。

## 红 / 绿 / 黄的含义

| 颜色 | 含义 | 本图内容 |
| --- | --- | --- |
| 红框、红字、红线 | 新增的结构或替代后的新计算路径 | Gated DSA ×24；独立索引 Q / K / head-weight 三路；FP8 索引计算；因果 mask、TopK≤2048；把选择的位置交给稀疏注意力 |
| 绿框、绿字 | 退出当前推理路径的旧结构 | K3 的 dense all-token attention；仅放在退役对照区，没有接入新推理流。MLA 的低秩投影、NoPE 和输出门没有删除 |
| 黄框、黄字 | 仅参数统计或配置变化 | quantization ignore 正则从 6 项变 8 项；HF 报告 BF16 tensor-elements 增加 178,526,208 |
| 中性蓝灰 | 两版共享结构、参数，或旧图说明的补全 | KDA、AttnRes、MoE、视觉分支，以及两版相同的 Q/KV ranks 等 |

旧 K3 图的 KDA 原来使用绿色；本图将共享模块统一改为中性蓝灰，避免误读为被删去。颜色分类由官方模型卡和源码人工核对，**不会把 config 删除的 `auto_map` 加载映射当成神经网络算子删除**。

## 核对出的结构差异

官方 K3.1-Pro 模型卡明确：将 K3 的 full-attention Gated MLA 替换为 Gated DSA。两个 checkpoint 的大部分结构配置完全一致：

- 93 主干层、hidden 7168、96 个主注意力 heads；69 KDA +24 非 KDA 层。配置层号为 **1-based**：DSA 位于 `4,8,…,92,93`，对应原 MLA 的位置。
- 896 routed experts、top-16、2 shared experts；latent 3584、expert intermediate 3072；SiTU-GLU 参数 4 /25。
- AttnRes block size 12；KDA head dim128、96 heads、ShortConv kernel4、full-rank gate。
- MoonViT-V2：27 层、hidden1024、QKV1536、12 heads、patch14；视觉配置和预处理配置没有变化。
- NoPE 和输出门仍在；Q rank1536、KV rank512、Q/K 的192维内容（128+未旋转64）、V128。这些在两个 config 里相同，图中补全它们属于中性说明。
- 两版 `first_k_dense_replace=1`，因此第一层 FFN 为 dense，其余92层为 MoE。旧图“dense FFN 位置未确定”现已澄清，不是 K3.1 的新结构变化。
- 两个发布 config 的 `num_nextn_predict_layers` 都为0；不因旧 K3 报告 Table1 写过1 MTP layer 就声称 K3.1 删除了 MTP。

新 `dsa_config` 为24层配置独立索引器：32 heads、head dim128、TopK2048、index RoPE dim0、key norm为LayerNorm、每个DSA层独立计算TopK（freq1）。

模型卡推荐的固定 SGLang 实现进一步明确：

1. Q 输入取主注意力的 normalized low-rank query `Qr[1536]`，投影到 `32×128`。
2. K 从 hidden7168 单独投影至128，做 **LayerNorm**，写入独立逐token索引key缓存；不是4/128-token压缩器。
3. head weights 由 hidden7168 独立投影至32，缩放 `32^-0.5 ×128^-0.5`，不是 softmax gate。
4. 索引分数按 `sum_h weights_h × ReLU(Q_h·K_j)` 聚合，因果可见性控制后选TopK2048，供主注意力读取相应token。
5. **NoPE；不做Hadamard旋转。** 这与通用 DeepSeek DSA 默认路径和之前 DeepSeek-V4 CSA 图不同。
6. 图示 FP8 Q/K 量化与索引cache来自所读 SGLang GPU 后端，是实现细节，不等于模型架构必须物理采用某个打包布局，也没有将专家 MXFP4 权重精度套到索引器上。

## 参数变化与证据边界

官方模型卡两版均以取整数报告约 **2.8T total /104B active**；旧 K3 报告的2.78T /104.2B与这些取整数字不能直接做参数增减比较。

HF API 的 safetensors 元数据报告 BF16 元素数从57,179,884,544变为57,358,410,752，相差178,526,208，恰与下列新增索引器参数量推导一致：

```
24 × (1536×32×128 + 7168×128 + 7168×32 + 2×128)
= 178,526,208
```

其中四项是每层 Q projection、K projection、head-weight projection、LayerNorm weight+bias。这是**公开元数据与源码的交叉一致性**，不是独立读取所有tensor headers后的全模型逻辑参数重计数。两个文件清单均包含96个safetensors shards；本次没有下载完整权重。

实际 config 的 quantization ignore 列表额外加入以下两个正则：

```
re:.*block_sparse_moe\.gate$
re:.*block_sparse_moe\.routed_expert_(up|down)_proj.*
```

这表示配置规则变化；不能仅据此断言已有权重的数据类型或神经网络宽度改变。

权重索引下载重定向被当前网络策略拒绝，官方raw接口只返回LFS指针；没有声称读取索引里的tensor名称或权重形状。K3.1-Pro固定HF文件清单没有附带forward模型实现；新增DSA计算按其模型卡推荐的SGLang源码核对。共享K3部分以旧报告、已读取的K3代码和两个相同配置字段交叉检查。没有导入执行下载的模型代码，没有运行GPU模型推理，未实测飞书客户端导入。

## 固定来源

- K3.1-Pro checkpoint：[`d9e99b0792a5e93b78ea9bea62a68167e36ddd9e`](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/tree/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e)
- K3 baseline checkpoint：[`f831ab66814297da540d832a5235f8e904f29d06`](https://huggingface.co/moonshotai/Kimi-K3/tree/f831ab66814297da540d832a5235f8e904f29d06)
- SGLang：[`b09bda75c89a88263811a49e13adeef7a7aa8bf7`](https://github.com/sgl-project/sglang/tree/b09bda75c89a88263811a49e13adeef7a7aa8bf7)
- 旧K3图的报告来源：[`3cb39dfd32e51c3328e2e4b4af21341247d06c43`](https://github.com/MoonshotAI/Kimi-K3/tree/3cb39dfd32e51c3328e2e4b4af21341247d06c43)

配置快照保存在本目录。完整模型卡及源码在本次运行缓存 `/workspace/kimi-k31-pro-research/`，可按来源URL重取并校验哈希。

## 重建

从仓库根目录执行：

```bash
python tools/model_architecture/examples/build_kimi_k31_pro.py
python models/kimi_k_3_1_pro/rebuild.py
python tools/model_architecture/model_architecture.py export-png \
  models/kimi_k_3_1_pro/kimi_k31_pro_architecture.drawio \
  --out models/kimi_k_3_1_pro/kimi_k31_pro_architecture.png --scale 1.5
python tools/model_architecture/model_architecture.py verify-png \
  models/kimi_k_3_1_pro/kimi_k31_pro_architecture.drawio \
  models/kimi_k_3_1_pro/kimi_k31_pro_architecture.png \
  models/kimi_k_3_1_pro/kimi_k31_pro_architecture.export.json
```

`tools/model_architecture/model_diff.py` 可复用逐字段比较与红绿黄主题；模型专用构造器负责有来源支持的算子增删分类，避免从字段差异自动猜测网络拓扑。旧K3图及文件保持原样。


## 连线和排版优化

`tools/model_architecture/examples/kimi_k31_presentation.py` 将显示层与结构差异分开：统一 Arial 字体及标题／算子／细节层级，对齐 AttnRes 主链，精简节点文字，并扩大视觉细节区的行距。完整说明仍保留在节点 tooltip 和证据文档中。

`tools/model_architecture/routing.py` 优先在两个节点间选择无障碍的同 x 或同 y 端口，直接连线；不能直连时尝试一个直角，再保留必要避让。所有 source/target 对保持不变，并检查无关算子边界及留白。此次实测154条连接中136条为直线、16条一个折点、2条两个折点，总折点由67减为20。

PNG 和 draw.io 保持同源；优化后重新运行文字、节点避让、连线正交和穿框检查。
