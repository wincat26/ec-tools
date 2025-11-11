# BigQuery SQL 查詢語法 - CDP 資料源

**資料表路徑**：`datalake360-saintpaul.cdp_data.lv0_orders`

---

## 📊 資料表結構

### 主要欄位

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| `id` | STRING | 訂單 ID |
| `order_number` | STRING | 訂單編號 |
| `customer_id` | STRING | 會員 ID |
| `status` | STRING | 訂單狀態（pending, confirmed, cancelled） |
| `subtotal` | INT64 | 訂單金額 |
| `order_payment` | STRING | 付款方式 |
| `created_at` | STRING | 建立時間（ISO 8601 格式） |
| `created_by_channel_name` | STRING | 建立通路 |
| `order_discount` | INT64 | 折扣金額 |
| `order_points` | INT64 | 使用點數 |

### 日期欄位格式

- `created_at`: ISO 8601 格式，例如 `2025-11-05T17:51:44.493+00:00`
- 需要使用 `TIMESTAMP(created_at)` 轉換為 TIMESTAMP 類型
- 然後使用 `DATE(TIMESTAMP(created_at))` 取得日期

---

## 📊 昨天業績查詢（基礎版）

```sql
SELECT
  DATE(TIMESTAMP(created_at)) AS date,
  COUNT(*) AS total_orders,
  COUNT(DISTINCT customer_id) AS unique_customers,
  SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS total_revenue,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS valid_orders,
  AVG(CASE WHEN status <> 'cancelled' THEN subtotal END) AS avg_order_value
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY DATE(TIMESTAMP(created_at))
ORDER BY date DESC;
```

---

## 📊 昨天業績查詢（完整版）

```sql
SELECT
  DATE(TIMESTAMP(created_at)) AS date,
  -- 訂單統計
  COUNT(*) AS total_orders,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS valid_orders,
  COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_number END) AS cancelled_orders,
  
  -- 營業額統計
  SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS total_revenue,
  SUM(subtotal) AS gross_total,
  SUM(CASE WHEN status = 'cancelled' THEN subtotal ELSE 0 END) AS cancelled_amount,
  
  -- 平均指標
  AVG(CASE WHEN status <> 'cancelled' THEN subtotal END) AS avg_order_value,
  
  -- 會員統計
  COUNT(DISTINCT customer_id) AS unique_customers,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN customer_id END) AS valid_customers
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY DATE(TIMESTAMP(created_at))
ORDER BY date DESC;
```

---

## 📊 指定日期查詢

```sql
-- 查詢 2025-11-05 的業績
SELECT
  DATE(TIMESTAMP(created_at)) AS date,
  SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS total_revenue,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS valid_orders,
  AVG(CASE WHEN status <> 'cancelled' THEN subtotal END) AS avg_order_value
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) = DATE('2025-11-05')
GROUP BY DATE(TIMESTAMP(created_at));
```

---

## 📊 訂單狀態查詢

```sql
-- 查看昨天各狀態訂單統計
SELECT
  status,
  COUNT(*) AS count,
  SUM(subtotal) AS total_amount,
  COUNT(DISTINCT customer_id) AS unique_customers
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY status
ORDER BY count DESC;
```

---

## 📊 訂單明細查詢

```sql
-- 查詢昨天的所有訂單明細
SELECT
  order_number,
  customer_id,
  status,
  subtotal,
  order_payment,
  created_at,
  created_by_channel_name
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
ORDER BY created_at DESC;
```

---

## 📊 按付款方式分類

```sql
-- 查詢昨天各付款方式的業績
SELECT
  order_payment AS payment_method,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS valid_orders,
  SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS total_revenue
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY order_payment
ORDER BY total_revenue DESC;
```

---

## 📊 日期範圍查詢

```sql
-- 查詢最近 7 天的業績
SELECT
  DATE(TIMESTAMP(created_at)) AS date,
  SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS total_revenue,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS valid_orders,
  AVG(CASE WHEN status <> 'cancelled' THEN subtotal END) AS avg_order_value
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) 
  AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY DATE(TIMESTAMP(created_at))
ORDER BY date DESC;
```

---

## 📊 月迄今（MTD）查詢

```sql
-- 查詢當月迄今的業績
SELECT
  DATE_TRUNC(DATE(TIMESTAMP(created_at)), MONTH) AS month,
  SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS mtd_revenue,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS mtd_orders,
  AVG(CASE WHEN status <> 'cancelled' THEN subtotal END) AS avg_order_value
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
  AND DATE(TIMESTAMP(created_at)) < CURRENT_DATE()
GROUP BY DATE_TRUNC(DATE(TIMESTAMP(created_at)), MONTH);
```

---

## 🔍 常用狀態說明

| 狀態 | 說明 |
|------|------|
| `pending` | 待處理訂單 |
| `confirmed` | 已確認訂單 |
| `cancelled` | 已取消訂單 |

---

## ⚙️ 常用篩選條件

### 只查詢有效訂單（排除取消）
```sql
WHERE status <> 'cancelled'
```

### 只查詢已確認訂單
```sql
WHERE status = 'confirmed'
```

### 組合條件
```sql
WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND status <> 'cancelled'
```

---

## 💡 快速查詢範例

### 1. 昨天業績（最簡單）
```sql
SELECT
  SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS total_revenue,
  COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS valid_orders
FROM `datalake360-saintpaul.cdp_data.lv0_orders`
WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);
```

### 2. 與上週同期比較
```sql
WITH yesterday AS (
  SELECT
    SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS revenue,
    COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS orders
  FROM `datalake360-saintpaul.cdp_data.lv0_orders`
  WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
),
last_week AS (
  SELECT
    SUM(CASE WHEN status <> 'cancelled' THEN subtotal ELSE 0 END) AS revenue,
    COUNT(DISTINCT CASE WHEN status <> 'cancelled' THEN order_number END) AS orders
  FROM `datalake360-saintpaul.cdp_data.lv0_orders`
  WHERE DATE(TIMESTAMP(created_at)) = DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY)
)
SELECT
  y.revenue AS yesterday_revenue,
  lw.revenue AS last_week_revenue,
  ROUND((y.revenue - lw.revenue) / lw.revenue * 100, 2) AS change_percent,
  y.orders AS yesterday_orders,
  lw.orders AS last_week_orders
FROM yesterday y, last_week lw;
```

---

**最後更新**：2025-11-06

