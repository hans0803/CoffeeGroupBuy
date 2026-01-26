#!/usr/bin/env python3
"""
Coffee Product Scraper
爬取來源網站的咖啡產品資訊
"""

import json
import re
import os
import time
import hashlib
from typing import Optional
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.oklaocoffee.net"
# 圖片目錄在專案根目錄的 static/images/products
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images', 'products')

# 目標分類 URL
CATEGORIES = {
    "beans": "/categories/coffeebean-%E5%92%96%E5%95%A1%E8%B1%86%E8%B2%B72%E9%80%811",
    "drip": "/categories/oklaoalldripcoffee",
    "giftbox": "/categories/oklao-drip-coffee-gift-box-%E4%BC%81%E6%A5%AD%E9%80%81%E7%A6%AE-%E5%92%96%E5%95%A1%E7%A6%AE%E7%9B%92-%E4%BC%B4%E6%89%8B%E7%A6%AE",
    "giftbox_newyear": "/pages/oklao-new-year-coffee-gift-box"
}

CATEGORY_NAMES = {
    "beans": "咖啡豆",
    "drip": "濾掛包",
    "giftbox": "咖啡禮盒",
    "giftbox_newyear": "新春禮盒"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}


def ensure_images_dir():
    """確保圖片目錄存在"""
    os.makedirs(IMAGES_DIR, exist_ok=True)


def download_image(image_url: str, product_id: str) -> str:
    """
    下載圖片到本地

    Args:
        image_url: 圖片網址
        product_id: 產品 ID（用於檔名）

    Returns:
        本地圖片路徑（相對於 static），失敗則回傳空字串
    """
    if not image_url:
        return ""

    ensure_images_dir()

    # 使用 product_id 作為檔名，避免特殊字元
    safe_id = hashlib.md5(product_id.encode()).hexdigest()[:12]

    # 取得副檔名
    ext = '.jpg'
    if '.png' in image_url.lower():
        ext = '.png'
    elif '.webp' in image_url.lower():
        ext = '.webp'

    filename = f"{safe_id}{ext}"
    filepath = os.path.join(IMAGES_DIR, filename)

    # 如果檔案已存在，直接回傳
    if os.path.exists(filepath):
        return f"/static/images/products/{filename}"

    try:
        response = requests.get(image_url, headers=HEADERS, timeout=30, verify=False)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        return f"/static/images/products/{filename}"

    except Exception as e:
        print(f"  下載圖片失敗 {product_id}: {e}")
        return ""


@dataclass
class Product:
    """咖啡產品資料結構"""
    id: str
    sku: str
    name: str
    price: int
    original_price: Optional[int]
    image_url: str
    product_url: str
    category: str
    category_name: str
    roast: Optional[str] = None
    processing: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


def extract_price(price_text: str) -> int:
    """從價格文字中提取數字"""
    if not price_text:
        return 0
    # 移除貨幣符號和逗號，只保留數字
    numbers = re.findall(r'\d+', price_text.replace(',', ''))
    if numbers:
        return int(numbers[0])
    return 0


def extract_roast(name: str) -> Optional[str]:
    """從名稱解析烘焙度"""
    # 按照長度排序，優先匹配較長/精確的詞彙
    roast_keywords = [
        '黑金烘焙(深烘)', '白金烘培(中烘)', '黃金烘焙(中淺)',
        '黑金烘焙', '黑金烘培',
        '白金烘培', '白金烘焙',
        '黃金烘焙', '黃金烘培',
        '淺烘焙', '淺烘培', '淺焙',
        '中烘焙', '中烘培', '中焙',
        '中深烘焙', '中深烘培', '中深焙',
        '深烘焙', '深烘培', '深焙',
        '中淺焙', '慢火烘焙'
    ]
    for keyword in roast_keywords:
        if keyword in name:
            return keyword
    return None


def extract_processing(name: str) -> Optional[str]:
    """從名稱解析處理法"""
    # 按照長度排序，優先匹配較長/精確的詞彙
    processing_keywords = [
        '厭氧緩慢日曬', '酵素水洗處理', '厭氧日曬處理', '葡萄乾蜜處理',
        '黑蜜處理', '紅蜜處理', '黃蜜處理', '白蜜處理',
        '厭氧水洗', '厭氧日曬', '雙重厭氧',
        '日曬處理', '水洗處理', '蜜處理',
        '日曬', '水洗', '濕刨法', '半水洗'
    ]
    for keyword in processing_keywords:
        if keyword in name:
            return keyword
    return None


def scrape_category_page(category_key: str, page: int = 1, limit: int = 24) -> tuple[list[Product], bool]:
    """
    爬取單一分類的單一頁面

    Returns:
        tuple: (產品列表, 是否有下一頁)
    """
    category_path = CATEGORIES.get(category_key)
    if not category_path:
        raise ValueError(f"Unknown category: {category_key}")

    url = f"{BASE_URL}{category_path}?page={page}&limit={limit}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return [], False

    soup = BeautifulSoup(response.text, 'lxml')
    products = []

    # 尋找所有產品項目
    product_items = soup.select('a.Product-item')

    for item in product_items:
        try:
            # 從 ga-product 屬性解析 JSON 資料
            ga_product = item.get('ga-product', '{}')
            try:
                product_data = json.loads(ga_product)
            except json.JSONDecodeError:
                product_data = {}

            product_id = product_data.get('id', '')
            sku = product_data.get('sku', '')

            # 取得產品名稱
            title_elem = item.select_one('.title')
            name = title_elem.get_text(strip=True) if title_elem else product_data.get('title', '未知產品')

            # 取得價格
            price_elem = item.select_one('.price')
            price_text = price_elem.get_text(strip=True) if price_elem else '0'
            price = extract_price(price_text)

            # 取得原價（如有折扣）
            original_price_elem = item.select_one('.compare-at-price, .original-price')
            original_price = None
            if original_price_elem:
                original_price = extract_price(original_price_elem.get_text(strip=True))

            # 取得圖片 URL
            img_elem = item.select_one('img')
            image_url = ''
            if img_elem:
                # 優先使用 data-src（lazy loading），否則用 src
                image_url = img_elem.get('data-src') or img_elem.get('src') or ''
                if image_url and not image_url.startswith('http'):
                    image_url = f"{BASE_URL}{image_url}"

            # 取得產品連結
            product_url = item.get('href', '')
            if product_url and not product_url.startswith('http'):
                product_url = f"{BASE_URL}{product_url}"

            if product_id or name != '未知產品':
                # 下載圖片到本地
                local_image_path = download_image(image_url, product_id or sku or str(hash(name)))

                # 解析屬性
                roast = extract_roast(name)
                processing = extract_processing(name)

                product = Product(
                    id=product_id or sku or str(hash(name)),
                    sku=sku,
                    name=name,
                    price=price,
                    original_price=original_price,
                    image_url=local_image_path,
                    product_url=product_url,
                    category=category_key,
                    category_name=CATEGORY_NAMES.get(category_key, category_key),
                    roast=roast,
                    processing=processing
                )
                products.append(product)

        except Exception as e:
            print(f"Error parsing product: {e}")
            continue

    # 檢查是否有下一頁
    has_next = len(product_items) >= limit

    return products, has_next


def scrape_products(category_key: str, max_pages: int = 10) -> list[Product]:
    """
    爬取指定分類的所有產品

    Args:
        category_key: 分類鍵值 (beans, drip, giftbox)
        max_pages: 最大頁數限制

    Returns:
        產品列表
    """
    all_products = []
    page = 1

    print(f"開始爬取分類: {CATEGORY_NAMES.get(category_key, category_key)}")

    while page <= max_pages:
        print(f"  正在爬取第 {page} 頁...")
        products, has_next = scrape_category_page(category_key, page)

        if not products:
            break

        all_products.extend(products)

        if not has_next:
            break

        page += 1
        time.sleep(1)  # 避免請求過快

    print(f"  完成！共爬取 {len(all_products)} 個產品")
    return all_products


def scrape_all_products() -> list[Product]:
    """爬取所有分類的產品"""
    all_products = []

    for category_key in CATEGORIES.keys():
        products = scrape_products(category_key)
        all_products.extend(products)
        time.sleep(2)  # 分類間暫停

    return all_products


def save_products_json(products: list[Product], filepath: str = "data/products.json"):
    """將產品資料儲存為 JSON 檔案"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    data = [p.to_dict() for p in products]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已儲存 {len(products)} 個產品到 {filepath}")


if __name__ == "__main__":
    # 測試爬蟲
    print("=" * 50)
    print("咖啡產品爬蟲")
    print("=" * 50)

    products = scrape_all_products()

    print("\n" + "=" * 50)
    print(f"總計爬取 {len(products)} 個產品")
    print("=" * 50)

    # 儲存結果
    save_products_json(products)

    # 儲存到資料庫
    try:
        from .models import save_products
        # Convert Product objects to simple dicts if needed, but save_products expects dicts
        products_dicts = [p.to_dict() for p in products]
        save_products(products_dicts)
    except ImportError:
        print("Warning: Could not import save_products from models. DB not updated.")
    except Exception as e:
        print(f"Error saving to DB: {e}")

    # 顯示範例
    if products:
        print("\n範例產品:")
        for p in products[:3]:
            print(f"  - {p.name}: NT${p.price}")
