## Spec Kit 導入指南

### 🎯 目的
- 定義 Spec Kit（Specify CLI + `/speckit.*` 指令）在 `ec-tools` 專案中的使用方式。
- 將既有的 SDD 文檔（如 `weekly_report_sdd.md`、`daily-report` 模組）與 Spec Kit 工作流整合，確保規格、計畫與任務清單可一致維護。
- 提供團隊成員與接手者快速上手的步驟與檢查點。

---

### 🧩 專案現況概覽
- 核心程式碼：
  - `demos/daily-report-mvp/`：日報產生與推播。
  - `demos/weekly-report-generator/`：週報產生與推播。
- 既有 SDD 文檔：
  - `docs/technical/sdd/`：包括 `project-overview.md`、`daily-report.md`、`weekly-report.md`、`weekly-views.md`。
  - `demos/weekly-report-generator/docs/weekly_report_sdd.md`：週報模組的詳細規格。
- 資料目標與設定：
  - `demos/daily-report-mvp/config/targets.yaml`、`clients.yaml` 等管理品牌營收目標。
  - `datalake360-saintpaul` BigQuery 專案提供主要資料來源。
- Spec Kit 原始碼與 CLI：
  - `tools/spec-kit/`：upstream repo，供查閱模板與原始文件。
  - `specify` CLI 已透過 `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` 安裝於本機。

---

### ⚙️ 前置準備
1. **命令與版本檢查**
   ```bash
   uv --version        # uv 套件管理器
   specify --help      # 確認 Specify CLI 可呼叫
   ```
2. **確認 PATH**
   - `uv` 會將工具安裝在 `~/.local/bin`，請確保該路徑納入 shell 的 `PATH`。
3. **AI 助手支援**
   - Spec Kit 支援 Cursor / Copilot / Claude 等多種代理，詳細對應可查 `tools/spec-kit/AGENTS.md`。

---

### 🚀 導入流程（推薦）

| 步驟 | 說明 | 對應指令 / 文件 | 注意事項 |
|------|------|-----------------|----------|
| 1 | 建立專案原則（可選） | `/speckit.constitution` | 若需統一開發守則，可在專案根目錄建立 constitution。 |
| 2 | 撰寫功能規格 | `/speckit.specify` → `specs/<feature>/spec.md` | 聚焦「What / Why」，以需求場景為主。 |
| 3 | 制定技術計畫 | `/speckit.plan` → `plan.md`、`research.md` | 清楚描述架構、資料流、技術限制。 |
| 4 | 任務拆解 | `/speckit.tasks` → `tasks.md` | 產出依賴順序、可平行項目、測試任務。 |
| 5 | 實作執行 | `/speckit.implement` 或手動照 `tasks.md` 執行 | 可由 AI 代理或人工執行，完成後更新狀態。 |
| 6 | 文件同步 | 將產物摘要寫回 `docs/technical/sdd/` 或對應模組的 `*_sdd.md` | 保持 SDD 與 Spec Kit 產出一致。 |

---

### 🗂️ 檔案放置規範
- **Spec Kit 產出**：統一放在 `specs/<feature-folder>/`（可依功能命名，如 `specs/weekly-report-refresh`）。
- **既有 SDD 的同步方式**：
  - `spec.md` → 摘要/需求段落可融入 `docs/technical/sdd/*.md` 或 `*_sdd.md`。
  - `plan.md` → 對應 Implementation Notes、Data Interface、架構說明。
  - `tasks.md` → 可複製重要任務至 `TASKS.md` 或相關專案看板。
- **版本控管**：Spec Kit 產出應納入版本控制，以便審查與歷史回溯。

---

### 📘 範例：週報模組改版流程
1. 於專案根目錄執行（假設目的是擴充推播模組）：
   ```bash
   /speckit.specify 擴充週報推播：需支援多品牌、多渠道通知，包含 SLA 監控與重試策略。
   /speckit.plan 週報推播將使用 Cloud Scheduler + Cloud Run Job，依 brand_id 撈取 BigQuery 資料……
   /speckit.tasks
   ```
2. 產出目錄範例：`specs/weekly-notifier-enhancement/`
3. 完成實作後，將最終決策同步回 `demos/weekly-report-generator/docs/weekly_report_sdd.md` 的對應章節（如推播、排程、Failure Modes）。

---

### 🔄 與既有工作流程的整合
- **SDD 檔案仍為主**：Spec Kit 的 `spec/plan/tasks` 主要補充細節與 AI 代理可執行的結構；最終規格仍應同步回 `docs/technical/sdd/` 或模組內文檔。
- **工作日誌**：重大任務（Spec Kit 產生後的實作）應記錄於 `docs/worklogs/YYYY-MM-DD.md`。
- **TODO / 任務追蹤**：可將 `tasks.md` 內容整合至 `TASKS.md`、Issue Tracker 或外部專案管理工具。
- **AI 代理協作**：在 Cursor / Claude / Copilot 等工具內呼叫 `/speckit.*` 指令時，請保持在專案根目錄執行，確保相對路徑一致。

---

### ✅ 導入檢查清單
- [ ] 已安裝 `uv`、`specify`，並可於 shell 中執行。
- [ ] 熟悉 `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement` 工作流。
- [ ] 確認 `specs/` 產出已納入版本控管並對應到實際功能。
- [ ] 完成實作後，已將重要資訊同步回 SDD 文檔與工作日誌。
- [ ] 團隊成員已知悉此流程，並能在接手時參照本指南快速上手。

---

### 📚 延伸資源
- Spec Kit 官方 README 與 Quick Start：[github/spec-kit](https://github.com/github/spec-kit)
- 內嵌文件：
  - `tools/spec-kit/docs/quickstart.md`
  - `tools/spec-kit/docs/spec-driven.md`
  - `tools/spec-kit/AGENTS.md`
- 專案既有文檔：
  - `docs/technical/sdd/` 系列
  - `demos/weekly-report-generator/docs/weekly_report_sdd.md`
  - `demos/daily-report-mvp/docs/HANDOVER_DOCUMENT.md`

---

### 🧭 後續建議
- 選擇一個近期需求（如「週報推播雲端化」）實際跑一次 `/speckit.*` 流程並記錄心得。
- 若需客製模板，可 fork `tools/spec-kit/templates/` 或建立內部專用模板組。
- 規劃 CI 檢查（如文件格式、Spec kit 任務完成狀態）以確保流程落地。


