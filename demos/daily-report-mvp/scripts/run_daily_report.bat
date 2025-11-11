@echo off
REM 每日數據彙整日報執行腳本（Windows）
REM 用途：供 Windows 工作排程器使用

REM 設定專案目錄（請根據實際路徑調整）
set PROJECT_DIR=%~dp0..
cd /d "%PROJECT_DIR%"

REM 設定 Python 路徑（請根據實際路徑調整）
set PYTHON_PATH=C:\path\to\python.exe

REM 設定環境變數
set GOOGLE_CLOUD_PROJECT=datalake360-saintpaul

REM 建立 logs 目錄（如果不存在）
if not exist logs mkdir logs

REM 執行日報程序
echo ========================================== >> logs\cron.log
echo 執行時間：%date% %time% >> logs\cron.log
echo ========================================== >> logs\cron.log

"%PYTHON_PATH%" main.py --client client_A >> logs\cron.log 2>&1

if %ERRORLEVEL% EQU 0 (
    echo ✅ 日報執行成功 >> logs\cron.log
) else (
    echo ❌ 日報執行失敗（退出碼：%ERRORLEVEL%） >> logs\cron.log
)

echo. >> logs\cron.log

exit /b %ERRORLEVEL%

