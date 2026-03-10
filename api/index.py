import sys
import os

# 將專案根目錄加入 PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app
