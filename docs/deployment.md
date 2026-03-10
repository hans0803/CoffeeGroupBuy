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
或直接執行:
```bash
gunicorn -w 4 -b 0.0.0.0:5001 src.app:app
```

**參數說明**:
- `-w 4`: 啟動 4 個 Worker processes，可同時處理 4 個併發請求。
- `-b 0.0.0.0:5001`: 綁定所有網路介面，Port 5001。
- `src.app:app`: 指定 Flask Application 的入口物件。

---

### 🟡 開發模式 (Development)
適合開發與除錯。使用 Flask 內建伺服器。

**啟動指令**:
```bash
python 2_server.py
```
**特性**:
- 支援 Hot Reload (程式碼修改後自動重啟)
- 單執行緒 (Single-threaded)，不適合多人同時操作。

## 4. 維運操作

### 更新產品資料
定期執行爬蟲以更新產品：
```bash
python 1_update.py
```

### 匯出訂單與結算
當團購結束時，執行匯出並清空資料庫：
```bash
python 3_export.py
```
- 產出檔案位於 `data/` 目錄。
- 建議備份 `data/orders_*.xlsx` 檔案。

## 5. 常見問題 (FAQ)

**Q: 為何執行 `run_prod.sh` 出現 Permission denied?**
A: 腳本可能沒有執行權限，請執行：
```bash
chmod +x run_prod.sh
```

**Q: 如何更改 Port?**
A: 修改 `run_prod.sh` 中的 `-b 0.0.0.0:5001`，將 5001 改為想要的 Port。
