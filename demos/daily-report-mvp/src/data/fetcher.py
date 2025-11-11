"""
BigQuery 資料查詢模組
負責從 BigQuery 查詢 E-com 和 GA4 資料
"""
from datetime import date
from config.bigquery import BigQueryConfig, TABLES
from src.utils.date_utils import format_date_for_sql, format_date_for_ga4, get_last_week_same_day


class DataFetcher:
    """資料查詢器"""
    
    def __init__(self, bq_config: BigQueryConfig):
        """
        初始化資料查詢器
        
        Args:
            bq_config: BigQuery 配置物件
        """
        self.bq_config = bq_config
    
    def fetch_daily_metrics(self, report_date: date) -> dict:
        """
        查詢指定日期的關鍵指標（使用 datalake_looker.daily_metrics view）
        
        Args:
            report_date: 要查詢的日期（T-1）
            
        Returns:
            dict: 包含 revenue, orders, aov, cvr 等指標
        """
        # 使用 datalake_looker.daily_metrics view
        date_str = format_date_for_sql(report_date)
        daily_metrics_view = f"{self.bq_config.project_id}.datalake_looker.daily_metrics"
        
        query = f"""
        SELECT
            total_revenue as revenue,
            total_orders as orders,
            avg_order_value as aov,
            conversion_rate_pct,
            total_sessions as sessions,
            google_ads_cost_usd,
            meta_ads_spend
        FROM `{daily_metrics_view}`
        WHERE date = DATE('{date_str}')
        LIMIT 1
        """
        
        result = self.bq_config.query(query).to_dataframe()
        
        if result.empty or result.iloc[0].get('revenue') is None:
            return {
                'revenue': 0,
                'orders': 0,
                'aov': 0.0,
                'sessions': 0,
                'cvr': 0.0,
                'google_ads_spend': None,
                'meta_ads_spend': None,
                'total_ad_spend': None,
            }
        
        row = result.iloc[0]
        revenue = float(row.get('revenue') or 0)
        orders = int(row.get('orders') or 0)
        aov = float(row.get('aov') or 0)
        sessions = int(row.get('sessions') or 0)
        # conversion_rate_pct 是百分比，需要轉換為小數（例如 1.71% -> 0.0171）
        conversion_rate_pct = float(row.get('conversion_rate_pct') or 0)
        cvr = conversion_rate_pct / 100.0 if conversion_rate_pct else 0.0
        
        # 廣告花費（從 view 取得）
        google_ads_spend = float(row.get('google_ads_cost_usd') or 0) if row.get('google_ads_cost_usd') is not None else None
        meta_ads_spend = float(row.get('meta_ads_spend') or 0) if row.get('meta_ads_spend') is not None else None
        
        # 計算總廣告花費
        total_ad_spend = None
        if google_ads_spend is not None or meta_ads_spend is not None:
            total_ad_spend = (google_ads_spend or 0) + (meta_ads_spend or 0)
            if total_ad_spend == 0:
                total_ad_spend = None
        
        return {
            'revenue': revenue,
            'orders': orders,
            'aov': aov,
            'sessions': sessions,
            'cvr': cvr,
            'google_ads_spend': google_ads_spend,
            'meta_ads_spend': meta_ads_spend,
            'total_ad_spend': total_ad_spend,
        }
    
    def fetch_ga4_sessions(self, report_date: date) -> int:
        """
        查詢指定日期的 GA4 sessions（優先使用 daily_metrics view）
        
        Args:
            report_date: 要查詢的日期（T-1）
            
        Returns:
            int: sessions 數量
        """
        # 優先從 daily_metrics view 取得（已包含在 fetch_daily_metrics 中）
        # 如果 view 沒有資料，降級到原本的 GA4 查詢
        try:
            daily_metrics = self.fetch_daily_metrics(report_date)
            if daily_metrics.get('sessions', 0) > 0:
                return daily_metrics['sessions']
        except:
            pass
        
        # 降級方案：從 GA4 事件表查詢
        ga4_table_ref = self.bq_config.get_ga4_table_ref('events_*')
        date_suffix = format_date_for_ga4(report_date)
        
        query = f"""
        SELECT
            COUNT(DISTINCT CONCAT(
                user_pseudo_id,
                '-',
                COALESCE(
                    CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS STRING),
                    CAST((SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'session_id') AS STRING),
                    ''
                )
            )) as sessions
        FROM `{ga4_table_ref}`
        WHERE _TABLE_SUFFIX = '{date_suffix}'
            AND event_name = 'session_start'
        """
        
        result = self.bq_config.query(query).to_dataframe()
        
        if result.empty:
            return 0
        
        return int(result.iloc[0].get('sessions', 0) or 0)
    
    def fetch_cvr(self, report_date: date, sessions: int = None) -> float:
        """
        計算轉換率（CVR）
        
        Args:
            report_date: 要查詢的日期（T-1）
            sessions: GA4 sessions 數量（可選，如果提供則使用，否則從 daily_metrics 取得）
            
        Returns:
            float: CVR（轉換率，0-1 之間）
        """
        # 優先從 daily_metrics view 取得 CVR（已計算好）
        daily_metrics = self.fetch_daily_metrics(report_date)
        if daily_metrics.get('cvr', 0) > 0:
            return daily_metrics['cvr']
        
        # 降級方案：手動計算
        if sessions is None:
            sessions = self.fetch_ga4_sessions(report_date)
        
        if sessions == 0:
            return 0.0
        
        orders = daily_metrics['orders']
        return orders / sessions if sessions > 0 else 0.0
    
    def fetch_ad_spend_and_roas(self, report_date: date, client_config: dict = None) -> tuple[float, float]:
        """
        查詢廣告花費和 ROAS（優先使用 daily_metrics view）
        
        優先順序：
        1. 從 daily_metrics view 取得（Google Ads + Meta Ads）
        2. 從客戶設定檔的手動輸入取得（降級方案）
        
        Args:
            report_date: 要查詢的日期（T-1）
            client_config: 客戶設定檔（包含手動廣告資料，僅作為降級方案）
            
        Returns:
            tuple[float, float]: (ad_spend, roas)
        """
        # 優先從 daily_metrics view 取得
        daily_metrics = self.fetch_daily_metrics(report_date)
        total_ad_spend = daily_metrics.get('total_ad_spend')
        
        if total_ad_spend is not None and total_ad_spend > 0:
            revenue = daily_metrics['revenue']
            roas = revenue / total_ad_spend if total_ad_spend > 0 else 0.0
            return total_ad_spend, roas
        
        # 降級方案：從客戶設定檔的手動輸入取得
        if client_config and 'ad_data' in client_config:
            ad_data = client_config.get('ad_data', {})
            manual_ad_spend = ad_data.get('manual_ad_spend', {})
            date_str = report_date.isoformat()
            
            if date_str in manual_ad_spend:
                manual_data = manual_ad_spend[date_str]
                meta_spend = float(manual_data.get('meta_ads', 0))
                google_spend = float(manual_data.get('google_ads', 0))
                total_spend = meta_spend + google_spend
                
                if total_spend > 0:
                    revenue = daily_metrics['revenue']
                    roas = revenue / total_spend if total_spend > 0 else 0.0
                    return total_spend, roas
        
        # 如果都沒有，返回 None（表示沒有資料）
        return None, None
    
    def fetch_weekly_comparison(self, report_date: date, metric: str) -> float:
        """
        計算與上週同期的變化百分比
        
        Args:
            report_date: 要查詢的日期（T-1）
            metric: 指標名稱（'revenue' 或 'cvr'）
            
        Returns:
            float: 變化百分比（-1.0 到 1.0 之間，例如 -0.15 表示下降 15%）
        """
        last_week_date = get_last_week_same_day(report_date)
        
        if metric == 'revenue':
            current_value = self.fetch_daily_metrics(report_date)['revenue']
            last_week_value = self.fetch_daily_metrics(last_week_date)['revenue']
        elif metric == 'cvr':
            current_sessions = self.fetch_ga4_sessions(report_date)
            last_week_sessions = self.fetch_ga4_sessions(last_week_date)
            current_value = self.fetch_cvr(report_date, current_sessions)
            last_week_value = self.fetch_cvr(last_week_date, last_week_sessions)
        else:
            raise ValueError(f"不支援的指標：{metric}")
        
        if last_week_value == 0:
            return 1.0 if current_value > 0 else 0.0
        
        return (current_value - last_week_value) / last_week_value
    
    def fetch_mtd_metrics(self, report_date: date) -> dict:
        """
        查詢月迄今（MTD）指標（使用 datalake_looker.daily_metrics view）
        
        Args:
            report_date: 要查詢的日期（T-1）
            
        Returns:
            dict: 包含 mtd_revenue, mtd_achievement_rate, mtd_projected_revenue
        """
        # 計算月初日期
        month_start = date(report_date.year, report_date.month, 1)
        date_str_start = format_date_for_sql(month_start)
        date_str_end = format_date_for_sql(report_date)
        
        daily_metrics_view = f"{self.bq_config.project_id}.datalake_looker.daily_metrics"
        
        query = f"""
        SELECT
            mtd_revenue,
            mtd_total_revenue
        FROM `{daily_metrics_view}`
        WHERE date = DATE('{date_str_end}')
        LIMIT 1
        """
        
        result = self.bq_config.query(query).to_dataframe()
        
        if result.empty:
            mtd_revenue = 0.0
            mtd_total_revenue = 0.0
        else:
            row = result.iloc[0]
            mtd_revenue = float(row.get('mtd_revenue', 0) or 0)
            mtd_total_revenue = float(row.get('mtd_total_revenue', 0) or 0)
        
        return {
            'mtd_revenue': mtd_revenue,
            'mtd_total_revenue': mtd_total_revenue,
        }

