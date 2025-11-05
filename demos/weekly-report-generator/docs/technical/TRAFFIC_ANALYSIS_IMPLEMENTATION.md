# 流量分析實作說明

**更新日期**：2025-01-27  
**狀態**：✅ SQL 查詢邏輯已實作

---

## 🎯 實作目標

整合 GA4 事件表和 Shopline 訂單表，透過 `transaction_id` JOIN `ord_id`，計算各流量來源的：
- **Sessions**：工作階段數
- **Conversions**：轉換數（成交訂單數）
- **CVR**：轉換率（Conversions / Sessions）
- **AOV**：平均訂單金額
- **Revenue**：營收

---

## 📊 資料來源

### 1. GA4 事件表

**路徑**：`datalake360-saintpaul.analytics_304437305.events_*`

**關鍵欄位**：
- `event_name`: 事件名稱（'session_start', 'purchase'）
- `traffic_source`: RECORD 類型，包含 `source` 和 `medium`
- `session_traffic_source_last_click`: RECORD 類型，最後點擊的流量來源
- `event_params`: ARRAY，包含 `transaction_id`（在 purchase 事件中）
- `user_pseudo_id`: 用戶識別碼
- `_TABLE_SUFFIX`: 日期分區（YYYYMMDD）

### 2. Shopline 訂單表

**路徑**：`datalake360-saintpaul.datalake_stpl.lv1_order_master`

**關鍵欄位**：
- `ord_id`: 訂單編號（對應 GA4 的 transaction_id）
- `ord_total`: 訂單付款總額
- `return_ord_id`: 退貨原訂單編號（NULL 表示成交訂單）
- `dt`: 訂單日期（TIMESTAMP）
- `touch_class`: 通路種類（'ec' 為電商）

---

## 🔗 JOIN 邏輯

### Transaction ID 對應

```
GA4 purchase 事件的 transaction_id = Shopline 訂單的 ord_id
```

**注意事項**：
- 確保 `transaction_id` 和 `ord_id` 格式一致
- 如果格式不同，可能需要清理或轉換

---

## 📝 SQL 查詢結構

### 步驟 1：計算 Sessions（從 GA4）

```sql
WITH ga4_sessions AS (
    SELECT
        -- 流量分類
        CASE ... END as traffic_category,
        -- 計算 Sessions（使用 user_pseudo_id + session_id）
        COUNT(DISTINCT CONCAT(user_pseudo_id, '-', session_id)) as sessions
    FROM `analytics_304437305.events_*`
    WHERE event_name = 'session_start'
    GROUP BY traffic_category
)
```

### 步驟 2：取得 Purchase 事件的 Transaction ID（從 GA4）

```sql
ga4_purchases AS (
    SELECT DISTINCT
        -- 從 event_params 取得 transaction_id
        (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id,
        -- 流量分類（使用 last touch）
        CASE ... END as traffic_category
    FROM `analytics_304437305.events_*`
    WHERE event_name = 'purchase'
        AND transaction_id IS NOT NULL
)
```

### 步驟 3：計算訂單指標（從 Shopline）

```sql
order_metrics AS (
    SELECT
        ord_id,
        SUM(CASE WHEN return_ord_id IS NULL THEN ord_total ELSE 0 END) as revenue,
        AVG(CASE WHEN return_ord_id IS NULL THEN ord_total END) as aov,
        COUNT(DISTINCT CASE WHEN return_ord_id IS NULL THEN ord_id END) as conversions
    FROM `datalake_stpl.lv1_order_master`
    WHERE touch_class = 'ec'
    GROUP BY ord_id
)
```

### 步驟 4：JOIN 計算最終指標

```sql
SELECT
    traffic_category as traffic_source,
    sessions,
    conversions,
    (conversions / sessions * 100) as cvr,
    aov,
    revenue
FROM ga4_sessions
FULL OUTER JOIN (
    SELECT 
        traffic_category,
        COUNT(DISTINCT transaction_id) as conversions,
        SUM(revenue) as revenue,
        AVG(aov) as aov
    FROM ga4_purchases
    INNER JOIN order_metrics ON transaction_id = ord_id
    GROUP BY traffic_category
) ON traffic_category
```

---

## 🔧 流量分類規則

使用 `src/traffic_classifier.py` 中的 `classify_traffic_source_sql()` 函式生成 SQL CASE WHEN 語句。

**分類對應**：
- `1. 直接流量` → 直接流量
- `2. 自然搜尋` → 自然搜尋
- `3. 付費廣告` → 付費廣告
- `4. 會員經營` → 會員經營（Email）
- `5. AI 助理` → AI 來源
- `6. 社群媒體` → 社群經營
- `7. 參照連結` → 參照連結
- `8. 其他` → 其他

---

## ⚠️ 注意事項

### 1. GA4 資料結構

- `traffic_source` 是 RECORD 類型，需要使用 `UNNEST([traffic_source])` 展開
- `session_traffic_source_last_click` 用於取得最後點擊的流量來源（更準確）
- `event_params` 是 ARRAY，需要使用 `UNNEST` 和 `WHERE key = 'transaction_id'` 查詢

### 2. Session ID 計算

- 使用 `user_pseudo_id + session_id` 組合計算唯一 Sessions
- `session_id` 在 `event_params` 中，key 為 `ga_session_id`

### 3. Transaction ID 格式

- 確認 GA4 的 `transaction_id` 格式與 Shopline 的 `ord_id` 格式一致
- 如果不一致，需要轉換或清理

### 4. 日期分區查詢

- GA4 事件表使用日期分區（`events_YYYYMMDD`）
- 需要使用 `_TABLE_SUFFIX IN ('20250120', '20250121', ...)` 過濾日期範圍

---

## 🧪 測試建議

### 1. 驗證 Transaction ID 對應

```sql
-- 檢查 GA4 transaction_id 和 Shopline ord_id 的格式
SELECT 
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as ga4_transaction_id,
    ord_id
FROM `analytics_304437305.events_*`,
`datalake_stpl.lv1_order_master`
WHERE event_name = 'purchase'
LIMIT 10
```

### 2. 驗證流量分類

```sql
-- 檢查流量分類結果
SELECT 
    source,
    medium,
    CASE ... END as traffic_category
FROM `analytics_304437305.events_*`,
UNNEST([traffic_source]) as ts
WHERE event_name = 'session_start'
LIMIT 100
```

### 3. 驗證 Sessions 計算

```sql
-- 檢查 Sessions 計算是否正確
SELECT 
    COUNT(DISTINCT CONCAT(user_pseudo_id, '-', session_id)) as sessions
FROM `analytics_304437305.events_*`
WHERE event_name = 'session_start'
```

---

## 📚 參考資料

- `src/traffic_classifier.py` - 流量分類器
- `src/data_fetcher.py` - 資料查詢模組（`fetch_traffic_analysis()` 方法）
- `TRAFFIC_CLASSIFICATION.md` - 流量分類規則說明

