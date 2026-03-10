# 資料庫設計文件 (Database Schema)

本系統使用 **SQLite** 作為主要資料儲存，檔案位於 `data/products.db`。

## 📋 資料表 (Tables)

### 1. `products` (產品表)
儲存從來源網站爬取的咖啡產品資訊。

| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| `id` | TEXT (PK) | 產品唯一 ID (UUID 或 Hash) |
| `sku` | TEXT | 產品編號 |
| `name` | TEXT | 產品名稱 |
| `price` | INTEGER | 售價 (NT$) |
| `original_price` | INTEGER | 原價 (若有) |
| `description` | TEXT | 產品描述 |
| `image_url` | TEXT | 圖片路徑 (本地 static 路徑) |
| `product_url` | TEXT | 官網原始連結 |
| `category` | TEXT | 分類 (beans, drip, giftbox) |
| `roast` | TEXT | 烘焙度 (淺焙, 中焙, 深焙...) |
| `processing` | TEXT | 處理法 (日曬, 水洗...) |
| `created_at` | DATETIME | 建立時間 |
| `purchase_count` | INTEGER | 歷史累積銷量 (用於首頁熱銷排行) |

### 2. `orders` (訂單表)
儲存使用者的訂單主檔。

| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| `id` | TEXT (PK) | 訂單 ID (UUID) |
| `customer_name` | TEXT | 訂購人姓名 |
| `total_amount` | INTEGER | 訂單總金額 |
| `status` | TEXT | 狀態 (pending, submitted, completed) |
| `created_at` | DATETIME | 訂單建立時間 |
| `is_submitted` | BOOLEAN | 是否已結算 (目前主要用 pending) |

### 3. `order_items` (訂單明細表)
儲存訂單內的具體商品項目。

| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| `id` | TEXT (PK) | 明細 ID |
| `order_id` | TEXT (FK) | 關聯訂單 ID |
| `product_id` | TEXT (FK) | 關聯產品 ID |
| `product_name` | TEXT | 產品名稱 (快照，避免產品刪除後顯示錯誤) |
| `price` | INTEGER | 購買時單價 |
| `quantity` | INTEGER | 數量 |

### 4. `reviews` (商品評論表)
儲存使用者對特定商品的評分與留言。

| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| `id` | INTEGER (PK) | 評論自動遞增 ID |
| `product_id` | TEXT (FK) | 關聯產品 ID |
| `reviewer_name` | TEXT | 評論者姓名 (匿名、顯示名稱) |
| `rating` | INTEGER | 評分 (1-5 星) |
| `comment` | TEXT | 評論內容 |
| `created_at` | DATETIME | 建立時間 |

---

## 📄 JSON 儲存

除了 SQLite，部分非結構化或輕量資料使用 JSON 檔案儲存：

### `data/feedback.json` (匿名回饋)
儲存來自前台使用者的匿名建議。
```json
[
  {
    "content": "希望可以增加更多深焙選項",
    "created_at": "2026-01-26 15:30:00"
  }
]
```

### `data/statistics.json` (歷史統計)
儲存上一期團購結算後的歷史統計數據，用於首頁展示「歷史熱銷」。
```json
{
  "top_products": [ ... ],
  "roast_stats": { "中深焙": 10, ... },
  "price_stats": { "50": 5, ... }
}
```
