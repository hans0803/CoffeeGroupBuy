# 咖啡團購系統 (Coffee Group Buy System) ☕

> [!CAUTION]
> **免責聲明 (Disclaimer)**
>
> 本專案僅供程式開發學習與內部教育用途，**非官方系統**。
> 本系統之爬蟲功能僅用於示範資料抓取技術，所有抓取之產品圖片、文案與商標權利均歸屬 **原品牌商 (Oklao 歐客佬)** 所有。
> 請勿將此系統部署於公開網路或用於商業營利行為。使用者應自行承擔使用本軟體之所有風險。

一個用於自動化部門同事之間咖啡團購流程的 Flask Web 應用程式。

## ✨ 主要功能更新 (New)

### 1. 📝 訂單管理 (My Orders)

- 訪問 `/my-orders` 或點擊導覽列「我的訂單」。
- 支援 **姓名查詢**、**修改數量**、**刪除訂單** 功能。

### 2. 📊 即時銷售分析 (Dashboard)

- 訪問 `/orders` 查看本期團購的熱銷排行與統計圖表。
- 包含烘焙度與價格帶分佈分析。

### 3. 💬 匿名回饋系統

- 點擊頁面底部的「匿名回饋」，可直接傳送建議給開發者。
- 內容儲存於本地 JSON。

---

## 🚀 快速開始

### 1️⃣ 更新網站 - 執行爬蟲

```bash
python 1_update.py
```

- 從**來源網站**爬取最新產品
- **下載圖片到本地** (`static/images/products/`)
- 儲存到 SQLite 資料庫

### 2️⃣ 啟動服務 (Server)

#### 開發模式 (單人測試)

```bash
python 2_server.py
```

#### 🟢 生產模式 (多人瀏覽 - 推薦)

若要讓多人同時連線點餐，請使用生產模式啟動：

```bash
sh run_prod.sh
```

- 使用 Gunicorn 啟動 4 個工作程序 (Workers)
- 大幅提升併發處理能力
- 瀏覽器打開：`http://localhost:5001`
- **區域網路分享**: 同事可透過 `http://<你的IP>:5001` 連線
    - Mac 查詢 IP: `ipconfig getifaddr en0` (例如 `192.168.1.100`)
    - Windows 查詢 IP: `ipconfig`

### 3️⃣ 收單 - 匯出並清空

```bash
python 3_export.py
```

- 產生商家訂購單與內部分發單 (.xlsx)
- 自動更新首頁的歷史熱銷排行
- 完成後可選擇是否清空當期訂單

---

## 📂 專案結構

```
coffee/
├── config.json            # 網站內容設定檔 (首頁文字/公告)
├── 1_update.py            # 入口：更新網站
├── 2_server.py            # 入口：啟動伺服器 (開發)
├── 3_export.py            # 入口：收單匯出
├── run_prod.sh            # 入口：啟動伺服器 (生產/Gunicorn)
├── src/                   # 核心模組
│   ├── app.py             # Flask 應用程式 (含 API)
│   ├── models.py          # 資料庫模型
│   └── scraper.py         # 產品爬蟲
├── data/                  # 資料儲存 (忽略 Git)
│   ├── products.db        # SQLite 資料庫
│   ├── feedback.json      # 匿名回饋
│   └── *.xlsx             # 匯出報表
├── static/
│   ├── images/products/   # 產品圖片 (忽略 Git)
│   ├── style.css
│   └── app.js
└── templates/             # HTML 模板
    ├── index.html         # 首頁 (含 Dashboard)
    ├── products.html      # 產品列表 (含篩選)
    ├── my_orders.html     # 我的訂單
    └── ...
```

## 依賴套件

```bash
pip install -r requirements.txt
```
