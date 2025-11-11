"""
BigQuery 連線與查詢設定
支援多客戶配置
"""
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()


class BigQueryConfig:
    """BigQuery 連線設定（支援多客戶）"""
    
    def __init__(self, project_id=None, dataset_id=None, ga4_dataset=None):
        """
        初始化 BigQuery 配置
        
        Args:
            project_id: Google Cloud 專案 ID（預設從環境變數讀取）
            dataset_id: E-com 資料集 ID（預設從環境變數讀取）
            ga4_dataset: GA4 資料集 ID（預設從環境變數讀取）
        """
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT', 'datalake360-saintpaul')
        self.dataset_id = dataset_id or os.getenv('BIGQUERY_DATASET', 'datalake_stpl')
        self.ga4_dataset = ga4_dataset or os.getenv('GA4_DATASET', 'analytics_304437305')
        self.client = None
        
        # 設定 quota project 環境變數（解決 ProjectId must be non-empty 錯誤）
        if 'GOOGLE_CLOUD_QUOTA_PROJECT' not in os.environ:
            os.environ['GOOGLE_CLOUD_QUOTA_PROJECT'] = self.project_id
        
    def get_client(self):
        """取得 BigQuery 客戶端實例"""
        if self.client is None:
            if not self.project_id:
                raise ValueError("專案 ID 未設定，請提供 project_id 或設定 GOOGLE_CLOUD_PROJECT 環境變數")
            
            self.client = bigquery.Client(project=self.project_id)
        return self.client
    
    def query(self, query_string, location=None, **kwargs):
        """
        執行查詢的輔助方法
        
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
TABLES = {
    'lv1_order_master': 'lv1_order_master',  # 訂單主檔
    'lv1_order': 'lv1_order',  # 訂單明細
    'lv1_user': 'lv1_user',
    'lv1_product': 'lv1_product',
}

