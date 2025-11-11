# 強化多品牌 Weekly Report 產線

## 短名（Short Name）

`weekly-report-pipeline-enhancement`

---

## 功能規格書（Feature Specification）

### 一、功能名稱
強化多品牌 Weekly Report 產線

---

### 二、問題陳述（Problem Statement）

目前營運團隊的 weekly report 產出流程存在下列問題：

- 各品牌報表需人工觸發或分別執行，導致 **跨品牌管理困難、作業時間長**。  
- 資料來源（GA4、Shopline）存在 **資料分散資源分散**，若報表延誤，缺乏自動化告警與降級策略。    
- 缺乏 **行動建議摘要**，使管理層難以根據數據即時採取動作。

---

### 三、目標（Goals）

#### 🎯 業務目標（Business Goals）

- 提升營運報表自動化程度與可用性。  
- 減少跨品牌報表彙整時間（目標：從 2 小時降至 <10 分鐘）。  
- 增強營運團隊決策效率與行動追蹤能力。

#### 👤 使用者目標（User Goals）

- 營運經理：可於每週固定時段自動接收各品牌報表與摘要。  
- 品牌老闆：能跨品牌快速掌握營運狀況與重點行動建議。  

#### 🚫 非目標（Non-Goals）

- 不處理報表可視化引擎改版（維持現有模板）。  
- 不特地去追求新資料來源整合。  

---

### 四、使用情境與流程（User Scenarios & Flow）

#### 核心流程：

1. **排程觸發**：  
   每週一 11:30（GMT+8）需透過穩定的排程機制觸發報告生成（可使用 GCP Cloud Scheduler + Cloud Run Job，或後續規劃的獨立排程服務）。  

2. **資料拉取與生成**：  
   - 依照多品牌參數（brand_id list）串接 Datalake （目前這個產品將匯集多個資料源）。  
   - 若任一品牌資料延遲超過閾值（預設 30 分鐘），觸發 SLA 告警。  
   - 成功收集資料後生成四分頁 HTML 週報（業績摘要、流量來源、轉換成效、建議行動）。

3. **AI 行動摘要生成**：  
   系統使用 AI 模組生成文字版「營運行動摘要」，供管理層參考。  

4. **報表推播**：  
   - 主要通路：Google Chat（沿用現有 Webhook 模組）  
   - 備援通路：Email（SendGrid / SMTP）  
   - 延伸通路：LINE Notify（需先進行插件與 API 研究，定義授權流程與訊息模板後再啟用）  

5. **報表完成與 SLA 驗證**：  
   若生成過程超過 5 分鐘，記錄降級狀態並上報監控系統。

---

### 五、功能需求（Functional Requirements）

| 編號 | 功能項目 | 說明 | 驗收標準 |
|------|----------|------|----------|
| FR1 | 多品牌報表生成 | 支援多品牌（brand_id）參數化輸入，自動生成各品牌週報 | 報表生成時間 < 5 分鐘 |
| FR2 | 自動排程產出 | 以 GCP Cloud Scheduler + Cloud Run Job 自動執行 | 每週一 11:30 準時觸發 |
| FR3 | 多通路推播 | 報表推播至 Google Chat、Email 備援、LINE Notify（延伸） | 三通路皆可配置與啟用測試 |
| FR4 | SLA 告警機制 | 若 GA4/Shopline 延遲或生成逾時，系統自動發出告警並執行降級報告 | SLA 告警成功率 ≥ 99% |
| FR5 | AI 行動摘要 | 自動生成可讀性高的 AI 行動方案摘要 | 文字摘要長度 < 500 字、可讀性經人工審核 |
| FR6 | HTML 週報格式 | 四分頁結構：摘要、流量、轉換、建議 | 瀏覽器可正常渲染、格式一致 |
| FR7 | 報表備份與派發記錄 | 週報需備份至內部資料庫/GCS 並寫入派發 log（含通路、狀態、時間戳、重試次數） | 可查詢歷史報表與推播紀錄 |

---

### 六、假設與限制（Assumptions & Constraints）

- GA4 與 Shopline 資料 API 已具備授權存取權限。  
- Cloud Scheduler 時區設定為台北時間。  
- 若 LINE Notify 未設定 token，則自動忽略該通路。  
- 報表儲存於既有 GCS bucket。  
- AI 模組可使用現有營運資料自訓練模型生成摘要。

---

### 七、成功條件（Success Criteria）

| 指標 | 目標值 | 驗證方式 |
|------|--------|----------|
| 推播準時率 | ≥ 99% | Scheduler job log 驗證 |
| 報表生成時間 | < 5 分鐘 | Cloud Run job duration |
| SLA 告警觸發準確率 | ≥ 98% | 比對延遲案例與告警記錄 |
| 多品牌支援 | ≥ 5 品牌並行 | 實際併行測試 |
| 管理層滿意度 | ≥ 90% | 問卷調查（AI 摘要可讀性） |

---

### 八、資料實體（Key Entities）

| 實體 | 描述 | 關聯 |
|------|------|------|
| Brand | 各品牌代碼與設定檔 | report_job.brand_id |
| ReportJob | 每次報表生成任務 | brand_id、start_time、status |
| ReportSummary | 各報表摘要與 AI 行動建議 | report_id、summary_text |
| NotificationLog | 各通路推播紀錄 | channel、status、timestamp |

---

### 九、待澄清事項（[NEEDS CLARIFICATION]）

1. [NEEDS CLARIFICATION: SLA 降級後的報告內容是否應標記「資料不完整」或僅發出告警而不中斷生成？]（需定義關鍵指標呈現方式，避免誤判）  
2. [RESOLVED] AI 行動摘要僅需中文版，暫不提供多語系。  
3. [RESOLVED] 週報需備份於內部資料庫並記錄派發 log（已轉為 FR7，後續在 plan/tasks 中落實）。  
4. [NEEDS CLARIFICATION - HIGH PRIORITY] LINE Notify 推播的授權、訊息格式與頻率限制需先完成插件/API 研究（視為緊急任務）。

---

### 十、驗證與測試（Validation & Testing）

- 測試場景：
  - 正常排程觸發（每週一 11:30）
  - 模擬 GA4 延遲、驗證 SLA 告警
  - 驗證 Email 備援通路是否自動啟用
  - 測試多品牌並行報表生成效能
  - AI 行動摘要生成語意合理性審核  

---

### 十一、風險與緩解策略（Risks & Mitigations）

| 風險 | 潛在影響 | 緩解策略 |
|------|-----------|----------|
| API 資料延遲 | 報表不完整 | SLA 告警 + 降級報告 |
| Cloud Run Job 逾時 | 報表產出中斷 | 任務分割 + timeout 監控 |
| 多通路推播錯誤 | 通知遺漏 | 通路重試機制與失敗告警 |
| LINE Notify 整合不明 | 無法支援主要品牌通路 | 先行進行插件/API 研究，確認授權/頻率限制後再實作；必要時提供替代方案 |
| AI 摘要品質不穩 | 行動建議失準 | 加入人工審核流程（初期階段） |

---

### 十二、商用合理性分析（Business Feasibility）

- **ROI 明確**：報表自動化可節省人力約 6 小時/週，預估年節省成本 > NT$250,000。  
- **跨品牌價值高**：支援多品牌可促進企業集團層級營運監控。  
- **延伸潛力**：AI 行動建議模組可延伸為「營運 KPI 追蹤」產品化功能。  
- **低開發風險**：基於現有 GCP 環境與報表產線，無需新增基礎架構。  

---

## ✅ 規格檢查清單（Specification Quality Checklist）

**路徑**：`specs/1-weekly-report-pipeline-enhancement/checklists/requirements.md`

```markdown
# Specification Quality Checklist: 強化多品牌 Weekly Report 產線

**建立日期**：2025-11-11  
**功能檔案**：[specs/1-weekly-report-pipeline-enhancement/spec.md](specs/1-weekly-report-pipeline-enhancement/spec.md)

## 內容品質
- [x] 無實作細節
- [x] 聚焦使用者價值與商業需求
- [x] 文字可供非技術利害關係人理解
- [x] 所有必要章節均已完成

## 需求完整性
- [ ] [NEEDS CLARIFICATION] 已處理
- [x] 需求可測且具體
- [x] 成功條件具可量測性
- [x] 無技術棧細節
- [x] 已定義接受條件與邊界
- [x] 明確識別假設與依賴

## 功能就緒度
- [x] 所有功能需求具驗收條件
- [x] 使用情境涵蓋主要流程
- [x] 成功條件對應可驗證結果
- [x] 規格未洩露實作細節

## 備註
- 有 3 項待澄清議題，待 `/speckit.clarify` 處理
