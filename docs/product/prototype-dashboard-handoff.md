# Prototype Dashboard Handoff

> 版本：2025-11-02｜負責人：AI 夥伴 ｜交接對象：下一任前端/產品夥伴

---

## 1. 專案現況快覽

- **Prototype 架構**：純 HTML/CSS/Vanilla JS，入口 `prototype/index.html`，主要頁面 `prototype/dashboard.html`、`prototype/data.html` 等。
- **資料來源**：全數使用 `prototype/js/mockData.js` 的靜態資料物件，已預留 GA4、CRM、廣告、任務等欄位。
- **最新重點**：
  - Dashboard 首屏精簡為「本週營運概況 + AI 洞察資訊流」。
  - Data 頁完成三大模組：GMV 拆解、流量分析、平均訂單金額分析、轉換率漏斗分析。
  - Onboarding、專家訂閱、AI 任務串接已具 Prototype 示意。

---

## 2. 已完成模組（重點檔案）

| 模組 | 核心檔案 | 功能重點 |
|------|----------|-----------|
| Dashboard 首屏卡片 | `prototype/dashboard.html`<br>`prototype/css/dashboard-cards.css`<br>`prototype/js/dashboard.js` | 三張主卡（數據分析 / 洞察中心 / 行動方案），AI 即時資訊流 + 精選行動。 |
| 本週營運概況 | `prototype/data.html` (上半部)<br>`prototype/js/dashboard.js` | 成交營收+總營業額雙卡，取消率進度條、GMV 指標公式。 |
| 流量分析 | `prototype/data.html`<br>`prototype/js/dashboard.js` | 八大來源切換、Sessions/AOV/CVR 指標卡、AI 洞察整合。 |
| 平均訂單金額分析 | `prototype/data.html`<br>`prototype/js/mockData.js` (aovAnalysis) | 整體/新客/回購客切換，購物車件數 & 價格帶雙圖、AI 洞察合併。 |
| 轉換率漏斗分析 | `prototype/data.html`<br>`prototype/js/mockData.js` (conversionFunnel) | 範圍切換垂直漏斗 + 商品/活動迷你漏斗，瓶頸解讀集中在 AI 區。 |
| Onboarding & Gamification | `prototype/js/onboarding.js`<br>`prototype/css/onboarding.css`<br>`doc/product_prd/onboarding-gamification-design.md` | Step-by-step 引導、進度徽章、重新啟動機制、滾動對應。 |
| 專家訂閱 Prototype | `prototype/expert-subscribe.html`<br>`prototype/js/expert-subscribe.js` | 流量來源→專家支援→導到訂閱頁邏輯已串接。 |

---

## 3. mockData 關鍵結構

```markdown
mockData.summary            // Dashboard & Data 快照用
mockData.trafficSources     // 流量分析、會員拆解
mockData.aovAnalysis        // 平均訂單金額（overall/new/returning）
mockData.conversionFunnel   // 新增：ranges、overall、productSegments、campaignSegments
mockData.guidelines         // AI 洞察資料源（多模組共用）
mockData.tasks              // 行動方案/任務串接
mockData.expertSupport      // 專家訂閱頁面資料
```

- 串 GA4 時只需以相同 key 產出 JSON，即可替換 Prototype 內部渲染。
- `conversionFunnel` 已用 GA4 標準事件命名（all_visitors/view_item/add_to_cart/begin_checkout/purchase）。

---

## 4. 待辦與建議（下一階段）

1. **Data 頁深化**
   - [ ] 將迷你漏斗導入圖表套件（ECharts/Chart.js），支援 hover tooltip。
   - [ ] 商品/活動篩選與更多維度（品牌、行銷渠道）。
   - [ ] Insights 與 Data 的資料來源統一後，規劃洞察頁資訊架構（目前待整併）。

2. **真實資料串接規劃**
   - [ ] 建立 mockData → API 的 mapping 文件，明確欄位對應 GA4、CRM、廣告平台。
   - [ ] 釐清資料刷新機制（預設 7/30/90 天 + 自訂），加上時間範圍控制元件。

3. **UI/UX 待優化**
   - [ ] 迷你漏斗 hover tooltip + CTA（導洞察/任務）。
   - [ ] Data 頁卡片在 Tablet/Mobile 的排版微調（需實機檢查）。
   - [ ] AI 洞察集中呈現：`insights.html` 與 Dashboard 的異常診斷去重。

4. **行動方案整合**
   - [ ] AI 精選行動與 `actions.html` 的任務列表需共用資料來源。
   - [ ] 行動採納流程（加入任務 → 任務詳情）尚未接上，需定義 wireflow。

---

## 5. 環境與操作建議

- Prototype 無需編譯，直接開啟 `prototype/index.html` 或 `prototype/dashboard.html`。
- 若需測試 GA4/後端串接，可使用 `live-server` 或任何簡易 HTTP server 以避免 CORS 問題。
- 更新樣式時注意
  - 共用變數集中於 `prototype/css/main.css`
  - 頁面專屬 CSS (`dashboard.css`, `dashboard-cards.css`, `data.css`)，避免交叉覆寫。
- 所有互動邏輯集中在 `prototype/js/*.js`：
  - `dashboard.js`：Dashboard + Data 頁共用函式。
  - `utils.js`：格式化、toast 等工具。
  - `navigation.js`：頂部導覽列狀態。

---

## 6. 文件與協作資源

- README（專案總覽）：`README.md`
- Prototype 說明：`prototype/README.md`
- Sitemap 與需求：`doc/product_prd/prototype-sitemap.md`
- Onboarding/Gamification：`doc/product_prd/onboarding-gamification-design.md`
- 任務追蹤：`TASKS.md`（已更新最新完成項目）

---

## 7. 移交備註

- 若需要 demo，建議路徑：登入 → Dashboard → Data（流量/AOV/漏斗） → Expert → Actions。
- 任何新功能請同步更新 `TASKS.md` 及此交接文件，以維持全員共識。
- 若轉為 Next.js/React 實作，可將各區塊拆成獨立 component，並沿用 mockData 轉為 `fixtures`。


