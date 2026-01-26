#!/bin/bash
# 啟動 Gunicorn 伺服器 (適合生產環境與多人瀏覽)
# 使用方式: sh run_prod.sh

# 檢查是否安裝 gunicorn
if ! command -v gunicorn &> /dev/null; then
    echo "未偵測到 gunicorn，正在安裝..."
    pip install gunicorn
fi

echo "=================================================="
echo "啟動 Gunicorn 伺服器 (Port 5001, 4 Workers)"
echo "請訪問 http://localhost:5001"
echo "按 Ctrl+C 停止"
echo "=================================================="

# 啟動命令
# -w 4: 4個工作進程 (適合處理並發)
# -b 0.0.0.0:5001: 綁定所有IP的 5001 Port
# src.app:app: 指定 flask app 位置
gunicorn -w 4 -b 0.0.0.0:5001 src.app:app
