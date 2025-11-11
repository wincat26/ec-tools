"""
每日彙總資料生成模組
生成符合 PRD v1.1 規格的單行 JSON 資料
"""
import calendar
from datetime import date
from typing import Optional, Dict, Any
from src.data.fetcher import DataFetcher


class DailyAggregationGenerator:
    """每日彙總資料生成器"""
    
    def __init__(self, data_fetcher: DataFetcher):
        """
        初始化生成器
        
        Args:
            data_fetcher: 資料查詢器
        """
        self.data_fetcher = data_fetcher
    
    def generate(
        self, 
        client_id: str, 
        report_date: date, 
        monthly_target_revenue: int, 
        client_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        生成每日彙總單行 JSON 資料（效能優化版本）
        
        優化點：
        1. 重用已查詢的資料，減少重複的 BigQuery 查詢
        2. 簡化邏輯，提升可讀性
        3. 加入錯誤處理
        
        Args:
            client_id: 客戶 ID
            report_date: 數據所屬日期（T-1）
            monthly_target_revenue: 當月營收目標
            client_config: 客戶設定檔（用於廣告資料查詢）
            
        Returns:
            dict: 符合 PRD v1.1 規格的單行 JSON 資料
            
        Raises:
            ValueError: 當無法取得必要的資料時
        """
        from src.utils.date_utils import get_last_week_same_day
        
        # 1. 查詢當日指標（只查一次，現在已包含 sessions 和 cvr）
        daily_metrics = self.data_fetcher.fetch_daily_metrics(report_date)
        if not daily_metrics:
            raise ValueError(f"無法取得 {report_date} 的每日指標")
        
        revenue = daily_metrics['revenue']
        orders = daily_metrics['orders']
        aov = daily_metrics['aov']
        sessions = daily_metrics.get('sessions', 0) or self._fetch_sessions(report_date, client_config)
        cvr = daily_metrics.get('cvr', 0.0) or (orders / sessions if sessions > 0 else 0.0)
        
        # 2. 查詢上週同期資料（只查一次，重用於所有週變化計算）
        last_week_date = get_last_week_same_day(report_date)
        last_week_metrics = self.data_fetcher.fetch_daily_metrics(last_week_date)
        last_week_sessions = last_week_metrics.get('sessions', 0) or self._fetch_sessions(last_week_date, client_config)
        last_week_cvr = last_week_metrics.get('cvr', 0.0) or (last_week_metrics['orders'] / last_week_sessions if last_week_sessions > 0 else 0.0)
        
        # 5. 計算週變化（重用已查詢的資料）
        revenue_change_wow = (
            (revenue - last_week_metrics['revenue']) / last_week_metrics['revenue']
            if last_week_metrics['revenue'] > 0 else 0.0
        )
        cvr_change_wow = (
            (cvr - last_week_cvr) / last_week_cvr
            if last_week_cvr > 0 else 0.0
        )
        sessions_change_wow = (
            (sessions - last_week_sessions) / last_week_sessions
            if last_week_sessions > 0 else 0.0
        )
        aov_change_wow = (
            (aov - last_week_metrics['aov']) / last_week_metrics['aov']
            if last_week_metrics['aov'] > 0 else 0.0
        )
        
        # 6. 查詢廣告花費和 ROAS（優先使用 daily_metrics view 中的資料）
        # daily_metrics view 已包含 google_ads_cost_usd 和 meta_ads_spend
        total_ad_spend = daily_metrics.get('total_ad_spend')
        google_ads_spend = daily_metrics.get('google_ads_spend')
        meta_ads_spend = daily_metrics.get('meta_ads_spend')
        ad_spend, roas = self._fetch_ad_spend_and_roas(report_date, revenue, client_config, total_ad_spend)
        
        # 7. 查詢月迄今指標
        mtd_metrics = self.data_fetcher.fetch_mtd_metrics(report_date)
        if not mtd_metrics:
            raise ValueError(f"無法取得 {report_date} 的月迄今指標")
        
        mtd_revenue = mtd_metrics['mtd_revenue']
        
        # 8. 計算目標達成率
        mtd_achievement_rate = (
            mtd_revenue / monthly_target_revenue
            if monthly_target_revenue > 0 else 0.0
        )
        
        # 9. 計算預估當月營收（簡化月份天數計算）
        days_passed = report_date.day
        days_in_month = calendar.monthrange(report_date.year, report_date.month)[1]
        mtd_projected_revenue = (
            (mtd_revenue / days_passed * days_in_month)
            if days_passed > 0 else 0
        )
        
        # 10. 生成單行 JSON 資料（符合 PRD v1.1 規格）
        return {
            'client_id': client_id,
            'report_date': report_date.isoformat(),  # YYYY-MM-DD
            'monthly_target_revenue': monthly_target_revenue,
            # 當日指標
            'revenue': int(revenue),
            'orders': orders,
            'aov': round(aov, 2),
            'cvr': round(cvr, 4),  # 保留 4 位小數（例如 0.0150）
            'sessions': sessions,
            'ad_spend': int(ad_spend) if ad_spend is not None else None,
            'roas': round(roas, 2) if roas is not None else None,
            'google_ads_spend': int(google_ads_spend) if google_ads_spend is not None else None,
            'meta_ads_spend': int(meta_ads_spend) if meta_ads_spend is not None else None,
            # 當日 vs. 前期
            'revenue_change_wow': round(revenue_change_wow, 4),  # -0.15 表示下降 15%
            'cvr_change_wow': round(cvr_change_wow, 4),
            'sessions_change_wow': round(sessions_change_wow, 4),
            'aov_change_wow': round(aov_change_wow, 4),
            # 月迄今 MTD
            'mtd_revenue': int(mtd_revenue),
            'mtd_achievement_rate': round(mtd_achievement_rate, 4),  # 0.17 表示 17%
            'mtd_projected_revenue': int(mtd_projected_revenue),
        }
    
    def _fetch_ad_spend_and_roas(
        self, 
        report_date: date, 
        revenue: float, 
        client_config: Optional[Dict[str, Any]] = None,
        view_total_ad_spend: Optional[float] = None
    ) -> tuple[Optional[float], Optional[float]]:
        """
        查詢廣告花費和 ROAS（內部方法，重用已查詢的 revenue）
        
        優先順序：
        1. 從 daily_metrics view 取得總廣告花費（Google Ads + Meta Ads）
        2. 從客戶設定檔的手動輸入取得（降級方案）
        3. 如果都沒有，返回 None
        
        Args:
            report_date: 要查詢的日期（T-1）
            revenue: 已查詢的當日營收（避免重複查詢）
            client_config: 客戶設定檔（包含手動廣告資料，僅作為降級方案）
            view_total_ad_spend: 從 daily_metrics view 取得的總廣告花費（Google Ads + Meta Ads）
            
        Returns:
            tuple: (ad_spend, roas)，如果沒有資料則返回 (None, None)
        """
        # 優先順序 1：從 view 取得總廣告花費（已包含 Google Ads + Meta Ads）
        if view_total_ad_spend is not None and view_total_ad_spend > 0:
            roas = revenue / view_total_ad_spend if view_total_ad_spend > 0 else 0.0
            return view_total_ad_spend, roas
        
        # 優先順序 2：從客戶設定檔的手動輸入取得（降級方案）
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
                    roas = revenue / total_spend
                    return total_spend, roas
        
        # 如果都沒有，返回 None（表示沒有資料）
        return None, None
    
    def _fetch_sessions(
        self, 
        report_date: date, 
        client_config: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        查詢 GA4 sessions（優先使用手動設定，如果沒有則查詢 BigQuery）
        
        Args:
            report_date: 要查詢的日期（T-1）
            client_config: 客戶設定檔（包含手動 sessions 資料）
            
        Returns:
            int: sessions 數量
        """
        # 優先從客戶設定檔的手動輸入取得
        if client_config and 'ga4_data' in client_config:
            ga4_data = client_config.get('ga4_data', {})
            manual_sessions = ga4_data.get('manual_sessions', {})
            date_str = report_date.isoformat()
            
            if date_str in manual_sessions:
                return int(manual_sessions[date_str])
        
        # 如果沒有手動設定，從 BigQuery 查詢
        return self.data_fetcher.fetch_ga4_sessions(report_date)

