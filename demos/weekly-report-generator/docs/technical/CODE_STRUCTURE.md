# 程式碼結構說明

**目的**：詳細說明每個檔案的用途和關鍵邏輯

---

## 📁 檔案結構總覽

```
weekly-report-generator/
├── config/                    # 配置模組
├── src/                       # 核心程式碼
├── templates/                 # HTML 模板
├── output/                    # 輸出目錄
└── test_*.py                 # 測試腳本
```

---

## 📂 config/ 目錄

### `bigquery_config.py`

**用途**：BigQuery 連線和配置管理

**關鍵類別**：`BigQueryConfig`

**重要方法**：
- `__init__()`：初始化配置，從環境變數讀取專案 ID 和資料集
- `get_client()`：取得 BigQuery 客戶端實例
- `get_table_ref()`：建構完整的資料表路徑
- `get_ga4_table_ref()`：建構 GA4 事件表路徑
- `query()`：執行 SQL 查詢的輔助方法

**關鍵設定**：
```python
project_id = 'datalake360-saintpaul'
dataset_id = 'datalake_stpl'
ga4_dataset = 'analytics_304437305'
```

**重要注意事項**：
- 不要明確指定 `location` 參數，讓 BigQuery 自動偵測
- 設定 `GOOGLE_CLOUD_QUOTA_PROJECT` 環境變數避免權限警告

### `chart_config.py`

**用途**：圖表樣式配置

**關鍵配置**：
- `CHART_THEME`：PyEcharts 主題（MACARONS）
- `COLOR_PALETTE`：顏色調色盤
- `TRAFFIC_SOURCE_COLORS`：流量來源對應顏色
- `TITLE_CONFIG`：標題字體大小
- `LABEL_CONFIG`：標籤字體大小
- `TOOLBOX_CONFIG`：工具箱設定

---

## 📂 src/ 目錄

### `main.py`

**用途**：主程式入口點

**執行流程**：
1. 初始化模組（DataFetcher, ChartGenerator, ReportBuilder）
2. 計算本週時間範圍（週一到週日）
3. 查詢 BigQuery 資料（5 個查詢）
4. 生成 PyEcharts 圖表（4 個圖表）
5. 組合資料字典（包含報告時間範圍）
6. 生成 HTML 報告

**關鍵變數**：
- `this_week_monday`, `this_week_sunday`：本週時間範圍
- `data_dict`：所有資料的字典
- `charts_dict`：所有圖表的字典

### `data_fetcher.py`

**用途**：從 BigQuery 查詢資料

**關鍵類別**：`DataFetcher`

**重要方法詳解**：

#### `fetch_gmv_metrics(start_date, end_date)`

**功能**：查詢 GMV 基本指標

**SQL 關鍵點**：
- 使用 `ord_rev` 欄位（不是 `ord_total`）
- 使用 `bhv1 <> '取消'` 判斷取消訂單（不是 `return_ord_id IS NULL`）
- 計算成交總額、總營業額、交易會員數、訂單統計

**返回資料結構**：
```python
{
    'net_revenue': float,        # 成交總額
    'gross_revenue': float,      # 總營業額
    'unique_users': int,         # 交易會員數
    'completed_orders': int,     # 成交訂單總量（所有訂單）
    'total_orders': int,         # 總訂單總量（排除取消）
    'cancelled_orders': int,     # 取消訂單數
    'cancelled_revenue': float,  # 取消訂單總額
    'cancel_rate': float,       # 取消率（百分比）
}
```

#### `fetch_weekly_comparison()`

**功能**：查詢本週與上週的比較資料

**關鍵邏輯**：
- 使用 `get_week_range()` 取得本週範圍
- 使用 `get_last_week_range()` 取得上週範圍
- 分別查詢本週和上週的 GMV 指標
- 計算變化百分比

**返回資料結構**：
```python
{
    'this_week': {...},      # 本週 GMV 指標
    'last_week': {...},      # 上週 GMV 指標
    'changes': {
        'revenue': float,    # 營收變化百分比
        'orders': float,     # 訂單變化百分比
    }
}
```

#### `fetch_traffic_analysis(start_date, end_date)`

**功能**：查詢流量分析資料

**關鍵邏輯**：
1. 生成日期字串列表（用於 GA4 表的分區查詢）
2. 查詢 GA4 Sessions（按流量來源分組）
3. 查詢 GA4 Purchases（取得 transaction_id 和流量來源）
4. 查詢 Shopline 訂單（取得 ord_id 和訂單金額）
5. **在 Python 中 JOIN**（避免位置錯誤）

**為什麼分步查詢？**
- GA4 事件表和 Shopline 訂單表可能在不同位置
- 直接在 SQL 中 JOIN 會出現位置錯誤（404 Not found）
- 解決方案：分步查詢，在 Python 中使用 pandas `merge()` JOIN

**返回資料**：`pandas.DataFrame`
- `traffic_source`：流量來源分類
- `sessions`：工作階段數
- `conversions`：轉換數
- `cvr`：轉換率（百分比）
- `aov`：平均訂單金額
- `revenue`：營收

#### `fetch_aov_analysis(start_date, end_date, dimension)`

**功能**：查詢平均訂單金額分析

**關鍵邏輯**：
- 從 `lv1_order` 表計算購物車件數分布
- 從 `lv1_order_master` 表計算價格帶結構
- 支援維度：`'overall'`, `'new'`, `'returning'`（新客/回購客目前未實作）

**返回資料結構**：
```python
{
    'item_distribution': [
        {
            'item_count': str,      # '1件', '2件', '3件', '4件以上'
            'order_count': int,     # 訂單數
            'avg_amount': float,    # 平均訂單金額
        },
        ...
    ],
    'price_band_distribution': [
        {
            'price_band': str,      # '<500', '500-1500', '≥1500'
            'order_count': int,     # 訂單數
        },
        ...
    ],
}
```

#### `fetch_conversion_funnel(start_date, end_date)`

**功能**：查詢轉換漏斗資料

**關鍵邏輯**：
- 查詢 GA4 事件表（使用日期分區）
- 計算 5 個階段的轉換率：
  1. 訪客（session_start）
  2. 商品瀏覽（view_item）
  3. 加入購物車（add_to_cart）
  4. 開始結帳（begin_checkout）
  5. 完成購買（purchase）

**返回資料結構**：
```python
{
    'overall': {
        'steps': [
            {'label': '訪客', 'count': int},
            {'label': '商品瀏覽', 'count': int},
            ...
        ]
    }
}
```

### `traffic_classifier.py`

**用途**：流量來源分類邏輯

**關鍵函數**：

#### `classify_traffic_source(source, medium)`

**功能**：Python 函式，根據 source 和 medium 分類流量來源

**分類邏輯**：
- 使用正規表達式匹配
- 按照優先順序檢查（直接流量 → 自然搜尋 → 付費廣告 → ...）
- 返回分類字串（例如：`'1. 直接流量'`）

#### `classify_traffic_source_sql(source_col, medium_col)`

**功能**：生成 SQL CASE WHEN 語句

**使用方式**：
```python
sql = classify_traffic_source_sql('ts.source', 'ts.medium')
# 返回 SQL CASE WHEN 語句，可直接嵌入 SQL 查詢
```

**注意事項**：
- 需要處理 `source` 和 `medium` 的 NULL 值
- 使用 `COALESCE()` 處理 NULL

### `chart_generator.py`

**用途**：生成 PyEcharts 圖表

**關鍵類別**：`ChartGenerator`

**重要方法**：

#### `generate_weekly_comparison_chart(comparison_data)`

**功能**：生成本週關鍵摘要圖表

**圖表類型**：柱狀圖（Bar Chart）

**資料來源**：
- `comparison_data['changes']['revenue']`：營收變化百分比
- `comparison_data['changes']['orders']`：訂單數變化百分比

**顏色邏輯**：
- 正值：綠色（`#52C41A`）
- 負值：紅色（`#F5222D`）

#### `generate_traffic_source_chart(traffic_df)`

**功能**：生成流量來源圖表

**圖表類型**：
1. 餅圖（Pie Chart）：按 Sessions 分布
2. 柱狀圖（Bar Chart）：按營收排序

**關鍵邏輯**：
- 使用 `color_map` 對應流量來源和顏色
- 標籤放在圖表外面（避免重疊）
- 柱狀圖標籤顯示在柱頂

#### `generate_aov_distribution_chart(aov_data)`

**功能**：生成 AOV 分布圖表

**圖表類型**：
1. 雙 Y 軸柱狀圖：購物車件數分布（訂單數 + 平均訂單金額）
2. 堆疊圖：價格帶結構

**關鍵邏輯**：
- 使用 `extend_axis()` 建立第二個 Y 軸
- 使用 `itemstyle_opts` 設定顏色

#### `generate_conversion_funnel_chart(funnel_data)`

**功能**：生成轉換漏斗圖

**圖表類型**：漏斗圖（Funnel Chart）

**關鍵設定**：
- `sort_="descending"`：從大到小排序，形成漏斗效果
- `gap=2`：階層間距
- `label_opts.position="inside"`：標籤在漏斗內部

### `ai_summary.py`

**用途**：生成週報的文字摘要

**關鍵函數**：

#### `generate_weekly_summary(data, use_llm=False)`

**功能**：生成週報摘要

**目前實作**：
- `use_llm=False`：使用規則式生成（`_generate_rule_based()`）
- `use_llm=True`：使用 LLM 生成（`_generate_with_llm()`，**尚未實作**）

#### `_generate_rule_based(data)`

**功能**：規則式摘要生成

**生成內容**：
1. 營收表現（成交總額、總營業額、訂單數、會員數）
2. 與上週比較（營收變化、訂單變化）
3. 流量來源分析（前 3 名）
4. 建議（根據變化提供建議）

**未來規劃**：
- 整合 LLM API（OpenAI、Anthropic 等）
- 更智能的觀察與建議
- 可自訂 prompt

### `report_builder.py`

**用途**：組合所有資料和圖表，生成 HTML 報告

**關鍵類別**：`ReportBuilder`

**重要方法**：

#### `build_report(data_dict, charts_dict, brand_name)`

**功能**：組合完整的 HTML 報告

**執行流程**：
1. 讀取 HTML 模板（`templates/report_template.html`）
2. 生成 AI 摘要（`generate_weekly_summary()`）
3. 提取報告時間範圍（`report_period`）
4. 使用 Jinja2 渲染模板
5. 儲存到 `output/` 目錄

**傳遞給模板的變數**：
- `brand_name`：品牌名稱
- `output_date`：產出時間
- `report_start_date`：觀察時間開始（週一）
- `report_end_date`：觀察時間結束（週日）
- `data`：所有資料字典
- `charts`：所有圖表 HTML
- `colors`：顏色配置
- `ai_summary`：AI 摘要文字
- `format_number`、`format_percentage`、`format_currency`：格式化函數

### `utils.py`

**用途**：工具函數

**關鍵函數**：

#### `get_week_range(date=None)`

**功能**：計算指定日期所在週的週一到週日範圍

**參數**：
- `date`：指定日期（`datetime.date`），如果為 `None` 則使用今天

**返回**：
- `tuple`：`(monday, sunday)` 週一到週日的日期

**邏輯**：
```python
# 計算週一（isoweekday: 1=Monday, 7=Sunday）
days_since_monday = date.isoweekday() - 1
monday = date - timedelta(days=days_since_monday)
# 計算週日（週一 + 6 天）
sunday = monday + timedelta(days=6)
```

#### `get_last_week_range(date=None)`

**功能**：計算上週的週一到週日範圍

**邏輯**：
```python
# 先取得本週的週一
monday, _ = get_week_range(date)
# 上週的週日 = 本週的週一 - 1 天
last_sunday = monday - timedelta(days=1)
# 上週的週一 = 上週的週日 - 6 天
last_monday = last_sunday - timedelta(days=6)
```

#### `format_number(value, decimals=0)`

**功能**：格式化數字

**參數**：
- `value`：數字值
- `decimals`：小數位數（0=整數，2=兩位小數）

**返回**：
- `str`：格式化後的數字字串（例如：`"1,234"`）

#### `format_percentage(value, decimals=2)`

**功能**：格式化百分比

**參數**：
- `value`：百分比數值（例如：5.01 表示 5.01%）
- `decimals`：小數位數（預設 2 位）

**返回**：
- `str`：格式化後的百分比字串（例如：`"5.01%"`）

#### `format_currency(value, currency='NT$')`

**功能**：格式化金額

**參數**：
- `value`：金額數值
- `currency`：貨幣符號（預設 `'NT$'`）

**返回**：
- `str`：格式化後的金額字串（例如：`"NT$ 518,919"`）

---

## 📂 templates/ 目錄

### `report_template.html`

**用途**：HTML 報告模板

**技術**：Jinja2 模板引擎

**結構**：
1. **Header**：報告標題、觀察時間、產出時間
2. **GMV 基本指標**：成交總額、總營業額卡片
3. **AI 摘要**：自動生成的觀察與建議
4. **本週關鍵摘要**：與上週比較的圖表
5. **流量分析**：餅圖 + 柱狀圖
6. **AOV 分析**：購物車件數分布 + 價格帶結構
7. **轉換漏斗**：漏斗圖

**關鍵變數**：
- `{{ brand_name }}`：品牌名稱
- `{{ report_start_date }}`：觀察時間開始
- `{{ report_end_date }}`：觀察時間結束
- `{{ output_date }}`：產出時間
- `{{ data.gmv_metrics.* }}`：GMV 指標
- `{{ charts.* }}`：圖表 HTML
- `{{ ai_summary }}`：AI 摘要文字

**格式化函數使用**：
```jinja2
{{ format_currency(data.gmv_metrics.net_revenue) }}
{{ format_percentage(data.weekly_comparison.changes.revenue) }}
{{ format_number(data.gmv_metrics.completed_orders) }}
```

---

## 📂 測試腳本

### `test_connection.py`

**用途**：測試 BigQuery 連線

**功能**：
- 測試連線是否成功
- 列出可用的資料集和資料表
- 檢查資料表結構

### `test_queries.py`

**用途**：測試所有查詢功能

**測試項目**：
1. GMV 基本指標
2. 本週關鍵摘要
3. 流量分析
4. AOV 分析
5. 轉換漏斗

**輸出格式**：
```
📊 測試 1: GMV 基本指標（最近 7 天）
   ✅ 成交營收: NT$ 518,919
   ✅ 總營業額: NT$ 518,919
   ...
```

### `check_transaction_id_format.py`

**用途**：檢查 GA4 transaction_id 與 Shopline ord_id 格式

**功能**：
- 查詢 GA4 transaction_id 範例
- 查詢 Shopline ord_id 範例
- 比較格式是否一致
- 測試 JOIN 是否成功

### `test_join_transaction_id.py`

**用途**：測試 transaction_id 與 ord_id 的 JOIN

**功能**：
- 查詢實際的 transaction_id
- 在 Shopline 中查找對應的 ord_id
- 驗證 JOIN 邏輯

### `list_tables.py`

**用途**：列出所有可用的資料集和資料表

**功能**：
- 列出 BigQuery 專案中的所有資料集
- 列出每個資料集中的資料表
- 顯示資料表結構

### `check_schema.py`

**用途**：檢查特定資料表的 Schema

**功能**：
- 檢查 `lv1_order_master` 的欄位
- 檢查 `lv1_order` 的欄位
- 檢查 `lv1_touch` 的欄位
- 檢查 `lv1_user` 的欄位
- 檢查 `lv1_product` 的欄位

---

## 🔄 資料流程詳解

### 完整流程

```
1. main.py 啟動
   ↓
2. 計算本週時間範圍（週一到週日）
   ↓
3. DataFetcher 查詢 BigQuery
   ├─ fetch_gmv_metrics() → 成交總額、總營業額等
   ├─ fetch_weekly_comparison() → 本週與上週比較
   ├─ fetch_traffic_analysis() → 流量來源分析
   ├─ fetch_aov_analysis() → AOV 分析
   └─ fetch_conversion_funnel() → 轉換漏斗
   ↓
4. ChartGenerator 生成圖表
   ├─ generate_weekly_comparison_chart() → 本週摘要圖表
   ├─ generate_traffic_source_chart() → 流量分析圖表
   ├─ generate_aov_distribution_chart() → AOV 分布圖表
   └─ generate_conversion_funnel_chart() → 轉換漏斗圖表
   ↓
5. AI Summary 生成摘要文字
   └─ generate_weekly_summary() → 規則式摘要
   ↓
6. ReportBuilder 組合報告
   ├─ 讀取 HTML 模板
   ├─ 使用 Jinja2 渲染
   └─ 儲存到 output/ 目錄
   ↓
7. 輸出 HTML 報告
```

### 流量分析特別流程

```
1. 查詢 GA4 Sessions（按流量來源分組）
   SQL: SELECT traffic_category, COUNT(DISTINCT session_id) as sessions
   FROM analytics_304437305.events_*
   ↓
2. 查詢 GA4 Purchases（取得 transaction_id 和流量來源）
   SQL: SELECT transaction_id, traffic_category
   FROM analytics_304437305.events_*
   WHERE event_name = 'purchase'
   ↓
3. 查詢 Shopline 訂單（取得 ord_id 和訂單金額）
   SQL: SELECT ord_id, ord_rev as revenue
   FROM datalake_stpl.lv1_order_master
   ↓
4. 在 Python 中 JOIN
   purchases_df.merge(orders_df, left_on='transaction_id', right_on='ord_id')
   ↓
5. 按流量來源聚合
   traffic_agg = traffic_orders.groupby('traffic_category').agg(...)
   ↓
6. 合併 Sessions 資料
   result_df = sessions_df.merge(traffic_agg, on='traffic_category', how='outer')
   ↓
7. 計算 CVR（轉換率）
   cvr = (conversions / sessions * 100)
```

---

## 🎯 關鍵設計決策

### 1. 為什麼分步查詢流量分析？

**問題**：GA4 和 Shopline 表在不同位置，直接 SQL JOIN 會失敗。

**解決方案**：
- 分步查詢兩個表
- 在 Python 中使用 pandas `merge()` JOIN
- 避免位置錯誤

### 2. 為什麼使用週一到週日而不是最近 7 天？

**原因**：
- 週報應該對應完整的週期（週一到週日）
- 便於比較（上週一到上週日 vs 本週一到本週日）
- 符合業務邏輯

### 3. 為什麼使用規則式 AI 摘要而不是 LLM？

**原因**：
- 初期階段，先建立規則式邏輯
- 後續可整合 LLM，不影響現有架構
- 降低依賴和成本

### 4. 為什麼使用 `ord_rev` 而不是 `ord_total`？

**原因**：
- 根據實際資料表結構，`ord_rev` 是正確的欄位
- `ord_total` 可能不存在或格式不同

### 5. 為什麼使用 `bhv1 <> '取消'` 而不是 `return_ord_id IS NULL`？

**原因**：
- 根據實際資料表結構，`bhv1` 欄位表示訂單狀態
- `'取消'` 值表示取消訂單
- `return_ord_id` 可能不適用於此資料表

---

## 📝 程式碼註解規範

### 函數註解格式

```python
def function_name(param1, param2):
    """
    函數功能描述
    
    Args:
        param1: 參數 1 說明
        param2: 參數 2 說明
        
    Returns:
        返回值說明
        
    Raises:
        Exception: 可能拋出的異常
    """
```

### 類別註解格式

```python
class ClassName:
    """
    類別功能描述
    
    Attributes:
        attr1: 屬性 1 說明
        attr2: 屬性 2 說明
    """
```

### SQL 註解格式

```sql
-- 註解：說明這段 SQL 的用途
SELECT
    -- 欄位註解：說明這個欄位的計算邏輯
    SUM(ord_rev) as net_revenue
FROM ...
```

---

## 🔍 除錯技巧

### 1. 查看 SQL 查詢

在 `data_fetcher.py` 中，可以在查詢前加入 `print(query)`：

```python
query = f"""
SELECT ...
"""
print("=== SQL Query ===")
print(query)
print("=================")
result = self.bq_config.query(query).to_dataframe()
```

### 2. 查看 DataFrame 內容

```python
# 查看前幾筆資料
print(df.head())

# 查看資料形狀
print(df.shape)

# 查看欄位名稱
print(df.columns.tolist())

# 查看資料類型
print(df.dtypes)
```

### 3. 查看圖表配置

在 `chart_generator.py` 中，可以輸出圖表的 HTML：

```python
chart_html = pie.render_embed()
print("=== Chart HTML ===")
print(chart_html[:500])  # 只顯示前 500 字元
print("==================")
```

### 4. 使用測試腳本

```bash
# 測試特定功能
python test_queries.py

# 檢查資料格式
python check_transaction_id_format.py

# 列出所有資料表
python list_tables.py
```

---

**最後更新**：2025-11-05

