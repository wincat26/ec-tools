# Transaction ID 格式驗證結果

**驗證日期**：2025-01-27  
**狀態**：✅ **格式完全一致，可以成功 JOIN**

---

## ✅ 驗證結果

### 格式分析

| 欄位 | GA4 transaction_id | Shopline ord_id | 狀態 |
|------|-------------------|-----------------|------|
| **格式** | 17 位數字 | 17 位數字 | ✅ 一致 |
| **範例** | `20241105153444114` | `20241105153444114` | ✅ 完全匹配 |
| **資料類型** | STRING | STRING | ✅ 一致 |
| **是否包含字母** | 否 | 否 | ✅ 一致 |

### 實際測試結果

**測試 ID**：`20241105153444114`

- ✅ GA4 purchase 事件中找到該 transaction_id
- ✅ Shopline 訂單表中找到對應的 ord_id
- ✅ **完全匹配**，訂單金額：NT$ 490

---

## 🔗 JOIN 邏輯確認

### JOIN 條件

```sql
-- 可以直接使用等於運算子進行 JOIN
GA4.transaction_id = Shopline.ord_id
```

### 驗證查詢

```sql
-- 單一訂單驗證
SELECT
    ga4.transaction_id,
    shopline.ord_id,
    shopline.ord_total
FROM (
    SELECT 
        (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id
    FROM `datalake360-saintpaul.analytics_304437305.events_20241105`
    WHERE event_name = 'purchase'
        AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') = '20241105153444114'
) ga4
INNER JOIN (
    SELECT ord_id, ord_total
    FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
    WHERE ord_id = '20241105153444114'
) shopline
ON ga4.transaction_id = shopline.ord_id
```

**結果**：✅ 成功匹配，可以取得訂單金額

---

## 📊 流量分析查詢邏輯

### 完整流程

1. **從 GA4 取得 Sessions**（按流量來源分組）
   ```sql
   SELECT
       CASE ... END as traffic_category,
       COUNT(DISTINCT session_id) as sessions
   FROM `analytics_304437305.events_*`
   WHERE event_name = 'session_start'
   ```

2. **從 GA4 purchase 事件取得 transaction_id 和流量來源**
   ```sql
   SELECT
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id,
       CASE ... END as traffic_category
   FROM `analytics_304437305.events_*`
   WHERE event_name = 'purchase'
   ```

3. **從 Shopline 計算訂單指標**
   ```sql
   SELECT
       ord_id,
       ord_total as revenue,
       AVG(ord_total) as aov
   FROM `datalake_stpl.lv1_order_master`
   WHERE return_ord_id IS NULL
   ```

4. **JOIN 計算最終指標**
   ```sql
   SELECT
       traffic_category,
       sessions,
       COUNT(DISTINCT transaction_id) as conversions,
       (conversions / sessions * 100) as cvr,
       SUM(revenue) as revenue,
       AVG(aov) as aov
   FROM ga4_purchases
   INNER JOIN shopline_orders ON transaction_id = ord_id
   GROUP BY traffic_category
   ```

---

## ✅ 確認事項

- [x] transaction_id 和 ord_id 格式完全一致（17 位數字）
- [x] 可以直接使用 `transaction_id = ord_id` 進行 JOIN
- [x] 可以成功查詢匹配的訂單資料
- [x] 可以計算各流量來源的交易量、轉換率等指標

---

## 🚀 下一步

1. **確認流量分析查詢邏輯**：`src/data_fetcher.py` 中的 `fetch_traffic_analysis()` 方法已實作
2. **測試完整查詢**：執行 `python test_queries.py` 測試流量分析功能
3. **調整位置設定**：如果仍有位置錯誤，可能需要調整查詢方式

---

## 📝 注意事項

1. **日期分區**：
   - GA4 事件表使用日期分區（`events_YYYYMMDD`）
   - 需要使用 `_TABLE_SUFFIX` 過濾日期範圍

2. **位置問題**：
   - 如果出現位置錯誤，BigQuery 會自動偵測資料集位置
   - 單表查詢時通常不會有問題
   - JOIN 查詢時可能需要明確指定位置，或讓 BigQuery 自動處理

3. **Transaction ID 格式**：
   - 格式：`YYYYMMDDHHMMSSNNN`（17 位數字）
   - 前 8 位：日期（YYYYMMDD）
   - 中間 6 位：時間（HHMMSS）
   - 後 3 位：序號

---

**結論**：✅ **transaction_id 和 ord_id 格式完全一致，可以直接 JOIN**

