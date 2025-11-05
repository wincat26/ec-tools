# 電商週報生成工具 - 資料需求對齊文件

**建立日期**：2025-01-27  
**目的**：確認 Python 腳本需要從 BigQuery 查詢哪些資料，以生成週報

---

## 📊 根據 data.html 的資料需求清單

### 1️⃣ GMV 基本指標（成交營收、總營業額、取消率）

**需要的資料**：
- 成交營收（成交金額）：已完成訂單的實收金額
- 總營業額：未扣除取消/退單金額
- 取消率：取消訂單數 / 總訂單數
- 成交訂單數
- 總訂單數

**BigQuery 對應表**：
- `saintpaul_data.orders_summary_daily`（日報表，已彙總）
- `saintpaul_data.orders`（訂單明細表）

**查詢邏輯**：
```sql
-- 需要查詢最近 7 天的資料
-- 計算：成交營收、總營業額、取消率、訂單數
```

---

### 2️⃣ 本週關鍵摘要（各種變化指標）

**需要的資料**：
- 營收變化（與上週比較）
- 流量變化（與上週比較）
- 轉換率變化（與上週比較）
- 客單價變化（與上週比較）
- 訂單筆數
- 取消退貨金額
- 行銷花費（需要確認資料來源）
- ROAS（需要行銷花費資料）

**BigQuery 對應表**：
- `saintpaul_data.orders_summary_daily`（日報表）
- 流量資料：需要從 GA4 查詢（可能需要其他表）

**查詢邏輯**：
```sql
-- 需要比較本週 vs 上週的資料
-- 計算各指標的變化百分比
```

---

### 3️⃣ 流量分析（各來源的 Sessions、CVR、AOV）

**需要的資料**：
- 各流量來源的 Sessions（工作階段數）
- 各流量來源的轉換率（CVR）
- 各流量來源的平均訂單金額（AOV）
- 各流量來源的營收

**流量來源分類**：
- 直接流量
- 付費廣告
- 會員經營（Email）
- AI 來源
- 自然搜尋
- 社群經營
- 參照連結
- 其他

**BigQuery 對應表**：
- `saintpaul_data.order_ga4_integration`（訂單與 GA4 整合表）
  - 包含 `last_touch_source`、`last_touch_medium`、`last_touch_channel`
- 可能需要 GA4 事件表查詢 Sessions

**查詢邏輯**：
```sql
-- 根據 last_touch_channel 或 last_touch_source_medium 分類
-- 計算各來源的 Sessions、CVR、AOV、營收
```

---

### 4️⃣ 平均訂單金額分析（AOV Analysis）

**需要的資料**：
- 購物車件數分布（1件、2件、3件、4件以上）
- 價格帶結構（高/中/低單價）
- 區分：整體 / 新客 / 回購客

**BigQuery 對應表**：
- `saintpaul_data.orders`（訂單明細）
- `saintpaul_data.order_ga4_integration`（判斷新客/回購客）

**查詢邏輯**：
```sql
-- 根據 order.product_count 計算件數分布
-- 根據 order.subtotal 計算價格帶
-- 根據 is_first_purchase 區分新客/回購客
```

---

### 5️⃣ 轉換率漏斗分析（Conversion Funnel）

**需要的資料**：
- 全站漏斗：訪客 → 商品瀏覽 → 加入購物車 → 開始結帳 → 完成購買
- 商品分區漏斗：Top 商品的轉換率
- 活動分區漏斗：活動表現的轉換率

**BigQuery 對應表**：
- GA4 事件表（需要查詢 GA4 相關表）
- `saintpaul_data.product_insights_daily`（商品洞察）
- `saintpaul_data.order_ga4_integration`（部分漏斗資料）

**查詢邏輯**：
```sql
-- 需要查詢 GA4 事件：
-- - view_item（商品瀏覽）
-- - add_to_cart（加入購物車）
-- - begin_checkout（開始結帳）
-- - purchase（完成購買）
```

**⚠️ 注意**：GA4 事件資料可能需要從其他資料集查詢

---

### 6️⃣ AI 洞察分析（Guideline / Recommendations）

**需要的資料**：
- 根據 KPI 異常自動生成建議
- 需要結合上述所有資料進行分析

**生成邏輯**：
- 使用 OpenAI API 根據資料生成洞察
- 參考 PRD 中的 Guideline AI 邏輯

---

## 🤔 需要確認的問題

### 問題 1：GA4 事件資料位置
- **問題**：流量 Sessions 和轉換漏斗需要 GA4 事件資料
- **確認**：GA4 事件資料在哪個資料集？是否在 `analytics_304437305` 中？

### 問題 2：行銷花費資料
- **問題**：本週關鍵摘要中的「行銷花費」和「ROAS」需要廣告花費資料
- **確認**：廣告花費資料在哪個表？是否有 `ad_data` 相關表？

### 問題 3：流量來源分類對應
- **問題**：如何將 BigQuery 的 `last_touch_channel` 對應到 data.html 的 8 種分類？
- **確認**：需要建立對應規則，例如：
  - `last_touch_channel = 'Organic Search'` → 自然搜尋
  - `last_touch_channel = 'Paid Search'` → 付費廣告
  - 等等...

### 問題 4：時間範圍
- **問題**：週報預設是「最近 7 天」，是否需要支援其他時間範圍？
- **確認**：是否只需要 7 天，還是也需要支援「昨天」、「最近 30 天」等？

### 問題 5：資料更新頻率
- **問題**：BigQuery 資料多久更新一次？
- **確認**：是否每日更新？更新時間是什麼時候？

---

## 📝 Python 腳本需要實作的功能

### 資料查詢模組（`data_fetcher.py`）

1. **查詢 GMV 基本指標**
   - 查詢 `orders_summary_daily` 或 `orders` 表
   - 計算成交營收、總營業額、取消率

2. **查詢本週關鍵摘要**
   - 查詢本週和上週的資料
   - 計算各指標變化

3. **查詢流量分析**
   - 查詢 `order_ga4_integration` 表
   - 根據流量來源分類統計

4. **查詢 AOV 分析**
   - 查詢 `orders` 表
   - 計算件數分布和價格帶

5. **查詢轉換漏斗**
   - 查詢 GA4 事件表（需要確認位置）
   - 計算各階段轉換率

---

## ✅ 下一步行動

1. **確認上述 5 個問題的答案**
2. **確認資料查詢邏輯是否正確**
3. **開始實作 Python 腳本**

---

**請您確認以上內容，特別是「需要確認的問題」部分，我們再開始實作！**

