"""
檢查 GA4 transaction_id 與 Shopline ord_id 格式是否一致
"""
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.bigquery import BigQueryConfig

def check_transaction_id_format():
    """檢查 transaction_id 和 ord_id 的格式"""
    print("=" * 60)
    print("檢查 GA4 transaction_id 與 Shopline ord_id 格式")
    print("=" * 60)
    
    config = BigQueryConfig()
    
    # 查詢最近可用的資料（使用 2024 年的日期）
    # 先查詢實際存在的日期分區
    date_query = """
    SELECT table_name
    FROM `datalake360-saintpaul.analytics_304437305.INFORMATION_SCHEMA.TABLES`
    WHERE table_name LIKE 'events_%'
    ORDER BY table_name DESC
    LIMIT 1
    """
    
    try:
        date_result = config.query(date_query).to_dataframe()
        if not date_result.empty:
            latest_table = date_result.iloc[0]['table_name']
            date_suffix = latest_table.replace('events_', '')
            print(f"   📅 使用最新的 GA4 事件表: {latest_table}")
        else:
            # 如果查不到，使用預設日期
            date_suffix = '20241105'
            print(f"   ⚠️  使用預設日期: events_{date_suffix}")
    except Exception as e:
        # 如果查詢失敗，使用預設日期
        date_suffix = '20241105'
        print(f"   ⚠️  無法查詢日期分區，使用預設日期: events_{date_suffix}")
    
    # 解析日期
    try:
        end_date = datetime.strptime(date_suffix, '%Y%m%d').date()
        start_date = end_date - timedelta(days=7)
    except:
        end_date = datetime(2024, 11, 5).date()
        start_date = datetime(2024, 10, 29).date()
    
    print(f"\n📅 查詢日期範圍：{start_date} 至 {end_date}")
    
    # 1. 檢查 GA4 transaction_id 格式
    print("\n📊 步驟 1: 檢查 GA4 transaction_id 格式")
    ga4_query = f"""
    SELECT DISTINCT
        (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id,
        event_date,
        event_timestamp
    FROM `datalake360-saintpaul.analytics_304437305.events_{date_suffix}`
    WHERE event_name = 'purchase'
        AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') IS NOT NULL
    ORDER BY event_timestamp DESC
    LIMIT 10
    """
    
    try:
        ga4_df = config.query(ga4_query).to_dataframe()
        
        if not ga4_df.empty:
            print(f"   ✅ 找到 {len(ga4_df)} 筆 GA4 transaction_id")
            print("\n   GA4 transaction_id 範例：")
            for idx, row in ga4_df.head(5).iterrows():
                trans_id = row['transaction_id']
                print(f"      - {trans_id} (長度: {len(str(trans_id))})")
            
            # 分析格式
            sample_ids = ga4_df['transaction_id'].head(5).tolist()
            print(f"\n   📝 格式分析：")
            print(f"      - 是否都是數字: {all(str(id).isdigit() for id in sample_ids if id)}")
            print(f"      - 是否包含字母: {any(any(c.isalpha() for c in str(id)) for id in sample_ids if id)}")
            print(f"      - 平均長度: {sum(len(str(id)) for id in sample_ids if id) / len([id for id in sample_ids if id]):.1f}")
        else:
            print("   ⚠️  沒有找到 GA4 transaction_id")
            
    except Exception as e:
        print(f"   ❌ 查詢 GA4 transaction_id 失敗: {str(e)}")
        return
    
    # 2. 檢查 Shopline ord_id 格式
    print("\n📦 步驟 2: 檢查 Shopline ord_id 格式")
    shopline_query = f"""
    SELECT DISTINCT
        ord_id,
        dt
    FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
    WHERE DATE(dt) BETWEEN DATE('{start_date}') AND DATE('{end_date}')
        AND touch_class = 'ec'
        AND return_ord_id IS NULL
    ORDER BY dt DESC
    LIMIT 10
    """
    
    try:
        shopline_df = config.query(shopline_query).to_dataframe()
        
        if not shopline_df.empty:
            print(f"   ✅ 找到 {len(shopline_df)} 筆 Shopline ord_id")
            print("\n   Shopline ord_id 範例：")
            for idx, row in shopline_df.head(5).iterrows():
                ord_id = row['ord_id']
                print(f"      - {ord_id} (長度: {len(str(ord_id))})")
            
            # 分析格式
            sample_ids = shopline_df['ord_id'].head(5).tolist()
            print(f"\n   📝 格式分析：")
            print(f"      - 是否都是數字: {all(str(id).isdigit() for id in sample_ids if id)}")
            print(f"      - 是否包含字母: {any(any(c.isalpha() for c in str(id)) for id in sample_ids if id)}")
            print(f"      - 平均長度: {sum(len(str(id)) for id in sample_ids if id) / len([id for id in sample_ids if id]):.1f}")
        else:
            print("   ⚠️  沒有找到 Shopline ord_id")
            
    except Exception as e:
        print(f"   ❌ 查詢 Shopline ord_id 失敗: {str(e)}")
        return
    
    # 3. 檢查是否有匹配的記錄
    print("\n🔗 步驟 3: 檢查 transaction_id 與 ord_id 的匹配情況")
    
    if not ga4_df.empty and not shopline_df.empty:
        ga4_ids = set(ga4_df['transaction_id'].dropna().astype(str))
        shopline_ids = set(shopline_df['ord_id'].dropna().astype(str))
        
        matched = ga4_ids.intersection(shopline_ids)
        
        print(f"   GA4 transaction_id 數量: {len(ga4_ids)}")
        print(f"   Shopline ord_id 數量: {len(shopline_ids)}")
        print(f"   ✅ 匹配的 ID 數量: {len(matched)}")
        
        if matched:
            print(f"\n   🎯 匹配的 ID 範例：")
            for matched_id in list(matched)[:5]:
                print(f"      - {matched_id}")
        else:
            print(f"\n   ⚠️  沒有找到匹配的 ID")
            print(f"   💡 可能原因：")
            print(f"      1. transaction_id 和 ord_id 格式不同")
            print(f"      2. 需要轉換格式（例如：去除前綴/後綴）")
            print(f"      3. 日期範圍內沒有同時存在的訂單")
    
    # 4. 嘗試 JOIN 測試（使用實際存在的日期）
    print("\n🧪 步驟 4: 測試 JOIN 查詢")
    
    # 使用實際存在的日期（從步驟 1 和 2 的結果中選擇一個共同的日期）
    # 先取得一個實際的 transaction_id 來查詢對應的日期
    if not ga4_df.empty and not shopline_df.empty:
        # 從 GA4 取得一個實際的 transaction_id
        sample_transaction_id = ga4_df.iloc[0]['transaction_id']
        sample_ord_id = shopline_df.iloc[0]['ord_id']
        
        print(f"   📝 測試 ID：")
        print(f"      - GA4 transaction_id: {sample_transaction_id}")
        print(f"      - Shopline ord_id: {sample_ord_id}")
        
        # 檢查是否完全匹配
        if str(sample_transaction_id) == str(sample_ord_id):
            print(f"      ✅ 格式完全一致！")
        else:
            # 檢查是否前綴/後綴不同
            trans_str = str(sample_transaction_id)
            ord_str = str(sample_ord_id)
            
            if trans_str.startswith(ord_str) or ord_str.startswith(trans_str):
                print(f"      ⚠️  格式部分匹配（可能是前綴/後綴不同）")
            else:
                print(f"      ⚠️  格式不一致")
        
        # 嘗試直接 JOIN 一個實際的 ID
        join_test_query = f"""
        WITH ga4_transactions AS (
            SELECT DISTINCT
                (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id
            FROM `datalake360-saintpaul.analytics_304437305.events_{date_suffix}`
            WHERE event_name = 'purchase'
                AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') = '{sample_transaction_id}'
        ),
        shopline_orders AS (
            SELECT DISTINCT
                ord_id,
                ord_total
            FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
            WHERE ord_id = '{sample_ord_id}'
                AND touch_class = 'ec'
                AND return_ord_id IS NULL
        )
        SELECT
            gt.transaction_id,
            so.ord_id,
            so.ord_total,
            CASE WHEN gt.transaction_id = so.ord_id THEN '✅ 匹配' ELSE '❌ 不匹配' END as match_status
        FROM ga4_transactions gt
        FULL OUTER JOIN shopline_orders so ON gt.transaction_id = so.ord_id
        """
        
        try:
            join_result = config.query(join_test_query).to_dataframe()
            
            if not join_result.empty:
                row = join_result.iloc[0]
                print(f"\n   ✅ JOIN 測試結果：")
                print(f"      - transaction_id: {row.get('transaction_id', 'N/A')}")
                print(f"      - ord_id: {row.get('ord_id', 'N/A')}")
                print(f"      - 匹配狀態: {row.get('match_status', 'N/A')}")
                
                if row.get('match_status') == '✅ 匹配':
                    print(f"      - 訂單金額: NT$ {row.get('ord_total', 0):,.0f}")
                    print(f"\n   🎉 格式完全一致！可以成功 JOIN")
                else:
                    print(f"\n   ⚠️  格式不一致，需要調整 JOIN 邏輯")
            else:
                print("   ⚠️  JOIN 測試沒有返回結果")
                
        except Exception as e:
            print(f"   ❌ JOIN 測試失敗: {str(e)}")
            print(f"   💡 錯誤訊息: {str(e)}")
            
            # 如果位置錯誤，提供建議
            if 'location' in str(e).lower() or 'not found' in str(e).lower():
                print(f"   💡 可能是資料表位置問題，建議檢查資料集位置設定")
    
    print("\n" + "=" * 60)
    print("檢查完成！")
    print("=" * 60)

if __name__ == '__main__':
    check_transaction_id_format()

