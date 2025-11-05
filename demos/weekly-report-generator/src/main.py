"""
週報生成器主程式
整合所有模組，生成完整的 HTML 週報
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 添加專案路徑到 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data import DataFetcher
from src.charts import ChartGenerator
from src.reports import ReportBuilder

load_dotenv()


def main():
    """主程式入口"""
    print("=" * 60)
    print("電商週報生成器 - 開始執行")
    print("=" * 60)
    
    # 初始化模組
    fetcher = DataFetcher()
    chart_gen = ChartGenerator()
    report_builder = ReportBuilder()
    
    # 設定參數
    from src.utils.date_utils import get_last_week_range
    brand_name = os.getenv('BRAND_NAME', '豆油伯')
    
    # 計算上週範圍（上週一到上週日）- 這是觀察週
    report_monday, report_sunday = get_last_week_range()
    
    print(f"\n📊 查詢參數：")
    print(f"   - 時間範圍：上週（{report_monday} 至 {report_sunday}）")
    print(f"   - 品牌名稱：{brand_name}")
    print(f"   - 查詢時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 查詢資料
    print(f"\n🔍 步驟 1/4：查詢 BigQuery 資料...")
    
    try:
        # GMV 基本指標（上週週一到週日）
        print("   - 查詢 GMV 基本指標...")
        gmv_metrics = fetcher.fetch_gmv_metrics(report_monday, report_sunday)
        
        # 本週關鍵摘要（上週與上上週比較）
        print("   - 查詢上週關鍵摘要...")
        weekly_comparison = fetcher.fetch_weekly_comparison()
        
        # 流量分析（上週週一到週日）
        print("   - 查詢流量分析...")
        traffic_df = fetcher.fetch_traffic_analysis(report_monday, report_sunday)
        
        # AOV 分析（上週週一到週日）
        print("   - 查詢 AOV 分析...")
        aov_data = fetcher.fetch_aov_analysis(report_monday, report_sunday, dimension='overall')
        
        # 轉換漏斗（上週週一到週日）
        print("   - 查詢轉換漏斗...")
        funnel_data = fetcher.fetch_conversion_funnel(report_monday, report_sunday)
        
        print("   ✅ 資料查詢完成")
        
    except Exception as e:
        print(f"   ❌ 資料查詢失敗：{str(e)}")
        return
    
    # 2. 生成圖表
    print(f"\n📈 步驟 2/4：生成 PyEcharts 圖表...")
    
    charts = {}
    
    try:
        # 本週關鍵摘要圖表
        print("   - 生成本週關鍵摘要圖表...")
        charts['weekly_comparison'] = chart_gen.generate_weekly_comparison_chart(weekly_comparison)
        
        # 流量來源圖表
        print("   - 生成流量來源圖表...")
        charts['traffic_source'] = chart_gen.generate_traffic_source_chart(traffic_df)
        
        # AOV 分布圖表
        print("   - 生成 AOV 分布圖表...")
        charts['aov_distribution'] = chart_gen.generate_aov_distribution_chart(aov_data)
        
        # 轉換漏斗圖表
        print("   - 生成轉換漏斗圖表...")
        charts['conversion_funnel'] = chart_gen.generate_conversion_funnel_chart(funnel_data)
        
        print("   ✅ 圖表生成完成")
        
    except Exception as e:
        print(f"   ❌ 圖表生成失敗：{str(e)}")
        return
    
    # 3. 組合資料字典
    print(f"\n📦 步驟 3/4：組合資料...")
    
    data_dict = {
        'gmv_metrics': gmv_metrics,
        'weekly_comparison': weekly_comparison,
        'traffic_analysis': traffic_df.to_dict('records') if not traffic_df.empty else [],
        'aov_analysis': aov_data,
        'funnel_data': funnel_data,
        'report_period': {
            'start_date': report_monday.strftime('%Y-%m-%d'),
            'end_date': report_sunday.strftime('%Y-%m-%d'),
        }
    }
    
    # 4. 生成 HTML 報告
    print(f"\n📄 步驟 4/4：生成 HTML 報告...")
    
    try:
        report_path = report_builder.build_report(
            data_dict=data_dict,
            charts_dict=charts,
            brand_name=brand_name,
        )
        
        print(f"   ✅ 報告生成完成")
        print(f"\n📁 報告檔案位置：{os.path.abspath(report_path)}")
        
        print(f"\n" + "=" * 60)
        print("✅ 週報生成完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"   ❌ 報告生成失敗：{str(e)}")
        return


if __name__ == '__main__':
    main()

