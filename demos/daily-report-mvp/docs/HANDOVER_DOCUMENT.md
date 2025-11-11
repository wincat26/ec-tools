# 每日數據彙整日報 - 交接文件

**建立日期**：2025-01-27  
**版本**：v1.1 (MVP)  
**狀態**：開發完成，可正常運作

---

## 📋 專案概述

### 專案名稱
每日數據彙整日報 - MVP v1.1

### 專案目標
驗證「Data (數據彙整)」的價值，自動彙整 E-com 和 GA4 數據，透過 Google Chat 每日推播，節省客戶手動撈取報表的時間。

### 當前狀態
- ✅ **核心功能完成**：100%
- ✅ **測試完成**：已測試實際資料查詢和推播
- ✅ **排程設定**：已設定每天早上 09:00 自動執行

---

## 🚀 快速開始（新電腦設定）

### 1. 環境需求

- Python 3.8+
- Google Cloud SDK (`gcloud`)
- Google Cloud 認證（Application Default Credentials）
- BigQuery 資料存取權限

### 2. 安裝步驟

#### 步驟 1：複製專案

```bash
# 專案位置
cd /Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp
```

#### 步驟 2：安裝 Python 依賴

```bash
# 建議使用虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt
```

#### 步驟 3：設定 Google Cloud 認證

```bash
# 登入 Google Cloud
gcloud auth application-default login

# 設定預設專案
gcloud config set project datalake360-saintpaul

# 設定 quota project（重要！）
gcloud auth application-default set-quota-project datalake360-saintpaul
```

#### 步驟 4：建立客戶設定檔

```bash
# 複製範例設定檔
cp config/clients.yaml.example config/clients.yaml

# 編輯設定檔，填入實際值
# 需要填寫：
# 1. BigQuery 資料集設定（如果與預設不同）
# 2. Google Chat Webhook URL
# 3. 每月營收目標
# 4. 廣告資料（手動輸入，或留空顯示 N/A）
```

#### 步驟 5：測試連線

```bash
# 測試 BigQuery 連線
python -c "from google.cloud import bigquery; client = bigquery.Client(project='datalake360-saintpaul'); print('✅ BigQuery 連線成功！')"

# 測試客戶設定檔
python -c "from src.config.client_config import ClientConfig; config = ClientConfig(); print(f'✅ 客戶設定載入成功：{config.list_clients()}')"
```

---

## 📁 專案結構

```
daily-report-mvp/
├── config/                      # 配置檔案
│   ├── bigquery.py              # BigQuery 連線設定
│   ├── clients.yaml             # 客戶設定檔（需建立）
│   ├── clients.yaml.example     # 客戶設定檔範例
│   └── targets.yaml             # 月份目標設定檔
├── src/                         # 核心程式碼
│   ├── config/                  # 配置讀取模組
│   │   ├── client_config.py     # 客戶設定檔讀取
│   │   └── target_config.py   # 目標設定檔讀取
│   ├── data/                    # 資料查詢模組
│   │   ├── fetcher.py          # BigQuery 查詢
│   │   └── validator.py         # GA4 數據驗證
│   ├── generator/               # 資料生成模組
│   │   └── daily_aggregation.py # 生成單行 JSON
│   ├── notification/            # 推播模組
│   │   └── google_chat.py      # Google Chat Webhook
│   └── utils/                   # 工具函數
│       └── date_utils.py        # 日期工具
├── scripts/                     # 執行腳本
│   ├── run_daily_report.sh      # 執行腳本（macOS/Linux）
│   ├── run_daily_report.bat    # 執行腳本（Windows）
│   ├── setup_crontab.sh         # crontab 設定腳本
│   ├── setup_launchagent.sh    # LaunchAgent 設定腳本
│   └── check_data_storage.py   # 檢查資料存儲位置
├── docs/                        # 文檔
│   ├── HANDOVER_DOCUMENT.md     # 本文件
│   ├── SCHEDULING_GUIDE.md      # 排程設定指南
│   ├── DATA_STORAGE.md          # 資料存儲說明
│   ├── MCP_INTEGRATION_PLAN.md  # MCP 整合規劃
│   └── ...                      # 其他文檔
├── logs/                        # 日誌檔案（自動建立）
├── main.py                      # 主程式入口
├── requirements.txt             # Python 依賴
└── README.md                    # 專案說明
```

---

## ⚙️ 配置說明

### 1. 客戶設定檔 (`config/clients.yaml`)

**必填項目**：
- `client_id`：客戶 ID
- `bigquery.project_id`：BigQuery 專案 ID
- `bigquery.dataset_id`：E-com 資料集 ID
- `bigquery.ga4_dataset`：GA4 資料集 ID
- `monthly_target_revenue`：每月營收目標（後備值）
- `google_chat_webhook`：Google Chat Webhook URL

**選填項目**：
- `ad_data.manual_ad_spend`：手動輸入的廣告資料（如果沒有，顯示 N/A）

**範例**：
```yaml
clients:
  - client_id: "client_A"
    bigquery:
      project_id: "datalake360-saintpaul"
      dataset_id: "datalake_stpl"
      ga4_dataset: "analytics_304437305"
    monthly_target_revenue: 2000000
    google_chat_webhook: "https://chat.googleapis.com/v1/spaces/..."
    ad_data:
      manual_ad_spend:
        "2025-11-04":
          meta_ads: 2199
          google_ads: 4587
```

### 2. 月份目標設定檔 (`config/targets.yaml`)

**用途**：支援不同月份有不同的目標

**格式**：
```yaml
targets:
  "2025-10": 1900000
  "2025-11": 2000000
  "2025-12": 3100000
  # ... 更多月份
```

**優先順序**：
1. 優先使用 `targets.yaml` 中的月份目標
2. 如果找不到，使用 `clients.yaml` 中的 `monthly_target_revenue`

---

## 🔄 執行方式

### 手動執行

```bash
# 基本執行（使用昨日資料）
python main.py --client client_A

# 指定日期
python main.py --client client_A --date 2025-11-04

# 乾跑模式（測試，不發送推播）
python main.py --client client_A --dry-run

# 跳過 GA4 驗證（僅用於測試）
python main.py --client client_A --skip-validation
```

### 自動排程（macOS - LaunchAgent）

**設定排程**：
```bash
./scripts/setup_launchagent.sh
```

**執行時間**：每天早上 09:00

**管理命令**：
```bash
# 查看狀態
launchctl list | grep daily-report

# 立即執行（測試）
launchctl start com.daily-report

# 查看日誌
tail -f logs/launchd.log

# 卸載服務
launchctl unload ~/Library/LaunchAgents/com.daily-report.plist
```

---

## 📊 資料來源

### BigQuery 資料存儲

**專案 ID**：`datalake360-saintpaul`

**主要資料集**：
- `datalake_stpl`：E-com 訂單資料（24 個表）
  - 使用表：`lv1_order_master`
- `analytics_304437305`：GA4 事件資料（1,421 個日期分區表）
  - 使用表：`events_*`（格式：`events_YYYYMMDD`）

**查詢位置**：
- `src/data/fetcher.py` - 所有資料查詢邏輯

### 廣告資料

**當前狀態**：手動輸入到 `config/clients.yaml`

**未來規劃**：使用 MCP 從 Meta Ads 和 Google Ads API 自動取得

---

## 🧪 測試與驗證

### 測試步驟

1. **測試 BigQuery 連線**
   ```bash
   python -c "from google.cloud import bigquery; client = bigquery.Client(project='datalake360-saintpaul'); print('✅ 連線成功')"
   ```

2. **測試客戶設定檔**
   ```bash
   python -c "from src.config.client_config import ClientConfig; config = ClientConfig(); print(config.list_clients())"
   ```

3. **測試資料查詢（乾跑模式）**
   ```bash
   python main.py --client client_A --dry-run
   ```

4. **測試實際推播**
   ```bash
   python main.py --client client_A --date 2025-11-04
   ```

### 檢查資料存儲位置

```bash
python scripts/check_data_storage.py
```

---

## 🐛 常見問題

### 問題 1：BigQuery 連線失敗

**錯誤訊息**：`ProjectId must be non-empty` 或 `USER_PROJECT_DENIED`

**解決方案**：
```bash
# 確認已設定認證
gcloud auth application-default login

# 設定 quota project
gcloud auth application-default set-quota-project datalake360-saintpaul

# 確認專案設定
gcloud config get-value project
```

### 問題 2：找不到客戶設定檔

**錯誤訊息**：`FileNotFoundError: 客戶設定檔不存在`

**解決方案**：
```bash
cp config/clients.yaml.example config/clients.yaml
# 然後編輯 config/clients.yaml 填入實際值
```

### 問題 3：GA4 數據驗證失敗

**錯誤訊息**：`GA4 數據延遲：report_date (...) 的 GA4 sessions 數據尚未匯入`

**解決方案**：
1. 確認 GA4 數據是否已匯入 BigQuery
2. 檢查資料集名稱是否正確
3. 如果數據確實延遲，使用 `--skip-validation` 跳過驗證（僅用於測試）

### 問題 4：Google Chat 推播失敗

**錯誤訊息**：`推播失敗：HTTP 400`

**解決方案**：
1. 確認 Webhook URL 正確
2. 確認 Webhook 未過期
3. 檢查 Google Chat 空間設定

### 問題 5：廣告資料顯示為 N/A

**原因**：沒有在 `clients.yaml` 中設定廣告資料

**解決方案**：
- 手動輸入：在 `clients.yaml` 中加入 `ad_data.manual_ad_spend`
- 或等待未來 MCP 整合自動取得

---

## 📝 重要檔案清單

### 必須建立的檔案
- `config/clients.yaml` - 客戶設定檔（從 `clients.yaml.example` 複製）

### 已存在的設定檔
- `config/targets.yaml` - 月份目標設定檔（已建立）
- `config/bigquery.py` - BigQuery 連線設定（已建立）

### 日誌檔案
- `logs/cron.log` - crontab 執行日誌（自動建立）
- `logs/launchd.log` - LaunchAgent 執行日誌（自動建立）
- `logs/launchd_error.log` - LaunchAgent 錯誤日誌（自動建立）

---

## 🔐 安全注意事項

### 敏感資訊

以下檔案包含敏感資訊，**不應提交到 Git**：
- `config/clients.yaml` - 包含 Google Chat Webhook URL
- `.env` - 環境變數（如果使用）

**`.gitignore` 已設定**：
```
config/clients.yaml
.env
```

### 認證資訊

- Google Cloud 認證：使用 Application Default Credentials
- 認證檔案位置：`~/.config/gcloud/application_default_credentials.json`
- 不要提交認證檔案到 Git

---

## 📚 相關文檔

### 核心文檔
- [README.md](../README.md) - 專案總覽
- [排程設定指南](./SCHEDULING_GUIDE.md) - 詳細排程設定說明
- [資料存儲說明](./DATA_STORAGE.md) - 資料來源和存儲位置
- [MCP 整合規劃](./MCP_INTEGRATION_PLAN.md) - 未來廣告資料自動化

### 技術文檔
- [Google Chat 模板設計](./GOOGLE_CHAT_TEMPLATE.md) - 卡片模板說明
- [模板總結](./TEMPLATE_SUMMARY.md) - 模板設計總結
- [實際資料查詢分析](./ACTUAL_DATA_QUERY_SUMMARY.md) - 查詢結果分析

---

## 🎯 功能清單

### ✅ 已完成功能

- [x] BigQuery 資料查詢（E-com + GA4）
- [x] GA4 數據驗證（前置檢查）
- [x] 週變化分析（營收、CVR、Sessions、AOV）
- [x] 月迄今指標（MTD 營收、達成率、預估營收）
- [x] 動態月份目標（支援不同月份不同目標）
- [x] 廣告資料支援（手動輸入，未來 MCP 自動化）
- [x] Google Chat 推播（完整卡片模板）
- [x] 營收公式拆解顯示（Sessions × CVR × AOV）
- [x] 自動排程（LaunchAgent，每天早上 09:00）
- [x] 錯誤處理和日誌記錄

### ⏳ 待實作功能

- [ ] MCP 整合（Meta Ads、Google Ads API）
- [ ] BigQuery 廣告資料表查詢
- [ ] AI 洞察生成（未來擴充）
- [ ] LINE 推播支援（未來擴充）

---

## 🔄 資料流程

```
1. 每天早上 09:00 觸發
   ↓
2. 讀取客戶設定檔
   ↓
3. GA4 數據驗證（前置檢查）
   ↓
4. 查詢 BigQuery 資料
   ├─ E-com 訂單資料（營收、訂單、AOV）
   ├─ GA4 事件資料（Sessions、CVR）
   └─ 廣告資料（手動輸入或 MCP）
   ↓
5. 計算週變化（vs. 上週同期）
   ↓
6. 計算月迄今指標（MTD、達成率）
   ↓
7. 生成單行 JSON 資料
   ↓
8. 套入 Google Chat 卡片模板
   ↓
9. 發送到 Google Chat
   ↓
10. 記錄執行日誌
```

---

## 📊 測試結果

### 最後測試日期：2025-11-04

**測試結果**：
- ✅ BigQuery 連線：成功
- ✅ 資料查詢：成功
  - 營收：$50,102
  - 訂單：37 筆
  - CVR：1.56%
  - Sessions：2,372
  - 廣告花費：$6,786
  - ROAS：7.38x
- ✅ Google Chat 推播：成功

---

## 🛠️ 開發環境設定

### Python 環境

```bash
# 建議使用虛擬環境
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 依賴套件

- `google-cloud-bigquery>=3.11.0` - BigQuery 查詢
- `requests>=2.31.0` - HTTP 請求（Google Chat Webhook）
- `pyyaml>=6.0` - YAML 設定檔讀取
- `python-dotenv>=1.0.0` - 環境變數管理
- `python-dateutil>=2.8.2` - 日期處理

---

## 📞 聯絡資訊

### 專案相關
- **專案位置**：`demos/daily-report-mvp/`
- **文檔位置**：`docs/`
- **執行腳本**：`scripts/`

### 技術支援
- 查看日誌：`logs/launchd.log` 或 `logs/cron.log`
- 檢查設定：`config/clients.yaml`
- 測試連線：使用 `scripts/check_data_storage.py`

---

## ✅ 交接檢查清單

### 環境設定
- [ ] Python 3.8+ 已安裝
- [ ] Google Cloud SDK 已安裝
- [ ] Google Cloud 認證已設定
- [ ] 專案依賴已安裝

### 配置檔案
- [ ] `config/clients.yaml` 已建立並填入正確值
- [ ] `config/targets.yaml` 已確認（月份目標）
- [ ] Google Chat Webhook URL 已設定

### 測試驗證
- [ ] BigQuery 連線測試成功
- [ ] 客戶設定檔載入成功
- [ ] 資料查詢測試成功（乾跑模式）
- [ ] 實際推播測試成功

### 排程設定
- [ ] LaunchAgent 已設定（macOS）
- [ ] 或 crontab 已設定（Linux）
- [ ] 或工作排程器已設定（Windows）
- [ ] 排程執行時間確認（09:00）

---

## 🎯 下一步建議

1. **測試完整流程**：在新電腦上執行一次完整測試
2. **確認排程設定**：確認自動排程正常運作
3. **監控日誌**：檢查前幾天的執行日誌，確認一切正常
4. **MCP 整合準備**：開始規劃 MCP 整合實作

---

**最後更新**：2025-01-27  
**交接完成**：✅

