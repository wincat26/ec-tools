# 故障排除指南

## 🔍 當前狀態

✅ **連線成功**：BigQuery 客戶端已成功初始化  
⚠️ **權限問題**：出現 "Project not found or deleted" 或 "USER_PROJECT_DENIED" 錯誤

---

## 📋 可能的原因

### 1. 專案名稱不正確

**錯誤訊息**：`Project 'projects/saintpaul-data' not found or deleted`

**解決方案**：
1. 確認實際的 Google Cloud 專案 ID
2. 檢查專案是否存在且有權限存取

**檢查方式**：
```bash
# 列出所有可用的專案
gcloud projects list

# 檢查當前設定的專案
gcloud config get-value project
```

### 2. 專案權限不足

**錯誤訊息**：`USER_PROJECT_DENIED`

**解決方案**：
1. 確認您的 Google 帳號有該專案的存取權限
2. 確認已正確登入：
   ```bash
   gcloud auth list
   ```

### 3. BigQuery API 未啟用

**解決方案**：
```bash
# 啟用 BigQuery API
gcloud services enable bigquery.googleapis.com --project=saintpaul-data
```

---

## 🛠️ 檢查步驟

### 步驟 1：確認專案 ID

```bash
gcloud projects list
```

找到正確的專案 ID，然後更新設定：

```bash
# 方式 A：使用環境變數
export GOOGLE_CLOUD_PROJECT="正確的專案ID"

# 方式 B：使用 .env 檔案
echo "GOOGLE_CLOUD_PROJECT=正確的專案ID" >> .env
```

### 步驟 2：確認權限

```bash
# 檢查當前登入的帳號
gcloud auth list

# 檢查專案權限
gcloud projects get-iam-policy saintpaul-data
```

### 步驟 3：確認資料集存在

```bash
# 列出 BigQuery 資料集
bq ls --project_id=saintpaul-data

# 或使用 Python
python -c "from google.cloud import bigquery; client = bigquery.Client(project='saintpaul-data'); datasets = list(client.list_datasets()); print([d.dataset_id for d in datasets])"
```

---

## 💡 下一步建議

1. **確認專案 ID**：請提供正確的 Google Cloud 專案 ID
2. **確認資料集**：確認 `saintpaul_data` 資料集是否存在
3. **確認權限**：確認您有 BigQuery 讀取權限

---

## 📝 修正後的設定

如果找到正確的專案 ID，請更新：

1. **環境變數**：
   ```bash
   export GOOGLE_CLOUD_PROJECT="正確的專案ID"
   ```

2. **或修改 config/bigquery_config.py**：
   ```python
   self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', '正確的專案ID')
   ```

3. **重新測試**：
   ```bash
   python test_connection.py
   ```

---

**需要協助？** 請提供：
- 正確的 Google Cloud 專案 ID
- 資料集名稱（可能不是 `saintpaul_data`）
- 您使用的 Google 帳號

