"""
AI 摘要生成模組
使用 LLM 分析週報資料並生成觀察與建議
暫時為後台功能，等實機成熟後可開放前台
"""
import os
import json
from typing import Dict, Any


def generate_weekly_summary(data: Dict[str, Any], use_llm: bool = False) -> str:
    """
    生成週報摘要文字
    
    Args:
        data: 包含所有週報資料的字典
        use_llm: 是否使用 LLM（暫時為 False，後續可整合）
        
    Returns:
        str: 摘要文字
    """
    if use_llm:
        # 後續整合 LLM（如 OpenAI, Anthropic 等）
        return _generate_with_llm(data)
    else:
        # 暫時使用規則式生成
        return _generate_rule_based(data)


def _generate_rule_based(data: Dict[str, Any]) -> str:
    """
    使用規則式方法生成摘要（暫時方案）
    
    Args:
        data: 週報資料
        
    Returns:
        str: 摘要文字
    """
    gmv = data.get('gmv_metrics', {})
    comparison = data.get('weekly_comparison', {})
    traffic = data.get('traffic_analysis', [])
    
    summary_parts = []
    
    # 1. 營收表現
    net_revenue = gmv.get('net_revenue', 0)
    gross_revenue = gmv.get('gross_revenue', 0)
    completed_orders = gmv.get('completed_orders', 0)
    total_orders = gmv.get('total_orders', 0)
    unique_users = gmv.get('unique_users', 0)
    
    summary_parts.append(f"本週成交總額為 NT$ {net_revenue:,.0f}，總營業額為 NT$ {gross_revenue:,.0f}，成交訂單總量為 {completed_orders:,} 筆，總訂單總量為 {total_orders:,} 筆，交易會員數為 {unique_users:,} 人。")
    
    # 2. 與上週比較
    changes = comparison.get('changes', {})
    revenue_change = changes.get('revenue', 0)
    orders_change = changes.get('orders', 0)
    
    if revenue_change > 0:
        summary_parts.append(f"營收較上週成長 {abs(revenue_change):.2f}%，表現優異。")
    elif revenue_change < 0:
        summary_parts.append(f"營收較上週下降 {abs(revenue_change):.2f}%，需要關注。")
    else:
        summary_parts.append("營收與上週持平。")
    
    if orders_change > 0:
        summary_parts.append(f"訂單數較上週成長 {abs(orders_change):.2f}%。")
    elif orders_change < 0:
        summary_parts.append(f"訂單數較上週下降 {abs(orders_change):.2f}%，但平均訂單金額可能提升。")
    
    # 3. 流量來源分析
    if traffic:
        top_traffic = sorted(traffic, key=lambda x: x.get('revenue', 0), reverse=True)[:3]
        if top_traffic:
            summary_parts.append("主要流量來源：")
            for i, source in enumerate(top_traffic, 1):
                source_name = source.get('traffic_source', '')
                revenue = source.get('revenue', 0)
                cvr = source.get('cvr', 0)
                summary_parts.append(f"{i}. {source_name}：營收 NT$ {revenue:,.0f}，轉換率 {cvr:.2f}%")
    
    # 4. 建議
    summary_parts.append("\n建議：")
    if revenue_change < -10:
        summary_parts.append("- 營收下降幅度較大，建議檢視行銷活動成效與商品組合。")
    if orders_change < -20:
        summary_parts.append("- 訂單數下降明顯，建議加強促銷活動或優化轉換流程。")
    if revenue_change > 0 and orders_change < 0:
        summary_parts.append("- 訂單數下降但營收成長，顯示客單價提升，建議持續優化商品推薦。")
    
    return "\n".join(summary_parts)


def _generate_with_llm(data: Dict[str, Any]) -> str:
    """
    使用 LLM 生成摘要（後續實作）
    
    Args:
        data: 週報資料
        
    Returns:
        str: LLM 生成的摘要文字
    """
    # TODO: 整合 LLM API（OpenAI, Anthropic, etc.）
    # 1. 準備 prompt
    # 2. 呼叫 LLM API
    # 3. 解析並返回結果
    
    prompt = f"""
請分析以下電商週報資料，提供：
1. 本週整體表現觀察
2. 與上週的關鍵變化
3. 具體優化建議

資料：
{json.dumps(data, indent=2, ensure_ascii=False)}
"""
    
    # 暫時返回規則式結果
    return _generate_rule_based(data)

