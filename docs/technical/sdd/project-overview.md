# 聖保羅營運自動化專案 SDD（Project-Level)

## 1. Purpose
- 建立「日報 + 週報」自動化系統，協助營運團隊每日掌握即時狀況、每週完成策略回顧與行動追蹤。
- 以 `BigQuery` 為單一數據源，透過 Python 腳本、GitHub Pages/Chat Webhook 提供圖文化輸出。

## 2. Core Functions
| 模組 | 說明 | 主要輸入 / 輸出 |
|------|------|----------------|
| F1. Daily Report MVP | 每天 09:30 自動彙整前一天數據、推播 Google Chat。 | Inputs: `daily_metrics` view；Output: Chat 卡片、logs |
| F2. Weekly Report Automation | 每週一 09:00 產出四分頁 HTML 週報與推播。 | Inputs: 週度 Views；Output: `weekly_report_YYYYWW.html`、Chat |
| F3. Data Views Layer | 維護日/週指標 view，提供一致的 KPI 計算規則。 | Inputs: 訂單、GA4、廣告、會員表；Output: `daily_metrics`, `weekly_*` views |
| F4. Monitoring & Worklogs | 排程狀態監測、工作日誌自動紀錄。 | Inputs: 腳本執行狀態；Output: `docs/worklogs/*.md` |

## 3. Data Architecture
- **來源**：Shopline 訂單、GA4 `events_*`, Google Ads / Meta Ads 花費、會員資料。
- **View 層**：每日 `daily_metrics`（已存在）、新建週度 `weekly_overview_metrics`、`weekly_ad_metrics`、`weekly_member_metrics`、`weekly_product_metrics`。
- **應用**：`demos/daily-report-mvp`, `demos/weekly-report-generator`。

## 4. Execution Steps（與子 SDD 對應）
1. **Step A**：維護每日數據 view & 日報（既有）→ SDD: `daily-report.md`
2. **Step B**：建置週度 view 層（新需求）→ `weekly-views.md`
3. **Step C**：調整週報產出流程（四分頁）→ `weekly-report.md`
4. **Step D**：排程、自動推播與工作日誌 → `automation-and-monitoring.md`

## 5. Repository 狀態（2025-11-07）
| 目錄 | 角色 | 優化動作 |
|------|------|-----------|
| `demos/daily-report-mvp/` | 日報腳本與文件 | GA4 驗證改為 view、排程為 09:30。 |
| `demos/weekly-report-generator/` | 週報腳本 | 待接入週度 view + 四分頁模板。 |
| `demos/prototype/` | Prototype 靜態頁 | GitHub Pages 使用 `.../demos/prototype/` 路徑；根目錄保有轉址頁。 |
| `docs/worklogs/` | 工作日誌 | 自 2025-11-07 起記錄日常作業。 |
| `docs/technical/sdd/` | 本文件夾 | 存放專案 SDD 與各步驟規格。 |


