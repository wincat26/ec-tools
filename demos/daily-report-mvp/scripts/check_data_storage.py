#!/usr/bin/env python3
"""
檢查資料存儲位置
"""
from google.cloud import bigquery

client = bigquery.Client(project='datalake360-saintpaul')

print('📊 資料存儲位置總覽')
print('=' * 60)
print()

datasets = list(client.list_datasets())
print(f'📁 專案：datalake360-saintpaul')
print(f'📁 資料集數量：{len(datasets)}')
print()

print('📋 主要資料集：')
for ds in datasets:
    try:
        tables = list(client.list_tables(ds.dataset_id))
        print(f'  • {ds.dataset_id} ({len(tables)} 個表)')
    except:
        print(f'  • {ds.dataset_id} (無法讀取)')

print()
print('📋 系統使用的資料來源：')
print('  • E-com 訂單：datalake_stpl.lv1_order_master')
print('  • GA4 事件：analytics_304437305.events_* (日期分區表)')
print('  • 廣告資料：待建立（目前使用 clients.yaml 手動輸入）')
print()
print('📋 資料更新頻率：')
print('  • E-com 訂單：每日自動同步')
print('  • GA4 事件：每日自動匯入（GA4 Export）')
print('  • 廣告資料：待建立（未來使用 MCP 自動匯入）')

