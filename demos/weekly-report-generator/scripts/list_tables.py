"""
列出 BigQuery 資料集中的所有資料表
"""
import sys
import os
from google.cloud import bigquery

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.bigquery import BigQueryConfig

def list_tables():
    """列出所有資料集和資料表"""
    config = BigQueryConfig()
    client = config.get_client()
    
    print("=" * 60)
    print("BigQuery 資料集與資料表清單")
    print("=" * 60)
    print(f"專案 ID: {config.project_id}\n")
    
    # 列出所有資料集
    datasets = list(client.list_datasets())
    
    if not datasets:
        print("❌ 找不到任何資料集")
        return
    
    print(f"找到 {len(datasets)} 個資料集：\n")
    
    for dataset in datasets:
        dataset_id = dataset.dataset_id
        dataset_ref = client.dataset(dataset_id)
        
        print(f"📁 資料集: {dataset_id}")
        
        # 列出資料集中的所有資料表
        try:
            tables = list(client.list_tables(dataset_ref))
            
            if tables:
                print(f"   資料表 ({len(tables)} 個):")
                for table in tables[:20]:  # 最多顯示 20 個
                    print(f"     - {table.table_id}")
                if len(tables) > 20:
                    print(f"     ... 還有 {len(tables) - 20} 個資料表")
            else:
                print(f"   ⚠️  此資料集中沒有資料表")
                
        except Exception as e:
            print(f"   ❌ 無法列出資料表: {str(e)}")
        
        print()
    
    print("=" * 60)

if __name__ == '__main__':
    list_tables()

