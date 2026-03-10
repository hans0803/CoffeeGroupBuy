# 系統架構文件 (System Architecture)

本文件描述咖啡團購系統的技術架構與設計理念。

## 🛠 技術堆疊 (Tech Stack)

### 後端 (Backend)
- **語言**: Python 3
- **框架**: Flask (Web Framework)
- **資料庫**: SQLite (本地輕量資料庫)
- **伺服器 (Production)**: Gunicorn (WSGI HTTP Server)

### 前端 (Frontend)
- **模板引擎**: Jinja2 (Flask 內建)
- **樣式**: Vanilla CSS (CSS3, Flexbox, Grid)
- **互動**: Vanilla JavaScript (ES6+, Fetch API)
- **圖表**: Chart.js (用於銷售儀表板)
- **UI Components**:
  - **Bottom Navigation**: Sticky bottom bar for mobile (≤ 768px) replacing hamburger menus.
  - **Bottom-Sheets**: Filter sidebars and review modals natively transform into swipe-dismissible bottom sheets on mobile.

### 爬蟲 (Scraper)
- **工具**: Requests + BeautifulSoup4
- **目標**: 來源網站 (Source Site)
- **資源**: 自動下載產品圖片至 `static/images/products/`

---

## 📂 系統模組架構

```
coffee/
├── config.json      # [設定] 網站設定檔
├── 1_update.py      # [入口] 爬蟲更新模組
├── 2_server.py      # [入口] 開發伺服器
├── 3_export.py      # [入口] 匯出報表模組
├── run_prod.sh      # [入口] 生產部署腳本
├── src/
│   ├── app.py       # Flask 應用核心、路由定義
│   ├── models.py    # 資料庫模型與操作 (ORM-like)
│   └── scraper.py   # 爬蟲邏輯
├── data/
│   ├── products.db  # 主要資料庫
│   └── feedback.json # 匿名回饋存檔
└── templates/       # HTML 視圖
```

## 🔄 核心流程 (Core Flows)

### 1. 產品同步 (Update Flow)
1. 執行 `1_update.py`
2. `scraper.py` 請求官網分類頁面
3. 解析產品名稱、價格、連結
4. **圖片下載**: 檢查本地 `static/images/products/` 是否存在，若無則下載
5. **資料去重**: 透過 SKU 或名稱檢查資料庫，更新價格
6. 存入 SQLite `products` 表格

### 2. 訂購流程 (Ordering Flow)
1. 使用者訪問首頁 (`/`) 或分類頁 (`/products/<cat>`)
2. `app.py` 查詢 SQLite，渲染頁面
3. 使用者加入購物車 -> 存入 Session (`session['cart']`)
4. 結帳頁面 (`/cart`) 輸入姓名
5. 提交訂單 (`POST /api/orders`)
   - 建立 `Order` 紀錄
   - 建立多筆 `OrderItem` 紀錄
   - 清空購物車
   - **更新即時統計**: `get_current_sales_statistics` 隨之變動

### 3. 商品評論流程 (Review Flow)
1. 使用者在商品卡片點擊「撰寫評論」。
2. 前端彈出 Modal 或 Bottom-Sheet 輸入 1-5 星評分與留言。
3. 提交至 `POST /api/reviews/<product_id>`。
4. 儲存於資料庫，前端即時更新該商品的平均星數與評論數量。

### 3. 即時儀表板 (Dashboard Flow)
1. 訪問 `/orders`
2. 後端 `get_current_sales_statistics()`:
   - 撈取所有 `orders` 與 `order_items`
   - 計算 Top 10 熱銷商品
   - 統計「烘焙度」分佈 (Pie Chart)
   - 統計「價格帶」銷量 (Bar Chart)
3. 前端透過 Chart.js 渲染圖表，若無數據則顯示空狀態動畫

### 4. 結算匯出 (Export Flow)
1. 執行 `3_export.py`
2. `export_orders_to_xlsx`:
   - **商家訂購單**: 按產品匯總數量 (Group by Product)
   - **內部分發單**: 按人員分組 (Group by Customer)，列出每人明細與總額
3. 使用 `openpyxl` 產生 Excel 檔案並套用樣式
4. 更新 `data/statistics.json` 做為歷史紀錄
5. (可選) 清空 `orders` 資料表，開啟新一輪團購
