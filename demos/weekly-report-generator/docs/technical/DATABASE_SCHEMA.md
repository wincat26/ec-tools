# 資料庫結構說明

**更新日期**：2025-01-27

---

## 📊 專案與資料集

- **專案 ID**：`datalake360-saintpaul`
- **主要資料集**：`datalake_stpl`
- **GA4 資料集**：`analytics_304437305`
- **位置**：`asia-northeast1`（自動偵測）

---

## 📁 datalake_stpl 資料集結構

### Level 0 原始資料表（lv0_*）

| 資料表名稱 | 說明 | 用途 |
|-----------|------|------|
| `lv0_orders` | 原始訂單資料 | 訂單明細 |
| `lv0_customers` | 原始客戶資料 | 客戶資訊 |
| `lv0_products` | 原始商品資料 | 商品資訊 |
| `lv0_channels` | 原始渠道資料 | 銷售渠道 |
| `lv0_addon_products` | 附加商品 | 加購商品 |
| `lv0_gifts` | 贈品資料 | 贈品資訊 |
| `lv0_promotions` | 促銷活動 | 活動資訊 |
| `lv0_return_orders` | 退貨訂單 | 退貨資料 |

### Level 1 處理後資料表（lv1_*）

| 資料表名稱 | 說明 | 用途 |
|-----------|------|------|
| `lv1_order` | 處理後的訂單資料 | **主要訂單表** |
| `lv1_order_master` | 訂單主檔 | 訂單彙總資訊 |
| `lv1_order_shipping_delivery` | 訂單配送資料 | 配送資訊 |
| `lv1_user` | 處理後的用戶資料 | **主要用戶表** |
| `lv1_user_level` | 用戶等級 | 會員等級 |
| `lv1_user_matrix` | 用戶矩陣 | 用戶分類 |
| `lv1_product` | 處理後的商品資料 | **主要商品表** |
| `lv1_touch` | 接觸點資料 | **可能包含 GA4 整合資料** |
| `lv1_event` | 事件資料 | 用戶行為事件 |
| `lv1_event_log` | 事件日誌 | 事件記錄 |
| `lv1_pay_log` | 付款日誌 | 付款記錄 |
| `lv1_point_log` | 點數日誌 | 點數記錄 |

---

## 🔍 GA4 資料集結構

### analytics_304437305 資料集

| 資料表名稱 | 說明 | 用途 |
|-----------|------|------|
| `events_*` | GA4 事件表（日期分區） | 每日事件資料 |

**查詢方式**：
```sql
-- 查詢最近 7 天的事件
SELECT * FROM `datalake360-saintpaul.analytics_304437305.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20250120' AND '20250127'
```

---

## 📝 資料表對應關係

### 週報生成需要的資料對應

| 需求 | 預期資料表 | 實際資料表 | 狀態 |
|------|-----------|-----------|------|
| **GMV 基本指標** | `orders_summary_daily` | `lv1_order` 或 `lv1_order_master` | ⚠️ 需調整 SQL |
| **訂單明細** | `orders` | `lv1_order` | ✅ 可直接使用 |
| **訂單與 GA4 整合** | `order_ga4_integration` | `lv1_touch` 或 `lv1_event` | ⚠️ 需 JOIN 查詢 |
| **商品洞察** | `product_insights_daily` | `lv1_product` | ⚠️ 需計算彙總 |
| **流量來源** | `order_ga4_integration` | `lv1_touch` + GA4 `events_*` | ⚠️ 需 JOIN 查詢 |
| **轉換漏斗** | GA4 事件表 | `analytics_304437305.events_*` | ✅ 可直接使用 |

---

## 🔧 下一步行動

### 1. 調整 SQL 查詢

需要更新 `src/data_fetcher.py` 中的查詢邏輯：

- **GMV 指標**：從 `lv1_order` 或 `lv1_order_master` 計算
- **流量分析**：從 `lv1_touch` 或 JOIN GA4 `events_*` 表
- **AOV 分析**：從 `lv1_order` 計算
- **轉換漏斗**：從 `analytics_304437305.events_*` 查詢

### 2. 確認欄位名稱

需要確認各表的實際欄位名稱，例如：
- `lv1_order` 表中的金額欄位名稱
- `lv1_order` 表中的狀態欄位名稱
- `lv1_touch` 表中的流量來源欄位名稱

### 3. 測試查詢

建議先執行簡單查詢確認資料結構：
```sql
SELECT * FROM `datalake360-saintpaul.datalake_stpl.lv1_order` LIMIT 10
```

---

## 📚 參考資料

- 實際資料表清單：執行 `python list_tables.py` 查看
- 資料表結構：需要在 BigQuery Console 中查看 Schema

