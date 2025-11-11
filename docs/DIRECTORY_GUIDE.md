# 資料夾結構與用途說明

**最後更新**：2025-11-07

---

## 根目錄（Project Root）
| 路徑 | 用途 | 備註 |
|------|------|------|
| `README.md` | 專案總覽（完全版平台願景） | 與產品定位對齊。 |
| `PROJECT_STRUCTURE.md` | 詳細的資料夾結構說明 | v2.0。 |
| `TASKS.md` | 任務清單（最新更新 2025-11-07） | 記錄 Prototype / Daily / Weekly。 |
| `交接文件檢查報告.md` | 交接文件盤點結果（2025-11-05） | 建議後續補週報文件。 |
| `完整文件檢查報告.md` | 全專案文檔檢查報告 | 用於文件治理。 |
| `scripts/` | 共用腳本（目前空） | 後續可放工具腳本。 |
| `sdd_template.txt` | SDD 撰寫模板 | 便利新 SDD 建立。 |

---

## 主要模組
| 資料夾 | 功能 | 使用方式 |
|--------|------|-----------|
| `frontend/` | Next.js 正式前端（規劃中） | 暫無程式；等待 Prototype 驗證。 |
| `backend/` | Node.js/Express 後端（規劃中） | 暫無實作。 |
| `data/` | BigQuery/Dataform 腳本（規劃中） | 已建目錄，待建模。 |
| `demos/` | Demo / MVP / Prototype 專案集合 | 每個子目錄各自有 README／docs。 |
| `docs/` | 官方文件（prd、product、technical 等） | 詳細說明見下方。 |
| `doc/` | 歷史遺留文件（尚未整理） | 建議後續整併到 `docs/`。 |
| `archive/` | 備份與臨時檔 | 歷史 HTML/PDF、tmp 資料。 |
| `prototype/` | GitHub Pages 轉址頁（導向 `demos/prototype/`） | 保留舊 URL 兼容。 |

---

## `demos/` 內子專案
| 目錄 | 描述 | 重要檔案 |
|------|------|----------|
| `daily-report-mvp/` | 每日數據日報 MVP | `docs/HANDOVER_DOCUMENT.md`, `scripts/run_daily_report.sh` 等。 |
| `weekly-report-generator/` | 週報生成工具（待強化） | `README.md`, `docs/` (部分空檔需補)、`src/main.py`。 |
| `prototype/` | HTML Prototype Demo | `README.md`, `css/`, `js/`、各頁面 。 |
| `ecommerce-growth-planner/` | 舊版 POE Demo | `README.md`。 |
| `daily-report-mvp/logs/` | 日報執行 log | `cron.log`, `launchd.log` 等。 |

---

## `docs/` 內子資料夾
| 資料夾 | 用途 | 說明 |
|--------|------|------|
| `prd/` | PRD 原始文件（txt） | 包含背景、功能列表、資料流程等。 |
| `product/` | 產品企劃/設計文件 | Sitemap、Onboarding、MRD 等。 |
| `technical/` | 技術文檔與 SDD | 內含 `sdd/` (Project-level, Daily, Weekly)、待新增 technical note。 |
| `guidelines/` | 開發/設計規範 | 遊戲化、八角框架等。 |
| `config/` | 配置文件（暫空） | 待填。 |
| `scripts/` | 文檔用腳本（暫空） | 待填。 |
| `log/` | 文檔變動紀錄（暫空） | 待填。 |
| `worklogs/` | 工作日誌 | 2025-11-07 起紀錄。 |
| `REORGANIZATION_SUMMARY.md` | 2025-01-27 結構重整說明 | 目前為空，待補。 |
| `VISION_AND_STRATEGY.md` | 整體願景與策略 | 與產品定位一致。 |

> **doc vs docs**：`docs/` 是目前正式使用的文檔資料夾；`doc/` 為歷史遺留，內容待釐清並搬移。建議逐步整併到 `docs/` 後刪除 `doc/`。 |

---

## 根目錄文件放置原因
- `交接文件檢查報告.md`、`完整文件檢查報告.md` 兩檔位於 root：
  - 方便快速檢視專案文件健康度；
  - 作為上層 oversight 文件。
- 若希望集中，可搬至 `docs/` 下（需同步更新參考連結）。

---

## 建議
1. **doc/ 清理**：確認內容後搬至 `docs/`，減少混淆。
2. **週報交接文件**：於 `demos/weekly-report-generator/docs/` 補寫 README/Handover（可引用 SDD）。
3. **`docs/REORGANIZATION_SUMMARY.md`**：填寫重整歷程（目前為空）。
4. **根目錄報告**：評估是否移至 `docs/`，讓 root 更精簡。

