@echo off
chcp 65001
echo ==================================================
echo 咖啡團購系統 - 啟動 Windows 生產伺服器
echo ==================================================

:: 檢查是否安裝 waitress
:: 檢查是否安裝 waitress
python -m pip show waitress >nul 2>&1
if %errorlevel% neq 0 (
    echo 未偵測到 waitress，準備安裝依賴套件...
)

echo 檢查並安裝所需的依賴套件 (requirements.txt)...
python -m pip install -r requirements.txt

:: 讀取 Config 中的 Port
for /f "tokens=*" %%i in ('python -c "import json; print(json.load(open('config.json', encoding='utf-8'))['server']['port'])"') do set PORT=%%i

echo ==================================================
echo 啟動 Waitress 伺服器 (Port %PORT%)
echo 本機訪問: http://localhost:%PORT%
echo 區網訪問: 請使用下方 IPv4 位址
ipconfig | findstr /R /C:"IPv4 Address" /C:"IP Address"
echo 按 Ctrl+C 停止
echo ==================================================

:: 啟動伺服器
python -m waitress --host=0.0.0.0 --port=%PORT% src.app:app
pause
