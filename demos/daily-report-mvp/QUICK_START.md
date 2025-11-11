# 快速開始指南（新電腦設定）

**建立日期**：2025-01-27  
**目的**：快速在新電腦上設定環境並開始使用

---

## ⚡ 5 分鐘快速設定

### 步驟 1：安裝依賴（2 分鐘）

```bash
# 進入專案目錄
cd /Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp

# 建立虛擬環境（可選）
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 步驟 2：設定 Google Cloud 認證（1 分鐘）

```bash
# 登入 Google Cloud
gcloud auth application-default login

# 設定專案
gcloud config set project datalake360-saintpaul
gcloud auth application-default set-quota-project datalake360-saintpaul
```

### 步驟 3：建立客戶設定檔（1 分鐘）

```bash
# 複製範例檔案
cp config/clients.yaml.example config/clients.yaml

# 編輯設定檔（填入 Google Chat Webhook URL）
# 可以使用任何編輯器開啟 config/clients.yaml
```

### 步驟 4：測試執行（1 分鐘）

```bash
# 測試連線和設定
python main.py --client client_A --dry-run
```

---

## ✅ 驗證清單

執行以下命令確認設定正確：

```bash
# 1. 測試 BigQuery 連線
python -c "from google.cloud import bigquery; client = bigquery.Client(project='datalake360-saintpaul'); print('✅ BigQuery 連線成功')"

# 2. 測試客戶設定檔
python -c "from src.config.client_config import ClientConfig; config = ClientConfig(); print(f'✅ 客戶設定：{config.list_clients()}')"

# 3. 測試資料查詢（乾跑模式）
python main.py --client client_A --dry-run
```

---

## 📋 必須設定的項目

### 1. Google Chat Webhook URL

在 `config/clients.yaml` 中填入：
```yaml
google_chat_webhook: "https://chat.googleapis.com/v1/spaces/..."
```

### 2. 廣告資料（可選）

如果沒有廣告資料，系統會顯示 "N/A（資料待匯入）"。

如果需要手動輸入：
```yaml
ad_data:
  manual_ad_spend:
    "2025-11-04":
      meta_ads: 2199
      google_ads: 4587
```

---

## 🚀 設定自動排程

### macOS（推薦）

```bash
./scripts/setup_launchagent.sh
```

執行時間：每天早上 09:00

---

## 📚 詳細文檔

- [完整交接文件](./docs/HANDOVER_DOCUMENT.md) - 詳細設定說明
- [排程設定指南](./docs/SCHEDULING_GUIDE.md) - 各種排程方案
- [資料存儲說明](./docs/DATA_STORAGE.md) - 資料來源位置

---

## 🆘 遇到問題？

查看 [交接文件](./docs/HANDOVER_DOCUMENT.md) 的「常見問題」章節。

---

**最後更新**：2025-01-27

