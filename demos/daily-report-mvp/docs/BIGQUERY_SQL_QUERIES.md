# BigQuery SQL 查詢語法

**資料表路徑**：`datalake360-saintpaul.datalake_stpl.lv1_order_master`

---

## 📊 昨天業績查詢（基礎版）

```sql
SELECT
  DATE(dt) AS `date`, 
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `總營業額`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS `總訂單總量`,
  AVG(CASE WHEN bhv1 <> '取消' THEN ord_rev END) AS `平均訂單金額(AOV)`,
  COUNT(DISTINCT user_id) AS `交易會員數`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND touch_class = 'ec'  -- 只查詢電商通路
GROUP BY DATE(dt)
ORDER BY `date` DESC;
```

---

## 📊 昨天業績查詢（詳細版 - 參考您提供的格式）

```sql
SELECT
  DATE(dt) AS `date`, 
  SUM(ord_rev) AS `成交總額`, 
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `總營業額`,
  COUNT(DISTINCT user_id) AS `交易會員數`,
  COUNT(DISTINCT ord_id) AS `成交訂單總量`,
  SUM(CASE WHEN bhv1 <> '取消' THEN 1 ELSE 0 END) AS `總訂單總量`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY DATE(dt)
ORDER BY `date` DESC;
```

---

## 📊 指定日期查詢

```sql
-- 查詢 2025-11-05 的業績
SELECT
  DATE(dt) AS `date`, 
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `總營業額`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS `總訂單總量`,
  AVG(CASE WHEN bhv1 <> '取消' THEN ord_rev END) AS `平均訂單金額(AOV)`,
  COUNT(DISTINCT user_id) AS `交易會員數`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) = DATE('2025-11-05')
  AND touch_class = 'ec'
GROUP BY DATE(dt);
```

---

## 📊 日期範圍查詢

```sql
-- 查詢最近 7 天的業績
SELECT
  DATE(dt) AS `date`, 
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `總營業額`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS `總訂單總量`,
  AVG(CASE WHEN bhv1 <> '取消' THEN ord_rev END) AS `平均訂單金額(AOV)`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND touch_class = 'ec'
GROUP BY DATE(dt)
ORDER BY `date` DESC;
```

---

## 📊 完整指標查詢（包含所有統計）

```sql
SELECT
  DATE(dt) AS `date`, 
  -- 營業額相關
  SUM(ord_rev) AS `成交總額`,
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `總營業額`,
  SUM(CASE WHEN bhv1 = '取消' THEN ord_rev ELSE 0 END) AS `取消訂單金額`,
  
  -- 訂單相關
  COUNT(DISTINCT ord_id) AS `成交訂單總量`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS `有效訂單總量`,
  COUNT(DISTINCT CASE WHEN bhv1 = '取消' THEN ord_id END) AS `取消訂單數量`,
  
  -- 會員相關
  COUNT(DISTINCT user_id) AS `交易會員數`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN user_id END) AS `有效交易會員數`,
  
  -- 平均指標
  AVG(CASE WHEN bhv1 <> '取消' THEN ord_rev END) AS `平均訂單金額(AOV)`,
  
  -- 取消率
  ROUND(
    COUNT(DISTINCT CASE WHEN bhv1 = '取消' THEN ord_id END) * 100.0 / 
    NULLIF(COUNT(DISTINCT ord_id), 0), 
    2
  ) AS `取消率(%)`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND touch_class = 'ec'
GROUP BY DATE(dt)
ORDER BY `date` DESC;
```

---

## 📊 訂單明細查詢

```sql
-- 查詢昨天的所有訂單明細
SELECT
  dt,
  ord_id,
  ord_rev,
  bhv1,
  touch_class,
  user_id
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND touch_class = 'ec'
ORDER BY dt DESC;
```

---

## 📊 按通路分類查詢

```sql
-- 查詢昨天各通路的業績
SELECT
  DATE(dt) AS `date`,
  touch_class AS `通路`,
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `總營業額`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS `總訂單總量`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY DATE(dt), touch_class
ORDER BY `date` DESC, `總營業額` DESC;
```

---

## 📊 月迄今（MTD）查詢

```sql
-- 查詢當月迄今的業績
SELECT
  DATE_TRUNC(DATE(dt), MONTH) AS `月份`,
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `月迄今營業額`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS `月迄今訂單總量`,
  AVG(CASE WHEN bhv1 <> '取消' THEN ord_rev END) AS `平均訂單金額(AOV)`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
  AND DATE(dt) < CURRENT_DATE()
  AND touch_class = 'ec'
GROUP BY DATE_TRUNC(DATE(dt), MONTH);
```

---

## 🔍 常用欄位說明

| 欄位名稱 | 說明 | 範例 |
|---------|------|------|
| `dt` | 訂單日期時間 | 2025-11-05 09:04:52 |
| `ord_id` | 訂單 ID | 20251105010452168 |
| `ord_rev` | 訂單金額 | 641.0 |
| `bhv1` | 行為狀態 | '購買'、'取消' |
| `touch_class` | 通路類別 | 'ec'（電商）、'line'、'fb' 等 |
| `user_id` | 會員 ID | 66cecaa2af65bc000aa728ac |

---

## ⚙️ 常用篩選條件

### 只查詢電商通路
```sql
WHERE touch_class = 'ec'
```

### 排除取消訂單
```sql
WHERE bhv1 <> '取消'
```

### 組合條件
```sql
WHERE touch_class = 'ec'
  AND bhv1 <> '取消'
```

---

## 💡 快速查詢範例

### 1. 昨天業績（最簡單）
```sql
SELECT
  SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS `總營業額`,
  COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS `總訂單總量`
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND touch_class = 'ec';
```

### 2. 昨天業績（與上週同期比較）
```sql
WITH yesterday AS (
  SELECT
    SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS revenue,
    COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS orders
  FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
  WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    AND touch_class = 'ec'
),
last_week AS (
  SELECT
    SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) AS revenue,
    COUNT(DISTINCT CASE WHEN bhv1 <> '取消' THEN ord_id END) AS orders
  FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
  WHERE DATE(dt) = DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY)
    AND touch_class = 'ec'
)
SELECT
  y.revenue AS `昨天營業額`,
  lw.revenue AS `上週同期營業額`,
  ROUND((y.revenue - lw.revenue) / lw.revenue * 100, 2) AS `週變化(%)`,
  y.orders AS `昨天訂單數`,
  lw.orders AS `上週同期訂單數`
FROM yesterday y, last_week lw;
```

---

**最後更新**：2025-11-06

