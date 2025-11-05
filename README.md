# AI 營運顧問系統

**版本**：MVP v1.0  
**建立日期**：2025-01-27

---

## 📋 專案概述

AI 營運顧問系統是一個「數據驅動行動的 SaaS 平台」，幫助中小型電商品牌：
- 自動整合多平台數據（GA4、Shopline、Cyberbiz、廣告平台）
- 即時監控 KPI 異常
- 自動生成 AI 營運建議（Guideline）
- 追蹤任務執行與成效回饋

## 🎯 核心價值

**從「數據呈現」到「行動引導」**：不只告訴你「哪裡有問題」，還告訴你「該怎麼做」

## 🏗️ 技術架構

### 前端
- **框架**：Next.js 14+ (App Router)
- **樣式**：Tailwind CSS
- **圖表**：Recharts
- **認證**：Firebase Auth

### 後端
- **框架**：Node.js + Express
- **資料庫**：BigQuery
- **ETL**：Dataform
- **AI**：BigQuery ML + OpenAI API

### 資料層
- **資料倉儲**：BigQuery
- **ETL 工具**：Dataform
- **資料來源**：GA4、Shopline、Cyberbiz、廣告平台 API

## 📁 專案結構

請參閱 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) 了解完整資料夾結構。

```
ec-tools/
├── frontend/          # Next.js 前端應用（正式開發中）
├── backend/           # Node.js API 服務（正式開發中）
├── data/              # BigQuery SQL & Dataform（正式開發中）
├── demos/             # Demo/POC 項目
│   ├── prototype/     # 視覺化 Prototype (HTML/CSS/JS)
│   ├── weekly-report-generator/  # 週報生成工具
│   └── ecommerce-growth-planner/ # 電商成長規劃器
├── docs/              # 專案文檔（重新整理）
│   ├── prd/           # PRD 原始檔案
│   ├── product/       # 產品文檔
│   ├── technical/     # 技術文檔
│   └── guidelines/    # 開發規範
└── archive/           # 備份與歷史檔案
```

## 🚀 快速開始

### 環境需求
- Node.js 18+
- npm 或 yarn
- Google Cloud Project (BigQuery)
- Firebase 專案

### 安裝步驟

1. **複製環境變數**
```bash
cp config/.env.example config/.env
# 編輯 config/.env 填入實際值
```

2. **安裝依賴（前端）**
```bash
cd frontend
npm install
```

3. **安裝依賴（後端）**
```bash
cd backend
npm install
```

4. **啟動開發環境**
```bash
# 終端 1: 啟動後端
cd backend
npm run dev

# 終端 2: 啟動前端
cd frontend
npm run dev
```

## 📖 文檔

- [專案總覽與背景說明](./docs/prd/專案總覽與背景說明.txt)
- [產品功能總覽](./docs/prd/產品功能總覽.txt)
- [系統架構與資料流程](./docs/prd/系統架構與資料流程.txt)
- [產品認知摘要](./docs/product/產品認知摘要.md)

## 🎨 Prototype

視覺化 Prototype 位於 `demos/prototype/` 目錄，可獨立運行：
```bash
cd demos/prototype
# 直接用瀏覽器開啟 index.html
```

## 👥 開發團隊

- **產品負責人**：Winson Lu
- **技術顧問**：RedDoor Data Team

## 📝 授權

內部專案，版權所有 © 2025 RedDoor Interactive

---

**最後更新**：2025-01-27  
**結構重組**：2025-01-27（重新歸類 demo/poc 項目與文檔）

