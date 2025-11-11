# 每日數據彙整日報 - MVP v1.1

**版本**：v1.1 (MVP)  
**建立日期**：2025-01-27  
**狀態**：✅ 開發完成，可正常運作

> **💡 新電腦設定？** 請先閱讀 [快速開始指南](./QUICK_START.md) 或 [完整交接文件](./docs/HANDOVER_DOCUMENT.md)

---

## 📋 專案概述

本模組實現「每日數據彙整日報」的 MVP v1.1 版本，核心目標是驗證「Data (數據彙整)」的價值。

### 核心功能
- 每日自動彙整 E-com 和 GA4 數據
- 透過 Google Chat、LINE Notify 推播營運摘要
- 節省客戶手動撈取報表的時間（15-30 分鐘 → 0 分鐘）

### MVP 範疇
- ✅ 數據彙整（E-com + GA4）
- ✅ 每日推播（Google Chat）
- ✅ 關鍵指標呈現（營收、訂單、CVR、ROAS 等）
- ✅ 當月目標達成率
- ❌ AI 洞察生成（已排除）
- ❌ 雲端自動化排程（手動執行）

---

## 🎯 成功指標

### 核心價值指標
- (質化) 客戶回饋：「這為我節省了每天 [X] 分鐘彙整報表的時間」
- (質化) 數據準確度 ≥ 4.5 / 5（客戶訪談）

### 採用指標
- 每日通知開啟率 ≥ 80%

### 參與指標
- 點擊「深入分析」按鈕 ≥ 20%

---

## 📁 專案結構

```
daily-report-mvp/
├── config/              # 配置模組
│   ├── __init__.py
│   ├── bigquery.py      # BigQuery 連線設定
│   └── clients.yaml     # 客戶設定檔（範例）
├── src/                 # 核心程式碼
│   ├── __init__.py
│   ├── data/            # 資料查詢模組
│   │   ├── __init__.py
│   │   ├── fetcher.py   # BigQuery 查詢
│   │   └── validator.py # GA4 數據驗證
│   ├── generator/       # 資料生成模組
│   │   ├── __init__.py
│   │   └── daily_aggregation.py  # 生成單行 JSON
│   ├── notification/    # 推播模組
│   │   ├── __init__.py
│   │   ├── google_chat.py  # Google Chat Webhook
│   │   └── line_notify.py  # LINE Flex Message
│   └── utils/           # 工具函數
│       ├── __init__.py
│       └── date_utils.py
├── main.py              # 主程式入口
├── requirements.txt     # Python 依賴
└── README.md           # 本文件
```

---

## 🚀 快速開始

### 1. 環境需求
- Python 3.8+
- Google Cloud 認證（Application Default Credentials）
- BigQuery 資料存取權限

### 2. 安裝依賴

```bash
cd demos/daily-report-mvp
pip install -r requirements.txt
```

### 3. 設定 Google Cloud 認證

```bash
# 使用 Application Default Credentials（推薦）
gcloud auth application-default login

# 設定預設專案
gcloud config set project datalake360-saintpaul
```

### 4. 設定客戶配置

複製範例設定檔並填入實際值：

```bash
cp config/clients.yaml.example config/clients.yaml
```

編輯 `config/clients.yaml`，設定客戶資訊：

```yaml
clients:
  - client_id: "client_A"
    bigquery:
      project_id: "datalake360-saintpaul"
      dataset_id: "datalake_stpl"
      ga4_dataset: "analytics_304437305"
    monthly_target_revenue: 2000000  # 後備值（如果目標檔中找不到對應月份時使用）
    google_chat_webhook: "https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=YYYYY&token=ZZZZZ"
```

### 4.5. 設定月份目標（可選，建議）

系統會優先使用 `config/targets.yaml` 中的動態月份目標。如果目標檔中找不到對應月份，則使用客戶設定檔中的 `monthly_target_revenue` 作為後備值。

目標檔格式（`config/targets.yaml`）：

```yaml
targets:
  "2025-10": 1900000
  "2025-11": 2000000
  "2025-12": 3100000
  "2026-01": 11500000
  # ... 更多月份
```

**優點**：
- 支援不同月份有不同的目標（例如：促銷月份目標較高）
- 無需修改客戶設定檔即可更新目標

### 5. 執行腳本

#### 基本執行（使用昨日資料）

```bash
python main.py --client client_A
```

#### 指定日期

```bash
python main.py --client client_A --date 2025-11-04
```

#### 乾跑模式（測試資料生成，不發送推播）

```bash
python main.py --client client_A --dry-run
```

#### 跳過 GA4 驗證（僅用於測試）

### 6. 設定 LINE 推播（可選，建議）

若要同時發送 LINE 通知，請將 `config/secrets.example.env` 複製為 `config/secrets.env` 或 `.env`，並填入：

```
LINE_CHANNEL_ACCESS_TOKEN=xxxxx         # LINE Developers 取得的 Channel access token
LINE_TARGET_IDS=Uxxxxxxxxxxxxxxxxxxxxxx # userId 或 groupId，逗號分隔
LINE_DASHBOARD_URL=https://lookerstudio.google.com/...  # 可選，預設為聖保羅 Looker 報表
```

執行腳本時會自動偵測上述環境變數，若存在即同步推播 LINE Flex Message 與文字摘要。

```bash
python main.py --client client_A --skip-validation
```

---

## 📊 資料模型

### 每日彙總單行 JSON

```json
{
  "client_id": "client_A",
  "report_date": "2025-11-04",
  "monthly_target_revenue": 2000000,
  "revenue": 85000,
  "orders": 50,
  "aov": 1700.0,
  "cvr": 0.015,
  "sessions": 3333,
  "ad_spend": 10000,
  "roas": 8.5,
  "revenue_change_wow": -0.15,
  "cvr_change_wow": -0.10,
  "mtd_revenue": 340000,
  "mtd_achievement_rate": 0.17,
  "mtd_projected_revenue": 1020000
}
```

---

## 🔄 執行流程

1. **[手動觸發 08:00]** Admin 在本地執行 Python 腳本
2. **[GA4 數據驗證]** 前置檢查昨日 GA4 sessions 數據是否已匯入
3. **[驗證失敗]** 停止執行，輸出錯誤訊息
4. **[驗證成功]** 繼續執行
5. **[查詢 BQ]** 查詢 E-com + GA4 資料
6. **[生成資料]** 生成單行 JSON 資料
7. **[生成訊息]** 套入 Google Chat 卡片模板
8. **[推播 09:00]** 透過 Google Chat Webhook API 發送

---

## 📝 注意事項

### MVP 限制
- 手動執行（不自動排程）
- 不含 AI 洞察
- 僅支援 Google Chat（不支援 LINE）
- 客戶設定需手動維護

### 資料要求
- BigQuery 中需有 E-com 訂單資料
- BigQuery 中需有 GA4 事件資料
- GA4 數據需在 08:00 前完成匯入

---

## 🔧 進階使用

### 命令列參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--client` | 客戶 ID（必填） | - |
| `--date` | 要彙整的日期（YYYY-MM-DD） | 昨日（T-1） |
| `--skip-validation` | 跳過 GA4 數據驗證 | False |
| `--dry-run` | 乾跑模式（不發送推播） | False |

### 排程執行（建議）

雖然 MVP 階段為手動執行，但可以使用系統排程工具：

#### macOS / Linux (crontab)

```bash
# 每天早上 08:00 執行（假設腳本在 /path/to/daily-report-mvp）
0 8 * * * cd /path/to/daily-report-mvp && python main.py --client client_A
```

#### Windows (工作排程器)

建立批次檔 `run_daily_report.bat`：

```batch
cd C:\path\to\daily-report-mvp
python main.py --client client_A
```

然後在 Windows 工作排程器中設定每天早上 08:00 執行。

---

## 🐛 故障排除

### 問題 1：找不到客戶設定檔

**錯誤**：`FileNotFoundError: 客戶設定檔不存在`

**解決方案**：
1. 確認 `config/clients.yaml` 檔案存在
2. 如果不存在，複製範例檔案：`cp config/clients.yaml.example config/clients.yaml`

### 問題 2：GA4 數據驗證失敗

**錯誤**：`GA4 數據延遲：report_date (...) 的 GA4 sessions 數據尚未匯入`

**解決方案**：
1. 確認 GA4 數據是否已匯入 BigQuery
2. 檢查資料集名稱是否正確
3. 如果數據確實延遲，可以使用 `--skip-validation` 跳過驗證（僅用於測試）

### 問題 3：BigQuery 連線失敗

**錯誤**：`BigQuery 連線失敗`

**解決方案**：
1. 確認已設定 Google Cloud 認證：`gcloud auth application-default login`
2. 確認專案 ID 正確
3. 確認有 BigQuery 讀取權限

### 問題 4：Google Chat 推播失敗

**錯誤**：`推播失敗：HTTP 400`

**解決方案**：
1. 確認 Webhook URL 正確
2. 確認 Webhook 未過期
3. 檢查 Google Chat 空間設定

---

## 📚 相關文檔

### 🚀 快速開始
- [快速開始指南](./QUICK_START.md) - **新電腦設定必讀**
- [完整交接文件](./docs/HANDOVER_DOCUMENT.md) - **詳細交接說明**

### 📖 核心文檔
- [排程設定指南](./docs/SCHEDULING_GUIDE.md) - 自動排程設定
- [資料存儲說明](./docs/DATA_STORAGE.md) - 資料來源和存儲位置
- [MCP 整合規劃](./docs/MCP_INTEGRATION_PLAN.md) - 未來廣告資料自動化

### 🔧 技術文檔
- [Google Chat 模板設計](./docs/GOOGLE_CHAT_TEMPLATE.md) - 卡片模板說明
- [模板總結](./docs/TEMPLATE_SUMMARY.md) - 模板設計總結
- [實際資料查詢分析](./docs/ACTUAL_DATA_QUERY_SUMMARY.md) - 查詢結果分析

### 📚 參考資料
- [週報生成工具](../weekly-report-generator/) - 參考資料查詢邏輯

---

**最後更新**：2025-01-27

