# 咖啡團購系統 (Coffee Group Buy System) ☕

> [!CAUTION]
> **免責聲明 (Disclaimer)**
>
> 本專案僅供程式開發學習與內部教育用途，**非官方系統**。
> 本系統之爬蟲功能僅用於示範資料抓取技術，所有抓取之產品圖片、文案與商標權利均歸屬 **原品牌商 (Oklao 歐客佬)** 所有。
> 請勿將此系統部署於公開網路或用於商業營利行為。使用者應自行承擔使用本軟體之所有風險。

一個用於自動化部門同事之間咖啡團購流程的 Flask Web 應用程式。

## ✨ 主要功能更新 (New)

### 1. 📝 訂單與購物管理 (My Orders & Cart)

- 支援 **姓名查詢**、**修改數量**、**刪除訂單** 功能。
- 已加入購物車的商品會以「已在購物車」標示，避免重複購買。
- 專為手機設計的**底部導覽列**，大幅提升手機下單體驗。

### 2. 📊 即時銷售分析與新品 (Dashboard & New Items)

- 首頁看板顯示本期團購的熱銷排行 Top 5 與即時統計圖表（烘焙度、價格帶分佈）。
- 設有「⭐ 本次新品」專區，自動標示最近一次爬蟲更新的新商品。

### 3. ⭐ 商品評論系統 (Reviews)

- 支援 1-5 星評分與文字留言，幫助同事間互相推薦咖啡豆。
- 手機版採用直覺的底部滑出面板 (Bottom Sheet) 閱讀與填寫。

### 4. 💬 匿名回饋系統

- 點擊頁面底部的「匿名回饋」，可直接傳送系統建議給開發者。

### 5. ☁️ 雲端與混合資料庫 (Hybrid Cloud DB)

- **自動切換**: 本地運行使用 SQLite；設定 `DATABASE_URL` 後自動切換為 **Postgres (Neon)** 雲端模式。
- **免本地存儲**: 支援遠端圖片 URL 與動態統計，完美適配 **Vercel** 部署。

---

## 🚀 快速開始

### 0️⃣ 首次安裝 (First Time Setup)

若要在新電腦上使用，請先下載專案：

```bash
git clone https://github.com/hans0803/CoffeeGroupBuy.git
cd CoffeeGroupBuy
```

### 🔄 更新專案 (Git Pull)

若專案有更新（例如功能新增或修復），請先執行以下指令拉取最新程式碼：

```bash
git pull
```

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

### 4️⃣ 雲端部署 (Vercel + Neon)

1. 在 [Neon.tech](https://neon.tech) 建立免費 PostgreSQL 並取得 `DATABASE_URL`。
2. 將連結放入 `.env` (本地) 或 Vercel 環境變數中。
3. 執行 `1_update.py` 將商品資料同步到雲端資料庫。
4. 將程式碼推送到 GitHub，Vercel 會自動完成部署。

---

## 📂 專案結構

```
coffee/
├── api/                   # Vercel 進入點 (index.py)
├── src/                   # 核心模組 (app.py, models.py, scraper.py)
├── data/                  # 本地資料 (SQLite, Excel)
├── static/                # 靜態資源 (CSS, JS, 圖片)
├── templates/             # HTML 模板
├── vercel.json            # Vercel 部署設定
└── config.json            # 網站內容設定
```

## 依賴套件

```bash
pip install -r requirements.txt
```
