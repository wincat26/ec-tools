"""
數字格式化工具函數
"""


def format_number(value, decimals=0):
    """
    格式化數字
    
    Args:
        value: 數字值
        decimals: 小數位數（0=整數，2=兩位小數）
        
    Returns:
        str: 格式化後的數字字串
    """
    if value is None:
        return '0'
    
    if decimals == 0:
        return f"{int(value):,}"
    else:
        return f"{float(value):,.{decimals}f}"


def format_percentage(value, decimals=2):
    """
    格式化百分比
    
    Args:
        value: 百分比數值（例如：5.01 表示 5.01%）
        decimals: 小數位數（預設 2 位）
        
    Returns:
        str: 格式化後的百分比字串（例如："5.01%"）
    """
    if value is None:
        return '0.00%'
    
    return f"{float(value):.{decimals}f}%"


def format_currency(value, currency='NT$'):
    """
    格式化金額
    
    Args:
        value: 金額數值
        currency: 貨幣符號（預設 'NT$'）
        
    Returns:
        str: 格式化後的金額字串（整數，例如："NT$ 518,919"）
    """
    if value is None:
        return f"{currency} 0"
    
    return f"{currency} {format_number(value, decimals=0)}"

