# Step C：週報產出（週報 HTML）SDD

## Purpose
- 以四分頁 HTML 呈現聖保羅上一週營運狀態，含總覽、廣告、會員經營、建議行動方案。

## Functions
| 功能 | 說明 |
|------|------|
| C1. 資料讀取 | 讀取 Step B 建立的週度 view (overview/ad/member/product)。 |
| C2. 模板渲染 | 使用 Jinja2 & PyEcharts 生成四個 Tab 的 HTML 報告。 |
| C3. 洞察文字 | 根據北極星 KPI、WoW 指標、商品旗標自動產生摘要。 |
| C4. 檔案輸出 | 儲存至 `demos/weekly-report-generator/output/weekly_report_YYYYWW.html`。 |

## Page 設計
### Page 1：總覽
- KPI 卡：業績達成率、GMV、營業額、ROAS、Sessions、CVR、AOV、新會員。
- 北極星 KPI：新會員增長 vs 目標、SRI（附護欄提醒）。
- WoW 表格 + 趨勢折線。

### Page 2：廣告
- 平台 KPI（花費、曝光、點擊、ROAS）。
- 活動列表：排序 by 花費或營收，附 WoW。
- 異常提醒：ROAS < 2 或 WoW 花費 -30% 等。

### Page 3：會員經營
- 新客激活率、未購名單、可聯絡資源、回購率。
- 新/舊客熱銷 Top 商品表格。
- 會員洞察 bullet（挑戰與槓桿）。

### Page 4：建議行動方案
- 優先任務 3~5 項（含影響、負責、時間）。
- 商品待優化清單（人氣高但轉換低）。
- 廣告與會員操作建議摘要。

## Implementation Notes
- 模板路徑：`demos/weekly-report-generator/templates/report_template.html`（需新增 Tabs）。
- 圖表：使用 PyEcharts (折線、長條、漏斗、圓餅)。
- JSON 結構：透過 `report_builder` 將 View 資料整理為 `context` dict。
- 測試：`python src/main.py --week 2025-W45 --dry-run` 檢查 HTML。 |

## Task Breakdown — 週報模組精準任務拆解
| 任務代碼 | 任務名稱 | 詳細描述 | 依賴 | 交付物 | 驗收標準 |
|----------|----------|----------|------|--------|----------|
| T1 | 需求對齊與資料盤點 | 整理週報四分頁的 KPI、圖表、文字需求；確認 `datalake_stpl`、`analytics_304437305`、`datalake_looker.daily_metrics` 欄位是否覆蓋；若缺欄位提出補充。 | `docs/reference/HANDOVER_DOCUMENT.md`、`weekly_report_sdd.md` | 更新後的需求摘要（Notion/MD） | 所有 KPI 均有資料來源、算法清楚，利害關係人確認 ✅ |
| T2 | 週度 View Schema 定義 | 與資料團隊確認 Step B 產出的週度 View (`weekly_overview`, `weekly_ads`, `weekly_member`) 欄位、型別、計算邏輯；補齊 `weekly-views.md` 文件。 | T1、`docs/technical/sdd/weekly-views.md` | Schema 表格與欄位描述 | View 可被 Query，欄位命名統一且通過 `scripts/check_schema.py` |
| T3 | DataFetcher 擴充 | 在 `src/data/fetcher.py` 實作抓取週度 View 與 GA4/Shopline 補充資料；支援 `--week` 參數與冪等執行。 | T2、程式碼庫 | Fetcher 模組 PR | 單元測試覆蓋主要函式；`python src/main.py --dry-run` 成功取得資料 |
| T4 | DataProcessor 與指標計算 | 實作週對週比較、占比、SRI、廣告 ROAS、會員活躍度等計算；標準化格式供模板使用。 | T3 | Processor 模組 PR + 計算規格 | 指標與手動驗算誤差 < 1%；邏輯寫入 `DATA_REQUIREMENTS.md` |
| T5 | 模板結構與 UI Layout | 將模板拆為四個 Tab，定義區塊（KPI cards、圖表、表格、洞察 bullet）；建立共用樣式與色盤設定。 | T1 | 更新 `report_template.html` + `config/charts.py` | 本地渲染頁面符合設計稿；Lighthouse 基本檢查通過 |
| T6 | PyEcharts Chart 實作 | 依頁面需求製作折線、柱狀、漏斗、圓餅圖；封裝 `charts/generator.py` 參數；確保圖例與色彩對應 8 類流量。 | T5 | Chart 模組 PR | 圖表可在 HTML 正常渲染，縮放/匯出正常；Example JSON 測試通過 |
| T7 | 洞察與 AI 摘要 | 依 `weekly_report_sdd.md` 中的規則撰寫摘要與 CTA 生成邏輯，預留 LLM 接口。 | T4 | `src/ai/summary.py` 更新 | 回傳摘要文字符合條件 mapping；測試涵蓋主要分支 |
| T8 | Report Builder 整合 | 組合資料、圖表、AI 摘要到模板，輸出檔名遵循 `{brand}_{artifact}_{timestamp}.html`；寫入 log 與雲端備份。 | T3-T7 | Builder 模組 PR | `output/saintpaul_weekly_report_*.html` 產出成功；備份路徑正確；log 含 SUCCESS |
| T9 | 推播訊息服務 | 擴充 `utils/notifier.py` 或新增模組，使用升級模板；支援多渠道與重試。 | T7、T8 | Notifier 模組 PR + 配置文件 | 本地模擬推播成功；失敗時重試並記錄 backlog |
| T10 | 自動化排程與監控 | 設定 Cloud Scheduler / Airflow 任務；串接監控（Slack/PagerDuty）；更新 `automation-and-monitoring.md`。 | T8、T9 | 排程設定檔、Runbook | 排程在沙盒環境成功執行 3 次；監控事件可收到通知 |
| T11 | 品質保證與驗收 | 撰寫整合測試、端對端測試（資料→HTML→推播）；建立 checklist 與回歸腳本。 | T3-T10 | 測試報告、Checklist | 測試全部通過；利害關係人 UAT 簽核 |
| T12 | 營運交接與知識庫 | 更新 `weekly_report_sdd.md`、`weekly_report_runbook.md`（若無則建立）；安排營運實際演練。 | T11 | 文件、培訓記錄 | 文件完成且上傳；營運能獨立操作並完成一次推播 |

