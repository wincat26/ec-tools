# PyEcharts 整合指南

**建立日期**：2025-01-27  
**目的**：說明如何將 PyEcharts 週報生成器整合到現有專案

---

## 📋 整合步驟

### 1. 環境設定

#### 1.1 安裝 Python 依賴

```bash
cd weekly-report-generator
pip install -r requirements.txt
```

#### 1.2 設定 BigQuery 認證

**方式 A：使用服務帳號金鑰（推薦用於開發環境）**

1. 下載服務帳號金鑰 JSON 檔案
2. 設定環境變數：
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

**方式 B：使用 Application Default Credentials（推薦用於生產環境）**

```bash
gcloud auth application-default login
```

#### 1.3 設定環境變數

建立 `.env` 檔案（參考 `.env.example`）：

```bash
cp .env.example .env
# 編輯 .env 填入實際值
```

---

### 2. 驗證 BigQuery 連線

建立測試腳本 `test_connection.py`：

```python
from config.bigquery_config import BigQueryConfig

# 測試連線
config = BigQueryConfig()
client = config.get_client()

# 測試查詢
query = "SELECT COUNT(*) as count FROM `saintpaul_data.orders_summary_daily` LIMIT 1"
result = client.query(query).to_dataframe()
print(f"連線成功！資料表記錄數：{result.iloc[0]['count']}")
```

執行測試：

```bash
python test_connection.py
```

---

### 3. 執行週報生成

#### 3.1 基本執行

```bash
cd weekly-report-generator
python src/main.py
```

#### 3.2 自訂參數

修改 `src/main.py` 或使用環境變數：

```bash
REPORT_DAYS=30 BRAND_NAME=豆油伯 python src/main.py
```

---

### 4. 整合到現有系統

#### 4.1 作為獨立服務（推薦）

將週報生成器作為獨立 Python 服務，透過 API 或排程觸發：

**選項 A：Cloud Scheduler + Cloud Functions**

```yaml
# cloud_functions/main.py
import functions_framework
from weekly_report_generator.src.main import main

@functions_framework.http
def generate_weekly_report(request):
    main()
    return {'status': 'success'}
```

**選項 B：Airflow DAG**

```python
# dags/weekly_report_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG('weekly_report_generator', schedule_interval='0 9 * * 1')  # 每週一早上 9 點

task = BashOperator(
    task_id='generate_report',
    bash_command='cd /path/to/weekly-report-generator && python src/main.py',
    dag=dag,
)
```

#### 4.2 整合到 Next.js 前端

**方式 A：透過 API 端點**

```javascript
// frontend/src/api/reports.ts
export async function generateWeeklyReport() {
  const response = await fetch('/api/reports/generate', {
    method: 'POST',
  });
  return response.json();
}
```

```typescript
// backend/src/routes/reports.ts
import { exec } from 'child_process';

router.post('/generate', async (req, res) => {
  exec('python /path/to/weekly-report-generator/src/main.py', (error, stdout) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    res.json({ success: true, output: stdout });
  });
});
```

**方式 B：直接嵌入 HTML 報告**

```typescript
// 前端顯示生成的 HTML 報告
<iframe src="/api/reports/latest" width="100%" height="800px" />
```

---

## 🔧 自訂設定

### 1. 修改圖表樣式

編輯 `config/chart_config.py`：

```python
# 更改主題
CHART_THEME = ThemeType.WONDERLAND  # 或其他主題

# 更改顏色配置
COLOR_PALETTE = {
    'primary': '#您的品牌色',
    # ...
}
```

### 2. 調整 SQL 查詢

編輯 `src/data_fetcher.py` 中的查詢邏輯，根據實際資料表結構調整。

### 3. 自訂 HTML 模板

編輯 `templates/report_template.html`，調整報告的視覺設計。

---

## 📊 輸出格式

生成的報告會儲存在 `output/` 目錄：

```
output/
├── weekly_report_20250127_143022.html
├── weekly_report_20250128_090000.html
└── ...
```

報告檔案命名規則：`weekly_report_{YYYYMMDD}_{HHMMSS}.html`

---

## 🐛 常見問題

### Q1: BigQuery 認證失敗

**錯誤訊息**：
```
google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials
```

**解決方案**：
1. 確認已設定 `GOOGLE_APPLICATION_CREDENTIALS` 環境變數
2. 或執行 `gcloud auth application-default login`

### Q2: 模組導入錯誤

**錯誤訊息**：
```
ModuleNotFoundError: No module named 'config'
```

**解決方案**：
1. 確認在專案根目錄執行
2. 或在 Python 路徑中加入專案根目錄

### Q3: 圖表無法顯示

**可能原因**：
1. PyEcharts 版本不相容
2. HTML 模板中的 JavaScript 未正確載入

**解決方案**：
```bash
pip install --upgrade pyecharts
```

---

## 📚 參考資源

- [PyEcharts 官方文檔](https://pyecharts.org/)
- [BigQuery Python Client 文檔](https://cloud.google.com/bigquery/docs/reference/libraries)
- [Jinja2 模板語法](https://jinja.palletsprojects.com/)

---

## ✅ 檢查清單

整合前請確認：

- [ ] Python 3.8+ 已安裝
- [ ] 所有依賴套件已安裝（`pip install -r requirements.txt`）
- [ ] BigQuery 認證已設定
- [ ] `.env` 檔案已配置
- [ ] BigQuery 連線測試通過
- [ ] 可以成功執行 `python src/main.py`
- [ ] 報告檔案已生成在 `output/` 目錄

---

**下一步**：完成整合後，可以開始調整 SQL 查詢邏輯，確保資料正確性。

