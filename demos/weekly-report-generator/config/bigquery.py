"""
BigQuery 連線與查詢設定
"""
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()


class BigQueryConfig:
    """BigQuery 連線設定"""
    
    def __init__(self):
        # 正確的專案 ID 和資料集
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'datalake360-saintpaul')
        self.dataset_id = os.getenv('BIGQUERY_DATASET', 'datalake_stpl')
        self.ga4_dataset = 'analytics_304437305'  # GA4 事件資料集
        self.client = None
        
        # 設定 quota project 環境變數（解決 ProjectId must be non-empty 錯誤）
        if 'GOOGLE_CLOUD_QUOTA_PROJECT' not in os.environ:
            os.environ['GOOGLE_CLOUD_QUOTA_PROJECT'] = self.project_id
        
    def get_client(self):
        """取得 BigQuery 客戶端實例"""
        if self.client is None:
            # 確保專案 ID 不為空
            if not self.project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT 環境變數未設定，請設定專案 ID")
            
            # 建立客戶端，明確指定專案（不指定位置，讓 BigQuery 自動偵測資料集位置）
            # 注意：查詢時會根據資料集的實際位置自動路由
            self.client = bigquery.Client(project=self.project_id)
        return self.client
    
    def query(self, query_string, location=None, **kwargs):
        """
        執行查詢的輔助方法，確保專案設定正確
        
        Args:
            query_string: SQL 查詢字串
            location: 查詢位置（可選，預設讓 BigQuery 自動偵測）
            **kwargs: 其他查詢參數
            
        Returns:
            QueryJob: 查詢作業物件
        """
        client = self.get_client()
        job_config = bigquery.QueryJobConfig()
        if location:
            job_config.location = location
        return client.query(query_string, job_config=job_config, **kwargs)
    
    def get_table_ref(self, table_name, dataset=None):
        """
        取得資料表完整路徑
        
        Args:
            table_name: 資料表名稱
            dataset: 資料集名稱（預設使用 self.dataset_id）
            
        Returns:
            str: 完整的資料表路徑
        """
        if dataset is None:
            dataset = self.dataset_id
        return f"{self.project_id}.{dataset}.{table_name}"
    
    def get_ga4_table_ref(self, table_name):
        """取得 GA4 事件表完整路徑"""
        return self.get_table_ref(table_name, dataset=self.ga4_dataset)


# 常用資料表名稱（對應到 datalake_stpl 資料集）
# 注意：實際資料表名稱與預期不同，需要根據實際結構調整查詢
TABLES = {
    # Level 0 原始資料表
    'lv0_orders': 'lv0_orders',
    'lv0_customers': 'lv0_customers',
    'lv0_products': 'lv0_products',
    'lv0_channels': 'lv0_channels',
    
    # Level 1 處理後資料表
    'lv1_order': 'lv1_order',
    'lv1_order_master': 'lv1_order_master',
    'lv1_user': 'lv1_user',
    'lv1_product': 'lv1_product',
    'lv1_touch': 'lv1_touch',  # 可能包含 GA4 整合資料
    'lv1_event': 'lv1_event',
    
    # 舊的資料表名稱（保留作為參考，可能需要從新表計算）
    'orders_summary_daily': None,  # 需要從 lv1_order 計算
    'orders': 'lv1_order',  # 使用 lv1_order
    'order_ga4_integration': None,  # 需要從 lv1_touch 或 lv1_event JOIN
    'product_insights_daily': None,  # 需要從 lv1_product 計算
}

# GA4 事件表（對應到 analytics_304437305 資料集）
GA4_TABLES = {
    'events': 'events_*',  # 使用萬用字元匹配所有日期分區表
}

