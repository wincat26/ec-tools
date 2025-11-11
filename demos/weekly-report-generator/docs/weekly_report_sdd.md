# 📘 Weekly Performance Report Generator & Notifier — SDD

> ⚙️ **目的**：讓產品、營運與工程團隊清楚「要做什麼、怎麼做、如何驗證正確性」。  
> 🧩 **適用範圍**：電商平台內的週報模組、資料整合排程、推播通知流程。

---

## 1️⃣ Context — 背景與使用情境
- **模組名稱**：Weekly Performance Report Generator & Notifier
- **所屬系統**：電商營運自動化平台 @ vibe_tools
- **使用場景**：
  - 自動：每週一（台北時區，Asia/Taipei）11:30 生成上一週（週一至週日）的營運週報並推播通知。
  - 手動：營運可於平台觸發重跑指定週期並重新推播（具冪等性）。
- **上游依賴**：
  - BigQuery 專案 `datalake360-saintpaul` 資料集：`datalake_stpl`、`datalake_looker`、`analytics_304437305`
  - GA4 事件表 `_TABLE_SUFFIX` 周期資料
  - 日報推播服務（共用通知 Webhook/Queue）
- **下游消費者**：
  - `saintpaul_weekly_report_YYYYMMDD.html`（平台內嵌頁面）
  - 推播訊息（Line/Chat Webhook、Email 備援）
  - 行動方案任務板

---

## 2️⃣ Purpose — 為什麼要做這個模組？
每週一中午前產出完整四分頁週報與摘要推播，協助營運快速掌握趨勢、識別異常、啟動後續行動。

---

## 3️⃣ Expected Outcome — 成功結果應該是什麼？
| 角色 | 看見什麼成果？ | 測量指標 |
|------|----------------|----------|
| 營運團隊 | 11:30 前收到推播訊息並可點擊檢視週報 | 準時率 ≥ 99%、推播 CTR ≥ 60% |
| PM / Data Lead | 指標齊全且正確 | 欄位覆蓋率 100%、誤差 < 1% |
| 系統 | 自動化與監控正常 | Return code 0、Log 含 SUCCESS、告警均處理 |

---

## 4️⃣ Functions — 功能說明與邏輯
| 功能編號 | 功能名稱 | 說明 |
|-----------|-----------|------|
| F1 | 週期計算 | 計算上一週區間，支援 `--week` 指定週期。 |
| F2 | 資料讀取 | 從 BigQuery 取得 GMV、訂單、流量、廣告、會員指標。 |
| F3 | 指標計算 | 產出週對週比較、占比、ROAS、會員動能等。 |
| F4 | 模板渲染 | PyEcharts + Jinja2 生成四分頁 HTML。 |
| F5 | 洞察生成 | 規則式引擎生成摘要與建議；支援 LLM 擴充。 |
| F6 | 檔案輸出 | 依 `{brand}_{artifact}_{timestamp}.html`（例：`saintpaul_weekly_report_20251110_120001.html`）命名並備份。 |
| F7 | 推播組裝 | 生成摘要文字與報告連結，新增追蹤參數。 |
| F8 | 通知發送 | 呼叫 Webhook 發送訊息，失敗重試 3 次並告警。 |

---

## 5️⃣ Data Interface — 輸入 / 輸出結構
**Datasets 與用途備註**
- `datalake_stpl`：Shopline 訂單事實表，用於 GMV / 訂單 / 會員指標。
- `analytics_304437305`：GA4 事件資料，用於 Sessions、轉換、流量來源。
- `datalake_looker`：行銷與廣告聚合資料集。核心檢視 `daily_metrics` 以 VIEW 形式整合 Shopline 訂單、GA4 Sessions、Google Ads、Meta Ads 與會員資料，產出 ROAS、花費、轉換率等週報指標。

**Input Example (BigQuery 查詢)**
```sql
WITH week_range AS (
  SELECT DATE('2025-11-03') AS start_date, DATE('2025-11-09') AS end_date
)
SELECT SUM(ord_rev) AS net_revenue, COUNT(DISTINCT ord_id) AS orders
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) BETWEEN (SELECT start_date FROM week_range) AND (SELECT end_date FROM week_range);
```

**Advertising / Growth Metrics Query（`datalake_looker.daily_metrics` 範例）**
```sql
SELECT
  date,
  net_revenue,
  total_sessions,
  google_ads_cost_usd,
  meta_ads_spend,
  roas
FROM `datalake360-saintpaul.datalake_looker.daily_metrics`
WHERE date BETWEEN DATE('2025-10-28') AND DATE('2025-11-03')
ORDER BY date DESC;
```
> `daily_metrics` 為 VIEW，於查詢時會即時 JOIN `datalake_stpl.lv1_order_master`、`cdp_data.lv0_customers`、`analytics_304437305.events_*`、`google_ads.ads_AccountStats_*` 與 `meta_ads.basic`；請留意成本欄位單位（USD 與原幣）並視需求再加總或轉換。

**Output Example (JSON)**
```json
{
  "report_file": "saintpaul_weekly_report_20251110_120001.html",
  "report_url": "https://ec-platform/reports/weekly?week=2025-W45",
  "push_message": {
    "title": "週報摘要｜2025-W45",
    "summary": "達成率 97.5%｜GMV +12%｜ROAS 1.9｜會員活躍 87%",
    "ai_summary": "🚀 營收強勁超標，主力商品轉換率提升明顯！",
    "cta_text": "🎉 表現亮眼，持續複製高 ROAS 活動策略。",
    "cta_url": "https://ec-platform/reports/weekly?week=2025-W45&utm_source=push"
  },
  "status": "success"
}
```

**命名規則備註**：輸出檔案需遵循 `{brand}_{artifact}_{timestamp}.html`，目前品牌為 `saintpaul`，artifact 建議維持 `weekly_report`，timestamp 採 `YYYYMMDD_HHMMSS`。程式端與備份路徑需共用此規則。

---

## 6️⃣ Page / UI 設計細節
- Page 1：總覽 — KPI 卡、流量結構圖、亮點/警訊
- Page 2：廣告 — 成本/ROAS 雙軸圖、Top Campaign 表格
- Page 3：會員經營 — 活躍率、回購率、分層表
- Page 4：行動方案 — 待辦清單、負責人、完成日

---

## 7️⃣ 推播訊息模板（升級版）
```
[週報摘要｜{week_label}]
{ai_summary}

📊 本週：達成率 {achievement_rate}%｜GMV {gmv_delta:+}%｜ROAS {roas:.1f}｜會員活躍 {member_active:.0f}%
{cta_text}

👉 點擊查看完整週報：{report_url}
```

### AI 摘要 (`{ai_summary}`)
AI 模組依據 KPI 趨勢產生一句敘事式摘要：
| 條件 | 範例摘要 |
|------|-----------|
| 達成率 < 90%、ROAS < 2 | ⚠️「廣告效率偏低，未達標主要受投放效益拖累。」 |
| 達成率 90–100%、活躍會員下滑 | 📉「整體表現穩定但會員互動下滑，需強化回購誘因。」 |
| 達成率 ≥ 100%、GMV 成長 > 10% | 🚀「營收強勁超標，主力商品轉換率提升明顯！」 |
| SRI > 1.15 | 🔥「短期成長過快，建議檢視永續性與庫存壓力。」 |

### CTA (`{cta_text}`)
依據表現生成行動導向句：
| 條件 | CTA 建議句 |
|------|-------------|
| 達成率 < 90% | ⚠️ 請立即檢查廣告花費與核心商品成效。 |
| 達成率 90–100% | 📈 接近目標，建議檢視會員活躍與回購動能。 |
| 達成率 ≥ 100% | 🎉 表現亮眼，持續複製高 ROAS 活動策略。 |

### Python 實作參考
```python
summary = ai_generate_summary(metrics)
cta_text = generate_cta(metrics['achievement_rate'], metrics['roas'], metrics['member_active'])
message = f"[週報摘要｜{metrics['week_label']}]\n{summary}\n\n📊 本週：達成率 {metrics['achievement_rate']:.1f}%｜GMV {metrics['gmv_delta']:+.1f}%｜ROAS {metrics['roas']:.1f}｜會員活躍 {metrics['member_active']:.0f}%\n{cta_text}\n\n👉 點擊查看完整週報：{metrics['report_url']}"
```

---

## 8️⃣ Failure Modes — 常見錯誤與防呆策略
| 錯誤情境 | 偵測方式 | 處理策略 |
|-----------|------------|------------|
| BigQuery 無資料 | 查詢結果為空 | 輸出降級版週報並發 Slack 告警 |
| GA4 Schema 變更 | `check_schema.py` | 中斷排程，Email + Slack 通知 |
| 模板渲染錯誤 | Jinja2 Exception | 重試 2 次，失敗則輸出簡報版 Markdown |
| 推播 API 失敗 | HTTP 4xx/5xx | 1/5/15 分鐘重試，仍失敗則記錄 backlog |

---

## 9️⃣ Success Metrics — 成功指標
| 指標 | 目標值 | 說明 |
|------|----------|------|
| 生成成功率 | ≥ 99% | 排程執行並產出 HTML |
| 推播送達率 | ≥ 99% | API 回應 2xx |
| 推播開啟率 | ≥ 60% | 點擊週報連結 |
| 指標準確率 | ≥ 99% | 與 BigQuery 驗證誤差 < 1% |
| 執行時間 | < 4 分鐘 | 查詢與渲染總耗時 |

---

## 🔐 Linked Docs — 關聯文件
- 🔗 上游：[weekly-views.md](./weekly-views.md)
- 🔗 下游：[automation-and-monitoring.md](./automation-and-monitoring.md)
- 🧩 專案概述：[project-overview.md](./project-overview.md)
- 🗂️ 結構對應：[PROJECT_STRUCTURE.md](../../PROJECT_STRUCTURE.md)

---

## 💡 AI Instruction（給 AI 工班的指令）
> 根據上述 Functions 與 Data Interface，使用 **Python (PyEcharts + Jinja2)** 實作週報生成模組。  
> 輸出 HTML 至 `output/`，並回傳報告 URL；具備重試、降級、告警、冪等與 AI 敘事摘要支援。
> 檔案輸出與備份路徑須遵循 `{brand}_{artifact}_{timestamp}` 命名規範，並預留品牌參數化設定。

---

### 🧾 附錄：版本資訊
| 欄位 | 內容 |
|------|------|
| 建立日期 | 2025-11-07 |
| 作者 | ChatPRD（Winson 協作） |
| 對應版本 | v1.2 |
| 最後更新 | 2025-11-07 |