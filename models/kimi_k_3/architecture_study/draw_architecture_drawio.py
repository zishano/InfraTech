"""Rebuild the editable reconstruction from the canonical reviewed graph.

Export PNG from the resulting draw.io using tools/model_architecture export-png.
Do not independently regenerate architecture PNGs with an image model.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/model_architecture'))
from model_architecture import read, drawio

if __name__ == '__main__':
    graph = read(ROOT / 'tools/model_architecture/examples/kimi_k3.graph.json')
    target = Path(__file__).with_name('kimi_k3_design_preview_v2.drawio')
    drawio(graph, target)
    print(target)
