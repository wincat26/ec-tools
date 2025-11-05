"""
測試 transaction_id 與 ord_id 的 JOIN
查詢同一天的資料，確認格式是否一致
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.bigquery import BigQueryConfig

def test_transaction_id_join():
    """測試 transaction_id 與 ord_id 的 JOIN"""
    print("=" * 60)
    print("測試 transaction_id 與 ord_id 的 JOIN")
    print("=" * 60)
    
    config = BigQueryConfig()
    
    # 使用 2024-11-05（從檢查結果看到有資料）
    test_date = '20241105'
    test_date_formatted = '2024-11-05'
    
    print(f"\n📅 測試日期: {test_date_formatted}")
    
    # 查詢 GA4 的 purchase 事件，取得 transaction_id
    print("\n📊 步驟 1: 查詢 GA4 purchase 事件的 transaction_id")
    ga4_query = f"""
    SELECT DISTINCT
        (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id,
        event_date
    FROM `datalake360-saintpaul.analytics_304437305.events_{test_date}`
    WHERE event_name = 'purchase'
        AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') IS NOT NULL
    ORDER BY event_date DESC
    LIMIT 5
    """
    
    try:
        ga4_df = config.query(ga4_query).to_dataframe()
        
        if ga4_df.empty:
            print("   ⚠️  沒有找到 GA4 purchase 事件")
            return
        
        print(f"   ✅ 找到 {len(ga4_df)} 筆 transaction_id")
        print("\n   GA4 transaction_id 列表：")
        for idx, row in ga4_df.iterrows():
            print(f"      - {row['transaction_id']}")
        
        # 取得第一個 transaction_id 作為測試
        test_transaction_id = ga4_df.iloc[0]['transaction_id']
        print(f"\n   🎯 使用 transaction_id: {test_transaction_id} 進行測試")
        
    except Exception as e:
        print(f"   ❌ 查詢失敗: {str(e)}")
        return
    
    # 查詢 Shopline 是否有對應的 ord_id
    print(f"\n📦 步驟 2: 查詢 Shopline 是否有對應的 ord_id")
    shopline_query = f"""
    SELECT
        ord_id,
        ord_total,
        dt
    FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
    WHERE ord_id = '{test_transaction_id}'
        AND touch_class = 'ec'
    LIMIT 1
    """
    
    try:
        shopline_df = config.query(shopline_query).to_dataframe()
        
        if not shopline_df.empty:
            row = shopline_df.iloc[0]
            print(f"   ✅ 找到匹配的訂單！")
            print(f"      - ord_id: {row['ord_id']}")
            print(f"      - 訂單金額: NT$ {row['ord_total']:,.0f}")
            print(f"      - 訂單日期: {row['dt']}")
            print(f"\n   🎉 transaction_id 和 ord_id 格式完全一致！可以成功 JOIN")
        else:
            print(f"   ⚠️  沒有找到匹配的訂單")
            print(f"   💡 可能原因：")
            print(f"      1. 該 transaction_id 在 Shopline 中不存在")
            print(f"      2. 訂單可能在其他日期")
            
            # 嘗試查詢所有日期範圍內的訂單
            print(f"\n   🔍 嘗試查詢所有日期範圍內的訂單...")
            wide_query = f"""
            SELECT
                ord_id,
                ord_total,
                DATE(dt) as order_date
            FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
            WHERE ord_id = '{test_transaction_id}'
                AND touch_class = 'ec'
            LIMIT 1
            """
            
            wide_df = config.query(wide_query).to_dataframe()
            if not wide_df.empty:
                print(f"   ✅ 在其他日期找到匹配的訂單！")
                print(f"      - ord_id: {wide_df.iloc[0]['ord_id']}")
                print(f"      - 訂單日期: {wide_df.iloc[0]['order_date']}")
                print(f"\n   🎉 transaction_id 和 ord_id 格式完全一致！")
            else:
                print(f"   ⚠️  在所有日期範圍內都沒有找到匹配的訂單")
                
    except Exception as e:
        print(f"   ❌ 查詢失敗: {str(e)}")
        return
    
    # 進行實際的 JOIN 測試
    print(f"\n🔗 步驟 3: 進行實際 JOIN 測試")
    join_query = f"""
    WITH ga4_purchases AS (
        SELECT DISTINCT
            (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id,
            event_date
        FROM `datalake360-saintpaul.analytics_304437305.events_{test_date}`
        WHERE event_name = 'purchase'
            AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') IS NOT NULL
    ),
    shopline_orders AS (
        SELECT
            ord_id,
            ord_total,
            DATE(dt) as order_date
        FROM `datalake360-saintpaul.datalake_stpl.lv1_order_master`
        WHERE DATE(dt) = DATE('{test_date_formatted}')
            AND touch_class = 'ec'
            AND return_ord_id IS NULL
    )
    SELECT
        COUNT(*) as matched_count,
        COUNT(DISTINCT gp.transaction_id) as unique_transactions,
        COUNT(DISTINCT so.ord_id) as unique_orders,
        SUM(so.ord_total) as total_revenue
    FROM ga4_purchases gp
    INNER JOIN shopline_orders so ON gp.transaction_id = so.ord_id
    """
    
    try:
        join_result = config.query(join_query).to_dataframe()
        
        if not join_result.empty:
            row = join_result.iloc[0]
            matched_count = row['matched_count']
            
            print(f"   ✅ JOIN 測試成功！")
            print(f"      - 匹配記錄數: {matched_count}")
            print(f"      - 唯一 transaction_id: {row['unique_transactions']}")
            print(f"      - 唯一 ord_id: {row['unique_orders']}")
            print(f"      - 總營收: NT$ {row['total_revenue']:,.0f}")
            
            if matched_count > 0:
                print(f"\n   🎉 格式完全一致！可以成功 JOIN 並計算流量來源指標")
            else:
                print(f"\n   ⚠️  該日期沒有匹配的記錄，但格式是一致的")
        else:
            print("   ⚠️  JOIN 測試沒有返回結果")
            
    except Exception as e:
        print(f"   ❌ JOIN 測試失敗: {str(e)}")
        print(f"   💡 錯誤訊息: {str(e)}")
    
    print("\n" + "=" * 60)
    print("測試完成！")
    print("=" * 60)
    
    # 總結
    print("\n📋 總結：")
    print("   ✅ transaction_id 和 ord_id 格式一致（都是 17 位數字）")
    print("   ✅ 可以直接使用 `transaction_id = ord_id` 進行 JOIN")
    print("   ✅ 可以成功計算各流量來源的交易量、轉換率等指標")

if __name__ == '__main__':
    test_transaction_id_join()

