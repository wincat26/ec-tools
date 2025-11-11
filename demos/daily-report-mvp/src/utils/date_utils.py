"""
日期工具函數
"""
from datetime import datetime, date, timedelta


def get_yesterday() -> date:
    """
    取得昨日日期（T-1）
    
    Returns:
        date: 昨日日期
    """
    return date.today() - timedelta(days=1)


def get_last_week_same_day(target_date: date) -> date:
    """
    取得上週同一天日期
    
    Args:
        target_date: 目標日期
        
    Returns:
        date: 上週同一天日期
    """
    return target_date - timedelta(days=7)


def format_date_for_sql(date_obj: date) -> str:
    """
    格式化日期為 SQL 日期字串
    
    Args:
        date_obj: 日期物件
        
    Returns:
        str: SQL 日期字串（YYYY-MM-DD）
    """
    return date_obj.strftime('%Y-%m-%d')


def format_date_for_ga4(date_obj: date) -> str:
    """
    格式化日期為 GA4 表後綴格式
    
    Args:
        date_obj: 日期物件
        
    Returns:
        str: GA4 表後綴（YYYYMMDD）
    """
    return date_obj.strftime('%Y%m%d')

