# 跨文件一致性與品質分析執行規範（/speckit.analyze）

**目的**：  
在功能進入實作階段前，對 `spec.md`（產品規格）、`plan.md`（技術規劃）、`tasks.md`（任務拆解）三份核心文件進行**只讀式的一致性與品質檢查**，  
找出潛在矛盾、重複、模糊、缺漏與未覆蓋項目，以確保規格落實與開發可執行性。

---

## 一、執行目標（Goal）

- 驗證三份文件（`spec.md`、`plan.md`、`tasks.md`）之間的一致性與完整性  
- 發現：
  - **矛盾（Inconsistency）**
  - **重複或歧義（Duplication / Ambiguity）**
  - **未規範或未覆蓋（Underspecification / Coverage Gap）**
- 確保符合憲章（`.specify/memory/constitution.md`）所定義之原則（MUST / SHOULD）
- 結果以 Markdown 格式輸出報告，不直接修改任何檔案

---

## 二、執行約束（Operating Constraints）

- **唯讀模式（STRICTLY READ-ONLY）**：禁止對任何檔案進行修改。  
- 僅可輸出分析報告，修正建議須由使用者手動批准後執行。  
- 若分析結果顯示違反憲章條文（Constitution MUST 原則），該問題視為 **CRITICAL**，必須修正。  
- 憲章條文不得於本流程中變更，若需修訂，須啟動獨立的憲章更新流程。

---

## 三、分析流程（Execution Steps）

### 第 1 步：初始化分析環境（Initialize Context）

執行：

```bash
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks

自動解析以下路徑（皆為絕對路徑）：

SPEC = FEATURE_DIR/spec.md
PLAN = FEATURE_DIR/plan.md
TASKS = FEATURE_DIR/tasks.md

若任一檔案缺失，立即中止，並提示使用者執行對應的 /speckit 指令補齊前置文件。

第 2 步：載入文件摘要（Progressive Disclosure）

僅擷取分析所需的最小上下文：

從 spec.md：

需求與目標（Functional / Non-Functional Requirements）
使用者故事（User Stories）
邊界條件（Edge Cases）

從 plan.md：

系統架構與技術堆疊（Architecture / Stack）
資料模型（Data Model）
各階段目標（Phases）
技術限制（Constraints）

從 tasks.md：

任務編號（Task IDs）
描述與階段（Descriptions / Phases）
平行任務標記 [P]
具體檔案路徑（File Paths）

從 constitution.md：

原則條文（Principles）
MUST / SHOULD 規範

第 3 步：建立語意模型（Semantic Models）

建立以下內部對應表（不輸出原始文件）：

需求清單（Requirements Inventory）：
每條功能與非功能需求皆轉為可追蹤 key，例如：
「系統可自動生成多品牌報表」→ auto-generate-multibrand-reports

使用者行為清單（User Story Inventory）：
各故事包含行為、角色、驗收準則。

任務覆蓋映射（Task Coverage Mapping）：
依關鍵字、ID 或明示對應關係比對每個任務對應的需求／故事。

憲章規範集（Constitution Rule Set）：
提取所有 MUST / SHOULD 條文以比對符合性。

第 4 步：偵測階段（Detection Passes）
A. 重複檢測（Duplication）

比對語意相近的需求句子（e.g.「自動生成報表」與「自動產出週報」）
標示建議合併的低品質版本

B. 模糊性檢測（Ambiguity）

掃描模糊形容詞（例：「快速」、「穩定」、「安全」、「直覺」）
若無明確量化標準 → 標記為需澄清

偵測暫存符號（TODO、TKTK、???、<placeholder>）

C. 未明確規範（Underspecification）

有動詞但無明確目標或測量標準的需求
使用者故事未明列驗收條件
任務提及未知檔案或模組（spec / plan 中未定義）

D. 憲章一致性（Constitution Alignment）

任務或需求違反 MUST 原則（例如缺少安全驗證步驟）
憲章要求之章節若缺失 → 直接列為 CRITICAL

E. 覆蓋缺口（Coverage Gaps）

需求無對應任務（零覆蓋）
任務未對應任何需求或故事（孤立任務）
非功能性需求（效能、安全、可靠性）未在 tasks 中體現

F. 不一致性（Inconsistency）

名詞漂移（如「報表執行紀錄」與「報表 log」）
plan 中提及之資料實體未於 spec 定義
任務執行順序與依賴邏輯矛盾（例如 API 任務早於模型建立）
技術堆疊衝突（如 spec 用 Python、plan 用 Node.js）

第 5 步：嚴重度分級（Severity Assignment）
等級	定義
CRITICAL	違反憲章 MUST 條文、關鍵需求零覆蓋、功能性阻斷
HIGH	需求重複／衝突、關鍵模糊性或無法測試
MEDIUM	名詞不一致、邊界條件未明確、非功能需求缺漏
LOW	文字風格或細部冗餘，不影響開發順序

第 6 步：輸出報告（Analysis Report）

報告以 Markdown 表格形式輸出（不寫入檔案）。

🔹 問題摘要表（Findings Table）
ID	類別	嚴重度	位置	摘要	建議
A1	Duplication	HIGH	spec.md:L132-144	「自動生成週報」與「報表自動產出」重複	合併並採用較清晰版本
C1	Coverage	CRITICAL	plan.md → tasks.md	SLA 告警未有任務對應	新增 T056 任務覆蓋此功能

🔹 覆蓋率摘要表（Coverage Summary）
需求 Key	是否覆蓋	任務 ID	備註
auto-generate-multibrand-reports	✅	T018–T024	完整覆蓋
line-notify-integration	⚠️	T028–T030	僅 PoC，需實作 API 授權
sla-alert-mechanism	❌	—	缺少任務實作告警流程

🔹 憲章一致性檢查（Constitution Alignment Issues）

CRITICAL-01：非功能需求「SLA 告警」未覆蓋 → 違反「系統可靠性監控為 MUST」條文
CRITICAL-02：plan.md 無安全性驗證段落 → 違反「所有自動化流程需具備授權驗證」原則

🔹 未對應任務（Unmapped Tasks）
任務 ID	描述	建議動作
T050	更新 research.md	與 spec 無對應需求，可併入文件同步故事

🔹 統計摘要（Metrics）
指標	數值
總需求數	27
任務總數	55
覆蓋率	85.2%
模糊項數	6
重複項數	3
重大問題數	2 (CRITICAL)

第 7 步：後續行動建議（Next Actions）

若存在 CRITICAL 問題：
❗ 應立即修正後再執行 /speckit.implement
建議動作：
於 plan.md 補上 SLA 告警與安全機制描述
於 tasks.md 新增對應任務（例：T056 Implement SLA monitoring handler）
若僅有 LOW / MEDIUM 問題：
可持續進入開發階段，但建議：
修正文案與名詞一致性
補足非功能需求任務（效能、安全、日誌）
指令建議：
/speckit.specify 重新細化需求說明
/speckit.plan 補齊架構細節
手動更新 tasks.md 對應未覆蓋功能


第 8 步：修正建議（Remediation Offer）

執行完分析後，系統應詢問使用者：
「是否需要我列出前 N 項關鍵問題的具體修正建議（不自動修改檔案）？」
使用者回覆「是」→ 產出修正建議（diff 格式）
使用者回覆「否」→ 僅保留報告，不執行進一步操作

四、分析原則（Operating Principles）
資訊效率（Context Efficiency）

僅處理高訊號片段（不展開全文）
限制輸出最多 50 條具體發現，其餘匯總為「Overflow Summary」
決定性（Determinism）
相同輸入再次執行應產生相同 ID 與結果
嚴謹性（Integrity）
不生成、假設或自動補任何缺失章節
僅報告事實性缺漏
憲章優先（Constitution Authority）
憲章 MUST 條文具有最高優先權
若有衝突，須修正 spec/plan/tasks，而非調整憲章
成功案例輸出
若分析無任何問題，報告應顯示：

✅ 所有文件一致且覆蓋完整
✅ 無模糊、重複或未覆蓋項目
✅ 可直接進入 /speckit.implement 階段

五、與專案治理流程對應（Enterprise Alignment）
專案階段	檢查重點	對應指令
規格階段	需求清晰度、憲章符合性	/speckit.specify
規劃階段	技術結構合理性、資料流定義	/speckit.plan
任務階段	開發可執行性、依賴順序	/speckit.tasks
分析階段	跨文件一致性、完整覆蓋	/speckit.analyze
實作階段	驗收測試、自動化驗證	/speckit.implement

六、範例輸出片段（Example Output）
## Specification Analysis Report

| ID | 類別 | 嚴重度 | 位置 | 摘要 | 建議 |
|----|------|---------|------|------|------|
| C1 | Coverage | CRITICAL | plan.md:L210 | SLA 告警機制未對應任務 | 新增任務 T056 並同步更新 plan.md |
| F2 | Inconsistency | HIGH | spec.md vs plan.md | 「LINE Notify」與「LINE Messenger Plugin」名稱不一致 | 統一命名為 LINE Plugin |


