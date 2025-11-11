"""
Google Chat Webhook 推播模組
生成並發送 Google Chat 卡片訊息
"""
import requests
from typing import Dict, Any


class GoogleChatNotifier:
    """Google Chat 推播器"""
    
    def __init__(self, webhook_url: str):
        """
        初始化推播器
        
        Args:
            webhook_url: Google Chat Webhook URL
        """
        self.webhook_url = webhook_url
    
    def format_number(self, value: float, is_currency: bool = False) -> str:
        """
        格式化數字顯示
        
        Args:
            value: 數值
            is_currency: 是否為貨幣格式
            
        Returns:
            str: 格式化後的字串
        """
        if is_currency:
            if value >= 10000:
                return f"${value/10000:.1f}萬"
            return f"${value:,.0f}"
        else:
            if value >= 10000:
                return f"{value/10000:.1f}萬"
            return f"{value:,.0f}"
    
    def format_percentage(self, value: float, show_sign: bool = True) -> str:
        """
        格式化百分比顯示
        
        Args:
            value: 百分比值（例如 -0.15 表示下降 15%）
            show_sign: 是否顯示正負號
            
        Returns:
            str: 格式化後的百分比字串
        """
        percentage = value * 100
        sign = "+" if percentage > 0 and show_sign else ""
        return f"{sign}{percentage:.1f}%"
    
    def create_card(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        建立 Google Chat 卡片訊息
        
        Args:
            data: 每日彙總資料（來自 DailyAggregationGenerator）
            
        Returns:
            dict: Google Chat 卡片格式的訊息
        """
        report_date = data['report_date']
        revenue = data['revenue']
        orders = data['orders']
        aov = data['aov']
        cvr = data['cvr']
        sessions = data['sessions']
        ad_spend = data['ad_spend']
        roas = data['roas']
        revenue_change_wow = data['revenue_change_wow']
        cvr_change_wow = data['cvr_change_wow']
        mtd_revenue = data['mtd_revenue']
        mtd_achievement_rate = data['mtd_achievement_rate']
        mtd_projected_revenue = data['mtd_projected_revenue']
        monthly_target = data['monthly_target_revenue']
        
        # 判斷趨勢顏色和圖示
        revenue_color = "#FF6B6B" if revenue_change_wow < 0 else "#51CF66"
        revenue_icon = "📉" if revenue_change_wow < 0 else "📈"
        
        cvr_color = "#FF6B6B" if cvr_change_wow < 0 else "#51CF66"
        cvr_icon = "📉" if cvr_change_wow < 0 else "📈"
        
        # 目標達成率顏色
        achievement_color = "#51CF66" if mtd_achievement_rate >= 0.8 else "#FFD93D" if mtd_achievement_rate >= 0.5 else "#FF6B6B"
        
        ga4_warning = data.get('ga4_warning')

        traffic_widgets = [
            {
                "keyValue": {
                    "topLabel": "流量 (Sessions)",
                    "content": f"{sessions:,}",
                    "bottomLabel": f"vs. 上週同期 {self.format_percentage(self._calculate_sessions_change_wow(data))} {self._get_sessions_icon(data)}"
                }
            },
            {
                "keyValue": {
                    "topLabel": "轉換率 (CVR)",
                    "content": f"{cvr_icon} {cvr*100:.2f}%",
                    "bottomLabel": f"vs. 上週同期 {self.format_percentage(cvr_change_wow)}"
                }
            },
            {
                "keyValue": {
                    "topLabel": "客單價 (AOV)",
                    "content": f"${aov:,.0f}",
                    "bottomLabel": f"vs. 上週同期 {self.format_percentage(self._calculate_aov_change_wow(data))} {self._get_aov_icon(data)}"
                }
            }
        ]

        if ga4_warning:
            traffic_widgets.append(
                {
                    "textParagraph": {
                        "text": f"<font color=\"#9E9E9E\"><i>{ga4_warning}</i></font>"
                    }
                }
            )

        ad_spend_display = f"${int(ad_spend):,}" if ad_spend is not None else "N/A（資料待匯入）"

        card = {
            "cards": [
                {
                    "header": {
                        "title": f"📊 聖保羅 · 每日數據彙整日報",
                        "subtitle": f"{report_date}",
                        "imageUrl": "https://fonts.gstatic.com/s/i/googlematerialicons/analytics/v14/24px.svg",
                        "imageStyle": "AVATAR"
                    },
                    "sections": [
                        {
                            "header": "📈 當日關鍵指標",
                            "widgets": [
                                {
                                    "keyValue": {
                                        "topLabel": "總營收",
                                        "content": f"{revenue_icon} {self.format_number(revenue, is_currency=True)}",
                                        "bottomLabel": f"vs. 上週同期 {self.format_percentage(revenue_change_wow)}"
                                    }
                                }
                            ]
                        },
                        {
                            "header": "🔍 營收公式拆解",
                            "widgets": traffic_widgets
                        },
                        {
                            "header": "📦 訂單資訊",
                            "widgets": [
                                {
                                    "keyValue": {
                                        "topLabel": "訂單數",
                                        "content": f"{orders:,} 筆",
                                        "bottomLabel": f"平均客單價 ${aov:,.0f}"
                                    }
                                }
                            ]
                        },
                        {
                            "header": "💰 廣告表現",
                            "widgets": [
                                {
                                    "keyValue": {
                                        "topLabel": "廣告花費",
                                        "content": ad_spend_display
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "ROAS",
                                        "content": f"{'✅' if roas is not None and roas >= 3.0 else '⚠️' if roas is not None and roas >= 2.0 else '❌' if roas is not None else ''} {roas:.2f}x" if roas is not None else "N/A",
                                        "bottomLabel": "≥3.0 優秀 / ≥2.0 良好 / <2.0 需注意" if roas is not None else "廣告資料尚未匯入"
                                    }
                                }
                            ]
                        },
                        {
                            "header": "🎯 當月目標達成",
                            "widgets": [
                                {
                                    "keyValue": {
                                        "topLabel": "目標達成率",
                                        "content": f"{'✅' if mtd_achievement_rate >= 0.8 else '⚠️' if mtd_achievement_rate >= 0.5 else '❌'} {mtd_achievement_rate*100:.1f}%",
                                        "bottomLabel": f"距離目標還差 {self.format_number(max(0, monthly_target - mtd_revenue), is_currency=True)}"
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "月迄今營收",
                                        "content": self.format_number(mtd_revenue, is_currency=True),
                                        "bottomLabel": f"預估當月營收 {self.format_number(mtd_projected_revenue, is_currency=True)}"
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "當月目標",
                                        "content": self.format_number(monthly_target, is_currency=True)
                                    }
                                },
                                {
                                    "keyValue": {
                                        "topLabel": "每日平均需達成",
                                        "content": self.format_number(self._calculate_daily_target_needed(data), is_currency=True),
                                        "bottomLabel": f"以達成當月目標"
                                    }
                                }
                            ]
                        },
                        {
                            "header": "💡 關鍵洞察",
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": "📊 數據彙整完成，點擊下方按鈕深入分析營運狀況"
                                    }
                                }
                            ]
                        },
                        {
                            "widgets": [
                                {
                                    "buttons": [
                                        {
                                            "textButton": {
                                                "text": "📊 深入分析",
                                                "onClick": {
                                                    "openLink": {
                                                        "url": "https://lookerstudio.google.com/s/p3-DhIeUVSY"
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        return card
    
    def _calculate_sessions_change_wow(self, data: Dict[str, Any]) -> float:
        """計算 Sessions 的週變化"""
        return data.get('sessions_change_wow', 0.0)
    
    def _get_sessions_icon(self, data: Dict[str, Any]) -> str:
        """取得 Sessions 趨勢圖示"""
        change = self._calculate_sessions_change_wow(data)
        return "📈" if change > 0.05 else "📉" if change < -0.05 else "➡️"
    
    def _calculate_aov_change_wow(self, data: Dict[str, Any]) -> float:
        """計算 AOV 的週變化"""
        return data.get('aov_change_wow', 0.0)
    
    def _get_aov_icon(self, data: Dict[str, Any]) -> str:
        """取得 AOV 趨勢圖示"""
        change = self._calculate_aov_change_wow(data)
        return "📈" if change > 0.05 else "📉" if change < -0.05 else "➡️"
    
    def _calculate_daily_target_needed(self, data: Dict[str, Any]) -> float:
        """計算每日平均需達成金額"""
        from datetime import date
        report_date = date.fromisoformat(data['report_date'])
        mtd_revenue = data['mtd_revenue']
        monthly_target = data['monthly_target_revenue']
        
        # 計算剩餘天數
        if report_date.month == 12:
            month_end = date(report_date.year + 1, 1, 1)
        else:
            month_end = date(report_date.year, report_date.month + 1, 1)
        
        days_passed = report_date.day
        days_in_month = (month_end - date(report_date.year, report_date.month, 1)).days
        days_remaining = days_in_month - days_passed
        
        if days_remaining <= 0:
            return 0.0
        
        remaining_target = monthly_target - mtd_revenue
        if remaining_target <= 0:
            return 0.0
        
        return remaining_target / days_remaining
    
    def send(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """
        發送 Google Chat 訊息
        
        Args:
            data: 每日彙總資料
            
        Returns:
            tuple[bool, str]: (是否成功, 錯誤訊息)
        """
        try:
            card = self.create_card(data)
            
            response = requests.post(
                self.webhook_url,
                json=card,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "推播成功"
            else:
                return False, f"推播失敗：HTTP {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, f"推播失敗：{str(e)}"

