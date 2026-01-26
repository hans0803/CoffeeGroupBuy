@echo off
chcp 65001
echo ==================================================
echo 咖啡團購系統 - 啟動 Windows 生產伺服器
echo ==================================================

:: 檢查是否安裝 waitress
pip show waitress >nul 2>&1
if %errorlevel% neq 0 (
    echo 未偵測到 waitress，正在安裝...
    pip install waitress
)

echo ==================================================
echo 啟動 Waitress 伺服器 (Port 5001)
echo 請訪問 http://localhost:5001
echo 按 Ctrl+C 停止
echo ==================================================

:: 啟動伺服器
waitress-serve --port=5001 src.app:app
pause
