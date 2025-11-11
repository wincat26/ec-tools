#!/bin/bash

# 排程狀態檢查工具
# 用途：診斷排程是否正常運作

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
STATUS_FILE="$PROJECT_DIR/logs/last_run_status.txt"
LOG_FILE="$PROJECT_DIR/logs/cron.log"
ERROR_LOG="$PROJECT_DIR/logs/cron_error.log"

echo "🔍 排程狀態檢查"
echo "=========================================="
echo ""

# 1. 檢查 LaunchAgent 服務狀態
echo "📋 1. LaunchAgent 服務狀態"
echo "----------------------------------------"
if launchctl list | grep -q "com.daily-report"; then
    echo "✅ LaunchAgent 服務已載入"
    launchctl list | grep daily-report
else
    echo "❌ LaunchAgent 服務未載入"
    echo "💡 執行以下命令載入："
    echo "   ./scripts/setup_launchagent.sh"
fi
echo ""

# 2. 檢查 plist 檔案
echo "📋 2. LaunchAgent 設定檔"
echo "----------------------------------------"
PLIST_FILE="$HOME/Library/LaunchAgents/com.daily-report.plist"
if [ -f "$PLIST_FILE" ]; then
    echo "✅ plist 檔案存在：$PLIST_FILE"
    echo "   排程時間：$(plutil -p "$PLIST_FILE" | grep -A 2 StartCalendarInterval | grep -E "(Hour|Minute)" | tr '\n' ' ')"
else
    echo "❌ plist 檔案不存在"
fi
echo ""

# 3. 檢查最後執行狀態
echo "📋 3. 最後執行狀態"
echo "----------------------------------------"
if [ -f "$STATUS_FILE" ]; then
    STATUS=$(head -n 1 "$STATUS_FILE")
    TIMESTAMP=$(sed -n '2p' "$STATUS_FILE")
    
    if [ "$STATUS" = "SUCCESS" ]; then
        echo "✅ 最後執行：成功"
        echo "   時間：$TIMESTAMP"
    else
        echo "❌ 最後執行：失敗"
        echo "   時間：$TIMESTAMP"
        if [ -f "$STATUS_FILE" ] && [ $(wc -l < "$STATUS_FILE") -gt 2 ]; then
            echo "   錯誤碼：$(tail -n 1 "$STATUS_FILE")"
        fi
    fi
else
    echo "⚠️  尚未執行過（或狀態檔不存在）"
fi
echo ""

# 4. 檢查日誌檔案
echo "📋 4. 日誌檔案"
echo "----------------------------------------"
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(wc -l < "$LOG_FILE")
    LAST_LOG=$(tail -n 5 "$LOG_FILE")
    echo "✅ 執行日誌存在（共 $LOG_SIZE 行）"
    echo "   最後 5 行："
    echo "$LAST_LOG" | sed 's/^/   /'
else
    echo "⚠️  執行日誌不存在"
fi
echo ""

if [ -f "$ERROR_LOG" ]; then
    ERROR_SIZE=$(wc -l < "$ERROR_LOG")
    if [ "$ERROR_SIZE" -gt 0 ]; then
        LAST_ERROR=$(tail -n 3 "$ERROR_LOG")
        echo "⚠️  錯誤日誌存在（共 $ERROR_SIZE 行）"
        echo "   最後 3 行："
        echo "$LAST_ERROR" | sed 's/^/   /'
    else
        echo "✅ 錯誤日誌為空（無錯誤）"
    fi
else
    echo "✅ 錯誤日誌不存在（無錯誤）"
fi
echo ""

# 5. 檢查 Python 環境
echo "📋 5. Python 環境"
echo "----------------------------------------"
PYTHON_PATHS=(
    "/opt/anaconda3/bin/python"
    "$(which python3 2>/dev/null)"
    "$(which python 2>/dev/null)"
)

FOUND=0
for PYTHON_PATH in "${PYTHON_PATHS[@]}"; do
    if [ -n "$PYTHON_PATH" ] && [ -f "$PYTHON_PATH" ]; then
        VERSION=$("$PYTHON_PATH" --version 2>&1)
        echo "✅ 找到 Python: $PYTHON_PATH"
        echo "   版本：$VERSION"
        FOUND=1
        break
    fi
done

if [ $FOUND -eq 0 ]; then
    echo "❌ 找不到 Python 執行檔"
fi
echo ""

# 6. 檢查專案檔案
echo "📋 6. 專案檔案"
echo "----------------------------------------"
if [ -f "$PROJECT_DIR/main.py" ]; then
    echo "✅ main.py 存在"
else
    echo "❌ main.py 不存在"
fi

if [ -f "$PROJECT_DIR/config/clients.yaml" ]; then
    echo "✅ config/clients.yaml 存在"
else
    echo "❌ config/clients.yaml 不存在"
fi

if [ -f "$PROJECT_DIR/scripts/run_daily_report.sh" ]; then
    if [ -x "$PROJECT_DIR/scripts/run_daily_report.sh" ]; then
        echo "✅ run_daily_report.sh 存在且可執行"
    else
        echo "⚠️  run_daily_report.sh 存在但無執行權限"
        echo "💡 執行：chmod +x $PROJECT_DIR/scripts/run_daily_report.sh"
    fi
else
    echo "❌ run_daily_report.sh 不存在"
fi
echo ""

# 7. 建議
echo "📋 7. 建議操作"
echo "----------------------------------------"
if ! launchctl list | grep -q "com.daily-report"; then
    echo "1. 載入 LaunchAgent："
    echo "   cd $PROJECT_DIR && ./scripts/setup_launchagent.sh"
    echo ""
fi

if [ -f "$STATUS_FILE" ] && [ "$(head -n 1 "$STATUS_FILE")" = "FAILED" ]; then
    echo "2. 最後執行失敗，建議："
    echo "   - 查看錯誤日誌：tail -f $ERROR_LOG"
    echo "   - 手動測試執行：./scripts/run_daily_report.sh"
    echo ""
fi

echo "3. 測試執行："
echo "   cd $PROJECT_DIR && ./scripts/run_daily_report.sh"
echo ""

echo "=========================================="
echo "檢查完成"

