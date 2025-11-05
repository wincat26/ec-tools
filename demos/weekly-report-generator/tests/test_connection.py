"""
BigQuery 連線測試腳本
用於驗證 BigQuery 認證與資料表存取是否正常
"""
import sys
import os
from google.cloud import bigquery

# 添加專案路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.bigquery import BigQueryConfig, TABLES


def test_connection():
    """測試 BigQuery 連線"""
    print("=" * 60)
    print("BigQuery 連線測試")
    print("=" * 60)
    
    try:
        # 初始化配置
        config = BigQueryConfig()
        client = config.get_client()
        
        print(f"\n✅ BigQuery 客戶端初始化成功")
        print(f"   - 專案 ID: {config.project_id}")
        print(f"   - 資料集: {config.dataset_id}")
        
        # 測試查詢
        print(f"\n🔍 測試查詢資料表...")
        
        for table_name, table_id in TABLES.items():
            try:
                table_ref = config.get_table_ref(table_id)
                query = f"SELECT COUNT(*) as count FROM `{table_ref}` LIMIT 1"
                
                # 使用 config 的 query 方法（確保專案設定正確）
                query_job = config.query(query)
                result = query_job.to_dataframe()
                
                if not result.empty:
                    count = result.iloc[0]['count']
                    print(f"   ✅ {table_name} ({table_id}): {count:,} 筆記錄")
                else:
                    print(f"   ⚠️  {table_name} ({table_id}): 資料表為空")
                    
            except Exception as e:
                print(f"   ❌ {table_name} ({table_id}): 查詢失敗 - {str(e)}")
        
        print(f"\n" + "=" * 60)
        print("✅ 連線測試完成！")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 連線失敗：{str(e)}")
        print("\n💡 請檢查：")
        print("   1. 是否已設定 GOOGLE_APPLICATION_CREDENTIALS 環境變數")
        print("   2. 或執行 gcloud auth application-default login")
        print("   3. 確認服務帳號有 BigQuery 讀取權限")
        return False


if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

