#!/usr/bin/env python3
"""
區塊二：啟動 Flask 服務
啟動網站伺服器（不會自動爬取）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import app
from src.models import init_db, get_categories


def main():
    print("=" * 50)
    print("咖啡團購系統 - 啟動伺服器")
    print("=" * 50)
    
    # 初始化資料庫
    init_db()
    
    # 檢查產品數量
    categories = get_categories()
    if categories:
        total = sum(c['count'] for c in categories)
        print(f"已載入 {total} 個產品")
    else:
        print("⚠️  尚無產品資料，請先執行 1_update.py")
    
    print("=" * 50)
    print("伺服器啟動中... 請訪問 http://localhost:5001")
    print("按 Ctrl+C 停止伺服器")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5001)


if __name__ == "__main__":
    main()
