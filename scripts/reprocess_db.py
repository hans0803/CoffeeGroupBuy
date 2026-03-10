
import sqlite3
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.scraper import extract_roast, extract_processing

def reprocess_db():
    conn = sqlite3.connect('data/products.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM products")
    products = cursor.fetchall()
    
    updated_count = 0
    for pid, name in products:
        roast = extract_roast(name)
        processing = extract_processing(name)
        
        if roast or processing:
            # Check if update is needed (optional, but good for log)
            # define logic: if DB value is None but extracted is not None
            cursor.execute("SELECT roast, processing FROM products WHERE id = ?", (pid,))
            cur_roast, cur_proc = cursor.fetchone()
            
            if cur_roast != roast or cur_proc != processing:
                print(f"Updating {name}: Roast [{cur_roast} -> {roast}], Proc [{cur_proc} -> {processing}]")
                cursor.execute("UPDATE products SET roast = ?, processing = ? WHERE id = ?", (roast, processing, pid))
                updated_count += 1
            
    conn.commit()
    conn.close()
    
    print(f"Reprocessed {len(products)} items. Updated {updated_count} items with new metadata.")

    # 匯出 Result 到 products.json 以供檢查
    print("Syncing DB to products.json...")
    try:
        import json
        conn = sqlite3.connect('data/products.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        
        products_list = [dict(row) for row in rows]
        
        # 確保路徑正確
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'products.json')
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(products_list, f, indent=2, ensure_ascii=False)
            
        print(f"Synced {len(products_list)} items to {json_path}")
        conn.close()
    except Exception as e:
        print(f"Error syncing JSON: {e}")

if __name__ == "__main__":
    reprocess_db()
