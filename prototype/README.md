# AI 營運顧問系統 - Prototype

## 📋 專案概述

這是 AI 營運顧問系統的視覺化 Prototype，使用純 HTML/CSS/JavaScript 開發，用於快速驗證 UI/UX 設計與使用者流程。

## 🗺️ Sitemap 架構

```
AI 營運顧問系統
├── 1. Dashboard (總覽)          - dashboard.html
├── 2. 數據分析 (Data)           - data.html
├── 3. 洞察中心 (Insights)        - insights.html
├── 4. 行動方案 (Actions)        - actions.html
├── 5. 角色/顧問池 (Consultants) - consultants.html
├── 6. 報告設定&歷史 (Reports)    - reports.html
└── 7. 基本資料設定 (Settings)    - settings.html
```

## 📁 檔案結構

```
prototype/
├── index.html                  # 登入頁
├── dashboard.html              # Dashboard 總覽
├── data.html                   # 數據分析
├── insights.html               # 洞察中心
├── actions.html                # 行動方案
├── consultants.html            # 角色/顧問池
├── reports.html                # 報告設定
├── settings.html               # 基本設定
├── expert-subscribe.html       # 專家訂閱頁面
├── layout-template.html        # 頁面模板（參考用）
│
├── css/
│   ├── main.css                # 主要樣式（變數、基礎樣式）
│   ├── components.css         # 組件樣式（按鈕、卡片、表格等）
│   ├── navigation.css         # 導航系統樣式
│   ├── dashboard.css          # Dashboard 專用樣式
│   ├── expert.css             # 專家訂閱頁面樣式
│   └── onboarding.css         # 引導系統樣式
│
└── js/
    ├── utils.js               # 工具函數
    ├── mockData.js            # 假資料
    ├── navigation.js          # 導航與路由邏輯
    ├── dashboard.js           # Dashboard 邏輯
    ├── expert-subscribe.js    # 專家訂閱邏輯
    └── onboarding.js         # 引導系統邏輯
```

## 🚀 快速開始

### 本地運行

1. 直接在瀏覽器中開啟 `index.html` 或 `dashboard.html`
2. 無需後端服務，所有資料均為 Mock Data

### 頁面導航

- 頂部導航欄可切換各個主要分區
- 每個頁面都有統一的導航結構
- 當前頁面會自動高亮顯示

## 📊 各頁面功能狀態

### ✅ 已完成功能

1. **Dashboard**
   - KPI 卡片（總營收、流量、轉換率、平均訂單金額）
   - 異常警示區塊
   - 快速訪問入口
   - KPI 詳細展開功能

2. **專家訂閱系統**
   - 專家訂閱頁面
   - 流量詳情中的專家建議（廣告區塊）

3. **導航系統**
   - 統一的主導航欄
   - 頁面路由邏輯
   - 當前頁面高亮

### 🔧 開發中功能

所有其他頁面（data.html, insights.html, actions.html, consultants.html, reports.html, settings.html）目前為框架結構，顯示「功能開發中」佔位符。

這些功能將逐步遷移和實作：
- 數據分析：將整合現有的 KPI 分解功能
- 洞察中心：將整合 AI 建議與專家建議
- 行動方案：將整合任務清單功能
- 角色/顧問池：新建角色對話功能
- 報告設定：新建報告管理功能
- 基本設定：新建設定管理功能

## 🎨 設計系統

### 顏色系統
```css
--color-primary: #2563eb (藍色)
--color-success: #10b981 (綠色)
--color-warning: #f59e0b (黃色)
--color-danger: #ef4444 (紅色)
```

### 間距系統
```css
--spacing-xs: 0.25rem
--spacing-sm: 0.5rem
--spacing-md: 1rem
--spacing-lg: 1.5rem
--spacing-xl: 2rem
--spacing-2xl: 3rem
```

## 📝 開發規範

1. **命名規範**
   - CSS 類別使用 kebab-case：`nav-link`, `card-header`
   - JavaScript 函數使用 camelCase：`initDashboard()`, `loadSummaryData()`

2. **結構規範**
   - 每個頁面都應包含統一的導航欄
   - 主要內容區使用 `.container` 類別
   - 卡片使用 `.card`, `.card-header`, `.card-body` 結構

3. **響應式設計**
   - 使用 Grid 系統進行佈局
   - 移動端使用媒體查詢調整

## 🔄 後續開發計畫

1. **第一階段**：完善 Dashboard 異常警示與快速訪問
2. **第二階段**：遷移 KPI 分解功能至數據分析頁
3. **第三階段**：整合 AI 建議至洞察中心
4. **第四階段**：整合任務清單至行動方案
5. **第五階段**：開發角色對話功能
6. **第六階段**：開發報告與設定功能

## 📚 相關文檔

- [Sitemap 設計文檔](../../doc/product_prd/prototype-sitemap.md)
- [產品 PRD](../../doc/product_prd/)

## 🐛 問題回報

如發現任何問題或需要改進，請建立 Issue 或聯繫開發團隊。
