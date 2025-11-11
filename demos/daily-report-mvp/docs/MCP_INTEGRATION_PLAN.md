# MCP 廣告平台整合規劃

**建立日期**：2025-01-27  
**目標**：使用 MCP (Model Context Protocol) 從 Meta Ads 和 Google Ads 自動拉取廣告資料

---

## 🎯 整合目標

### 當前狀態（暫時方案）
- ✅ 支援手動輸入廣告資料（透過 `clients.yaml`）
- ✅ 可正確計算 ROAS
- ⚠️ 需要每日手動更新廣告花費

### 未來目標（MCP 整合）
- ✅ 自動從 Meta Ads API 拉取廣告花費
- ✅ 自動從 Google Ads API 拉取廣告花費
- ✅ 無需手動輸入，每日自動更新
- ✅ 支援歷史資料查詢

---

## 📊 當前資料來源

### 2025-11-04 實際數據
- **Meta Ads 花費**：$2,199
- **Google Ads 花費**：$4,587
- **總廣告花費**：$6,786
- **當日營收**：$50,102
- **ROAS**：$50,102 / $6,786 = 7.38x

---

## 🔧 MCP 整合架構

### 架構設計

```
┌─────────────────────────────────────────────────────────┐
│                   每日數據彙整日報系統                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              廣告資料查詢模組 (DataFetcher)              │
│                                                          │
│  優先順序：                                               │
│  1. MCP 從廣告平台 API 取得（未來）                      │
│  2. 從 BigQuery 查詢（未來）                             │
│  3. 從客戶設定檔手動輸入（當前）                         │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    MCP 整合層                            │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │  Meta Ads MCP    │  │ Google Ads MCP   │           │
│  │                  │  │                  │           │
│  │  - 取得廣告花費  │  │  - 取得廣告花費  │           │
│  │  - 取得成效數據  │  │  - 取得成效數據  │           │
│  └──────────────────┘  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              廣告平台 API                                │
│                                                          │
│  • Meta Ads Marketing API                                │
│  • Google Ads API                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 實作計劃

### 階段 1：MCP 整合準備（目前）

#### 1.1 設定 MCP Server
- [ ] 建立 Meta Ads MCP Server
- [ ] 建立 Google Ads MCP Server
- [ ] 設定 API 認證（Access Token、API Key）

#### 1.2 資料結構設計
```python
# 廣告資料結構
ad_data = {
    'date': '2025-11-04',
    'meta_ads': {
        'spend': 2199,
        'impressions': 0,  # 未來擴充
        'clicks': 0,       # 未來擴充
        'conversions': 0   # 未來擴充
    },
    'google_ads': {
        'spend': 4587,
        'impressions': 0,
        'clicks': 0,
        'conversions': 0
    },
    'total_spend': 6786,
    'roas': 7.38
}
```

### 階段 2：MCP 整合實作（未來）

#### 2.1 建立 MCP 客戶端
```python
# src/data/mcp_client.py
class MCPAdsClient:
    """MCP 廣告平台客戶端"""
    
    def __init__(self):
        # 初始化 MCP 連線
        pass
    
    def fetch_meta_ads_spend(self, date: date) -> float:
        """從 Meta Ads API 取得廣告花費"""
        # 使用 MCP 呼叫 Meta Ads API
        pass
    
    def fetch_google_ads_spend(self, date: date) -> float:
        """從 Google Ads API 取得廣告花費"""
        # 使用 MCP 呼叫 Google Ads API
        pass
```

#### 2.2 更新資料查詢邏輯
```python
# src/data/fetcher.py
def fetch_ad_spend_and_roas(self, report_date: date, client_config: dict = None) -> tuple[float, float]:
    """
    查詢廣告花費和 ROAS
    
    優先順序：
    1. 使用 MCP 從廣告平台 API 取得（未來實作）
    2. 從 BigQuery 查詢（未來實作）
    3. 從客戶設定檔手動輸入（當前方案）
    """
    # 優先使用 MCP
    try:
        mcp_client = MCPAdsClient()
        meta_spend = mcp_client.fetch_meta_ads_spend(report_date)
        google_spend = mcp_client.fetch_google_ads_spend(report_date)
        total_spend = meta_spend + google_spend
        
        # 計算 ROAS
        daily_metrics = self.fetch_daily_metrics(report_date)
        revenue = daily_metrics['revenue']
        roas = revenue / total_spend if total_spend > 0 else 0.0
        
        return total_spend, roas
    except Exception as e:
        # MCP 失敗，降級到其他方案
        pass
    
    # 降級方案：從 BigQuery 或手動輸入
    # ...
```

---

## 🔐 認證與權限

### Meta Ads API
- **認證方式**：Access Token
- **取得方式**：Facebook Marketing API
- **權限需求**：
  - `ads_read`
  - `ads_management`

### Google Ads API
- **認證方式**：OAuth 2.0
- **取得方式**：Google Cloud Console
- **權限需求**：
  - `googleads` API 存取權限

---

## 📊 資料欄位規劃

### Meta Ads 資料欄位
```python
{
    'date': '2025-11-04',
    'account_id': 'act_123456789',
    'spend': 2199,
    'impressions': 50000,
    'clicks': 1000,
    'conversions': 50,
    'cpm': 43.98,
    'cpc': 2.20,
    'ctr': 2.0
}
```

### Google Ads 資料欄位
```python
{
    'date': '2025-11-04',
    'customer_id': '1234567890',
    'spend': 4587,
    'impressions': 80000,
    'clicks': 1500,
    'conversions': 75,
    'cpm': 57.34,
    'cpc': 3.06,
    'ctr': 1.88
}
```

---

## 🚀 實作步驟

### Step 1：設定 MCP Server
1. 安裝 MCP SDK
2. 建立 Meta Ads MCP Server
3. 建立 Google Ads MCP Server
4. 設定 API 認證

### Step 2：建立 MCP 客戶端
1. 建立 `MCPAdsClient` 類別
2. 實作 `fetch_meta_ads_spend()` 方法
3. 實作 `fetch_google_ads_spend()` 方法
4. 加入錯誤處理和重試機制

### Step 3：整合到現有系統
1. 更新 `fetch_ad_spend_and_roas()` 方法
2. 加入降級機制（MCP → BigQuery → 手動輸入）
3. 測試整合流程

### Step 4：優化與擴充
1. 加入快取機制（避免重複查詢）
2. 加入資料驗證
3. 支援歷史資料查詢

---

## 📝 當前實作（手動輸入方案）

### 客戶設定檔格式
```yaml
clients:
  - client_id: "client_A"
    # ... 其他設定 ...
    ad_data:
      manual_ad_spend:
        "2025-11-04":
          meta_ads: 2199
          google_ads: 4587
```

### 查詢邏輯
```python
# 優先從客戶設定檔的手動輸入取得
if client_config and 'ad_data' in client_config:
    ad_data = client_config.get('ad_data', {})
    manual_ad_spend = ad_data.get('manual_ad_spend', {})
    date_str = report_date.isoformat()
    
    if date_str in manual_ad_spend:
        manual_data = manual_ad_spend[date_str]
        meta_spend = float(manual_data.get('meta_ads', 0))
        google_spend = float(manual_data.get('google_ads', 0))
        total_spend = meta_spend + google_spend
        
        # 計算 ROAS
        daily_metrics = self.fetch_daily_metrics(report_date)
        revenue = daily_metrics['revenue']
        roas = revenue / total_spend if total_spend > 0 else 0.0
        
        return total_spend, roas
```

---

## 🎯 未來擴充

### 短期（1-2 週）
- [ ] 建立 MCP Server 基礎架構
- [ ] 實作 Meta Ads API 整合
- [ ] 實作 Google Ads API 整合

### 中期（1 個月）
- [ ] 加入資料快取機制
- [ ] 加入錯誤處理和重試
- [ ] 支援歷史資料查詢

### 長期（2-3 個月）
- [ ] 加入更多廣告平台（TikTok Ads、LINE Ads 等）
- [ ] 加入廣告成效分析（CTR、CPC、CPM 等）
- [ ] 自動化資料匯入 BigQuery

---

## 📚 參考資源

### Meta Ads API
- [Facebook Marketing API 文檔](https://developers.facebook.com/docs/marketing-apis)
- [Meta Ads API 認證指南](https://developers.facebook.com/docs/marketing-api/overview/authentication)

### Google Ads API
- [Google Ads API 文檔](https://developers.google.com/google-ads/api/docs/start)
- [Google Ads API 認證指南](https://developers.google.com/google-ads/api/docs/oauth/overview)

### MCP (Model Context Protocol)
- [MCP 官方文檔](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

**最後更新**：2025-01-27

