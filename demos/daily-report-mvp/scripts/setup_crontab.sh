#!/bin/bash

# 設定 crontab 的輔助腳本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_SCRIPT="$SCRIPT_DIR/run_daily_report.sh"

echo "🔧 設定 crontab 排程..."
echo ""
echo "腳本位置：$RUN_SCRIPT"
echo ""

# 檢查腳本是否存在
if [ ! -f "$RUN_SCRIPT" ]; then
    echo "❌ 錯誤：找不到執行腳本 $RUN_SCRIPT"
    exit 1
fi

# 設定執行權限
chmod +x "$RUN_SCRIPT"
echo "✅ 已設定執行權限"

# 顯示 crontab 設定
echo ""
echo "請執行以下命令來設定 crontab："
echo ""
echo "crontab -e"
echo ""
echo "然後加入以下行（每天早上 08:00 執行）："
echo ""
echo "0 8 * * * $RUN_SCRIPT"
echo ""
echo "或者使用以下命令直接加入（會覆蓋現有的 crontab）："
echo ""
echo "(crontab -l 2>/dev/null; echo '0 8 * * * $RUN_SCRIPT') | crontab -"
echo ""
echo "⚠️  注意：如果使用上述命令，會覆蓋現有的 crontab 設定"
echo ""

read -p "是否要自動加入 crontab？（y/N）: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 備份現有的 crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null
    
    # 加入新的排程（避免重複）
    (crontab -l 2>/dev/null | grep -v "$RUN_SCRIPT"; echo "0 8 * * * $RUN_SCRIPT") | crontab -
    
    echo "✅ crontab 已更新"
    echo ""
    echo "目前的 crontab 設定："
    crontab -l
else
    echo "已取消，請手動設定 crontab"
fi

