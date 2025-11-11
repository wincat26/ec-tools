# Step B：週度資料 View 建置 SDD

## Purpose
- 建立 4 個週度 View，提供週報所需指標與規則（總覽、廣告、會員、商品）。

## Functions & Details

### B1. `weekly_overview_metrics`
- **粒度**：每週一筆（週一至週日）。
- **欄位**：`week_start_date`, `week_end_date`, `brand`, `gmv`, `gross_revenue`, `orders`, `sessions`, `conversion_rate`, `avg_order_value`, `google_ads_cost`, `meta_ads_cost`, `total_ad_cost`, `roas`, `weekly_new_members`, `weekly_target_revenue`, `achievement_rate`, `sri`, `sri_flag`, `wow_*`。
- **計算**：以 `daily_metrics` 彙總；SRI = `(近7日營收 ÷ 近28日營收) × 4`，護欄 0.85–1.15。
- **資料來源**：`datalake_looker.daily_metrics` + `targets`（週目標）。

### B2. `weekly_ad_metrics`
- **粒度**：週 × 平台/活動。
- **欄位**：`channel`, `campaign`, `impressions`, `clicks`, `sessions`, `orders`, `revenue`, `spend`, `ctr`, `cpc`, `cpm`, `conversion_rate`, `roas`, `wow_spend`, `wow_roas`。
- **來源**：Google Ads, Meta Ads 原始表或 `daily_metrics` 廣告欄位 + UTM 追蹤。

### B3. `weekly_member_metrics`
- **粒度**：週。
- **欄位**：`new_registered`, `new_first_purchase`, `new_activation_rate`, `new_non_purchase`, `contactable_edm`, `contactable_line`, `existing_repurchase`, `existing_revenue`, `member_total_buyers`, `member_total_revenue`, `vip_repurchase_rate`, `wow_member_revenue` 等。
- **來源**：會員資料表、訂單、行銷訂閱資料。

### B4. `weekly_product_metrics`
- **粒度**：週 × 商品/品類 × 客群（`new`, `existing`, `all`）。
- **欄位**：`product_id`, `product_name`, `category`, `customer_segment`, `units_sold`, `buyers`, `revenue`, `avg_price`, `pageviews`, `add_to_cart`, `conversion_rate`, `wow_revenue`, `is_hot_seller`, `is_hot_view_low_sale`。
- **來源**：訂單明細、商品表、GA4 商品瀏覽/加購事件。
- **規則**：
  - `is_hot_seller`：週營收前 10% 或銷量 Top 10。
  - `is_hot_view_low_sale`：`pageviews` 高於 75 分位且 `conversion_rate` < 1%。

## Deliverables
- BigQuery 建立於 `datalake_looker` dataset。
- 欄位說明文件與 SQL 範本附於此目錄。
- 每日凌晨刷新；週報程式在週一 08:30 後讀取。

