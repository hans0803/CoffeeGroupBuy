#!/usr/bin/env python3
"""
區塊一：更新網站
執行爬蟲來更新本地產品資訊與圖片
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import init_db, save_products
from src.scraper import scrape_all_products


def main():
    print("=" * 50)
    print("咖啡團購系統 - 更新網站")
    print("=" * 50)
    
    # 初始化資料庫
    init_db()
    
    # 執行爬蟲（會自動下載圖片）
    print("\n正在爬取產品資料並下載圖片...")
    products = scrape_all_products()
    
    # 儲存到資料庫
    products_dict = [p.to_dict() for p in products]
    save_products(products_dict)
    
    print("\n" + "=" * 50)
    print(f"✅ 更新完成！共 {len(products)} 個產品")
    print("=" * 50)


if __name__ == "__main__":
    main()
