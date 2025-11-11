# 任務規劃文件（tasks.md）
**功能名稱**：強化多品牌 Weekly Report 產線  
**分支名稱**：`1-weekly-report-pipeline-enhancement`  
**輸出目標**：可依序執行、可獨立驗證的開發與部署任務清單  

---

## Phase 1：專案初始化（Setup Phase）

> 建立專案結構、環境與雲端基礎設定，所有後續任務皆依此階段為基礎。

- [ ] T001 建立專案目錄結構（`/src`, `/tests`, `/contracts`, `/infra`）
- [ ] T002 初始化 Git 分支與 GCP 專案設定（`/infra/gcp/`）
- [ ] T003 建立 Cloud Run 容器化基礎 Dockerfile（`/infra/docker/Dockerfile`）
- [ ] T004 [P] 建立 requirements.txt 並安裝主要依賴（Python / Node.js）
- [ ] T005 設定 BigQuery 與 GCS 存取權限（`/infra/gcp/iam-config.yaml`）
- [ ] T006 初始化 SendGrid API 金鑰與 SMTP 測試環境（`/infra/email/config.json`）
- [ ] T007 建立 `.env` 模板並記錄環境變數需求（`/infra/env.example`）
- [ ] T008 設定專案 CI/CD（Cloud Build YAML, 自動部署至 Cloud Run）

---

## Phase 2：基礎模組構建與關鍵研究（Foundational Phase）

> 建立共用資料結構、基礎模組與排程／監控框架。

- [ ] T009 建立 BigQuery 資料存取層（`/src/data/bq_client.py`）
- [ ] T010 [P] 建立 GCS 儲存模組（`/src/data/gcs_storage.py`）
- [ ] T011 設計並建立報表執行紀錄表 `weekly_report_runs`（`/infra/bq/schema.sql`）
- [ ] T012 設定 Cloud Scheduler Job（`/infra/gcp/scheduler.yaml`）
- [ ] T013 建立 Cloud Run Job 觸發 API（`/src/jobs/report_job.py`）
- [ ] T014 [P] 設定 IAM 角色：Cloud Scheduler → Cloud Run Job（`/infra/gcp/permissions.yaml`）
- [ ] T015 [P] 設定 Pub/Sub Topic 以支援 SLA 告警流程（`/infra/gcp/pubsub-alerts.yaml`）
- [ ] T016 整合 Stackdriver 監控並建立 SLA 指標（`/infra/gcp/monitoring.yaml`）
- [ ] T017 撰寫環境初始化腳本（`/scripts/init_env.sh`）
- [ ] T029 ⚠️ 前置：LINE Notify API/權限/速率研究（`/research/line_notify.md`，完成後才能進行 Phase 4 推播開發）

---

## Phase 3：使用者故事一（US1）- 自動產生多品牌報表（P1）

> 系統應能依照多品牌設定自動生成 HTML 週報，並於每週一 11:30 觸發。

- [ ] T018 [US1] 實作報表生成邏輯（`/src/core/report_generator.py`）
- [ ] T019 [US1] 串接 BigQuery daily_metrics / weekly_* 視圖（`/src/data/query_metrics.py`）
- [ ] T020 [US1] [P] 生成多品牌報表模板渲染器（`/src/templates/weekly_report.html`）
- [ ] T021 [US1] 設定報表生成時間上限 < 5 分鐘（timeout 控制）
- [ ] T022 [US1] 儲存報表 HTML 至 GCS（`/src/data/gcs_storage.py`）
- [ ] T023 [US1] 寫入執行紀錄至 BigQuery（`weekly_report_runs`）
- [ ] T024 [US1] 新增單元測試（`/tests/test_report_generator.py`）

---

## Phase 4：使用者故事二（US2）- 推播模組擴充與整合（P1）

> 系統需支援多通路推播（Google Chat、Email、LINE Notify），並具備容錯與備援。

- [ ] T025 [US2] 整合現有 Google Chat 推播（`/src/notify/google_chat.py`）
- [ ] T026 [US2] 新增 Email 備援模組（`/src/notify/email_sender.py`）
- [ ] T027 [US2] 實作通路選擇邏輯與 fallback 流程（`/src/notify/dispatcher.py`）
- [ ] T028 [US2] [P] 撰寫 LINE Notify Plugin 原型（`/src/notify/plugins/line_notify.py`）
- [ ] T030 [US2] [P] 實作 Plugin Loader 機制（`/src/notify/plugin_loader.py`）
- [ ] T031 [US2] 實作錯誤重試與 log 機制（`/src/notify/retry_handler.py`）
- [ ] T032 [US2] 推播模組整合測試（`/tests/test_notify_dispatcher.py`）

---

## Phase 5：使用者故事三（US3）- SLA 告警與降級報告（P2）

> 當 GA4 或 Shopline 資料延遲、排程失敗或生成超時時，系統需自動告警並降級報告。

- [ ] T033 [US3] 實作 SLA 監控邏輯（`/src/monitoring/sla_checker.py`）
- [ ] T034 [US3] 建立告警觸發流程（Pub/Sub → 通知服務）（`/src/monitoring/alert_dispatcher.py`）
- [ ] T035 [US3] 降級報表生成邏輯（顯示「資料不完整」標記）（`/src/core/degraded_report.py`）
- [ ] T036 [US3] 測試 SLA 模擬案例（`/tests/test_sla_checker.py`）
- [ ] T037 [US3] 驗證 Pub/Sub 訂閱與 Stackdriver 整合（`/infra/gcp/pubsub-test.yaml`）

---

## Phase 6：使用者故事四（US4）- 報表備份與派發紀錄（P2）

> 系統需在報表生成後記錄派發資訊，並支援後續查詢。

- [ ] T038 [US4] 新增 ReportSummary 實體模型（`/src/models/report_summary.py`）
- [ ] T039 [US4] 記錄報表派發 log 至 BigQuery（`weekly_report_runs`）
- [ ] T040 [US4] 建立 API 介面：查詢最新週報摘要（`/contracts/get_latest_report.yaml`）
- [ ] T041 [US4] 實作 API Endpoint（`/src/api/get_latest_report.py`）
- [ ] T042 [US4] [P] 撰寫單元測試（`/tests/test_get_latest_report.py`）

---

## Phase 7：測試與驗證（Testing & Validation）

> 驗證所有模組之間整合運作正確，涵蓋乾跑、Sandbox、E2E 測試。

- [ ] T043 建立 Sandbox brand 測試配置（`/tests/config/sandbox_brand.json`）
- [ ] T044 [P] 實作乾跑模式（dry-run，不實際推播）（`/src/jobs/dry_run_mode.py`）
- [ ] T045 建立 E2E 測試場景（`/tests/test_end_to_end.py`）
- [ ] T046 [P] 執行多品牌併行壓力測試（初期以雙品牌：聖保羅 + 勤億，後續再擴充至 ≥5 brands）（`/tests/test_concurrency.py`）
- [ ] T047 驗證 Cloud Scheduler job log 與告警回報（`/tests/test_scheduler_logs.py`）
- [ ] T048 匯整測試報告與通過率（`/reports/testing_summary.md`）

---

## Phase 8：收尾與文件同步（Polish & Documentation）

> 文件化流程、更新使用手冊與部署說明。

- [ ] T049 更新 `quickstart.md`，新增 LINE Plugin 配置指引
- [ ] T050 [P] 補充 `research.md` 中 LINE Notify 決策與 API 參數
- [ ] T051 更新 `plan.md`，加入 Stackdriver 指標與 SLA 成本
- [ ] T052 同步 `README.md`，補充部署與測試指令
- [ ] T053 檢查 `.env.example` 與實際環境變數一致性
- [ ] T054 完成代碼註解與型別提示（`/src/**/*.py`）
- [ ] T055 最終回歸測試 + 版本標記 (`v1.0.0-rc1`)

---

## 依賴關係圖（Dependency Graph）

Phase 1 → Phase 2 → US1 → US2 → (US3, US4 可併行) → Testing → Polish


---

## 可平行執行任務（Parallel Opportunities）

| 任務 | 描述 |
|------|------|
| T004, T010, T014 | 初始化依賴可平行 |
| T020, T028, T030 | 模組設計並行開發 |
| T044, T046 | 測試階段可併行執行 |
| T050, T051 | 文件更新可同步進行 |

---

## 建議 MVP 範圍

> **最小可行版本（MVP）** 應涵蓋：
- US1（自動生成多品牌報表）
- US2（LINE Notify 正式推播 + Email 備援；Google Chat 僅供 SIT/UAT 測試）
- SLA 初步監控（僅延遲告警）
  
完成後即可內部試運行，後續再加入 LINE Plugin 與降級報表功能。

---

## 任務統計摘要

| 類別 | 任務數量 |
|------|----------|
| Setup | 8 |
| Foundational | 9 |
| US1 | 7 |
| US2 | 8 |
| US3 | 5 |
| US4 | 5 |
| Testing | 6 |
| Polish | 7 |
| **總計** | **55 項任務** |

---

## 檔案輸出報告

**輸出路徑**：  
`specs/1-weekly-report-pipeline-enhancement/tasks.md`  

**摘要**：  
- ✅ 共產生 55 項明確任務  
- ✅ 含可平行任務 7 組  
- ✅ 每個使用者故事具獨立驗證標準  
- ✅ 提供 MVP 範圍與開發順序  
- ✅ 格式符合 `/speckit.tasks` 規範（checkbox + ID + Story + path）
