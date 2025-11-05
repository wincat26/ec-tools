# 配置總結

**更新日期**：2025-01-27

---

## ✅ 已完成的配置

### 1. 專案與資料集設定

- **專案 ID**：`datalake360-saintpaul`
- **主要資料集**：`datalake_stpl`（訂單、商品等資料）
- **GA4 資料集**：`analytics_304437305`（GA4 事件資料）
- **位置**：`asia-east1`（台灣）

### 2. 環境變數設定

```bash
# 建議在 .env 檔案或環境變數中設定
GOOGLE_CLOUD_PROJECT=datalake360-saintpaul
BIGQUERY_DATASET=datalake_stpl
```

### 3. gcloud 設定

```bash
# 設定預設專案
gcloud config set project datalake360-saintpaul

# 設定 ADC quota project（解決 ProjectId must be non-empty 錯誤）
gcloud auth application-default set-quota-project datalake360-saintpaul
```

---

## 📊 資料表對應

### datalake_stpl 資料集

| 用途 | 資料表名稱 |
|------|-----------|
| 日報表（已彙總） | `orders_summary_daily` |
| 訂單明細 | `orders` |
| 訂單與 GA4 整合 | `order_ga4_integration` |
| 商品洞察 | `product_insights_daily` |

### analytics_304437305 資料集（GA4）

| 用途 | 資料表名稱 |
|------|-----------|
| GA4 事件 | `events_*`（日期分區表） |

---

## 🔧 配置檔案位置

- **BigQuery 配置**：`config/bigquery_config.py`
- **圖表配置**：`config/chart_config.py`
- **環境變數範例**：`.env.example`

---

## 🚀 下一步

1. **確認資料集存在**：確認 `datalake_stpl` 和 `analytics_304437305` 資料集確實存在
2. **確認資料表名稱**：確認資料表名稱是否與配置一致
3. **測試連線**：執行 `python test_connection.py` 驗證連線

---

## ⚠️ 注意事項

- 如果資料集在不同的位置，可能需要調整 `location` 參數
- 如果資料表名稱不同，需要更新 `config/bigquery_config.py` 中的 `TABLES` 字典

