import sqlite3
import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
SQLITE_PATH = 'data/products.db'

def migrate():
    if not DATABASE_URL:
        print("❌ Error: DATABASE_URL not found in .env file")
        return

    print(f"🚀 Starting migration from {SQLITE_PATH} to Neon...")
    
    # 1. Connect to both
    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    pg_conn = psycopg2.connect(DATABASE_URL)
    
    sqlite_curr = sqlite_conn.cursor()
    pg_curr = pg_conn.cursor()
    
    try:
        # 2. Migrate Orders
        sqlite_curr.execute("SELECT * FROM orders")
        orders = sqlite_curr.fetchall()
        print(f"📦 Found {len(orders)} orders locally.")
        
        # 3. Migrate Products (specifically purchase_count)
        sqlite_curr.execute("SELECT id, name, purchase_count FROM products WHERE purchase_count > 0")
        products = sqlite_curr.fetchall()
        print(f"📦 Found {len(products)} products with sales history locally.")
        
        for p in products:
            pg_curr.execute(
                "UPDATE products SET purchase_count = %s WHERE name = %s OR id = %s",
                (p['purchase_count'], p['name'], p['id'])
            )

        # 4. Migrate Reviews
        sqlite_curr.execute("SELECT * FROM reviews")
        reviews = sqlite_curr.fetchall()
        print(f"💬 Found {len(reviews)} reviews locally.")
        
        for review in reviews:
            pg_curr.execute(
                "INSERT INTO reviews (product_id, reviewer_name, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (review['product_id'], review['reviewer_name'], review['rating'], review['comment'], review['created_at'])
            )
            
        pg_conn.commit()
        print("✅ Migration successful!")
        
    except Exception as e:
        pg_conn.rollback()
        print(f"❌ Migration failed: {e}")
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    migrate()
