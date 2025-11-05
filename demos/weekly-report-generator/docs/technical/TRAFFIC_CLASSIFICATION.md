# 流量來源分類邏輯

**更新日期**：2025-01-27  
**來源**：Looker Studio 正規表達式規則轉換為 SQL

---

## 📊 分類規則

根據 GA4 的 `source` 和 `medium` 欄位，將流量來源分類為 8 種類別：

| 分類 | 規則 | SQL 條件 |
|------|------|---------|
| **1. 直接流量** | `source = '(direct)'` AND `medium = '(none)'` 或 `'(not set)'` | `source = '(direct)' AND (medium = '(none)' OR medium = '(not set)')` |
| **2. 自然搜尋** | `source/medium` 包含 `/ organic` 或包含 `search` | `REGEXP_CONTAINS(LOWER(source_medium), r'/ organic$|.*search.*')` |
| **3. 付費廣告** | `medium` 為 `ads|cpc|paid|ppc|cpm|pmax|ad|fb-SiteLink` | `REGEXP_CONTAINS(source_medium, r'/ (ads\|cpc\|paid\|ppc\|cpm\|pmax\|ad\|fb-SiteLink)$')` |
| **4. 會員經營** | `source/medium` 包含 `edm|line|push|sms|cdp|crm` | `REGEXP_CONTAINS(source_medium, r'(edm\|line\|push\|sms\|cdp\|crm)')` |
| **5. AI 助理** | `source` 開頭為 `chatgpt|perplexity|copilot|bard|gemini` | `REGEXP_CONTAINS(LOWER(source_medium), r'^(chatgpt\|perplexity\|copilot\|bard\|gemini)')` |
| **6. 社群媒體** | `source/medium` 包含 `facebook|threads|instagram|t.co|line|linktr.ee|pinterest|linkedin` | `REGEXP_CONTAINS(source_medium, r'(facebook\|threads\|instagram\|t\\.co\|line\|linktr\\.ee\|pinterest\|linkedin)')` |
| **7. 參照連結** | `medium = 'referral'` | `REGEXP_CONTAINS(source_medium, r'/ referral$')` |
| **8. 其他** | 不符合以上規則 | `ELSE '8. 其他'` |

---

## 🔧 實作方式

### SQL 查詢（BigQuery）

```sql
CASE
    WHEN source = '(direct)' AND (medium = '(none)' OR medium = '(not set)') THEN '1. 直接流量'
    WHEN REGEXP_CONTAINS(LOWER(CONCAT(source, ' / ', medium)), r'/ organic$|.*search.*') THEN '2. 自然搜尋'
    WHEN REGEXP_CONTAINS(CONCAT(source, ' / ', medium), r'/ (ads|cpc|paid|ppc|cpm|pmax|ad|fb-SiteLink)$') THEN '3. 付費廣告'
    WHEN REGEXP_CONTAINS(CONCAT(source, ' / ', medium), r'(edm|line|push|sms|cdp|crm)') THEN '4. 會員經營'
    WHEN REGEXP_CONTAINS(LOWER(CONCAT(source, ' / ', medium)), r'^(chatgpt|perplexity|copilot|bard|gemini)') THEN '5. AI 助理'
    WHEN REGEXP_CONTAINS(CONCAT(source, ' / ', medium), r'(facebook|threads|instagram|t\.co|line|linktr\.ee|pinterest|linkedin)') THEN '6. 社群媒體'
    WHEN REGEXP_CONTAINS(CONCAT(source, ' / ', medium), r'/ referral$') THEN '7. 參照連結'
    ELSE '8. 其他'
END
```

### Python 函式

```python
from src.traffic_classifier import classify_traffic_source

# 使用範例
category = classify_traffic_source('google', 'organic')  # 返回 '2. 自然搜尋'
category = classify_traffic_source('(direct)', '(none)')  # 返回 '1. 直接流量'
```

---

## 🔗 資料整合流程

### 1. GA4 事件表查詢

從 `analytics_304437305.events_*` 查詢：
- **Sessions**：從 `session_start` 事件計算
- **流量來源**：使用 `traffic_source` 或 `session_traffic_source_last_click`
- **Transaction ID**：從 `purchase` 事件的 `event_params` 中取得

### 2. Shopline 訂單表查詢

從 `datalake_stpl.lv1_order_master` 查詢：
- **訂單金額**：`ord_total`
- **訂單編號**：`ord_id`
- **成交判斷**：`return_ord_id IS NULL`

### 3. JOIN 邏輯

```sql
-- GA4 purchase 事件的 transaction_id = Shopline 訂單的 ord_id
SELECT 
    ga4.traffic_category,
    ga4.transaction_id,
    order.ord_id,
    order.ord_total
FROM ga4_purchases ga4
INNER JOIN order_metrics order ON ga4.transaction_id = order.ord_id
```

---

## 📊 查詢範例

### 完整流量分析查詢

```sql
WITH ga4_sessions AS (
    -- 計算各流量來源的 Sessions
    SELECT
        CASE ... END as traffic_category,
        COUNT(DISTINCT session_id) as sessions
    FROM `datalake360-saintpaul.analytics_304437305.events_*`
    WHERE event_name = 'session_start'
    GROUP BY traffic_category
),
ga4_purchases AS (
    -- 取得 purchase 事件的 transaction_id 和流量來源
    SELECT
        (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id,
        CASE ... END as traffic_category
    FROM `datalake360-saintpaul.analytics_304437305.events_*`
    WHERE event_name = 'purchase'
),
order_metrics AS (
    -- 計算訂單指標
    SELECT
        ord_id,
        ord_total as revenue
    FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
    WHERE return_ord_id IS NULL
)
-- JOIN 計算最終指標
SELECT
    traffic_category,
    sessions,
    conversions,
    (conversions / sessions * 100) as cvr,
    revenue
FROM ...
```

---

## ⚠️ 注意事項

1. **Transaction ID 對應**：
   - GA4 的 `transaction_id` 需要與 Shopline 的 `ord_id` 完全匹配
   - 如果格式不同，可能需要轉換或清理

2. **流量來源時機**：
   - 使用 `session_traffic_source_last_click` 取得最後點擊的流量來源
   - 或使用 `traffic_source` 取得工作階段開始的流量來源

3. **日期分區**：
   - GA4 事件表使用日期分區（`events_YYYYMMDD`）
   - 需要使用 `_TABLE_SUFFIX` 過濾日期範圍

---

## 📚 參考資料

- `src/traffic_classifier.py` - Python 流量分類器
- `src/data_fetcher.py` - 資料查詢模組（包含流量分析查詢）

