#!/bin/bash

# 設定 LaunchAgent 的輔助腳本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$LAUNCH_AGENTS_DIR/com.daily-report.plist"

echo "🔧 設定 LaunchAgent 排程..."
echo ""
echo "專案目錄：$PROJECT_DIR"
echo ""

# 建立 LaunchAgents 目錄（如果不存在）
mkdir -p "$LAUNCH_AGENTS_DIR"

# 建立 plist 檔案
cat > "$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.daily-report</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$PROJECT_DIR/scripts/run_daily_report.sh</string>
    </array>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/anaconda3/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>GOOGLE_CLOUD_PROJECT</key>
        <string>datalake360-saintpaul</string>
    </dict>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/logs/launchd.log</string>
    
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/logs/launchd_error.log</string>
    
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "✅ 已建立 plist 檔案：$PLIST_FILE"
echo ""

# 確保執行腳本有執行權限
chmod +x "$PROJECT_DIR/scripts/run_daily_report.sh"
echo "✅ 已設定執行腳本權限"
echo ""

# 載入 LaunchAgent（使用新的 macOS 語法）
# macOS 10.11+ 使用 bootstrap 子系統
if launchctl list | grep -q "com.daily-report"; then
    echo "🔄 卸載現有服務..."
    launchctl bootout gui/$(id -u)/com.daily-report 2>/dev/null || \
    launchctl unload "$PLIST_FILE" 2>/dev/null
fi

echo "📦 載入 LaunchAgent..."
launchctl bootstrap gui/$(id -u) "$PLIST_FILE" 2>/dev/null || \
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent 已載入"
    echo ""
    echo "目前狀態："
    launchctl list | grep daily-report || echo "  服務已載入（等待排程時間）"
    echo ""
    echo "管理命令："
    echo "  查看狀態：launchctl list | grep daily-report"
    echo "  立即執行：launchctl start com.daily-report"
    echo "  查看日誌：tail -f $PROJECT_DIR/logs/launchd.log"
    echo "  查看錯誤：tail -f $PROJECT_DIR/logs/launchd_error.log"
    echo "  卸載服務：launchctl bootout gui/\$(id -u)/com.daily-report"
    echo ""
    echo "📊 排程時間：每天早上 09:00"
else
    echo "❌ LaunchAgent 載入失敗"
    echo "💡 提示：請檢查 plist 檔案格式是否正確"
    exit 1
fi

