# SQL 查詢邏輯更新總結

**更新日期**：2025-01-27  
**狀態**：✅ 已根據實際資料表結構調整

---

## 📊 資料表對應更新

### 實際資料表結構

| 需求 | 原預期資料表 | 實際資料表 | 更新狀態 |
|------|------------|-----------|---------|
| **GMV 基本指標** | `orders_summary_daily` | `lv1_order_master` | ✅ 已更新 |
| **訂單明細** | `orders` | `lv1_order` | ✅ 已更新 |
| **流量來源** | `order_ga4_integration` | `lv1_order_master.touch_name` + GA4 | ⚠️ 部分實作 |
| **AOV 分析** | `orders` | `lv1_order` + `lv1_order_master` | ✅ 已更新 |
| **轉換漏斗** | GA4 事件表 | `analytics_304437305.events_*` | ✅ 已更新 |

---

## 🔧 主要變更

### 1. GMV 基本指標查詢

**使用資料表**：`lv1_order_master`

**關鍵欄位**：
- `ord_total`: 訂單付款總額
- `return_ord_id`: 退貨原訂單編號（用於判斷是否為成交訂單）
- `dt`: 日期（TIMESTAMP）
- `touch_class`: 通路種類（'ec' 為電商）

**查詢邏輯**：
```sql
-- 成交營收 = 排除退貨的訂單總額
SUM(CASE WHEN return_ord_id IS NULL THEN ord_total ELSE 0 END)

-- 取消率 = 退貨訂單數 / 總訂單數
COUNT(DISTINCT CASE WHEN return_ord_id IS NOT NULL THEN ord_id END) / COUNT(DISTINCT ord_id)
```

### 2. 本週關鍵摘要

**使用資料表**：`lv1_order_master`

**查詢邏輯**：比較本週與上週的資料，計算變化百分比

### 3. 流量分析

**目前實作**：使用 `lv1_order_master.touch_name` 作為流量來源分類

**注意事項**：
- ⚠️ `touch_name` 是通路名稱（如：官網、門店），不是真正的流量來源
- ⚠️ 目前沒有 Sessions 資料，需要從 GA4 `events_*` 表查詢
- ⚠️ 需要整合 GA4 資料才能取得真正的流量來源（直接流量、付費廣告等）

**待完善**：
- 查詢 GA4 `events_*` 表取得 Sessions
- 整合 GA4 流量來源資料（`traffic_source`, `medium`, `campaign` 等）

### 4. AOV 分析

**使用資料表**：
- `lv1_order`: 訂單明細（計算購物車件數）
- `lv1_order_master`: 訂單主檔（計算價格帶）

**查詢邏輯**：
- **購物車件數**：從 `lv1_order` 按 `ord_id` 分組，計算每個訂單的件數
- **價格帶**：從 `lv1_order_master` 使用 `ord_total` 分類

**待完善**：
- 新客/回購客判斷：需要 JOIN `lv1_user` 表，判斷首次購買日期

### 5. 轉換漏斗

**使用資料表**：`analytics_304437305.events_*`（GA4 事件表）

**查詢邏輯**：
- 使用日期分區表（`events_YYYYMMDD`）
- 查詢標準 GA4 事件：
  - `session_start`: 訪客
  - `view_item`: 商品瀏覽
  - `add_to_cart`: 加入購物車
  - `begin_checkout`: 開始結帳
  - `purchase`: 完成購買

**待完善**：
- 商品分區漏斗：按商品分類查詢
- 活動分區漏斗：按促銷活動查詢

---

## 📝 查詢範例

### GMV 基本指標

```sql
SELECT
    SUM(CASE WHEN return_ord_id IS NULL THEN ord_total ELSE 0 END) as net_revenue,
    SUM(ord_total) as gross_revenue,
    COUNT(DISTINCT CASE WHEN return_ord_id IS NULL THEN ord_id END) as completed_orders,
    COUNT(DISTINCT ord_id) as total_orders
FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
WHERE DATE(dt) BETWEEN DATE('2025-01-20') AND DATE('2025-01-27')
    AND touch_class = 'ec'
```

### 轉換漏斗

```sql
SELECT
    COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) as visitors,
    COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) as view_item,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) as add_to_cart,
    COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN user_pseudo_id END) as begin_checkout,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) as purchase
FROM `datalake360-saintpaul.analytics_304437305.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20250120' AND '20250127'
```

---

## ⚠️ 注意事項

### 1. 日期範圍計算

- 查詢時使用 `DATE(dt) BETWEEN start_date AND end_date`，包含兩端
- 需要確保 `start_date` 和 `end_date` 的計算正確

### 2. 資料類型

- `dt` 欄位是 `TIMESTAMP`，需要使用 `DATE()` 函數轉換
- `ord_total`, `ord_price` 等是 `FLOAT`，注意處理 NULL 值

### 3. 成交訂單判斷

- 使用 `return_ord_id IS NULL` 判斷是否為成交訂單
- 退貨訂單會有 `return_ord_id` 指向原訂單編號

### 4. 電商通路過濾

- 所有查詢都加上 `touch_class = 'ec'` 條件，只查詢電商通路
- 如果需要包含門店，可以移除此條件

---

## 🚀 下一步

1. **安裝缺失套件**：
   ```bash
   pip install db-dtypes
   ```

2. **測試查詢**：
   ```bash
   python test_queries.py
   ```

3. **確認資料正確性**：
   - 檢查查詢結果是否合理
   - 確認日期範圍計算正確
   - 確認金額計算邏輯正確

4. **完善流量分析**：
   - 整合 GA4 Sessions 查詢
   - 建立流量來源分類邏輯

5. **完善新客/回購客判斷**：
   - JOIN `lv1_user` 表
   - 計算首次購買日期

---

## 📚 參考文件

- `DATABASE_SCHEMA.md` - 資料庫結構說明
- `check_schema.py` - 檢查資料表 Schema 的工具
- `test_queries.py` - 測試查詢功能的腳本

