"""
每日數據彙整日報主程式
執行流程：
1. 讀取客戶設定
2. GA4 數據驗證（前置檢查）
3. 查詢 BigQuery 資料
4. 生成單行 JSON 資料
5. 推播通知（Google Chat、LINE）
"""
import argparse
import os
import sys
from datetime import date
from config.bigquery import BigQueryConfig
from src.config.client_config import ClientConfig
from src.config.target_config import TargetConfig
from src.data.validator import GA4DataValidator
from src.data.fetcher import DataFetcher
from src.generator.daily_aggregation import DailyAggregationGenerator
from src.notification.google_chat import GoogleChatNotifier
from src.notification.line_notify import LineNotifier
from src.utils.date_utils import get_yesterday


def main():
    """主程式入口"""
    parser = argparse.ArgumentParser(description='每日數據彙整日報 - MVP v1.1')
    parser.add_argument(
        '--client',
        type=str,
        required=True,
        help='客戶 ID（必須在 config/clients.yaml 中設定）'
    )
    parser.add_argument(
        '--date',
        type=str,
        default=None,
        help='要彙整的日期（YYYY-MM-DD），預設為昨日（T-1）'
    )
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='跳過 GA4 數據驗證（僅用於測試）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='乾跑模式：只生成資料，不發送推播'
    )
    
    args = parser.parse_args()
    
    # 解析日期
    if args.date:
        try:
            report_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"❌ 錯誤：日期格式不正確，應為 YYYY-MM-DD")
            sys.exit(1)
    else:
        report_date = get_yesterday()
    
    print(f"🚀 開始執行每日數據彙整日報")
    print(f"📅 報告日期：{report_date}")
    print(f"👤 客戶 ID：{args.client}")
    print("-" * 50)
    
    # 步驟 1: 讀取客戶設定
    try:
        client_config = ClientConfig()
        client = client_config.get_client(args.client)
        
        if not client:
            print(f"❌ 錯誤：找不到客戶 '{args.client}'")
            print(f"💡 可用的客戶：{', '.join(client_config.list_clients())}")
            sys.exit(1)
        
        print(f"✅ 客戶設定載入成功")
        
        # 提取設定
        bq_config = client['bigquery']
        webhook_url = client['google_chat_webhook']
        client_config = client  # 保存完整客戶設定，供廣告資料查詢使用
        
        # 步驟 1.5: 讀取目標設定（動態月份目標）
        try:
            target_config = TargetConfig()
            # 根據報告日期取得當月目標（優先使用目標檔）
            monthly_target = target_config.get_monthly_target(
                report_date,
                default=client.get('monthly_target_revenue')  # 如果找不到，使用客戶設定檔的預設值
            )
            
            if monthly_target is None:
                print(f"⚠️  警告：找不到 {report_date.strftime('%Y-%m')} 的目標設定，且客戶設定檔中沒有預設值")
                print(f"💡 請在 config/targets.yaml 中設定，或在 config/clients.yaml 中設定 monthly_target_revenue")
                sys.exit(1)
            
            print(f"✅ 目標設定載入成功：{report_date.strftime('%Y-%m')} 目標 ${monthly_target:,}")
            
        except Exception as e:
            print(f"⚠️  警告：無法載入目標設定檔 - {str(e)}")
            # 如果目標檔讀取失敗，使用客戶設定檔的預設值
            monthly_target = client.get('monthly_target_revenue')
            if monthly_target is None:
                print(f"❌ 錯誤：找不到目標設定，請在 config/targets.yaml 或 config/clients.yaml 中設定")
                sys.exit(1)
            print(f"✅ 使用客戶設定檔的預設目標：${monthly_target:,}")
        
    except Exception as e:
        print(f"❌ 錯誤：無法載入客戶設定 - {str(e)}")
        sys.exit(1)
    
    # 步驟 2: 初始化 BigQuery 配置
    try:
        bq = BigQueryConfig(
            project_id=bq_config['project_id'],
            dataset_id=bq_config['dataset_id'],
            ga4_dataset=bq_config['ga4_dataset']
        )
        print(f"✅ BigQuery 連線成功")
    except Exception as e:
        print(f"❌ 錯誤：BigQuery 連線失敗 - {str(e)}")
        sys.exit(1)
    
    ga4_warning_note: str | None = None
    # 步驟 3: GA4 數據驗證（前置檢查）
    if not args.skip_validation:
        print(f"🔍 執行 GA4 數據驗證...")
        validator = GA4DataValidator(bq)
        status, message = validator.validate_ga4_data(report_date)

        if status == "ok":
            print(f"✅ {message}")
        elif status == "warning":
            print(f"⚠️ {message}")
            ga4_warning_note = message
        else:
            print(f"⚠️ GA4 數據驗證失敗：{message}")
            ga4_warning_note = message
    else:
        print(f"⚠️  跳過 GA4 數據驗證（--skip-validation）")
    
    # 步驟 4: 查詢 BigQuery 資料
    print(f"📊 查詢 BigQuery 資料...")
    try:
        fetcher = DataFetcher(bq)
        generator = DailyAggregationGenerator(fetcher)
        
        # 生成單行 JSON 資料（傳入客戶設定以取得廣告資料）
        daily_data = generator.generate(
            client_id=args.client,
            report_date=report_date,
            monthly_target_revenue=monthly_target,
            client_config=client_config  # 傳入客戶設定
        )

        brand_name = client.get("brand_name")
        if brand_name:
            daily_data["brand_name"] = brand_name

        if ga4_warning_note:
            daily_data['ga4_warning'] = ga4_warning_note
        
        print(f"✅ 資料生成成功")
        print(f"   - 營收：${daily_data['revenue']:,}")
        print(f"   - 訂單：{daily_data['orders']:,} 筆")
        print(f"   - CVR：{daily_data['cvr']*100:.2f}%")
        print(f"   - Sessions：{daily_data['sessions']:,}")
        print(f"   - 目標達成率：{daily_data['mtd_achievement_rate']*100:.1f}%")
        
    except Exception as e:
        print(f"❌ 錯誤：資料查詢失敗 - {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # 步驟 5: 推播到 Google Chat / LINE
    if args.dry_run:
        print(f"⚠️  乾跑模式：不發送推播")
        print(f"📋 生成的資料（JSON）：")
        import json
        print(json.dumps(daily_data, indent=2, ensure_ascii=False))
    else:
        # Google Chat
        print(f"📤 發送 Google Chat 推播...")
        try:
            notifier = GoogleChatNotifier(webhook_url)
            success, message = notifier.send(daily_data)
            if success:
                print(f"✅ Google Chat：{message}")
            else:
                print(f"❌ Google Chat：{message}")
        except Exception as e:
            print(f"❌ Google Chat 推播失敗 - {str(e)}")
            import traceback
            traceback.print_exc()
        
        # LINE 推播（若環境變數設定）
        line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
        line_targets_env = os.environ.get("LINE_TARGET_IDS")
        line_targets = [t.strip() for t in line_targets_env.split(",")] if line_targets_env else []
        if line_token and line_targets:
            print(f"📤 發送 LINE 推播...")
            try:
                line_notifier = LineNotifier(
                    access_token=line_token,
                    target_ids=line_targets,
                    dashboard_url=os.environ.get("LINE_DASHBOARD_URL"),
                    brand_name=brand_name,
                )
                line_success, line_message = line_notifier.send(daily_data)
                if line_success:
                    print(f"✅ LINE：{line_message}")
                else:
                    print(f"❌ LINE：{line_message}")
            except Exception as e:
                print(f"❌ LINE 推播失敗 - {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print("ℹ️  LINE 推播未啟用（缺少 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_TARGET_IDS）")
    
    print("-" * 50)
    print(f"🎉 執行完成！")


if __name__ == '__main__':
    main()

