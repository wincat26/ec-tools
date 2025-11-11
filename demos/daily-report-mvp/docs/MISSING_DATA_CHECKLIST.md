# 缺少資料檢查清單

**建立日期**：2025-01-27  
**測試日期**：2025-11-04

---

## ✅ 已成功查詢的資料

### 基本指標（100% 完成）
- ✅ 營收（revenue）
- ✅ 訂單數（orders）
- ✅ 平均客單價（AOV）
- ✅ 轉換率（CVR）
- ✅ 工作階段（Sessions）

### 週變化分析（100% 完成）
- ✅ 營收週變化（revenue_change_wow）
- ✅ CVR 週變化（cvr_change_wow）
- ✅ Sessions 週變化（sessions_change_wow）
- ✅ AOV 週變化（aov_change_wow）

### 月迄今指標（100% 完成）
- ✅ MTD 營收（mtd_revenue）
- ✅ 目標達成率（mtd_achievement_rate）
- ✅ 預估當月營收（mtd_projected_revenue）

---

## ❌ 缺少的資料

### 1. 廣告資料（高優先級）

**問題**：
- ❌ `ad_spend`：目前返回 0（未實作）
- ❌ `roas`：目前返回 0.0（未實作）

**影響**：
- Google Chat 卡片中的「💰 廣告表現」區塊無法顯示實際數據
- 無法評估廣告投放效率

**需要的資料表**：
根據 PRD 文件，應該有以下資料表：
- `ad_data.meta_ads_daily`（Meta Ads 每日資料）
- `ad_data.google_ads_daily`（Google Ads 每日資料）

**實際狀況**：
- ⚠️ 目前 BigQuery 中**沒有 `ad_data` 資料集**
- 需要確認：
  1. 廣告資料是否存在於其他資料集？
  2. 廣告資料是否尚未匯入 BigQuery？
  3. 是否需要從其他來源取得？

**解決方案選項**：

#### 選項 A：使用現有資料表（如果存在）
```python
# 需要確認資料表位置
# 可能的位置：
# - datalake_stpl 中的某個表
# - 其他資料集中的表
```

#### 選項 B：暫時返回預設值（當前狀態）
```python
# 目前實作：返回 (0.0, 0.0)
# 優點：不會中斷流程
# 缺點：無法顯示實際廣告數據
```

#### 選項 C：從其他來源整合（未來擴充）
- 從 Meta Ads API 直接取得
- 從 Google Ads API 直接取得
- 從手動上傳的資料表取得

---

## 🔍 需要確認的項目

### 1. 廣告資料表位置

**檢查步驟**：
```sql
-- 檢查是否有廣告相關的表
SELECT table_name 
FROM `datalake360-saintpaul.datalake_stpl.INFORMATION_SCHEMA.TABLES`
WHERE table_name LIKE '%ad%' OR table_name LIKE '%meta%' OR table_name LIKE '%google%'
```

**或使用 Python**：
```python
from google.cloud import bigquery
client = bigquery.Client(project='datalake360-saintpaul')

# 檢查所有資料集
for dataset in client.list_datasets():
    tables = list(client.list_tables(dataset.dataset_id))
    ad_tables = [t for t in tables if 'ad' in t.table_id.lower() or 'meta' in t.table_id.lower() or 'google' in t.table_id.lower()]
    if ad_tables:
        print(f"在 {dataset.dataset_id} 中找到：{[t.table_id for t in ad_tables]}")
```

### 2. 廣告資料結構

**需要確認的欄位**：
- 日期欄位（date 或 report_date）
- 廣告花費（spend、cost、ad_spend）
- 營收或轉換（revenue、conversions、purchases）
- 平台（platform：meta、google）

### 3. 資料匯入狀態

**需要確認**：
- 廣告資料是否每日自動匯入？
- 匯入時間為何？（需確認是否在 08:00 前完成）
- 資料品質如何？

---

## 📋 實作建議

### 階段 1：確認資料來源（立即）

1. **檢查 BigQuery 中的廣告資料表**
   ```bash
   # 執行檢查腳本
   python scripts/check_ad_tables.py
   ```

2. **確認資料結構**
   - 查看表結構
   - 確認欄位名稱
   - 確認日期格式

### 階段 2：實作查詢邏輯（短期）

3. **實作 `fetch_ad_spend_and_roas()` 方法**
   ```python
   def fetch_ad_spend_and_roas(self, report_date: date) -> tuple[float, float]:
       # 查詢 Meta Ads
       meta_spend = self._fetch_meta_ads_spend(report_date)
       meta_revenue = self._fetch_meta_ads_revenue(report_date)
       
       # 查詢 Google Ads
       google_spend = self._fetch_google_ads_spend(report_date)
       google_revenue = self._fetch_google_ads_revenue(report_date)
       
       # 合計
       total_spend = meta_spend + google_spend
       total_revenue = meta_revenue + google_revenue
       
       # 計算 ROAS
       roas = total_revenue / total_spend if total_spend > 0 else 0.0
       
       return total_spend, roas
   ```

4. **測試查詢結果**
   - 驗證資料正確性
   - 處理邊界情況（無資料、資料為 0）

### 階段 3：優化與擴充（長期）

5. **支援多平台**
   - Meta Ads
   - Google Ads
   - 其他廣告平台

6. **資料品質檢查**
   - 異常值檢測
   - 資料完整性檢查

---

## 🎯 下一步行動

### 立即執行（今天）

1. ✅ **檢查 BigQuery 中的廣告資料表**
   - 列出所有可能的廣告相關表
   - 確認資料結構

2. ✅ **確認資料匯入狀態**
   - 廣告資料是否已匯入？
   - 匯入時間為何？

### 短期（本週）

3. **實作廣告資料查詢**
   - 根據實際表結構實作查詢邏輯
   - 測試查詢結果

4. **整合到主流程**
   - 更新資料生成模組
   - 測試完整流程

### 中期（下週）

5. **優化與擴充**
   - 支援多平台
   - 加入資料品質檢查

---

## 📊 資料完整性狀態

| 資料類別 | 完成度 | 狀態 |
|---------|--------|------|
| **基本指標** | 100% | ✅ 完成 |
| **週變化分析** | 100% | ✅ 完成 |
| **月迄今指標** | 100% | ✅ 完成 |
| **廣告資料** | 0% | ❌ 未實作 |

**整體完成度：75%**

---

## 💡 建議

### 當前狀態
- 核心功能（數據彙整、週變化、目標達成）已完整
- 廣告資料部分需要補齊

### 優先順序
1. **高優先級**：確認廣告資料表位置和結構
2. **中優先級**：實作廣告資料查詢
3. **低優先級**：優化和擴充功能

---

**最後更新**：2025-01-27

