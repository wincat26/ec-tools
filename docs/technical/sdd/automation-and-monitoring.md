# Step D：排程、自動推播與監控 SDD

## Purpose
- 確保日報與週報在指定時間自動生成、推播並留下執行紀錄與錯誤警示。

## Functions
| 功能 | 說明 |
|------|------|
| D1. 排程設定 | macOS LaunchAgent (日報 `com.daily-report`, 週報 `com.weekly-report`)；或 GitHub Actions 備援。 |
| D2. 執行腳本 | `scripts/run_daily_report.sh`, `scripts/run_weekly_report.sh`（待新增） → 負責設環境、重試、寫 log。 |
| D3. 狀態監控 | `logs/cron.log`, `logs/last_run_status.txt`，以及 `scripts/check_schedule_status.sh` 擴充為支援週報。 |
| D4. 推播 | Google Chat Webhook (日報/週報)；週報附 HTML 連結，日報為卡片資訊。 |
| D5. 工作日誌 | 自動 append 執行結果至 `docs/worklogs/YYYY-MM-DD.md`。 |

## Implementation Checklist
- LaunchAgent plist 放置於 `~/Library/LaunchAgents/`，設定 `StartCalendarInterval` (日報 09:30，每日；週報 09:00，週一)。
- 腳本返回值：0 → 成功；非 0 → 記錄失敗並發送警示。
- Chat 推播：
  - 日報：摘要 KPI + GA4 warning。
  - 週報：三條亮點/缺口 + 週報 URL。
- 日誌 Schema:
  ```
  - **HH:MM** － <任務>（成功/失敗）
    - KPI 摘要...
    - 備註...
  ```
- 監控腳本需檢查：plist 是否載入、最近執行時間、log 檔有無 ERROR、狀態檔是否 SUCCESS。

