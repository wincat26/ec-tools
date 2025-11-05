"""
測試資料查詢功能
驗證 SQL 查詢是否能正確取得資料
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_fetcher import DataFetcher

def test_queries():
    """測試所有查詢功能"""
    print("=" * 60)
    print("測試資料查詢功能")
    print("=" * 60)
    
    fetcher = DataFetcher()
    
    # 測試 1: GMV 基本指標
    print("\n📊 測試 1: GMV 基本指標（最近 7 天）")
    try:
        gmv_data = fetcher.fetch_gmv_metrics(days=7)
        print(f"   ✅ 成交營收: NT$ {gmv_data['net_revenue']:,.0f}")
        print(f"   ✅ 總營業額: NT$ {gmv_data['gross_revenue']:,.0f}")
        print(f"   ✅ 成交訂單數: {gmv_data['completed_orders']:,} 筆")
        print(f"   ✅ 總訂單數: {gmv_data['total_orders']:,} 筆")
        print(f"   ✅ 取消率: {gmv_data['cancel_rate']:.2f}%")
    except Exception as e:
        print(f"   ❌ 查詢失敗: {str(e)}")
    
    # 測試 2: 本週關鍵摘要
    print("\n📈 測試 2: 本週關鍵摘要（與上週比較）")
    try:
        comparison = fetcher.fetch_weekly_comparison(days=7)
        print(f"   ✅ 本週營收: NT$ {comparison['this_week']['net_revenue']:,.0f}")
        print(f"   ✅ 上週營收: NT$ {comparison['last_week']['net_revenue']:,.0f}")
        print(f"   ✅ 營收變化: {comparison['changes']['revenue']:+.2f}%")
        print(f"   ✅ 訂單變化: {comparison['changes']['orders']:+.2f}%")
    except Exception as e:
        print(f"   ❌ 查詢失敗: {str(e)}")
    
    # 測試 3: 流量分析
    print("\n🌐 測試 3: 流量分析")
    try:
        traffic_df = fetcher.fetch_traffic_analysis(days=7)
        if not traffic_df.empty:
            print(f"   ✅ 找到 {len(traffic_df)} 個流量來源")
            for idx, row in traffic_df.head(8).iterrows():
                sessions = int(row.get('sessions', 0))
                conversions = int(row.get('conversions', 0))
                cvr = row.get('cvr', 0.0)
                revenue = row.get('revenue', 0)
                aov = row.get('aov', 0)
                print(f"      - {row['traffic_source']}:")
                print(f"         Sessions: {sessions:,} | CVR: {cvr:.2f}% | AOV: NT$ {aov:,.0f} | 營收: NT$ {revenue:,.0f}")
        else:
            print("   ⚠️  沒有找到流量資料")
    except Exception as e:
        print(f"   ❌ 查詢失敗: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 測試 4: AOV 分析
    print("\n🛒 測試 4: AOV 分析")
    try:
        aov_data = fetcher.fetch_aov_analysis(days=7, dimension='overall')
        if aov_data['item_distribution']:
            print(f"   ✅ 購物車件數分布:")
            for item in aov_data['item_distribution']:
                print(f"      - {item['item_count']}: {item['order_count']} 筆訂單, 平均 NT$ {item['avg_amount']:.0f}")
        if aov_data['price_band_distribution']:
            print(f"   ✅ 價格帶分布:")
            for price in aov_data['price_band_distribution']:
                print(f"      - {price['price_band']}: {price['order_count']} 筆訂單")
    except Exception as e:
        print(f"   ❌ 查詢失敗: {str(e)}")
    
    # 測試 5: 轉換漏斗
    print("\n🔽 測試 5: 轉換漏斗")
    try:
        funnel_data = fetcher.fetch_conversion_funnel(days=7)
        if funnel_data['overall']['steps']:
            print(f"   ✅ 全站轉換漏斗:")
            for step in funnel_data['overall']['steps']:
                print(f"      - {step['label']}: {step['count']:,} 人")
    except Exception as e:
        print(f"   ❌ 查詢失敗: {str(e)}")
    
    print("\n" + "=" * 60)
    print("測試完成！")
    print("=" * 60)

if __name__ == '__main__':
    test_queries()

