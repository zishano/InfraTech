"""Rebuild editable XML; PNG must be exported from it with export-png."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/model_architecture'))
from model_architecture import read,drawio
if __name__=='__main__':
    drawio(read(ROOT/'tools/model_architecture/examples/deepseek_v4_flash.graph.json'),
           Path(__file__).with_name('deepseek_v4_flash.drawio'))
