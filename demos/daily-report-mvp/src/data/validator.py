"""
GA4 數據驗證模組
執行前置檢查，確認 GA4 數據是否已匯入
"""
from datetime import date
from config.bigquery import BigQueryConfig


class GA4DataValidator:
    """GA4 數據驗證器"""
    
    def __init__(self, bq_config: BigQueryConfig):
        """
        初始化驗證器
        
        Args:
            bq_config: BigQuery 配置物件
        """
        self.bq_config = bq_config
    
    def validate_ga4_data(self, report_date: date):
        """
        验证指定日期的 GA4 sessions 数据是否已同步（使用 daily_metrics view）

        Args:
            report_date: 要驗證的日期（T-1）

        Returns:
            tuple[str, str]: (狀態, 訊息)
                - "ok": 資料同步正常
                - "warning": 資料尚未同步，但不中斷流程
                - "error": 發生例外錯誤
        """
        try:
            daily_metrics_view = f"{self.bq_config.project_id}.datalake_looker.daily_metrics"
            query = f"""
            SELECT
                total_sessions,
                conversion_rate_pct
            FROM `{daily_metrics_view}`
            WHERE date = DATE('{report_date.isoformat()}')
            LIMIT 1
            """

            result = self.bq_config.query(query).to_dataframe()

            if result.empty:
                return "warning", f"GA4 數據尚未同步（daily_metrics 尚無 {report_date} 資料）"

            sessions = result.iloc[0].get('total_sessions')

            if sessions in (None, 0):
                return "warning", f"GA4 數據尚未同步（sessions 為 {sessions or 'N/A'}）"

            return "ok", f"GA4 數據已同步：sessions={int(sessions):,}"

        except Exception as e:
            return "error", f"GA4 數據驗證失敗：{str(e)}"

