# 部署指南 (Deployment Guide)

本系統支援兩種運行模式：**開發模式** 與 **生產模式**。

## 1. 系統需求
- Python 3.8+
- SQLite 3
- Gunicorn (生產環境用)

## 2. 安裝依賴
在專案根目錄執行：
```bash
pip install -r requirements.txt
```
(將會自動安裝 Flask, Gunicorn, BeautifulSoup4, OpenPyXL 等套件)

## 3. 運行模式

### 🟢 生產模式 (Production) - 推薦
適合多人同時使用。使用 Gunicorn 作為 WSGI 伺服器，支援多工處理 (Multi-workers)。

**啟動指令**:
```bash
sh run_prod.sh
```

### 🟡 開發模式 (Development)
適合本地測試與開發。
```bash
python 2_server.py
```

## 4. 維運操作

### 更新產品資料
```bash
python 1_update.py
```

### 匯出訂單與結算
當團購結束時，執行匯出並清空資料庫：
```bash
python 3_export.py
```

## 5. 雲端部署 (Vercel + Neon) - ✨ 全新支援

本系統現在支援透過 **Vercel** 進行無伺服器 (Serverless) 部署。

### 步驟 A：建立資料庫
1. 在 [Neon.tech](https://neon.tech) 建立一個免費的 PostgreSQL 專案。
2. 取得 `DATABASE_URL` 連線字串。

### 步驟 B：同步商品資料
在本地電腦設定 `.env` 包含雲端 `DATABASE_URL`，然後執行：
```bash
python 1_update.py
```
這會將最新的商品資料從官網爬取並直接寫入雲端 Neon 資料庫。

### 步驟 C：Vercel 設定
1. 將專案推送到 GitHub。
2. 在 Vercel 建立新專案。
3. 在 **Settings -> Environment Variables** 加入：
   - `DATABASE_URL`: 您的 Neon 連線字串。
4. Vercel 會讀取 `vercel.json` 並自動完成部署。

### 步驟 D：圖片與統計
- **圖片**: 系統現在使用遠端 URL，因此 Vercel 不需存放圖片檔案。
- **統計**: 首頁圖表改為從 DB 即時計算，確保資料在無伺服器環境下依然持久且準確。
