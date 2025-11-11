# 新電腦設定檢查清單

**建立日期**：2025-01-27  
**用途**：確保在新電腦上能順利設定並運作

---

## ✅ 安裝與設定

### 1. 環境準備
- [ ] Python 3.8+ 已安裝
- [ ] Google Cloud SDK (`gcloud`) 已安裝
- [ ] 專案已複製到新電腦

### 2. Python 環境設定
- [ ] 建立虛擬環境（可選但建議）
- [ ] 安裝依賴：`pip install -r requirements.txt`
- [ ] 確認所有套件安裝成功

### 3. Google Cloud 認證
- [ ] 執行 `gcloud auth application-default login`
- [ ] 設定專案：`gcloud config set project datalake360-saintpaul`
- [ ] 設定 quota project：`gcloud auth application-default set-quota-project datalake360-saintpaul`
- [ ] 測試 BigQuery 連線

### 4. 配置檔案
- [ ] 複製 `config/clients.yaml.example` 為 `config/clients.yaml`
- [ ] 填入 Google Chat Webhook URL
- [ ] 確認 BigQuery 設定（如果與預設不同）
- [ ] 確認月份目標設定（`config/targets.yaml`）

---

## 🧪 測試驗證

### 1. 連線測試
- [ ] BigQuery 連線測試成功
- [ ] 客戶設定檔載入測試成功
- [ ] 目標設定檔載入測試成功

### 2. 功能測試
- [ ] 資料查詢測試（乾跑模式）
- [ ] 廣告資料顯示測試（有資料 / 無資料）
- [ ] Google Chat 推播測試

### 3. 排程測試
- [ ] LaunchAgent / crontab 設定完成
- [ ] 手動觸發執行測試成功
- [ ] 確認日誌檔案正常產生

---

## 📋 必須確認的資訊

### Google Cloud
- [ ] 專案 ID：`datalake360-saintpaul`
- [ ] 資料集：`datalake_stpl`、`analytics_304437305`
- [ ] 認證狀態：已設定 Application Default Credentials

### Google Chat
- [ ] Webhook URL：已填入 `config/clients.yaml`
- [ ] Webhook 測試：發送測試訊息成功

### 客戶設定
- [ ] 客戶 ID：`client_A`（或您的客戶 ID）
- [ ] 每月營收目標：已設定
- [ ] 廣告資料：已設定（或留空顯示 N/A）

---

## 🔧 排程設定

### macOS
- [ ] LaunchAgent 已設定：`./scripts/setup_launchagent.sh`
- [ ] 執行時間：每天早上 09:00
- [ ] 日誌位置：`logs/launchd.log`

### Linux
- [ ] crontab 已設定：`./scripts/setup_crontab.sh`
- [ ] 執行時間：每天早上 09:00
- [ ] 日誌位置：`logs/cron.log`

### Windows
- [ ] 工作排程器已設定
- [ ] 執行腳本：`scripts/run_daily_report.bat`
- [ ] 執行時間：每天早上 09:00

---

## 📝 重要檔案確認

### 必須存在的檔案
- [ ] `config/clients.yaml` - 客戶設定檔（必須建立）
- [ ] `config/targets.yaml` - 月份目標設定檔（已存在）
- [ ] `config/bigquery.py` - BigQuery 連線設定（已存在）

### 日誌檔案（自動建立）
- [ ] `logs/` 目錄已建立
- [ ] 日誌檔案可正常寫入

---

## 🎯 驗證命令

### 快速驗證腳本

```bash
# 1. 測試 BigQuery 連線
python -c "from google.cloud import bigquery; client = bigquery.Client(project='datalake360-saintpaul'); print('✅ BigQuery 連線成功')"

# 2. 測試客戶設定檔
python -c "from src.config.client_config import ClientConfig; config = ClientConfig(); print(f'✅ 客戶設定：{config.list_clients()}')"

# 3. 測試目標設定檔
python -c "from src.config.target_config import TargetConfig; config = TargetConfig(); print(f'✅ 目標設定檔載入成功，包含 {len(config.list_all_targets())} 個月份目標')"

# 4. 測試資料查詢（乾跑模式）
python main.py --client client_A --dry-run
```

---

## 🆘 常見問題快速檢查

### 問題 1：BigQuery 連線失敗
- [ ] 確認已執行 `gcloud auth application-default login`
- [ ] 確認已設定 quota project
- [ ] 確認專案 ID 正確

### 問題 2：找不到客戶設定檔
- [ ] 確認 `config/clients.yaml` 存在
- [ ] 確認檔案格式正確（YAML 語法）

### 問題 3：排程未執行
- [ ] 確認 LaunchAgent / crontab 已載入
- [ ] 檢查日誌檔案是否有錯誤
- [ ] 確認執行時間設定正確

---

## ✅ 完成確認

所有項目完成後，系統應該能夠：
- ✅ 每天早上 09:00 自動執行
- ✅ 查詢 BigQuery 資料
- ✅ 生成日報並推送到 Google Chat
- ✅ 記錄執行日誌

---

**最後更新**：2025-01-27

