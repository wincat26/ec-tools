"""
流量來源分類器
將 GA4 的 source/medium 分類為 8 種流量來源
"""
import re


def classify_traffic_source(source, medium):
    """
    根據 source 和 medium 分類流量來源
    
    Args:
        source: GA4 的 traffic_source.source
        medium: GA4 的 traffic_source.medium
        
    Returns:
        str: 流量來源分類（1-8）
    """
    # 組合 source/medium（模擬 GA4 的格式）
    source_medium = f"{source} / {medium}" if source and medium else f"{source or ''} / {medium or ''}"
    source_medium_lower = source_medium.lower()
    
    # 1. 直接流量
    if source == '(direct)' and medium in ['(none)', '(not set)']:
        return '1. 直接流量'
    
    # 2. 自然搜尋
    if re.search(r'/ organic$|.*search.*', source_medium_lower):
        return '2. 自然搜尋'
    
    # 3. 付費廣告
    if re.search(r'/ (ads|cpc|paid|ppc|cpm|pmax|ad|fb-SiteLink)$', source_medium, re.IGNORECASE):
        return '3. 付費廣告'
    
    # 4. 會員經營
    if re.search(r'(edm|line|push|sms|cdp|crm)', source_medium, re.IGNORECASE):
        return '4. 會員經營'
    
    # 5. AI 助理
    if re.search(r'^(chatgpt|perplexity|copilot|bard|gemini)', source_medium_lower):
        return '5. AI 助理'
    
    # 6. 社群媒體
    if re.search(r'(facebook|threads|instagram|t\.co|line|linktr\.ee|pinterest|linkedin)', source_medium, re.IGNORECASE):
        return '6. 社群媒體'
    
    # 7. 參照連結
    if re.search(r'/ referral$', source_medium, re.IGNORECASE):
        return '7. 參照連結'
    
    # 8. 其他
    return '8. 其他'


def classify_traffic_source_sql(source_col='source', medium_col='medium'):
    """
    生成 SQL CASE WHEN 語句用於流量分類
    
    Args:
        source_col: source 欄位名稱
        medium_col: medium 欄位名稱
        
    Returns:
        str: SQL CASE WHEN 語句
    """
    source_medium_expr = f"CONCAT(COALESCE({source_col}, ''), ' / ', COALESCE({medium_col}, ''))"
    
    return f"""
    CASE
        WHEN {source_col} = '(direct)' AND ({medium_col} = '(none)' OR {medium_col} = '(not set)') THEN '1. 直接流量'
        WHEN REGEXP_CONTAINS(LOWER({source_medium_expr}), r'/ organic$|.*search.*') THEN '2. 自然搜尋'
        WHEN REGEXP_CONTAINS({source_medium_expr}, r'/ (ads|cpc|paid|ppc|cpm|pmax|ad|fb-SiteLink)$') THEN '3. 付費廣告'
        WHEN REGEXP_CONTAINS({source_medium_expr}, r'(edm|line|push|sms|cdp|crm)') THEN '4. 會員經營'
        WHEN REGEXP_CONTAINS(LOWER({source_medium_expr}), r'^(chatgpt|perplexity|copilot|bard|gemini)') THEN '5. AI 助理'
        WHEN REGEXP_CONTAINS({source_medium_expr}, r'(facebook|threads|instagram|t\\.co|line|linktr\\.ee|pinterest|linkedin)') THEN '6. 社群媒體'
        WHEN REGEXP_CONTAINS({source_medium_expr}, r'/ referral$') THEN '7. 參照連結'
        ELSE '8. 其他'
    END
    """

