# 日報排程設定指南

**建立日期**：2025-01-27  
**目的**：設定每日自動執行日報程序

---

## 📋 排程方案總覽

### 方案比較

| 方案 | 優點 | 缺點 | 適用場景 |
|------|------|------|---------|
| **本地 crontab (macOS/Linux)** | 免費、簡單、可靠 | 需要電腦常開 | 開發/測試環境 |
| **本地 LaunchAgent (macOS)** | 系統級排程 | macOS 專用 | macOS 開發環境 |
| **Windows 工作排程器** | 內建、簡單 | Windows 專用 | Windows 開發環境 |
| **GCP Cloud Scheduler** | 雲端、可靠、無需常開電腦 | 需要 GCP 設定 | 生產環境 |
| **GitHub Actions** | 免費、CI/CD 整合 | 需要 GitHub 帳號 | 開源專案 |

---

## 🍎 方案 1：macOS - crontab（推薦）

### 優點
- ✅ 簡單易用
- ✅ 系統內建
- ✅ 穩定可靠

### 設定步驟

#### 1. 建立執行腳本

建立 `scripts/run_daily_report.sh`：

```bash
#!/bin/bash

# 設定環境變數
export PATH="/opt/anaconda3/bin:$PATH"
export GOOGLE_CLOUD_PROJECT="datalake360-saintpaul"

# 切換到專案目錄
cd /Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp

# 執行日報程序
python main.py --client client_A

# 記錄執行結果
echo "$(date): Daily report executed" >> logs/cron.log 2>&1
```

#### 2. 設定執行權限

```bash
chmod +x scripts/run_daily_report.sh
```

#### 3. 設定 crontab

```bash
# 編輯 crontab
crontab -e

# 加入以下行（每天早上 08:00 執行）
0 8 * * * /Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp/scripts/run_daily_report.sh
```

#### 4. 驗證 crontab

```bash
# 查看目前的 crontab
crontab -l

# 測試執行（先手動執行一次）
./scripts/run_daily_report.sh
```

### crontab 時間格式說明

```
分 時 日 月 週 命令
*  *  *  *  *  command
│  │  │  │  │
│  │  │  │  └── 星期幾 (0-7, 0和7都代表星期日)
│  │  │  └───── 月份 (1-12)
│  │  └──────── 日期 (1-31)
│  └─────────── 小時 (0-23)
└────────────── 分鐘 (0-59)
```

**常用範例**：
- `0 8 * * *`：每天早上 08:00
- `0 9 * * 1-5`：週一到週五早上 09:00
- `0 */2 * * *`：每 2 小時執行一次

---

## 🍎 方案 2：macOS - LaunchAgent（系統級）

### 優點
- ✅ 系統級排程（即使未登入也能執行）
- ✅ 更穩定可靠
- ✅ 支援開機自動啟動

### 設定步驟

#### 1. 建立 LaunchAgent plist 檔案

建立 `~/Library/LaunchAgents/com.daily-report.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.daily-report</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/opt/anaconda3/bin/python</string>
        <string>/Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp/main.py</string>
        <string>--client</string>
        <string>client_A</string>
    </array>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/anaconda3/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>GOOGLE_CLOUD_PROJECT</key>
        <string>datalake360-saintpaul</string>
    </dict>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp/logs/launchd.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/winson/Dropbox/vibe_tools/ec-tools/demos/daily-report-mvp/logs/launchd_error.log</string>
</dict>
</plist>
```

#### 2. 載入 LaunchAgent

```bash
# 載入服務
launchctl load ~/Library/LaunchAgents/com.daily-report.plist

# 啟動服務（立即執行一次測試）
launchctl start com.daily-report

# 查看狀態
launchctl list | grep daily-report
```

#### 3. 管理 LaunchAgent

```bash
# 卸載服務
launchctl unload ~/Library/LaunchAgents/com.daily-report.plist

# 重新載入（修改 plist 後）
launchctl unload ~/Library/LaunchAgents/com.daily-report.plist
launchctl load ~/Library/LaunchAgents/com.daily-report.plist
```

---

## 🪟 方案 3：Windows - 工作排程器

### 設定步驟

#### 1. 建立批次檔

建立 `scripts/run_daily_report.bat`：

```batch
@echo off
cd /d C:\path\to\daily-report-mvp
C:\path\to\python.exe main.py --client client_A
```

#### 2. 設定工作排程器

1. 開啟「工作排程器」（Task Scheduler）
2. 建立基本工作
3. 設定名稱：「每日數據彙整日報」
4. 觸發條件：每日，08:00
5. 動作：啟動程式
   - 程式：`C:\path\to\python.exe`
   - 引數：`main.py --client client_A`
   - 開始於：`C:\path\to\daily-report-mvp`

---

## ☁️ 方案 4：GCP Cloud Scheduler（雲端方案）

### 優點
- ✅ 不需要電腦常開
- ✅ 雲端可靠執行
- ✅ 支援重試機制
- ✅ 可整合 Cloud Functions

### 設定步驟

#### 1. 建立 Cloud Function

建立 `cloud_function/main.py`：

```python
import functions_framework
import subprocess
import os

@functions_framework.http
def daily_report(request):
    """Cloud Function 觸發器"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(project_root, 'demos', 'daily-report-mvp', 'main.py')
    
    result = subprocess.run(
        ['python', script_path, '--client', 'client_A'],
        cwd=os.path.dirname(script_path),
        capture_output=True,
        text=True
    )
    
    return {
        'statusCode': 200 if result.returncode == 0 else 500,
        'body': result.stdout + result.stderr
    }
```

#### 2. 部署 Cloud Function

```bash
gcloud functions deploy daily-report \
  --runtime python311 \
  --trigger-http \
  --entry-point daily_report \
  --region asia-east1
```

#### 3. 建立 Cloud Scheduler

```bash
gcloud scheduler jobs create http daily-report-job \
  --schedule="0 8 * * *" \
  --uri="https://asia-east1-datalake360-saintpaul.cloudfunctions.net/daily-report" \
  --http-method=GET \
  --time-zone="Asia/Taipei"
```

---

## 🛠️ 方案 5：GitHub Actions（免費 CI/CD）

### 設定步驟

#### 1. 建立 GitHub Actions Workflow

建立 `.github/workflows/daily-report.yml`：

```yaml
name: Daily Report

on:
  schedule:
    # 每天早上 08:00 UTC (台灣時間 16:00)
    - cron: '0 0 * * *'
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
```

---

## 📝 推薦方案

### 開發/測試環境
- **macOS**：使用 **LaunchAgent**（系統級、穩定）
- **Windows**：使用 **工作排程器**（簡單、內建）

### 生產環境
- **GCP Cloud Scheduler**（雲端、可靠）

---

## 🔧 建立執行腳本

讓我為您建立執行腳本：

