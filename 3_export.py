#!/usr/bin/env python3
"""
區塊三：收單
匯出訂單到 Excel（商家版 + 內部版）並清空資料庫
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import init_db, get_all_orders, export_orders, clear_orders, update_sales_statistics


def main():
    print("=" * 50)
    print("咖啡團購系統 - 收單")
    print("=" * 50)
    
    # 初始化資料庫
    init_db()
    
    # 檢查訂單數量
    orders = get_all_orders()
    if not orders:
        print("\n⚠️  目前沒有訂單")
        print("=" * 50)
        return
    
    print(f"\n找到 {len(orders)} 筆訂單")
    
    # 確認是否繼續
    confirm = input("\n確定要匯出並清空訂單嗎？(y/N): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 匯出訂單（兩個版本）
    print("\n正在匯出訂單...")
    vendor_path, internal_path = export_orders()
    
    # 更新銷售統計 (累積)
    print("正在更新銷售統計...")
    update_sales_statistics()
    
    # 清空訂單
    print("正在清空訂單...")
    count = clear_orders()
    
    print("\n" + "=" * 50)
    print(f"✅ 收單完成！已處理 {count} 筆訂單")
    print(f"\n📄 商家訂購單: {vendor_path}")
    print(f"📋 內部分發單: {internal_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
