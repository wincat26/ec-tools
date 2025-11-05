"""
檢查關鍵資料表的 Schema（欄位名稱）
"""
import sys
import os
from google.cloud import bigquery

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.bigquery import BigQueryConfig

def check_schema(table_name, dataset='datalake_stpl'):
    """檢查資料表的 Schema"""
    config = BigQueryConfig()
    client = config.get_client()
    
    table_ref = client.get_table(f"{config.project_id}.{dataset}.{table_name}")
    
    print(f"\n{'='*60}")
    print(f"📊 資料表: {dataset}.{table_name}")
    print(f"{'='*60}")
    print(f"建立時間: {table_ref.created}")
    print(f"最後修改: {table_ref.modified}")
    print(f"記錄數: {table_ref.num_rows:,}" if table_ref.num_rows else "記錄數: 未知")
    print(f"\n欄位 (共 {len(table_ref.schema)} 個):\n")
    
    for i, field in enumerate(table_ref.schema, 1):
        field_type = field.field_type
        mode = field.mode if field.mode else 'NULLABLE'
        print(f"  {i:2d}. {field.name:30s} | {field_type:15s} | {mode}")
        if field.description:
            print(f"      說明: {field.description}")
    
    print(f"\n{'='*60}\n")

def main():
    """檢查主要資料表的 Schema"""
    print("🔍 檢查關鍵資料表的 Schema\n")
    
    # 檢查主要資料表
    tables_to_check = [
        ('lv1_order', 'datalake_stpl'),
        ('lv1_order_master', 'datalake_stpl'),
        ('lv1_touch', 'datalake_stpl'),
        ('lv1_user', 'datalake_stpl'),
        ('lv1_product', 'datalake_stpl'),
    ]
    
    for table_name, dataset in tables_to_check:
        try:
            check_schema(table_name, dataset)
        except Exception as e:
            print(f"❌ 無法取得 {dataset}.{table_name} 的 Schema: {str(e)}\n")

if __name__ == '__main__':
    main()

