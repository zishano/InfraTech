# DeepSeek-V4.1-Flash 模型架构

- **[PNG 总览图](deepseek_v41_flash_architecture.png)** / [同源可编辑 draw.io](deepseek_v41_flash_architecture.drawio)：137个原生图元、98条连接。
- **[CSA2 详细图](deepseek_v41_flash_csa2.png)** / [同源可编辑 draw.io](deepseek_v41_flash_csa2.drawio)：64个原生图元、43条连接。
- [逐节点证据](evidence.md)、[官方配置](official_config.json)、[配套推理配置](official_inference_config.json)。
- [权重索引核对摘要](checkpoint_summary.json)、[来源清单](sources.json)、[下载结果与哈希](source_inventory.json)、[审阅记录](review.json)。

采用官方 **`deepseek-ai/DeepSeek-V4.1-Flash`**，固定revision **`314113f8a7dadb388215396ba5fbee2c610a04d6`**。搜索同时发现了`DeepSeek-V4.1-Flash-1017`，本图按用户给出的无后缀型号绘制，没有自动替换日期变体。全部代码只作为文本审阅，未加载远程模型代码。

版式采用用户确认的GLM-5.3风格：中央紧凑主干、两侧模块展开、功能分色、无图例、白底、分组无填充；重要HF配置参数位于模块留白处，张量维度直接标在计算连线上。重复层用框及左上角×N表示。

## 核心参数与拓扑

| 项目 | 官方checkpoint / 所读实现 |
| --- | --- |
| 模型类型 | DeepseekV41ForCausalLM；原生图文输入、文本输出 |
| CED主干 | 40层，因果encoder L0–19 +decoder L20–39，各×20；hidden5120、词表129280 |
| 压缩排布 | 主干L0–1 ratio0（纯SWA）；L2–19 ratio2；L20–39 ratio1；辅助40–42 ratio0 |
| 主注意力 | Q heads64；单共享K=V head；head_dim512，尾部RoPE64；Q rank1280 |
| 输出投影 | 8组，每组8×512=4096→1024，再8192→5120 |
| 滑窗 | 所有40层各有独立SWA128；包含当前token，因果可见 |
| 主KV / index K源 | L2、L8、L14、L20 |
| 索引刷新源 | L2、L8、L14、L20、L24、L28、L32、L36 |
| 索引器 | 32heads×128，TopK≤512；Full拥有K投影，Reindex没有自己的K投影 |
| 分层候选 | L20按8位置一组取max，选≤2048个块；强制保留最新可见块；后续Reindex在共享候选上选≤512位置 |
| MoE | 所有主干层384 routed /top6 +1 shared；专家中间2304；sqrt(Softplus)评分，归一化×1.5 |
| 残差 | Single-pass mHC，4 streams，Sinkhorn20；当次生成的pre用于下一子层 |
| Engram | 仅L1、L14；2/3/4-gram，各8heads×256；24次查询拼接为6144维 |
| 视觉 | DeepSeek-ViT32层、hidden1024、16heads、FFN2816；patch14；3×3 pixel-unshuffle，再9216→5120→5120 |
| DSpark | 独立3辅助层，不计入40主干层；5草稿位置；128 routed /top3 +1 shared；Markov rank256 |
| 上下文 | 配置1048576；基础rope_theta10000，压缩路径theta160000，YaRN factor16 |

官方模型卡报告 **552B backbone +196B Engram**，prefill/decode激活参数分别8B/16B；这是官方统计口径，不是本地重计数或推理测试。HF元数据的I8/FP8等存储元素数包含量化布局，不能直接相加解释为逻辑网络参数数。

## CSA2：与旧V4-Flash不同的核心结构

本图没有套用旧版CSA4/HCA128、43层、hidden4096、256专家或Hash前三层路由。V4.1的实际源码为同一CSA2框架：

- **Full（4层）**：生成新的共享global KV、index K及TopK索引J。Encoder源层2/8/14使用r=2；Decoder源层20使用r=1。
- **Reindex（4层）**：L24/28/32/36复用L20的global KV与index K，但用自己的Qi和head weights重新计算J。
- **Reuse（30层）**：其余L2–39无自身compressor/indexer，消费最近源层的共享KV/K/J。
- L0–1为纯SWA；所有层本地SWA KV仍独立。压缩率和共享策略是不同维度：r=1不表示删除全局分支，也不表示每个decoder层拥有独立global KV。

CED概念上以最后encoder状态构造decoder的共享global KV；参考实现中对应L20注意力输入的归一化状态。SWA本层K=V仍来自当前层输入。主注意力没有旧MLA的KV-up重建：本地与global KV直接是512维共享K=V，Q和分组输出才使用低秩投影。

r=2压缩器有独立Wkv/Wgate，按两个token槽逐通道softmax，值旁路参与乘法求和，之后RMSNorm；没有旧CSA4的前后窗Ca/Cb拼接。Decode只在两槽填满后输出条目，尾部状态保留；r=1只有投影与归一化，没有gate/池化。Indexer读取**旋转前**latent，之后主global latent才旋转与量化写cache。

分层索引先屏蔽不可见位置，对每块8个位置取max，将最新可见块分数设为+inf，再选择最多2048个有效块并展开为位置mask。后续Reindex层保留自己的当前分数，只按共享候选mask筛选；最终TopK≤512，按位置排序并偏移，非法位置置-1。候选上限16384不是global缓存容量。

**参考源码仍先对完整index K做einsum，再施加候选mask**；因此不能由这段Python代码声称已经实现只扫描16384位置的物理稀疏kernel。模型卡关于深层索引成本受候选界限约束的设计与参考执行细节分别记录。

## mHC、Engram、MoE与视觉细节

- mHC：flatten四流20480维，归一化统计与FP32 Linear产生24个系数，拆pre4/post4/comb16；pre=Sigmoid+eps、post=2Sigmoid、comb经Softmax/Sinkhorn。当前子层使用来自**前一子层**的pre-collapse，当前新pre传给下一子层；输出post-expand与combᵀ residual mixing相加。
- Engram：归一化token映射后计算2/3/4-gram哈希，查询24×256维；Wkv从6144投影为四流key与共享value。每个流独立归一化dot，再signed sqrt→Sigmoid，gate×value写回残差。图像token不参与n-gram、不接受Engram贡献。
- MoE：FP32 router→sqrt(Softplus)，text与image-span使用不同的选择bias；bias只用于选专家，权重取原始分数归一化×1.5。专家gate只上截断10，up双侧截断±10，SiLU(gate)×up之后**先乘路由权重，再down**；shared expert不乘路由权重。没有旧版token-hash路由。
- 视觉：每张图的ViT为双向2D-RoPE attention；pixel-unshuffle前会padding到3的倍数，Nv=ceil(nh/3)×ceil(nw/3)。图像特征**替换**image token span，不是与文本embedding相加；分隔符和换行符另用learned embeddings。配置max_image_tokens不包含所有文本／分隔符位置。

## DSpark与部署边界

DSpark从L37/38/39的**层输入**取四流平均后拼接15360维，而不是三层输出；main_proj+Norm得到main_x，用于草稿SWA的KV条件。草稿输入是seed+noise token embedding，广播为4流，经过独立3阶段。最终collapse hidden经Norm送共享LM head，Markov低秩头逐位置加logit bias；confidence使用**未经该最终Norm的collapse hidden**与Markov embedding拼接（5120+256→1）。图中特别保留了这条旁路。

官方minimal README明确：仅提供DSpark forward，`generate.py`仍为普通自回归采样，不调用forward_spec；confidence-scheduled verification未在该循环实现。模型卡的CED prefill优化、SWA Bounded Replay、缓存驱逐/重放也没有在这个最小forward中独立实现（该forward逐层运行全部40层）。这些部署设计写在文档中，不伪装为已执行的模型算子链。

量化区分：本地SWA为FP8 Q/DQ，连RoPE尾部一并量化；global KV为FP4 E2M1、每16通道E4M3 scale；index Qi/Ki为FP4、每32通道E8M0 scale。所读V4.1路径没有旧版Hadamard变换。参考调用`inplace=True`后写回的是反量化浮点值，cache缓冲也是浮点张量；图使用Q/DQ标记，不能当作已验证物理FP4缓存打包。官方890 bytes/token及约1/8持久缓存等数据属于模型卡声明，未本地实测。

## 来源与核验

已读取同一固定版本的config、inference/config、model、kernel、engram、vision、generate、inference README、模型卡及完整权重索引。索引共**96,085个名称、48个shard**，与配置交叉核对：

- 只有主干L2/8/14/20有compressor和Indexer K投影。
- 只有8个index source层有Indexer Q/weights；其余Reuse无这些模块。
- Engram仅L1/L14；视觉blocks0–31；mtp0/1/2各128专家。

这些是名称存在性和分片映射核验，不是tensor-header形状或数值检查。技术报告PDF的官方CDN重定向被代理403阻断，未将其当作已读取来源；结构依据模型卡与上述完整参考代码。未下载完整权重、执行模型/GPU、做精度/吞吐测试或实测飞书导入。

固定来源：[官方仓库](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/tree/314113f8a7dadb388215396ba5fbee2c610a04d6)、[config](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/config.json)、[实现](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/model.py)。

## 复现

```bash
python models/deepseek_v4_1/flash/rebuild.py
python tools/model_architecture/model_architecture.py export-png models/deepseek_v4_1/flash/deepseek_v41_flash_architecture.drawio --out models/deepseek_v4_1/flash/deepseek_v41_flash_architecture.png --scale 2
python tools/model_architecture/model_architecture.py export-png models/deepseek_v4_1/flash/deepseek_v41_flash_csa2.drawio --out models/deepseek_v4_1/flash/deepseek_v41_flash_csa2.png --scale 2
python tools/model_architecture/model_architecture.py verify-png models/deepseek_v4_1/flash/deepseek_v41_flash_architecture.drawio models/deepseek_v4_1/flash/deepseek_v41_flash_architecture.png models/deepseek_v4_1/flash/deepseek_v41_flash_architecture.export.json
python tools/model_architecture/model_architecture.py verify-png models/deepseek_v4_1/flash/deepseek_v41_flash_csa2.drawio models/deepseek_v4_1/flash/deepseek_v41_flash_csa2.png models/deepseek_v4_1/flash/deepseek_v41_flash_csa2.export.json
```

每张图保留同名layout与export记录，PNG直接由XML渲染。重建仅运行仓库中的绘图代码，不import或执行下载的模型源码。
