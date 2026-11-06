# Graph JSON v1

最小示例（下方输入、上方输出；占位节点未核实）：

```json
{
  "version": 1,
  "title": "New model architecture draft",
  "width": 1000,
  "height": 1000,
  "sources": {"config": "https://huggingface.co/org/model/resolve/COMMIT/config.json"},
  "nodes": [
    {"id": "input", "label": "Input", "box": [300, 800, 400, 60], "status": "unverified"},
    {"id": "module", "label": "Module pending source review", "box": [300, 500, 400, 100], "status": "unverified"},
    {"id": "output", "label": "Output", "box": [300, 250, 400, 60], "status": "unverified"}
  ],
  "edges": [
    {"source": "input", "target": "module", "dashed": true},
    {"source": "module", "target": "output", "dashed": true}
  ],
  "limitations": ["Forward graph has not been verified."]
}
```

- `box`：`[x, y, width, height]`，坐标向下增大；自下向上计算需让 target 的 y 小于 source。
- `status`：`verified` / `inferred` / `unverified`。缺省视为 unverified；未核实节点使用虚线。推断节点在证据报告中标注，不冒充已验证。
- `evidence`：列表，例如 `[{"source":"report", "locator":"§2.1.1, Eq. 5"}]`。`source` 必须存在于 `sources`。config 可以使用 JSON Pointer；源码应使用固定提交 URL 和类名/方法名/行号。
- `kind: "decoration"`：背景框或标题，不表示运算节点。
- `style`：可选 diagrams.net 样式字符串；建议 `html=0` 和 Arial，避免依赖 HTML / 自定义字体。SVG 支持基本颜色、文字、圆角框、椭圆、虚线，复杂 mxGraph 样式不保证完全一致。
- `edges[].ports`：`[exitX, exitY, entryX, entryY]`，均为 0–1；缺省 `[0.5,0,0.5,1]`，即 source 顶部连接 target 底部。
- `edges[].points`：可选正交折线路径中间坐标，`[[x,y], ...]`；两种输出都复用此路径。未提供时由各自渲染器处理简单正交连线，结果可能略有区别。
- `edges[].label` / `dashed`：连接说明、是否虚线。跨模块解释线也应明确标记，不能与数据流混淆。

形状和连接应体现具体模块：Q/K/V 与 α/β 等控制路径分开；输出门另画旁路；MoE 的 router、latent projection、shared experts 并行；残差/跨层聚合要有实际连线。不要通过省略运算掩盖尚未理解的结构。

本格式只保存模块级结构、证据和布局，不能执行模型，不能验证数值等价。使用前应阅读 README 中的审阅步骤。

正式 PNG 必须经 `export-png` 直接读取已保存的 draw.io XML 生成；不能由另一套图像提示词独立作图。PNG 与 draw.io 的配对记录使用 `.export.json`。SVG 是辅助预览，不是正式 PNG 导出的中间结构引擎。


## 显示、版本差异与实现边界

构造新模型前先阅读 [WORKFLOW.md](WORKFLOW.md)。建议保持事实与展示分离，以下元数据供已审阅构造器／工具使用，**不表示通用校验器能验证模型语义**：

- `nodes[].description`：长说明，draw.io写入节点tooltip；图上 `label` 主要保留算子和必要维度。
- `nodes[].change`：`added` / `removed` / `parameter_changed` / `unchanged`。配色由 `model_diff.mark` 应用，必须附来源。绿色退役节点不接入当前推理；旧图澄清不标新增。
- `edges[].color`：六位十六进制颜色，如 `#c62828`，用于新增路径的红色连线。
- `edges[].routing: "straight"`：原生XML关闭额外自动绕线。无waypoint时直接连接；有一个waypoint时按显式单直角连接。源／目标端口必须对齐，仍需通过实际渲染的正交和穿框检查。
- `port_bindings`：命名张量端口到真实来源的映射，例如 `{"Qr":{"source":"q_norm","target":"index_q_input","shape":["T",1536]}}`。建图者核对端点、形状和同一张量含义，不能据此添加复制操作。
- `comparison`、`presentation`、`routing_summary`：保存基线与目标版本、显示规则及走线策略。折点数量以 `.layout.json` 的实际routes为准。
- `review.json` 的 `optimization_claims`：将优化按introduced / inherited / backend_specific / unverified记录，附来源、硬件／后端范围及实测边界；不是将所有实现kernel串进模型主干。

标准图形检查只负责结构合法性、证据引用及原生几何；颜色含义、端口语义、softmax轴、缓存读写和模型优化归属仍需模型专属审阅／验证。

## 连线上的输入输出维度

`edges[].label` 是原生连接文字，可用于 `[B,S,64,256]` 等张量形状；`label_font_size` 可设为6–48（默认7，正式大图建议16–20），`label_offset: [dx,dy]` 控制相对连线中点的像素偏移。维度标签应跟随实际计算连接，避免用独立维度表替代；仅有排版变化不得改变source/target或删去计算边。长reshape可分两行并增加算子间距。维度语义与证据由模型构造器核对。

原生导出新增实测 `edge_labels`、`edge_label_node_overlaps` 和 `edge_label_overlaps`；后两项非空时拒绝导出。旧布局报告兼容，但不据此宣称已执行新增标签检查。

`background: "none"`指定透明画布，原生XML写入mxGraphModel.background，PNG同步保留alpha；也可使用六位十六进制背景色。省略时维持白色导出。节点XML样式每个属性仅输出最终值一次，避免导入器处理重复fillColor等属性时产生歧义。
