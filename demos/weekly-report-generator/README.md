# 電商週報生成器

**專案說明**：使用 Python + PyEcharts 自動生成電商週報，整合 BigQuery 資料與 GA4 流量分析。

---

## 🚀 快速開始

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 設定 Google Cloud 認證
gcloud auth application-default login
gcloud auth application-default set-quota-project datalake360-saintpaul

# 3. 生成週報
python src/main.py
```

**詳細說明**：請參考 [快速開始指南](QUICK_START.md)

---

## 📚 文件索引

### 🎯 必讀文件（新接手請先看這些）

1. **[🚀 快速開始指南](QUICK_START.md)** - 5 分鐘快速上手
   - 環境準備、認證設定、測試連線、生成週報

2. **[📖 完整交接文件](HANDOVER_DOCUMENT.md)** - **最重要！必讀！**
   - 專案概述、系統架構、技術棧、核心功能模組
   - 資料庫配置、關鍵邏輯說明、常見問題排錯
   - 待辦事項、快速開始指南

3. **[💻 程式碼結構說明](CODE_STRUCTURE.md)** - 每個檔案的詳細說明
   - 檔案結構總覽、每個模組的功能
   - 關鍵函數詳解、資料流程、設計決策

### 📋 技術文件

4. **[🔐 認證設定指南](AUTHENTICATION_SETUP.md)** - Google Cloud 認證設定
   - `gcloud CLI` 安裝與設定
   - Application Default Credentials 設定
   - Service Account 設定（替代方案）

5. **[🗄️ 資料庫結構說明](DATABASE_SCHEMA.md)** - BigQuery 資料表結構
   - 資料集說明、關鍵資料表、欄位說明

6. **[📊 SQL 查詢更新記錄](SQL_QUERY_UPDATE.md)** - SQL 查詢邏輯更新
   - 資料表對應更新、主要變更、查詢範例

7. **[🌐 流量分類規則](TRAFFIC_CLASSIFICATION.md)** - 8 種流量來源分類
   - 分類規則、SQL 實作、Python 函式

8. **[📈 流量分析實作](TRAFFIC_ANALYSIS_IMPLEMENTATION.md)** - 流量分析詳細說明
   - 資料整合流程、JOIN 邏輯、查詢範例

9. **[🔗 Transaction ID 驗證](TRANSACTION_ID_VERIFICATION.md)** - Transaction ID 格式驗證
   - 格式驗證結果、JOIN 邏輯確認

### 📝 其他文件

10. **[⚙️ 配置總結](CONFIGURATION_SUMMARY.md)** - BigQuery 配置總結
11. **[📋 資料需求](DATA_REQUIREMENTS.md)** - 資料需求規格
12. **[📝 更新日誌](CHANGELOG.md)** - 版本更新記錄
13. **[✅ 完成總結](FINAL_SUMMARY.md)** - 專案完成總結

---

## 🏗️ 專案結構

```
weekly-report-generator/
├── README.md                    # 本文件（專案說明）
├── QUICK_START.md              # 快速開始指南
├── HANDOVER_DOCUMENT.md        # 完整交接文件（必讀）
├── CODE_STRUCTURE.md           # 程式碼結構說明
├── requirements.txt            # Python 依賴套件
├── config/                     # 配置模組
│   ├── bigquery_config.py      # BigQuery 連線設定
│   └── chart_config.py         # 圖表樣式設定
├── src/                        # 核心程式碼
│   ├── main.py                 # 主程式入口
│   ├── data_fetcher.py         # BigQuery 資料查詢
│   ├── traffic_classifier.py   # 流量來源分類
│   ├── chart_generator.py      # PyEcharts 圖表生成
│   ├── ai_summary.py           # AI 摘要生成
│   ├── report_builder.py       # HTML 報告組合
│   └── utils.py                # 工具函數
├── templates/                  # HTML 模板
│   └── report_template.html    # 週報 HTML 模板
└── output/                     # 輸出目錄
    └── weekly_report_*.html    # 生成的週報檔案
```

---

## ⚙️ 核心功能

1. **GMV 基本指標**：成交總額、總營業額、交易會員數、訂單統計
2. **本週關鍵摘要**：與上週的比較分析（營收、訂單數變化）
3. **流量分析**：8 種流量來源的分類與分析（Sessions、CVR、AOV、營收）
4. **AOV 分析**：購物車件數分布、價格帶結構
5. **轉換漏斗**：從訪客到成交的轉換率分析
6. **AI 摘要**：自動生成週報觀察與建議（目前為規則式，後續可整合 LLM）

---

## 🔧 技術棧

- **Python 3.11+**
- **BigQuery**：資料查詢
- **PyEcharts**：圖表生成
- **Jinja2**：HTML 模板
- **pandas**：資料處理

---

## 📊 報告時間範圍

- **觀察時間**：本週週一到週日（例如：2025-11-04 至 2025-11-10）
- **比較基準**：上週週一到上週日
- **產出時間**：報告生成的時間戳記

---

## 🚨 重要提醒

1. **時間範圍**：週報使用「週一到週日」，不是「最近 7 天」
2. **欄位名稱**：使用 `ord_rev` 不是 `ord_total`，使用 `bhv1` 判斷取消
3. **位置問題**：GA4 和 Shopline 表在不同位置，需要分步查詢
4. **數字格式**：百分比兩位小數，金額取整數
5. **Transaction ID**：格式為 17 位數字，可以直接 JOIN

---

## 📞 需要幫助？

1. **第一次使用**：請先閱讀 [快速開始指南](QUICK_START.md)
2. **深入了解**：請閱讀 [完整交接文件](HANDOVER_DOCUMENT.md)
3. **程式碼問題**：請參考 [程式碼結構說明](CODE_STRUCTURE.md)
4. **常見問題**：請參考 [完整交接文件 - 常見問題](HANDOVER_DOCUMENT.md#常見問題與排錯)

---

## 📝 更新記錄

詳細的更新記錄請參考 [CHANGELOG.md](CHANGELOG.md)

---

**最後更新**：2025-11-05
