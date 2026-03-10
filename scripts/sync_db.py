
import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import save_products

def sync_products():
    json_path = 'data/products.json'
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    print(f"Loading products from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Found {len(products)} products.")
    
    # Save to SQLite
    save_products(products)
    print("Database updated successfully.")

if __name__ == "__main__":
    sync_products()
