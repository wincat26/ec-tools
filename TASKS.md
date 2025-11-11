# AI 營運顧問系統 — 開發任務清單

**建立日期**：2025-01-27  
**最後更新**：2025-11-07

---

## 📋 已完成任務

### ✅ 專案結構建立
- [x] 建立完整資料夾結構（frontend, backend, data, prototype, doc 等）
- [x] 建立 `.gitignore` 檔案
- [x] 建立 `README.md` 專案總覽
- [x] 建立 `PROJECT_STRUCTURE.md` 結構說明文件
- [x] 建立環境變數範本檔案

### ✅ Prototype 開發
- [x] 規劃 Prototype 技術選型（純 HTML/CSS/JS）
- [x] 建立假資料（mockData.js）
- [x] 建立工具函數（utils.js）
- [x] 建立主要樣式（main.css）
- [x] 建立 Dashboard 專用樣式（dashboard.css）
- [x] 建立登入頁面（index.html）
- [x] 建立 Dashboard 主頁面（dashboard.html）
- [x] 實作 Dashboard 互動邏輯（dashboard.js）
- [x] 建立 Prototype README 說明文件
- [x] 數據分析頁「營收與訂單總覽」面板初版
- [x] 數據分析頁「流量分析」指標卡 + AI 洞察整合
- [x] 數據分析頁「平均訂單金額分析」模組化重構
- [x] 數據分析頁「轉換率漏斗分析」主視覺與側欄分區

### ✅ 文件與協作
- [x] 複核 `prototype-dashboard-handoff.md` 交接內容
- [x] 盤點 `prototype` 目錄主要頁面、樣式與腳本模組
- [x] GitHub 遠端同步策略整理（Repo 結構、忽略項目、協作流程）

### ✅ Daily Report MVP
- [x] 改寫 GA4 驗證流程（改讀 `datalake_looker.daily_metrics` 並顯示 warning）
- [x] 調整 Google Chat 卡片（新增 GA4 小字提醒、廣告花費整數化）
- [x] 強化 `run_daily_report.sh`（重試機制、狀態檔、detail log）
- [x] LaunchAgent 排程調整為每日 09:30
- [x] 建立 `docs/worklogs/` 並記錄 2025-11-07 作業

---

## 🔄 進行中任務
### Prototype 優化
- [ ] Dashboard 首屏佈局重構（卡片等高、內容溢出、響應式）
- [ ] JS 載入流程與 Skeleton 行為調整（移除多餘高度計算、優化載入 UX）
- [ ] AI 即時洞察資訊流模組化（資料來源、動態渲染、互動設計）
- [ ] 數據分析頁 Insights／智能診斷資訊架構整併
- [ ] 數據分析頁 KPI 互動（來源切換聯動其他模組）

### Weekly Report Automation
- [ ] 建立 4 個週度 View（overview/ad/member/product）
- [ ] 更新 `weekly-report-generator` 模板為四分頁架構
- [ ] 規劃週報排程腳本與 Google Chat 推播
- [ ] 補齊 weekly-report-generator 交接文件（README / Handover / Quick Start）

---

## 📝 未來規劃任務

### Phase 0: 協作與版本控管
- [x] 建立 GitHub 遠端倉庫並同步 Prototype 首版
- [x] 建立 GitHub Pages 首頁導向（根目錄 index.html → prototype/index.html）
- [ ] 整理 GitHub 專用 README／Wiki（介紹 Demo 路徑、Mock 資料來源）
- [ ] 設定分支策略與 PR Flow（main/develop/feature）
- [ ] 建立 Issue 模板與標籤規則
- [ ] GitHub Pages 啟用與網址驗證（main / root）

### Phase 1: Prototype 優化
- [ ] 優化響應式設計（手機、平板適配）
- [ ] 加入更多互動動畫效果
- [ ] 優化圖表視覺化（考慮使用 Chart.js）
- [ ] 加入任務篩選與搜尋功能
- [ ] 加入 Guideline 評分功能

### Phase 2: 前端開發（Next.js）
- [ ] 初始化 Next.js 專案
- [ ] 設定 Tailwind CSS
- [ ] 建立組件庫（SummaryCard, KPIPyramid, GuidelineCard 等）
- [ ] 實作認證流程（Firebase Auth）
- [ ] 實作 API 整合（與後端對接）

### Phase 3: 後端開發（Node.js + Express）
- [ ] 初始化 Express 專案
- [ ] 設定 BigQuery 連線
- [ ] 建立 API 路由結構
- [ ] 實作 Dashboard 資料查詢 API
- [ ] 實作 Guideline 生成服務
- [ ] 實作任務管理 API

### Phase 4: 資料層開發（BigQuery + Dataform）
- [ ] 設定 Dataform 專案
- [ ] 建立 Staging Layer SQL
- [ ] 建立 Processed Layer SQL
- [ ] 建立指標計算視圖
- [ ] 建立 Guideline Trigger 邏輯

### Phase 5: AI 模組開發
- [ ] 整合 OpenAI API
- [ ] 建立 Prompt 範本系統
- [ ] 實作 Guideline 生成邏輯
- [ ] 實作成效回饋學習機制

---

## 🎯 當前重點

### 優先級 1：Prototype 驗證
- **目標**：透過 Prototype 驗證 UI/UX 設計與使用者流程
- **下一步**：
  1. 開啟 `prototype/index.html` 測試登入流程
  2. 開啟 `prototype/dashboard.html` 測試 Dashboard 功能
  3. 收集使用者回饋並優化設計

### 優先級 2：技術架構確認
- **目標**：確認前後端技術選型與架構設計
- **下一步**：
  1. 確認 Next.js 14+ App Router 設定
  2. 確認 BigQuery 連線與權限設定
  3. 確認 Firebase Auth 整合方式

---

## 📊 專案狀態

| 模組 | 狀態 | 進度 | 備註 |
|------|------|------|------|
| 專案結構 | ✅ 完成 | 100% | 資料夾與設定檔已建立 |
| Prototype | ✅ 完成 | 100% | 可獨立運行，包含所有核心功能 |
| Daily Report MVP | ✅ 完成 | 100% | GA4 驗證、排程、推播皆穩定 |
| Weekly Report Automation | 🔄 進行中 | 20% | 規格 (SDD) 完成，待建立 view 與模板 |
| 月報 / 其他模組 | ⏸️ 待開始 | 0% | 依整體 Roadmap 規劃 |
| 前端（正式版） | ⏸️ 待開始 | 0% | 等待 Prototype 驗證 |
| 後端 / API | ⏸️ 待開始 | 0% | 等待前端需求 |
| 資料層（Dataform） | ⏸️ 待開始 | 0% | 等待週報後續需求 |

---

## 🔗 相關檔案

- [專案結構說明](./PROJECT_STRUCTURE.md)
- [產品認知摘要](./docs/product/產品認知摘要.md)
- [Prototype README](./demos/prototype/README.md)

---

**最後更新**：2025-11-03

