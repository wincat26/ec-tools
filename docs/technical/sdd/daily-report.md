# Step A：每日數據日報 SDD

## Purpose
- 自動彙整前一日營運指標，於工作日早上推播 Google Chat，提供即時異常偵測與行動提醒。

## Functions
| 功能 | 說明 |
|------|------|
| A1. 客戶/目標設定載入 | `config/clients.yaml`, `config/targets.yaml` 讀取。 |
| A2. GA4 驗證 | 使用 `daily_metrics.total_sessions` 判斷數據是否同步；若延遲顯示 warning。 |
| A3. 指標生成 | `DailyAggregationGenerator` 查詢 `daily_metrics` 與 BigQuery 其他表，輸出 JSON。 |
| A4. 推播 & 日誌 | Google Chat 卡片推播，logs 更新至 `logs/cron.log`, `docs/worklogs/`。 |

## Implementation Notes
- 排程：LaunchAgent `com.daily-report` → 09:30。腳本：`scripts/run_daily_report.sh`（含重試、狀態檔）。
- 指標來源：`datalake_looker.daily_metrics`（營收、訂單、Sessions、廣告花費）。
- Warning Display：若 GA4 未同步，在卡片「營收公式拆解」區塊顯示灰字提醒。
- 乾跑模式：`python main.py --client client_A --dry-run` 用於驗證。
- 待辦：無。日報系統目前穩定。 |

