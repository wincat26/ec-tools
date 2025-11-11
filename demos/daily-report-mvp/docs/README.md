# 文檔索引

**建立日期**：2025-01-27  
**目的**：快速找到需要的文檔

---

## 🚀 新電腦設定（必讀）

### 快速開始
1. **[快速開始指南](../QUICK_START.md)** - 5 分鐘快速設定
2. **[完整交接文件](./HANDOVER_DOCUMENT.md)** - 詳細交接說明
3. **[新電腦檢查清單](./CHECKLIST_NEW_COMPUTER.md)** - 設定檢查清單

---

## 📖 核心文檔

### 設定與配置
- **[排程設定指南](./SCHEDULING_GUIDE.md)** - 自動排程設定（macOS/Linux/Windows/GCP）
- **[資料存儲說明](./DATA_STORAGE.md)** - 資料來源和存儲位置
- **[資料與排程總結](./DATA_AND_SCHEDULING_SUMMARY.md)** - 快速總結

### 功能說明
- **[Google Chat 模板設計](./GOOGLE_CHAT_TEMPLATE.md)** - 卡片模板完整說明
- **[模板總結](./TEMPLATE_SUMMARY.md)** - 模板設計總結
- **[MCP 整合規劃](./MCP_INTEGRATION_PLAN.md)** - 未來廣告資料自動化

### 測試與分析
- **[實際資料查詢分析](./ACTUAL_DATA_QUERY_SUMMARY.md)** - 實際查詢結果分析
- **[資料查詢分析](./DATA_QUERY_ANALYSIS.md)** - 詳細查詢分析
- **[缺少資料檢查清單](./MISSING_DATA_CHECKLIST.md)** - 資料完整性檢查

---

## 📋 文檔分類

### 按用途分類

| 用途 | 推薦文檔 |
|------|---------|
| **新電腦設定** | [快速開始指南](../QUICK_START.md) → [完整交接文件](./HANDOVER_DOCUMENT.md) |
| **設定排程** | [排程設定指南](./SCHEDULING_GUIDE.md) |
| **了解資料來源** | [資料存儲說明](./DATA_STORAGE.md) |
| **了解模板設計** | [Google Chat 模板設計](./GOOGLE_CHAT_TEMPLATE.md) |
| **未來擴充** | [MCP 整合規劃](./MCP_INTEGRATION_PLAN.md) |
| **故障排除** | [完整交接文件](./HANDOVER_DOCUMENT.md) 的「常見問題」章節 |

### 按讀者分類

**新接手的開發者**：
1. [快速開始指南](../QUICK_START.md)
2. [完整交接文件](./HANDOVER_DOCUMENT.md)
3. [新電腦檢查清單](./CHECKLIST_NEW_COMPUTER.md)

**需要設定排程**：
1. [排程設定指南](./SCHEDULING_GUIDE.md)

**需要了解資料來源**：
1. [資料存儲說明](./DATA_STORAGE.md)
2. [實際資料查詢分析](./ACTUAL_DATA_QUERY_SUMMARY.md)

**需要了解功能設計**：
1. [Google Chat 模板設計](./GOOGLE_CHAT_TEMPLATE.md)
2. [模板總結](./TEMPLATE_SUMMARY.md)

---

## 📝 快速參考

### 重要路徑
- **專案根目錄**：`demos/daily-report-mvp/`
- **客戶設定檔**：`config/clients.yaml`（需建立）
- **月份目標檔**：`config/targets.yaml`
- **執行腳本**：`scripts/run_daily_report.sh`
- **日誌檔案**：`logs/launchd.log` 或 `logs/cron.log`

### 重要命令
```bash
# 測試執行（乾跑模式）
python main.py --client client_A --dry-run

# 實際執行
python main.py --client client_A

# 設定排程（macOS）
./scripts/setup_launchagent.sh

# 檢查資料存儲
python scripts/check_data_storage.py
```

---

**最後更新**：2025-01-27

