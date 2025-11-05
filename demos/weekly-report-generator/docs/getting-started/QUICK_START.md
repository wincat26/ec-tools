# 快速開始指南

**適用對象**：新接手的開發者

---

## 🚀 5 分鐘快速上手

### 1. 環境準備

```bash
# 進入專案目錄
cd weekly-report-generator

# 安裝依賴（如果還沒安裝）
pip install -r requirements.txt
```

### 2. 設定 Google Cloud 認證

```bash
# 設定預設專案
gcloud config set project datalake360-saintpaul

# 登入認證
gcloud auth application-default login

# 設定 quota project（避免權限警告）
gcloud auth application-default set-quota-project datalake360-saintpaul
```

### 3. 測試連線

```bash
# 測試 BigQuery 連線是否正常
python test_connection.py
```

**預期輸出**：
```
✅ BigQuery 連線成功！
✅ 專案 ID: datalake360-saintpaul
✅ 資料集: datalake_stpl
```

### 4. 生成週報

```bash
# 執行主程式
python src/main.py
```

**預期輸出**：
```
============================================================
電商週報生成器 - 開始執行
============================================================

📊 查詢參數：
   - 時間範圍：本週（2025-11-04 至 2025-11-10）
   - 品牌名稱：豆油伯
   ...

✅ 週報生成完成！
📁 報告檔案位置：/path/to/output/weekly_report_20251105_112000.html
```

### 5. 查看報告

開啟 `output/` 目錄中的 HTML 檔案，在瀏覽器中查看。

---

## 🔍 測試查詢功能

```bash
# 測試所有查詢功能
python test_queries.py
```

**預期輸出**：
```
============================================================
測試資料查詢功能
============================================================

📊 測試 1: GMV 基本指標（最近 7 天）
   ✅ 成交營收: NT$ 518,919
   ✅ 總營業額: NT$ 518,919
   ...

📈 測試 2: 本週關鍵摘要（與上週比較）
   ✅ 本週營收: NT$ 518,919
   ✅ 上週營收: NT$ 494,151
   ✅ 營收變化: +5.01%
   ...
```

---

## 🛠️ 常見問題快速解決

### 問題 1：找不到 gcloud 命令

**解決方案**：
```bash
# macOS
brew install google-cloud-sdk

# 或參考官方文件安裝
```

### 問題 2：認證失敗

**解決方案**：
```bash
# 重新登入
gcloud auth application-default login

# 確認專案設定
gcloud config get-value project
```

### 問題 3：查詢失敗（位置錯誤）

**解決方案**：
- 檢查 `config/bigquery_config.py`，確認沒有明確指定 `location`
- 讓 BigQuery 自動偵測位置

### 問題 4：缺少 db-dtypes 套件

**解決方案**：
```bash
pip install db-dtypes
```

---

## 📖 下一步

1. 閱讀 **HANDOVER_DOCUMENT.md** 了解完整架構
2. 查看 **程式碼註解** 了解每個函數的用途
3. 執行 **測試腳本** 驗證功能
4. 嘗試修改 **配置** 熟悉專案

---

**需要更多資訊？** 請參考 `HANDOVER_DOCUMENT.md`

