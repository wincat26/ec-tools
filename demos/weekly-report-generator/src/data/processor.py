"""
資料處理與計算模組
負責從原始資料計算衍生指標（KPI）
"""
import pandas as pd
from datetime import datetime, timedelta


class DataProcessor:
    """資料處理器"""
    
    @staticmethod
    def calculate_cvr(sessions, conversions):
        """
        計算轉換率
        
        Args:
            sessions: 工作階段數
            conversions: 轉換數
            
        Returns:
            float: 轉換率（百分比）
        """
        if sessions == 0:
            return 0.0
        return round((conversions / sessions) * 100, 2)
    
    @staticmethod
    def calculate_aov(revenue, orders):
        """
        計算平均訂單金額
        
        Args:
            revenue: 總營收
            orders: 訂單數
            
        Returns:
            float: 平均訂單金額
        """
        if orders == 0:
            return 0.0
        return round(revenue / orders, 2)
    
    @staticmethod
    def calculate_change_percentage(current, previous):
        """
        計算變化百分比
        
        Args:
            current: 當前值
            previous: 先前值
            
        Returns:
            float: 變化百分比（正數表示成長，負數表示下降）
        """
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 2)
    
    @staticmethod
    def format_currency(amount):
        """
        格式化金額顯示
        
        Args:
            amount: 金額數值
            
        Returns:
            str: 格式化後的字串（例如：NT$ 1,234,567）
        """
        return f"NT$ {amount:,.0f}"
    
    @staticmethod
    def format_percentage(value, decimals=2):
        """
        格式化百分比顯示
        
        Args:
            value: 百分比數值
            decimals: 小數位數
            
        Returns:
            str: 格式化後的字串（例如：12.34%）
        """
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def categorize_traffic_source(channel):
        """
        將 BigQuery 的 last_touch_channel 對應到 8 種分類
        
        Args:
            channel: BigQuery 的 last_touch_channel 值
            
        Returns:
            str: 對應的分類名稱
        """
        # 流量來源對應規則
        mapping = {
            # 直接流量
            'Direct': '直接流量',
            'direct': '直接流量',
            
            # 付費廣告
            'Paid Search': '付費廣告',
            'Paid Social': '付費廣告',
            'Display': '付費廣告',
            'paid_search': '付費廣告',
            'cpc': '付費廣告',
            
            # 自然搜尋
            'Organic Search': '自然搜尋',
            'organic': '自然搜尋',
            'organic_search': '自然搜尋',
            
            # 社群經營
            'Social': '社群經營',
            'social': '社群經營',
            'facebook': '社群經營',
            'instagram': '社群經營',
            'line': '社群經營',
            
            # 參照連結
            'Referral': '參照連結',
            'referral': '參照連結',
            
            # 會員經營（Email）
            'Email': '會員經營',
            'email': '會員經營',
            'mail': '會員經營',
            
            # AI 來源（需要根據實際情況調整）
            'AI': 'AI 來源',
            'ai': 'AI 來源',
        }
        
        return mapping.get(channel, '其他')
    
    @staticmethod
    def aggregate_traffic_by_category(df):
        """
        將流量資料按 8 種分類聚合
        
        Args:
            df: 包含 traffic_source 欄位的 DataFrame
            
        Returns:
            DataFrame: 聚合後的資料
        """
        if df.empty:
            return df
        
        # 應用分類對應
        df['category'] = df['traffic_source'].apply(
            DataProcessor.categorize_traffic_source
        )
        
        # 按分類聚合
        aggregated = df.groupby('category').agg({
            'sessions': 'sum',
            'conversions': 'sum',
            'revenue': 'sum',
        }).reset_index()
        
        # 計算衍生指標
        aggregated['cvr'] = aggregated.apply(
            lambda row: DataProcessor.calculate_cvr(row['sessions'], row['conversions']),
            axis=1
        )
        
        aggregated['aov'] = aggregated.apply(
            lambda row: DataProcessor.calculate_aov(row['revenue'], row['conversions']),
            axis=1
        )
        
        # 重新命名欄位
        aggregated.rename(columns={'category': 'traffic_source'}, inplace=True)
        
        return aggregated.sort_values('revenue', ascending=False)

