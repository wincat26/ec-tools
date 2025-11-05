# BigQuery 認證設定指南

**目的**：設定 Google Cloud 認證，讓 Python 腳本可以存取 BigQuery

---

## 🔐 兩種認證方式

### 方式 A：Application Default Credentials（推薦，適合開發環境）

**優點**：設定簡單，不需要管理 JSON 檔案  
**適用**：本地開發、測試

#### 步驟 1：安裝 Google Cloud SDK（如果還沒安裝）

```bash
# macOS
brew install google-cloud-sdk

# 或下載安裝檔
# https://cloud.google.com/sdk/docs/install
```

#### 步驟 2：登入 Google Cloud

```bash
gcloud auth application-default login
```

這會開啟瀏覽器，讓您登入 Google 帳號並授權。

#### 步驟 3：設定預設專案（可選）

```bash
gcloud config set project saintpaul-data
```

#### 步驟 4：測試連線

```bash
cd weekly-report-generator
python test_connection.py
```

---

### 方式 B：服務帳號金鑰檔案（推薦，適合生產環境）

**優點**：更安全，適合自動化腳本、CI/CD  
**適用**：生產環境、伺服器部署

#### 步驟 1：建立服務帳號（在 Google Cloud Console）

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 選擇專案：`saintpaul-data`
3. 導航至：**IAM & Admin** → **Service Accounts**
4. 點擊 **Create Service Account**
5. 輸入服務帳號名稱（例如：`weekly-report-generator`）
6. 點擊 **Create and Continue**

#### 步驟 2：授予權限

1. 在 **Grant this service account access to project** 中：
   - 選擇角色：**BigQuery Data Viewer** 和 **BigQuery Job User**
2. 點擊 **Continue** → **Done**

#### 步驟 3：建立金鑰

1. 找到剛建立的服務帳號，點擊進入
2. 切換到 **Keys** 標籤
3. 點擊 **Add Key** → **Create new key**
4. 選擇 **JSON** 格式
5. 下載 JSON 檔案（**請妥善保管，不要提交到 Git**）

#### 步驟 4：設定環境變數

```bash
# 設定環境變數（臨時，僅限當前終端）
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

# 或加入 ~/.zshrc 或 ~/.bash_profile（永久）
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"' >> ~/.zshrc
source ~/.zshrc
```

#### 步驟 5：測試連線

```bash
cd weekly-report-generator
python test_connection.py
```

---

## 🔍 驗證認證是否成功

執行測試腳本：

```bash
python test_connection.py
```

**成功輸出應該類似**：
```
============================================================
BigQuery 連線測試
============================================================

✅ BigQuery 客戶端初始化成功
   - 專案 ID: saintpaul-data
   - 資料集: saintpaul_data

🔍 測試查詢資料表...
   ✅ orders_summary_daily (orders_summary_daily): 1,234 筆記錄
   ✅ orders (orders): 5,678 筆記錄
   ...

============================================================
✅ 連線測試完成！
============================================================
```

---

## ⚠️ 常見問題

### Q1: `gcloud: command not found`

**解決方案**：
- 安裝 Google Cloud SDK（見上方步驟 1）
- 或使用方式 B（服務帳號金鑰）

### Q2: `Permission denied` 或 `Access Denied`

**可能原因**：
- 服務帳號沒有 BigQuery 讀取權限
- 專案 ID 設定錯誤

**解決方案**：
1. 確認服務帳號有 **BigQuery Data Viewer** 角色
2. 確認 `GOOGLE_CLOUD_PROJECT` 環境變數或 `.env` 檔案中的專案 ID 正確

### Q3: `Your default credentials were not found`

**解決方案**：
- 執行 `gcloud auth application-default login`
- 或設定 `GOOGLE_APPLICATION_CREDENTIALS` 環境變數

---

## 📝 快速檢查清單

- [ ] Google Cloud SDK 已安裝（方式 A）或服務帳號已建立（方式 B）
- [ ] 已執行 `gcloud auth application-default login`（方式 A）
- [ ] 已設定 `GOOGLE_APPLICATION_CREDENTIALS` 環境變數（方式 B）
- [ ] 服務帳號有 BigQuery 讀取權限
- [ ] `test_connection.py` 執行成功

---

## 🎯 下一步

認證設定完成後，可以開始：

1. **調整 SQL 查詢**：根據實際資料表結構修改 `src/data_fetcher.py`
2. **執行週報生成**：`python src/main.py`
3. **查看生成的報告**：在 `output/` 目錄中找到 HTML 檔案

---

**需要協助？** 請確認：
- 您使用的是方式 A 還是方式 B？
- 是否有 Google Cloud 專案的存取權限？
- 專案 ID 是什麼？（應該是 `saintpaul-data`）

