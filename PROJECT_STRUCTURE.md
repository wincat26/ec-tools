# AI 營運顧問系統 — 專案資料夾結構規劃

**建立日期**：2025-01-27  
**版本**：v1.0

---

## 📁 專案根目錄結構

```
ec-tools/
├── README.md                          # 專案總覽說明
├── PROJECT_STRUCTURE.md               # 本檔案：資料夾結構說明
├── .gitignore                         # Git 忽略檔案設定
│
├── frontend/                          # 前端應用（Next.js）
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── .env.local                     # 環境變數（不提交）
│   ├── public/                        # 靜態資源
│   │   ├── images/
│   │   └── icons/
│   ├── src/
│   │   ├── app/                       # Next.js App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx               # Dashboard 首頁
│   │   │   ├── login/
│   │   │   ├── dashboard/
│   │   │   ├── api/                   # API Routes
│   │   │   └── globals.css
│   │   ├── components/                # 可重用組件
│   │   │   ├── common/                # 通用組件
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── dashboard/            # Dashboard 專用組件
│   │   │   │   ├── SummaryCard.tsx
│   │   │   │   ├── KPIPyramid.tsx
│   │   │   │   ├── TrafficTable.tsx
│   │   │   │   ├── ConversionFunnel.tsx
│   │   │   │   └── ProductInsight.tsx
│   │   │   ├── guideline/            # Guideline 模組組件
│   │   │   │   ├── GuidelineCard.tsx
│   │   │   │   └── GuidelineList.tsx
│   │   │   └── tasks/                # Action Queue 組件
│   │   │       ├── TaskItem.tsx
│   │   │       ├── TaskList.tsx
│   │   │       └── TaskForm.tsx
│   │   ├── lib/                      # 工具函數與配置
│   │   │   ├── api.ts                # API 呼叫封裝
│   │   │   ├── auth.ts               # 認證相關
│   │   │   ├── utils.ts              # 通用工具
│   │   │   └── constants.ts          # 常數定義
│   │   ├── hooks/                    # Custom React Hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useDashboard.ts
│   │   │   └── useTasks.ts
│   │   ├── types/                    # TypeScript 型別定義
│   │   │   ├── dashboard.ts
│   │   │   ├── guideline.ts
│   │   │   └── task.ts
│   │   └── styles/                   # 樣式檔案
│   │       └── components.css
│   └── __tests__/                    # 測試檔案
│
├── backend/                           # 後端 API 服務（Node.js + Express）
│   ├── package.json
│   ├── tsconfig.json
│   ├── .env                          # 環境變數（範本）
│   ├── src/
│   │   ├── index.ts                  # 應用程式入口
│   │   ├── routes/                   # API 路由
│   │   │   ├── dashboard.ts
│   │   │   ├── guideline.ts
│   │   │   ├── tasks.ts
│   │   │   └── auth.ts
│   │   ├── controllers/             # 控制器邏輯
│   │   │   ├── dashboardController.ts
│   │   │   ├── guidelineController.ts
│   │   │   └── taskController.ts
│   │   ├── services/                # 業務邏輯層
│   │   │   ├── bigqueryService.ts   # BigQuery 查詢服務
│   │   │   ├── guidelineService.ts  # Guideline 生成服務
│   │   │   └── aiService.ts         # AI/LLM 服務
│   │   ├── middleware/              # 中介軟體
│   │   │   ├── auth.ts              # 認證中介軟體
│   │   │   ├── errorHandler.ts
│   │   │   └── logger.ts
│   │   ├── models/                  # 資料模型
│   │   │   ├── Dashboard.ts
│   │   │   ├── Guideline.ts
│   │   │   └── Task.ts
│   │   └── config/                  # 配置檔案
│   │       ├── bigquery.ts
│   │       ├── firebase.ts
│   │       └── openai.ts
│   └── __tests__/
│
├── data/                              # 資料層（BigQuery SQL、Dataform）
│   ├── dataform/                     # Dataform 專案
│   │   ├── dataform.json
│   │   ├── includes/
│   │   │   └── constants.sqlx
│   │   ├── models/
│   │   │   ├── staging/
│   │   │   │   ├── stg_orders.sqlx
│   │   │   │   └── stg_customers.sqlx
│   │   │   ├── processed/
│   │   │   │   ├── lv0_orders.sqlx
│   │   │   │   ├── daily_summary.sqlx
│   │   │   │   └── source_metrics.sqlx
│   │   │   └── views/
│   │   │       └── view_dashboard_summary.sqlx
│   │   └── assertions/
│   │       └── data_quality.sqlx
│   ├── sql/                          # 手動 SQL 查詢腳本
│   │   ├── queries/
│   │   │   ├── dashboard_queries.sql
│   │   │   └── guideline_queries.sql
│   │   └── migrations/
│   └── scripts/                      # 資料處理腳本
│       ├── data_ingestion/
│       │   ├── shopline_import.js
│       │   └── ga4_sync.js
│       └── data_quality/
│           └── validation.js
│
├── doc/                              # 專案文檔（現有）
│   ├── product_prd/                  # PRD 相關文檔
│   ├── config/                       # 配置文檔
│   ├── scripts/                      # 文檔腳本
│   └── log/                          # 日誌檔案
│
├── prd/                              # PRD 原始檔案（現有）
│
├── prototype/                         # 視覺化 Prototype（HTML/CSS/JS）
│   ├── index.html                    # Prototype 首頁
│   ├── dashboard.html                # Dashboard 頁面
│   ├── login.html                    # 登入頁面
│   ├── css/
│   │   ├── main.css                  # 主要樣式
│   │   ├── components.css            # 組件樣式
│   │   └── dashboard.css              # Dashboard 專用樣式
│   ├── js/
│   │   ├── main.js                   # 主要邏輯
│   │   ├── dashboard.js              # Dashboard 邏輯
│   │   ├── mockData.js               # 假資料
│   │   └── utils.js                  # 工具函數
│   └── assets/
│       ├── images/
│       └── icons/
│
├── scripts/                          # 開發與部署腳本
│   ├── setup.sh                      # 環境設定腳本
│   ├── deploy.sh                     # 部署腳本
│   └── test.sh                       # 測試腳本
│
├── config/                           # 全域配置檔案
│   ├── development.json
│   ├── production.json
│   └── .env.example                  # 環境變數範本
│
└── .github/                           # GitHub Actions 工作流程
    └── workflows/
        ├── ci.yml                    # CI/CD 流程
        └── deploy.yml
```

---

## 📋 各資料夾用途說明

### `frontend/` — 前端應用
- **技術棧**：Next.js 14+ (App Router) + TypeScript + Tailwind CSS + Recharts
- **用途**：使用者介面與互動邏輯
- **主要功能模組**：
  - Dashboard（營運儀表板）
  - Guideline（智能建議）
  - Action Queue（任務清單）
  - 認證與權限管理

### `backend/` — 後端 API
- **技術棧**：Node.js + Express + TypeScript
- **用途**：提供 RESTful API，處理業務邏輯與資料查詢
- **主要功能**：
  - BigQuery 資料查詢封裝
  - Guideline AI 生成邏輯
  - 任務管理 API
  - 認證與授權中介軟體

### `data/` — 資料層
- **技術棧**：Dataform + BigQuery SQL
- **用途**：ETL 流程、資料轉換、指標計算
- **結構**：
  - `dataform/`：Dataform 專案檔案
  - `sql/`：手動查詢與遷移腳本
  - `scripts/`：資料匯入與品質檢查腳本

### `prototype/` — 視覺化 Prototype
- **技術棧**：純 HTML/CSS/JavaScript（無框架，快速驗證）
- **用途**：快速視覺化驗證 UI/UX 設計、使用者流程
- **特色**：使用假資料，可離線運行，便於展示與討論

### `doc/` — 專案文檔
- PRD 相關文檔
- API 文件
- 開發規範
- 部署指南

---

## 🔧 環境設定檔案

### `.env` 範本結構

```env
# 前端環境變數 (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_auth_domain

# 後端環境變數 (.env)
PORT=3001
NODE_ENV=development

# BigQuery
GOOGLE_CLOUD_PROJECT_ID=your_project_id
BIGQUERY_DATASET=cdp_data
GOOGLE_APPLICATION_CREDENTIALS=./config/gcp-key.json

# Firebase
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key

# OpenAI
OPENAI_API_KEY=your_openai_key

# LINE Notify
LINE_NOTIFY_TOKEN=your_line_token
```

---

## 📦 依賴管理

### 前端主要依賴
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "tailwindcss": "^3.0.0",
    "recharts": "^2.0.0",
    "firebase": "^10.0.0"
  }
}
```

### 後端主要依賴
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "@google-cloud/bigquery": "^7.0.0",
    "firebase-admin": "^12.0.0",
    "openai": "^4.0.0"
  }
}
```

---

## ✅ 下一步行動

1. ✅ 確認資料夾結構
2. 🔄 建立基礎檔案與配置
3. 🔄 設計 Prototype
4. 🔄 實作 Prototype 核心頁面

---

## 📝 備註

- 此結構支援 MVP 階段開發
- 可根據實際需求調整資料夾命名與位置
- Prototype 可獨立運行，不依賴後端服務

