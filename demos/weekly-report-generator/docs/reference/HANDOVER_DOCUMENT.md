# 電商週報生成器 - 交接文件

**文件版本**：v1.0  
**最後更新**：2025-11-05  
**維護者**：開發團隊

---

## 📋 目錄

1. [專案概述](#專案概述)
2. [系統架構](#系統架構)
3. [技術棧與依賴](#技術棧與依賴)
4. [專案結構](#專案結構)
5. [資料庫配置](#資料庫配置)
6. [核心功能模組](#核心功能模組)
7. [使用說明](#使用說明)
8. [關鍵邏輯說明](#關鍵邏輯說明)
9. [常見問題與排錯](#常見問題與排錯)
10. [待辦事項與未來規劃](#待辦事項與未來規劃)
11. [相關文件](#相關文件)

---

## 📖 專案概述

### 專案目的

電商週報生成器是一個自動化工具，用於：
- 從 BigQuery 查詢電商營運資料
- 整合 GA4 流量分析資料
- 生成包含圖表和 AI 摘要的 HTML 週報
- 提供每週一到週日的數據分析報告

### 核心功能

1. **GMV 基本指標**：成交總額、總營業額、交易會員數、訂單統計
2. **本週關鍵摘要**：與上週的比較分析（營收、訂單數變化）
3. **流量分析**：8 種流量來源的分類與分析（Sessions、CVR、AOV、營收）
4. **AOV 分析**：購物車件數分布、價格帶結構
5. **轉換漏斗**：從訪客到成交的轉換率分析
6. **AI 摘要**：自動生成週報觀察與建議（目前為規則式，後續可整合 LLM）

### 報告時間範圍

- **觀察時間**：本週週一到週日（例如：2025-11-04 至 2025-11-10）
- **比較基準**：上週週一到上週日
- **產出時間**：報告生成的時間戳記

---

## 🏗️ 系統架構

### 整體架構圖

```
┌─────────────────────────────────────────────────────────┐
│                    週報生成器流程                        │
└─────────────────────────────────────────────────────────┘

1. 資料查詢層 (Data Fetcher)
   ├─ BigQuery 連線
   ├─ SQL 查詢執行
   └─ 資料轉換為 DataFrame

2. 資料處理層 (Data Processor)
   ├─ KPI 計算
   ├─ 週期比較
   └─ 資料格式化

3. 圖表生成層 (Chart Generator)
   ├─ PyEcharts 圖表生成
   ├─ 流量分類邏輯
   └─ HTML 嵌入

4. AI 摘要層 (AI Summary)
   ├─ 規則式摘要（目前）
   └─ LLM 整合（未來）

5. 報告組合層 (Report Builder)
   ├─ Jinja2 模板渲染
   ├─ 資料整合
   └─ HTML 輸出
```

### 資料流程

```
BigQuery (GA4 + Shopline)
    ↓
DataFetcher (SQL 查詢)
    ↓
DataProcessor (資料處理)
    ↓
ChartGenerator (PyEcharts)
    ↓
AI Summary (文字生成)
    ↓
ReportBuilder (HTML 組合)
    ↓
輸出 HTML 報告
```

---

## 🛠️ 技術棧與依賴

### Python 版本

- **Python 3.11+**

### 核心依賴套件

```txt
# BigQuery 資料查詢
google-cloud-bigquery>=3.11.0
google-auth>=2.23.0
db-dtypes>=1.2.0  # BigQuery 資料類型支援

# 資料處理
pandas>=2.0.0
numpy>=1.24.0

# 圖表生成
pyecharts>=2.0.0

# 模板引擎
jinja2>=3.1.0

# 環境變數管理
python-dotenv>=1.0.0

# 日期處理
python-dateutil>=2.8.0
```

### 安裝方式

```bash
# 進入專案目錄
cd weekly-report-generator

# 安裝依賴
pip install -r requirements.txt
```

### Google Cloud 認證

需要設定 Google Cloud 認證才能連接 BigQuery：

```bash
# 設定預設專案
gcloud config set project datalake360-saintpaul

# 設定 Application Default Credentials
gcloud auth application-default login

# 設定 quota project（避免權限警告）
gcloud auth application-default set-quota-project datalake360-saintpaul
```

詳細認證設定請參考：`AUTHENTICATION_SETUP.md`

---

## 📁 專案結構

```
weekly-report-generator/
├── README.md                          # 專案說明文件
├── HANDOVER_DOCUMENT.md               # 本交接文件（重要！）
├── requirements.txt                   # Python 依賴套件
├── .env.example                       # 環境變數範例
├── .gitignore                         # Git 忽略檔案
│
├── config/                            # 配置模組
│   ├── __init__.py
│   ├── bigquery_config.py            # BigQuery 連線設定
│   └── chart_config.py               # 圖表樣式設定
│
├── src/                               # 核心程式碼
│   ├── __init__.py
│   ├── main.py                        # 主程式入口
│   ├── data_fetcher.py                # BigQuery 資料查詢
│   ├── data_processor.py              # 資料處理（目前未使用）
│   ├── traffic_classifier.py          # 流量來源分類邏輯
│   ├── chart_generator.py             # PyEcharts 圖表生成
│   ├── ai_summary.py                  # AI 摘要生成
│   ├── report_builder.py              # HTML 報告組合
│   └── utils.py                       # 工具函數（日期計算、格式化）
│
├── templates/                         # HTML 模板
│   └── report_template.html           # 週報 HTML 模板
│
├── output/                            # 輸出目錄
│   └── weekly_report_*.html          # 生成的週報檔案
│
└── 文件資料夾/
    ├── AUTHENTICATION_SETUP.md        # 認證設定指南
    ├── CONFIGURATION_SUMMARY.md       # 配置總結
    ├── DATABASE_SCHEMA.md             # 資料庫結構說明
    ├── SQL_QUERY_UPDATE.md            # SQL 查詢更新記錄
    ├── TRAFFIC_CLASSIFICATION.md      # 流量分類規則
    ├── TRAFFIC_ANALYSIS_IMPLEMENTATION.md  # 流量分析實作
    ├── TRANSACTION_ID_VERIFICATION.md # Transaction ID 驗證
    ├── FINAL_SUMMARY.md               # 完成總結
    └── test_*.py                      # 測試腳本
```

---

## 🗄️ 資料庫配置

### BigQuery 專案設定

**專案 ID**：`datalake360-saintpaul`

**資料集**：
- `datalake_stpl`：Shopline 訂單資料
- `analytics_304437305`：GA4 事件資料

**位置**：`asia-northeast1`（自動偵測）

### 關鍵資料表

#### Shopline 訂單表

| 資料表 | 用途 | 關鍵欄位 |
|--------|------|---------|
| `lv1_order_master` | 訂單主檔 | `ord_id`, `ord_rev`, `user_id`, `dt`, `bhv1`, `touch_class` |
| `lv1_order` | 訂單明細 | `ord_id`, `pro_id`, `ord_qty`, `ord_price` |

#### GA4 事件表

| 資料表 | 用途 | 關鍵欄位 |
|--------|------|---------|
| `events_YYYYMMDD` | 日期分區事件表 | `event_name`, `user_pseudo_id`, `event_params`, `traffic_source` |

### 重要欄位說明

#### `lv1_order_master` 關鍵欄位

- **`ord_rev`**：訂單金額（使用此欄位，不是 `ord_total`）
- **`bhv1`**：訂單狀態（`'取消'` 表示取消訂單）
- **`dt`**：訂單日期（TIMESTAMP）
- **`touch_class`**：通路種類（`'ec'` 表示電商通路）
- **`user_id`**：會員 ID
- **`ord_id`**：訂單編號（17 位數字，格式：`YYYYMMDDHHMMSSNNN`）

#### GA4 事件表關鍵欄位

- **`event_name`**：事件名稱（`'session_start'`, `'purchase'`, `'view_item'` 等）
- **`event_params`**：事件參數（ARRAY，包含 `transaction_id`）
- **`traffic_source`**：流量來源（RECORD，包含 `source` 和 `medium`）
- **`session_traffic_source_last_click`**：最後點擊的流量來源（RECORD）

### 查詢邏輯重點

#### 1. GMV 指標查詢

```sql
-- 成交總額：所有訂單的 ord_rev
SUM(ord_rev) as net_revenue

-- 總營業額：排除取消訂單的 ord_rev
SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) as gross_revenue

-- 成交訂單總量：所有訂單數（包含取消）
COUNT(DISTINCT ord_id) as completed_orders

-- 總訂單總量：排除取消的訂單數
SUM(CASE WHEN bhv1 <> '取消' THEN 1 ELSE 0 END) as total_orders

-- 交易會員數
COUNT(DISTINCT user_id) as unique_users
```

**重要**：取消訂單的判斷是 `bhv1 = '取消'`，不是 `return_ord_id IS NULL`

#### 2. Transaction ID 對應

- GA4 的 `transaction_id` 格式：17 位數字（例如：`20241105153444114`）
- Shopline 的 `ord_id` 格式：17 位數字（完全相同）
- **可以直接 JOIN**：`transaction_id = ord_id`

#### 3. 日期範圍計算

- **本週**：使用 `get_week_range()` 計算週一到週日
- **上週**：使用 `get_last_week_range()` 計算上週一到上週日
- **日期分區**：GA4 事件表使用 `_TABLE_SUFFIX` 過濾（格式：`YYYYMMDD`）

---

## 🔧 核心功能模組

### 1. DataFetcher (`src/data_fetcher.py`)

負責從 BigQuery 查詢資料。

#### 主要方法

| 方法 | 功能 | 參數 | 返回 |
|------|------|------|------|
| `fetch_gmv_metrics()` | 查詢 GMV 基本指標 | `start_date`, `end_date` | `dict` |
| `fetch_weekly_comparison()` | 查詢本週與上週比較 | 無 | `dict` |
| `fetch_traffic_analysis()` | 查詢流量分析 | `start_date`, `end_date` | `DataFrame` |
| `fetch_aov_analysis()` | 查詢 AOV 分析 | `start_date`, `end_date`, `dimension` | `dict` |
| `fetch_conversion_funnel()` | 查詢轉換漏斗 | `start_date`, `end_date` | `dict` |

#### 關鍵查詢邏輯

**流量分析**：
- 分兩步查詢（避免位置錯誤）
- 步驟 1：查詢 GA4 Sessions（按流量來源分組）
- 步驟 2：查詢 GA4 Purchases + JOIN Shopline 訂單（在 Python 中 JOIN）
- 原因：GA4 和 Shopline 表可能在不同位置，直接 SQL JOIN 會失敗

### 2. TrafficClassifier (`src/traffic_classifier.py`)

流量來源分類邏輯，將 GA4 的 `source` 和 `medium` 分類為 8 種類別。

#### 分類規則

| 分類 | 規則 | SQL 條件 |
|------|------|---------|
| 1. 直接流量 | `source = '(direct)'` AND `medium = '(none)'` | `source = '(direct)' AND (medium = '(none)' OR medium = '(not set)')` |
| 2. 自然搜尋 | `source/medium` 包含 `/ organic` 或包含 `search` | `REGEXP_CONTAINS(LOWER(source_medium), r'/ organic$|.*search.*')` |
| 3. 付費廣告 | `medium` 為 `ads|cpc|paid|ppc|cpm|pmax|ad|fb-SiteLink` | `REGEXP_CONTAINS(source_medium, r'/ (ads\|cpc\|paid\|ppc\|cpm\|pmax\|ad\|fb-SiteLink)$')` |
| 4. 會員經營 | `source/medium` 包含 `edm|line|push|sms|cdp|crm` | `REGEXP_CONTAINS(source_medium, r'(edm\|line\|push\|sms\|cdp\|crm)')` |
| 5. AI 助理 | `source` 開頭為 `chatgpt|perplexity|copilot|bard|gemini` | `REGEXP_CONTAINS(LOWER(source_medium), r'^(chatgpt\|perplexity\|copilot\|bard\|gemini)')` |
| 6. 社群媒體 | `source/medium` 包含 `facebook|threads|instagram|t.co|line|linktr.ee|pinterest|linkedin` | `REGEXP_CONTAINS(source_medium, r'(facebook\|threads\|instagram|t\\.co\|line\|linktr\\.ee\|pinterest\|linkedin)')` |
| 7. 參照連結 | `medium = 'referral'` | `REGEXP_CONTAINS(source_medium, r'/ referral$')` |
| 8. 其他 | 不符合以上規則 | `ELSE '8. 其他'` |

#### 使用方法

```python
from src.traffic_classifier import classify_traffic_source, classify_traffic_source_sql

# Python 函式
category = classify_traffic_source('google', 'organic')  # 返回 '2. 自然搜尋'

# SQL 語句生成
sql = classify_traffic_source_sql('ts.source', 'ts.medium')
```

### 3. ChartGenerator (`src/chart_generator.py`)

使用 PyEcharts 生成互動式圖表。

#### 生成的圖表類型

1. **本週關鍵摘要圖表**：柱狀圖（營收變化、訂單數變化）
2. **流量來源分布圖**：餅圖（Sessions） + 柱狀圖（營收）
3. **AOV 分布圖**：雙 Y 軸柱狀圖（購物車件數） + 堆疊圖（價格帶）
4. **轉換漏斗圖**：漏斗圖（從大到小排序）

#### 圖表配置

- **主題**：MACARONS（可在 `config/chart_config.py` 修改）
- **顏色**：使用 `TRAFFIC_SOURCE_COLORS` 對應流量來源
- **字體大小**：統一在 `config/chart_config.py` 中設定

### 4. AI Summary (`src/ai_summary.py`)

生成週報的文字摘要。

#### 目前實作

- **模式**：規則式生成（`use_llm=False`）
- **功能**：
  - 分析營收表現
  - 與上週比較
  - 流量來源分析
  - 提供建議

#### 未來規劃

- 整合 LLM API（OpenAI、Anthropic 等）
- 更智能的觀察與建議
- 可自訂 prompt

### 5. ReportBuilder (`src/report_builder.py`)

組合所有資料和圖表，生成最終的 HTML 報告。

#### 工作流程

1. 讀取 HTML 模板（`templates/report_template.html`）
2. 生成 AI 摘要
3. 使用 Jinja2 渲染模板
4. 儲存到 `output/` 目錄

#### 輸出檔案命名

格式：`weekly_report_YYYYMMDD_HHMMSS.html`

例如：`weekly_report_20251105_111952.html`

### 6. Utils (`src/utils.py`)

工具函數。

#### 主要函數

| 函數 | 功能 | 範例 |
|------|------|------|
| `get_week_range()` | 計算指定日期所在週的週一到週日 | `(date(2025, 11, 4), date(2025, 11, 10))` |
| `get_last_week_range()` | 計算上週的週一到週日 | `(date(2025, 10, 28), date(2025, 11, 3))` |
| `format_number()` | 格式化數字 | `format_number(1234.56, decimals=0)` → `"1,235"` |
| `format_percentage()` | 格式化百分比 | `format_percentage(5.01)` → `"5.01%"` |
| `format_currency()` | 格式化金額 | `format_currency(518919)` → `"NT$ 518,919"` |

---

## 🚀 使用說明

### 基本使用

```bash
# 1. 進入專案目錄
cd weekly-report-generator

# 2. 確保已安裝依賴
pip install -r requirements.txt

# 3. 確認 Google Cloud 認證
gcloud auth application-default login

# 4. 執行週報生成
python src/main.py
```

### 環境變數設定（可選）

建立 `.env` 檔案：

```env
# 品牌名稱
BRAND_NAME=豆油伯

# 報告天數（目前不使用，固定為週一到週日）
REPORT_DAYS=7

# Google Cloud 專案（可在程式碼中設定）
GOOGLE_CLOUD_PROJECT=datalake360-saintpaul
```

### 測試腳本

```bash
# 測試 BigQuery 連線
python test_connection.py

# 測試所有查詢功能
python test_queries.py

# 檢查 transaction_id 格式
python check_transaction_id_format.py

# 測試 JOIN 功能
python test_join_transaction_id.py
```

### 輸出結果

生成的報告會儲存在 `output/` 目錄，可以直接在瀏覽器中開啟查看。

---

## 🔍 關鍵邏輯說明

### 1. 時間範圍計算

**重要**：週報使用「週一到週日」的概念，不是「最近 7 天」。

```python
from src.utils import get_week_range, get_last_week_range

# 本週範圍（週一到週日）
monday, sunday = get_week_range()
# 例如：date(2025, 11, 4) 至 date(2025, 11, 10)

# 上週範圍（上週一到上週日）
last_monday, last_sunday = get_last_week_range()
# 例如：date(2025, 10, 28) 至 date(2025, 11, 3)
```

### 2. 流量分析 JOIN 邏輯

**為什麼分兩步查詢？**

因為 GA4 事件表（`analytics_304437305.events_*`）和 Shopline 訂單表（`datalake_stpl.lv1_order_master`）可能在不同位置，直接在 SQL 中 JOIN 會出現位置錯誤。

**解決方案**：
1. 步驟 1：查詢 GA4 Sessions（按流量來源分組）
2. 步驟 2：查詢 GA4 Purchases（取得 transaction_id 和流量來源）
3. 步驟 3：查詢 Shopline 訂單（取得 ord_id 和訂單金額）
4. 步驟 4：在 Python 中使用 pandas `merge()` JOIN

```python
# 在 Python 中 JOIN
traffic_orders = purchases_df.merge(
    orders_df,
    left_on='transaction_id',
    right_on='ord_id',
    how='inner'
)
```

### 3. Transaction ID 對應

**格式**：17 位數字（例如：`20241105153444114`）

**結構**：
- 前 8 位：日期（YYYYMMDD）
- 中間 6 位：時間（HHMMSS）
- 後 3 位：序號

**驗證**：GA4 的 `transaction_id` 和 Shopline 的 `ord_id` 格式完全一致，可以直接 JOIN。

### 4. 流量來源分類邏輯

**資料來源**：
- **Sessions**：使用 `traffic_source.source` 和 `traffic_source.medium`
- **Purchases**：使用 `session_traffic_source_last_click.manual_campaign` 或 `cross_channel_campaign`

**分類 SQL**：
```sql
CASE
    WHEN source = '(direct)' AND (medium = '(none)' OR medium = '(not set)') THEN '1. 直接流量'
    WHEN REGEXP_CONTAINS(LOWER(CONCAT(source, ' / ', medium)), r'/ organic$|.*search.*') THEN '2. 自然搜尋'
    ...
END
```

### 5. 數字格式化規則

| 類型 | 格式 | 函數 | 範例 |
|------|------|------|------|
| 金額 | 整數，千分位 | `format_currency()` | `NT$ 518,919` |
| 百分比 | 兩位小數 | `format_percentage()` | `5.01%` |
| 訂單數 | 整數，千分位 | `format_number()` | `238` |

---

## ⚠️ 常見問題與排錯

### 1. BigQuery 連線失敗

**錯誤訊息**：
```
Your default credentials were not found.
```

**解決方案**：
```bash
# 設定 Application Default Credentials
gcloud auth application-default login

# 設定 quota project
gcloud auth application-default set-quota-project datalake360-saintpaul
```

### 2. 位置錯誤（Location Error）

**錯誤訊息**：
```
404 Not found: Dataset datalake360-saintpaul:datalake_stpl was not found in location asia-east1
```

**原因**：資料集實際位置是 `asia-northeast1`，但查詢時指定了錯誤位置。

**解決方案**：
- 在 `bigquery_config.py` 中，不要明確指定 `location` 參數
- 讓 BigQuery 自動偵測資料集位置

### 3. Transaction ID 格式不一致

**症狀**：流量分析沒有資料，JOIN 失敗。

**檢查方式**：
```bash
python check_transaction_id_format.py
```

**解決方案**：
- 確認 GA4 的 `transaction_id` 和 Shopline 的 `ord_id` 格式一致
- 如果格式不同，需要調整 JOIN 邏輯

### 4. 流量分析顏色沒有區分

**原因**：PyEcharts 的顏色配置沒有正確應用。

**解決方案**：
- 檢查 `chart_generator.py` 中的 `color_map` 配置
- 確認 `TRAFFIC_SOURCE_COLORS` 在 `chart_config.py` 中正確定義

### 5. 數字格式化錯誤

**症狀**：百分比顯示為小數，金額顯示為浮點數。

**解決方案**：
- 使用 `format_percentage()` 格式化百分比（兩位小數）
- 使用 `format_currency()` 格式化金額（整數）

### 6. 日期範圍錯誤

**症狀**：查詢的資料不是週一到週日。

**檢查方式**：
```python
from src.utils import get_week_range
monday, sunday = get_week_range()
print(f"本週範圍：{monday} 至 {sunday}")
```

**解決方案**：
- 確認所有查詢方法都使用 `start_date` 和 `end_date` 參數
- 不要使用 `days=7` 參數（已棄用）

---

## 📝 待辦事項與未來規劃

### 已完成

- [x] BigQuery 連線設定
- [x] 資料查詢模組（GMV、流量分析、AOV、轉換漏斗）
- [x] 流量分類邏輯（8 種分類）
- [x] PyEcharts 圖表生成
- [x] HTML 報告模板
- [x] 數字格式化（百分比兩位小數，金額取整數）
- [x] 時間範圍計算（週一到週日）
- [x] AI 摘要生成（規則式）

### 待完成

#### 高優先級

- [ ] **LLM 整合**：將 AI 摘要從規則式改為 LLM 生成
  - 支援 OpenAI API
  - 支援 Anthropic API
  - 可自訂 prompt
  - 後台執行，不影響前台效能

- [ ] **新客/回購客判斷**：實作首次購買日期的判斷邏輯
  - JOIN `lv1_user` 表
  - 計算首次購買日期
  - 區分新客和回購客的 AOV 分析

- [ ] **錯誤處理加強**：
  - 更詳細的錯誤訊息
  - 日誌記錄
  - 查詢失敗時的降級處理

#### 中優先級

- [ ] **效能優化**：
  - 使用 BigQuery 批次查詢
  - 快取機制（避免重複查詢）
  - 並行查詢

- [ ] **測試覆蓋**：
  - 單元測試
  - 整合測試
  - 查詢邏輯測試

- [ ] **配置管理**：
  - 支援多品牌配置
  - 環境變數驗證
  - 配置檔案範例

#### 低優先級

- [ ] **報告客製化**：
  - 可選的圖表類型
  - 自訂顏色主題
  - 多語言支援

- [ ] **排程功能**：
  - 自動每週生成報告
  - Email 發送
  - 上傳到 Google Drive

---

## 📚 相關文件

### 核心文件

1. **README.md**：專案基本說明
2. **HANDOVER_DOCUMENT.md**：本交接文件（**最重要**）
3. **AUTHENTICATION_SETUP.md**：Google Cloud 認證設定指南

### 技術文件

1. **DATABASE_SCHEMA.md**：資料庫結構說明
2. **SQL_QUERY_UPDATE.md**：SQL 查詢邏輯更新記錄
3. **TRAFFIC_CLASSIFICATION.md**：流量分類規則詳細說明
4. **TRAFFIC_ANALYSIS_IMPLEMENTATION.md**：流量分析實作說明
5. **TRANSACTION_ID_VERIFICATION.md**：Transaction ID 格式驗證結果

### 配置文件

1. **CONFIGURATION_SUMMARY.md**：BigQuery 配置總結
2. **FINAL_SUMMARY.md**：專案完成總結

### 測試腳本

1. **test_connection.py**：測試 BigQuery 連線
2. **test_queries.py**：測試所有查詢功能
3. **check_transaction_id_format.py**：檢查 transaction_id 格式
4. **test_join_transaction_id.py**：測試 JOIN 功能

---

## 🔑 關鍵資訊速查

### 專案路徑
```
/Users/winson/Dropbox/vibe_tools/ec-tools/weekly-report-generator
```

### BigQuery 專案
```
專案 ID: datalake360-saintpaul
資料集: datalake_stpl, analytics_304437305
```

### 關鍵欄位
```
訂單表: ord_rev (金額), bhv1 (狀態), ord_id (訂單編號)
GA4 表: transaction_id (17位數字), traffic_source (流量來源)
```

### 時間計算
```
週一到週日: get_week_range()
上週一到上週日: get_last_week_range()
```

### 執行命令
```bash
# 生成週報
python src/main.py

# 測試連線
python test_connection.py

# 測試查詢
python test_queries.py
```

---

## 📞 聯絡資訊

如有問題，請參考：
1. 相關文件（見上方）
2. 測試腳本（用於診斷問題）
3. 程式碼註解（詳細說明每個函數）

---

## 🎯 快速開始指南

### 第一次使用

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定認證**
   ```bash
   gcloud auth application-default login
   gcloud auth application-default set-quota-project datalake360-saintpaul
   ```

3. **測試連線**
   ```bash
   python test_connection.py
   ```

4. **生成週報**
   ```bash
   python src/main.py
   ```

5. **查看報告**
   - 開啟 `output/` 目錄中的 HTML 檔案

### 常見修改

**修改品牌名稱**：
- 編輯 `.env` 檔案：`BRAND_NAME=新品牌名稱`

**修改圖表顏色**：
- 編輯 `config/chart_config.py`：修改 `TRAFFIC_SOURCE_COLORS`

**修改查詢邏輯**：
- 編輯 `src/data_fetcher.py`：修改對應的 SQL 查詢

**修改報告模板**：
- 編輯 `templates/report_template.html`：調整 HTML 結構

---

## 📌 重要提醒

1. **時間範圍**：週報使用「週一到週日」，不是「最近 7 天」
2. **欄位名稱**：使用 `ord_rev` 不是 `ord_total`，使用 `bhv1` 判斷取消
3. **位置問題**：GA4 和 Shopline 表在不同位置，需要分步查詢
4. **數字格式**：百分比兩位小數，金額取整數
5. **Transaction ID**：格式為 17 位數字，可以直接 JOIN

---

**文件維護**：請定期更新此文件，特別是當有重大變更時。

**最後更新**：2025-11-05

