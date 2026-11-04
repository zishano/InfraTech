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
