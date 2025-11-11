#!/usr/bin/env python3
"""
驗證 daily_metrics view 的結構和資料
使用 BigQuery 直接查詢驗證
"""
import sys
import os
from datetime import date, timedelta
from google.cloud import bigquery

# 添加專案路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.bigquery import BigQueryConfig


def verify_view_structure():
    """驗證 view 的結構（欄位）"""
    print("=" * 60)
    print("驗證 daily_metrics view 結構")
    print("=" * 60)
    
    bq_config = BigQueryConfig()
    view_name = "datalake360-saintpaul.datalake_looker.daily_metrics"
    
    try:
        # 先查詢一筆資料來了解結構
        query = f"""
        SELECT *
        FROM `{view_name}`
        LIMIT 1
        """
        
        result = bq_config.query(query).to_dataframe()
        
        if result.empty:
            print(f"⚠️  View 存在但沒有資料")
            # 嘗試從 INFORMATION_SCHEMA 查詢結構
            try:
                schema_query = f"""
                SELECT column_name, data_type
                FROM `datalake360-saintpaul.datalake_looker.INFORMATION_SCHEMA.COLUMNS`
                WHERE table_name = 'daily_metrics'
                ORDER BY ordinal_position
                """
                schema_result = bq_config.query(schema_query).to_dataframe()
                if not schema_result.empty:
                    print(f"\n✅ View 結構（共 {len(schema_result)} 個欄位）：")
                    print("-" * 60)
                    for _, row in schema_result.iterrows():
                        print(f"  • {row['column_name']:30s} {row['data_type']}")
                    return True
            except:
                pass
            return False
        
        print(f"\n✅ View 結構（共 {len(result.columns)} 個欄位）：")
        print("-" * 60)
        for col in result.columns:
            print(f"  • {col}")
        
        return True
        
    except Exception as e:
        print(f"❌ 查詢失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def verify_view_data(report_date: date = None):
    """驗證 view 的資料"""
    print("\n" + "=" * 60)
    print("驗證 daily_metrics view 資料")
    print("=" * 60)
    
    if report_date is None:
        report_date = date.today() - timedelta(days=1)  # 昨日
    
    bq_config = BigQueryConfig()
    view_name = "datalake360-saintpaul.datalake_looker.daily_metrics"
    
    try:
        # 先查詢所有資料來了解結構（使用 date 欄位排序）
        query = f"""
        SELECT *
        FROM `{view_name}`
        ORDER BY date DESC
        LIMIT 1
        """
        
        result = bq_config.query(query).to_dataframe()
        
        if result.empty:
            print(f"⚠️  View 沒有資料")
            return False
        
        print(f"\n✅ 找到資料（查看最近一筆）")
        print("-" * 60)
        print("資料欄位和值：")
        for col in result.columns:
            value = result.iloc[0][col]
            print(f"  • {col:30s} = {value}")
        
        # 嘗試找出日期欄位
        date_columns = [col for col in result.columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_columns:
            print(f"\n可能的日期欄位：{', '.join(date_columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 查詢失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def get_view_sample_data(days: int = 7):
    """取得最近幾天的樣本資料"""
    print("\n" + "=" * 60)
    print(f"取得最近 {days} 天的樣本資料")
    print("=" * 60)
    
    bq_config = BigQueryConfig()
    view_name = "datalake360-saintpaul.datalake_looker.daily_metrics"
    
    try:
        query = f"""
        SELECT *
        FROM `{view_name}`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
        ORDER BY date DESC
        LIMIT {days}
        """
        
        result = bq_config.query(query).to_dataframe()
        
        if result.empty:
            print("⚠️  沒有資料")
            return
        
        print(f"\n✅ 找到 {len(result)} 筆資料")
        print("-" * 60)
        # 只顯示關鍵欄位
        key_columns = ['date', 'total_revenue', 'total_orders', 'avg_order_value', 
                      'conversion_rate_pct', 'total_sessions', 'google_ads_cost_usd', 'meta_ads_spend']
        display_cols = [col for col in key_columns if col in result.columns]
        if display_cols:
            print(result[display_cols].to_string(index=False))
        else:
            print(result.to_string(index=False))
        
    except Exception as e:
        print(f"❌ 查詢失敗：{str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """主程式"""
    print("🔍 驗證 daily_metrics view")
    print(f"View 路徑：datalake360-saintpaul.datalake_looker.daily_metrics")
    print()
    
    # 1. 驗證結構
    structure_ok = verify_view_structure()
    
    # 2. 驗證資料（昨日）
    yesterday = date.today() - timedelta(days=1)
    data_ok = verify_view_data(yesterday)
    
    # 3. 取得樣本資料
    if structure_ok or data_ok:
        get_view_sample_data(days=7)
    
    print("\n" + "=" * 60)
    if structure_ok and data_ok:
        print("✅ 驗證完成：view 結構和資料都正常")
    elif structure_ok:
        print("⚠️  驗證部分完成：view 存在但昨日無資料")
    else:
        print("❌ 驗證失敗：請檢查 view 是否存在或權限設定")
    print("=" * 60)


if __name__ == '__main__':
    main()

