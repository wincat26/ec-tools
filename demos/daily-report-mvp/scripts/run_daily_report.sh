#!/bin/bash

# 每日數據彙整日報執行腳本（改進版）
# 用途：供 crontab 或 LaunchAgent 使用
# 特色：錯誤處理、重試機制、詳細日誌

set -e  # 遇到錯誤立即退出（但我們會手動處理）

# 取得腳本所在目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# 切換到專案目錄
cd "$PROJECT_DIR"

# 建立 logs 目錄（如果不存在）
mkdir -p logs

# 日誌檔案
LOG_FILE="$PROJECT_DIR/logs/cron.log"
ERROR_LOG="$PROJECT_DIR/logs/cron_error.log"
STATUS_FILE="$PROJECT_DIR/logs/last_run_status.txt"

# 函數：記錄日誌
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ ERROR: $1" | tee -a "$ERROR_LOG" | tee -a "$LOG_FILE"
}

# 函數：檢查 Python 環境
check_python() {
    # 嘗試多個可能的 Python 路徑
    PYTHON_PATHS=(
        "/opt/anaconda3/bin/python"
        "$(which python3)"
        "$(which python)"
        "/usr/local/bin/python3"
    )
    
    for PYTHON_PATH in "${PYTHON_PATHS[@]}"; do
        if [ -f "$PYTHON_PATH" ] && "$PYTHON_PATH" --version >/dev/null 2>&1; then
            echo "$PYTHON_PATH"
            return 0
        fi
    done
    
    log_error "找不到可用的 Python 執行檔"
    return 1
}

# 函數：執行日報（帶重試）
run_daily_report() {
    local PYTHON_CMD="$1"
    local CLIENT="$2"
    local REPORT_DATE="$3"
    local MAX_RETRIES=3
    local RETRY_DELAY=60  # 重試間隔（秒）
    
    for attempt in $(seq 1 $MAX_RETRIES); do
        log "嘗試執行日報（第 $attempt 次/$MAX_RETRIES）"
        
        if "$PYTHON_CMD" main.py --client "$CLIENT" --date "$REPORT_DATE" >> "$LOG_FILE" 2>&1; then
            log "✅ 日報執行成功"
            echo "SUCCESS" > "$STATUS_FILE"
            echo "$(date '+%Y-%m-%d %H:%M:%S')" >> "$STATUS_FILE"
            return 0
        else
            local EXIT_CODE=$?
            log_error "日報執行失敗（退出碼：$EXIT_CODE）"
            
            if [ $attempt -lt $MAX_RETRIES ]; then
                log "等待 $RETRY_DELAY 秒後重試..."
                sleep $RETRY_DELAY
            else
                log_error "已達最大重試次數，執行失敗"
                echo "FAILED" > "$STATUS_FILE"
                echo "$(date '+%Y-%m-%d %H:%M:%S')" >> "$STATUS_FILE"
                echo "Exit code: $EXIT_CODE" >> "$STATUS_FILE"
                return 1
            fi
        fi
    done
}

# 主程式開始
log "=========================================="
log "開始執行每日數據彙整日報"
log "=========================================="

# 設定環境變數
export PATH="/opt/anaconda3/bin:/usr/local/bin:$PATH"
export GOOGLE_CLOUD_PROJECT="datalake360-saintpaul"

# 檢查 Python 環境
PYTHON_CMD=$(check_python)
if [ $? -ne 0 ]; then
    log_error "Python 環境檢查失敗"
    exit 1
fi
log "使用 Python: $PYTHON_CMD"

# 檢查專案檔案
if [ ! -f "main.py" ]; then
    log_error "找不到 main.py，請確認專案目錄正確"
    exit 1
fi

# 檢查客戶設定檔
if [ ! -f "config/clients.yaml" ]; then
    log_error "找不到 config/clients.yaml"
    exit 1
fi

# 計算昨日日期（T-1）
YESTERDAY=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d '1 day ago' '+%Y-%m-%d')
log "報告日期：$YESTERDAY"

# 執行日報（帶重試機制）
if run_daily_report "$PYTHON_CMD" "client_A" "$YESTERDAY"; then
    log "=========================================="
    log "✅ 日報執行完成"
    log "=========================================="
    exit 0
else
    log "=========================================="
    log_error "❌ 日報執行失敗"
    log "=========================================="
    exit 1
fi

