# 排程穩定性改進指南

**建立日期**：2025-11-05  
**目的**：解決日報排程不穩定問題，提供穩定的自動化排程方案

---

## 🎯 操作脈絡

### 目標
- ✅ 確保日報每日穩定執行
- ✅ 自動重試機制（失敗時自動重試）
- ✅ 完整的錯誤處理與日誌記錄
- ✅ 監控與診斷工具

### 環境
- macOS 系統
- LaunchAgent 排程系統
- Python 3.x 環境

### 可行方案（比較）

| 方案 | 穩定性 | 設定難度 | 維護成本 | 推薦度 |
|------|--------|---------|---------|--------|
| **改進的 LaunchAgent** | ⭐⭐⭐⭐ | 簡單 | 低 | ⭐⭐⭐⭐⭐ |
| **GCP Cloud Scheduler** | ⭐⭐⭐⭐⭐ | 中等 | 低 | ⭐⭐⭐⭐⭐ |
| **GitHub Actions** | ⭐⭐⭐⭐ | 簡單 | 低 | ⭐⭐⭐⭐ |

---

## 🔧 方案 1：改進的 LaunchAgent（推薦）

### 改進內容

#### 1. **改進的執行腳本** (`scripts/run_daily_report.sh`)

**新增功能**：
- ✅ 自動偵測 Python 路徑（支援多個 Python 環境）
- ✅ 自動重試機制（最多 3 次，間隔 60 秒）
- ✅ 詳細的日誌記錄（成功/失敗/錯誤）
- ✅ 狀態檔案記錄（`logs/last_run_status.txt`）
- ✅ 完整的錯誤處理

**使用方式**：
```bash
# 手動執行測試
cd demos/daily-report-mvp
./scripts/run_daily_report.sh
```

#### 2. **改進的 LaunchAgent 設定** (`scripts/setup_launchagent.sh`)

**改進內容**：
- ✅ 使用執行腳本而非直接執行 Python
- ✅ 支援新版 macOS 的 `bootstrap` 語法
- ✅ 自動設定執行權限
- ✅ 更清晰的狀態回報

**設定步驟**：
```bash
cd demos/daily-report-mvp
./scripts/setup_launchagent.sh
```

#### 3. **排程狀態檢查工具** (`scripts/check_schedule_status.sh`)

**功能**：
- ✅ 檢查 LaunchAgent 服務狀態
- ✅ 檢查最後執行狀態
- ✅ 檢查日誌檔案
- ✅ 檢查 Python 環境
- ✅ 檢查專案檔案完整性
- ✅ 提供診斷建議

**使用方式**：
```bash
cd demos/daily-report-mvp
./scripts/check_schedule_status.sh
```

---

## 🚀 快速設定步驟

### 步驟 1：設定改進的 LaunchAgent

```bash
cd /Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp
./scripts/setup_launchagent.sh
```

**預期輸出**：
```
🔧 設定 LaunchAgent 排程...
專案目錄：/Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp
✅ 已建立 plist 檔案：/Users/winson/Library/LaunchAgents/com.daily-report.plist
✅ 已設定執行腳本權限
📦 載入 LaunchAgent...
✅ LaunchAgent 已載入
```

### 步驟 2：驗證排程狀態

```bash
./scripts/check_schedule_status.sh
```

**預期輸出**：
```
🔍 排程狀態檢查
==========================================
📋 1. LaunchAgent 服務狀態
✅ LaunchAgent 服務已載入
...
```

### 步驟 3：測試執行

```bash
# 手動執行一次測試
./scripts/run_daily_report.sh

# 或使用 LaunchAgent 立即執行
launchctl start com.daily-report
```

### 步驟 4：監控日誌

```bash
# 查看執行日誌
tail -f logs/cron.log

# 查看錯誤日誌
tail -f logs/cron_error.log

# 查看 LaunchAgent 日誌
tail -f logs/launchd.log
```

---

## 📊 監控與診斷

### 檢查最後執行狀態

```bash
cat logs/last_run_status.txt
```

**輸出範例**：
```
SUCCESS
2025-11-05 09:00:15
```

或失敗時：
```
FAILED
2025-11-05 09:00:15
Exit code: 1
```

### 常見問題診斷

#### 問題 1：LaunchAgent 服務未載入

**症狀**：
```bash
launchctl list | grep daily-report
# 無輸出
```

**解決方案**：
```bash
./scripts/setup_launchagent.sh
```

#### 問題 2：Python 路徑找不到

**症狀**：
```
❌ ERROR: 找不到可用的 Python 執行檔
```

**解決方案**：
- 確認 Python 已安裝
- 檢查 `which python3` 或 `which python`
- 修改 `scripts/run_daily_report.sh` 中的 `PYTHON_PATHS` 陣列

#### 問題 3：執行失敗但無錯誤訊息

**解決方案**：
```bash
# 查看詳細日誌
tail -50 logs/cron.log
tail -50 logs/cron_error.log

# 手動執行並查看即時輸出
./scripts/run_daily_report.sh
```

---

## ☁️ 方案 2：GCP Cloud Scheduler（雲端方案）

### 優點
- ✅ **不需要電腦常開**：完全雲端執行
- ✅ **最高穩定性**：Google 基礎設施保證
- ✅ **自動重試**：內建重試機制
- ✅ **監控與告警**：整合 Cloud Monitoring

### 設定步驟

#### 1. 建立 Cloud Function

建立 `cloud_function/main.py`：

```python
import functions_framework
import subprocess
import os
import json

@functions_framework.http
def daily_report(request):
    """Cloud Function 觸發器"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(project_root, 'demos', 'daily-report-mvp', 'main.py')
    
    # 取得客戶 ID（從請求參數或環境變數）
    client_id = request.args.get('client', 'client_A')
    
    # 計算昨日日期
    from datetime import date, timedelta
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    result = subprocess.run(
        ['python3', script_path, '--client', client_id, '--date', yesterday],
        cwd=os.path.dirname(script_path),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'message': 'Daily report sent successfully',
                'output': result.stdout
            })
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'success': False,
                'message': 'Daily report failed',
                'error': result.stderr
            })
        }
```

#### 2. 部署 Cloud Function

```bash
gcloud functions deploy daily-report \
  --runtime python311 \
  --trigger-http \
  --entry-point daily_report \
  --region asia-east1 \
  --timeout 540s \
  --memory 512MB \
  --set-env-vars GOOGLE_CLOUD_PROJECT=datalake360-saintpaul
```

#### 3. 建立 Cloud Scheduler

```bash
gcloud scheduler jobs create http daily-report-job \
  --schedule="0 9 * * *" \
  --uri="https://asia-east1-datalake360-saintpaul.cloudfunctions.net/daily-report?client=client_A" \
  --http-method=GET \
  --time-zone="Asia/Taipei" \
  --attempt-deadline=600s
```

#### 4. 設定重試策略

```bash
gcloud scheduler jobs update http daily-report-job \
  --max-retry-attempts=3 \
  --min-backoff-duration=60s \
  --max-backoff-duration=300s
```

---

## 🔄 方案 3：GitHub Actions（免費 CI/CD）

### 優點
- ✅ **完全免費**：GitHub 提供免費額度
- ✅ **CI/CD 整合**：與程式碼版本控制整合
- ✅ **簡單設定**：YAML 設定檔

### 設定步驟

建立 `.github/workflows/daily-report.yml`：

```yaml
name: Daily Report

on:
  schedule:
    # 每天早上 09:00 UTC (台灣時間 17:00)
    # 如需台灣時間 09:00，改為：cron: '0 1 * * *'
    - cron: '0 1 * * *'
  workflow_dispatch:  # 允許手動觸發

jobs:
  daily-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd demos/daily-report-mvp
          pip install -r requirements.txt
      
      - name: Set up Google Cloud Auth
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Run daily report
        run: |
          cd demos/daily-report-mvp
          python main.py --client client_A
        env:
          GOOGLE_CLOUD_PROJECT: datalake360-saintpaul
      
      - name: Upload logs
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: daily-report-logs
          path: demos/daily-report-mvp/logs/
```

---

## 📝 驗證方法

### 1. 檢查排程是否正常運作

```bash
# 使用診斷工具
./scripts/check_schedule_status.sh

# 檢查服務狀態
launchctl list | grep daily-report

# 查看排程時間
plutil -p ~/Library/LaunchAgents/com.daily-report.plist | grep -A 2 StartCalendarInterval
```

### 2. 測試執行

```bash
# 手動執行
./scripts/run_daily_report.sh

# 或使用 LaunchAgent 立即執行
launchctl start com.daily-report
```

### 3. 監控日誌

```bash
# 即時監控
tail -f logs/cron.log

# 查看最後執行狀態
cat logs/last_run_status.txt
```

---

## 🎯 建議的下一步

### 短期（立即執行）
1. ✅ 執行 `./scripts/setup_launchagent.sh` 設定改進的排程
2. ✅ 執行 `./scripts/check_schedule_status.sh` 驗證狀態
3. ✅ 手動測試執行一次確認正常運作

### 中期（1-2 週內）
1. 監控一週的執行狀況
2. 確認重試機制正常運作
3. 根據日誌優化錯誤處理

### 長期（1 個月後）
1. 考慮遷移到 GCP Cloud Scheduler（雲端方案）
2. 建立告警機制（執行失敗時通知）
3. 整合監控儀表板

---

## 📚 相關文檔

- [排程設定指南](./SCHEDULING_GUIDE.md) - 各種排程方案比較
- [完整交接文件](./HANDOVER_DOCUMENT.md) - 專案完整說明
- [快速開始指南](../QUICK_START.md) - 快速設定步驟

---

**最後更新**：2025-11-05

