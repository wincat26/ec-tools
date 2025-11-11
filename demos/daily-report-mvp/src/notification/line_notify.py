"""
LINE Messaging API 推播模組
"""
from __future__ import annotations

import os
from typing import Dict, Any, List, Tuple

import requests


LINE_PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"


class LineNotifier:
    """LINE Notify 推播器"""

    def __init__(
        self,
        access_token: str,
        target_ids: List[str],
        dashboard_url: str | None = None,
        brand_name: str | None = None,
    ):
        """
        初始化 LINE 推播器

        Args:
            access_token: LINE Channel access token (Bearer)
            target_ids: 需要推播的 userId / groupId 列表
            dashboard_url: 週報/日報儀表板連結
            brand_name: 品牌名稱（若為 None 則取 data['client_id']）
        """
        if not access_token:
            raise ValueError("LINE access token 未設定")
        if not target_ids:
            raise ValueError("LINE 推播目標清單為空")

        self.access_token = access_token
        self.target_ids = [target.strip() for target in target_ids if target.strip()]
        self.dashboard_url = dashboard_url or os.environ.get(
            "LINE_DASHBOARD_URL",
            "https://lookerstudio.google.com/s/p3-DhIeUVSY",
        )
        self.brand_name = brand_name or os.environ.get("LINE_BRAND_NAME")

    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _format_currency(value: float) -> str:
        if value >= 1_000_000:
            return f"${value/1_000_000:.2f}M"
        if value >= 10_000:
            return f"${value/10_000:.1f}萬"
        return f"${value:,.0f}"

    @staticmethod
    def _format_percentage(value: float) -> str:
        return f"{value * 100:.1f}%"

    @staticmethod
    def _format_delta(value: float) -> str:
        arrow = "▲" if value > 0 else "▼" if value < 0 else "●"
        sign = "+" if value > 0 else ""
        return f"{arrow} {sign}{value * 100:.1f}%"

    def _highlight_chip(self, title: str, delta: float) -> Dict[str, Any]:
        color = "#2E7D32" if delta > 0 else "#C62828" if delta < 0 else "#616161"
        bg = "#E8F5E9" if delta > 0 else "#FFEBEE" if delta < 0 else "#F5F5F5"
        return {
            "type": "box",
            "layout": "vertical",
            "flex": 1,
            "backgroundColor": bg,
            "cornerRadius": "md",
            "paddingAll": "8px",
            "contents": [
                {"type": "text", "text": title, "size": "xs", "color": "#757575"},
                {
                    "type": "text",
                    "text": self._format_delta(delta),
                    "size": "sm",
                    "weight": "bold",
                    "color": color,
                    "wrap": True,
                },
            ],
        }

    def _build_insight_text(self, data: Dict[str, Any]) -> str:
        if data.get("insight_text"):
            return data["insight_text"]

        revenue_wow = data.get("revenue_change_wow", 0.0)
        cvr_wow = data.get("cvr_change_wow", 0.0)
        mtd_rate = data.get("mtd_achievement_rate", 0.0)

        if revenue_wow >= 0.05 and cvr_wow >= 0.02:
            return "🚀 營收與轉換率同步成長，請延續成功活動或加碼廣告。"
        if revenue_wow < 0 and cvr_wow < 0:
            return "⚠️ 營收與轉換率同步下滑，請檢查落差最大之流量/商品。"
        if mtd_rate < 0.5:
            return "⚠️ 月目標達成率偏低，請檢視會員喚醒與轉換漏斗。"
        return "ℹ️ 指標穩定，持續觀察流量與轉換率變化。"

    # ------------------------------------------------------------------
    # Message builders
    # ------------------------------------------------------------------
    def _build_flex_contents(self, data: Dict[str, Any]) -> Dict[str, Any]:
        report_date = data["report_date"]
        revenue = data["revenue"]
        orders = data["orders"]
        sessions = data["sessions"]
        cvr = data["cvr"]
        aov = data["aov"]
        ad_spend = data.get("ad_spend")
        roas = data.get("roas")
        google_ads_spend = data.get("google_ads_spend")
        meta_ads_spend = data.get("meta_ads_spend")
        revenue_wow = data.get("revenue_change_wow", 0.0)
        cvr_wow = data.get("cvr_change_wow", 0.0)
        sessions_wow = data.get("sessions_change_wow", 0.0)
        mtd_revenue = data["mtd_revenue"]
        mtd_achievement_rate = data["mtd_achievement_rate"]
        mtd_projected_revenue = data["mtd_projected_revenue"]
        monthly_target = data["monthly_target_revenue"]
        ga4_warning = data.get("ga4_warning")
        brand_name = self.brand_name or data.get("brand_name") or data.get("client_id", "營運品牌")

        def metric_row(label: str, value: str, color: str = "#111111"):
            return {
                "type": "box",
                "layout": "baseline",
                "margin": "sm",
                "contents": [
                    {"type": "text", "text": label, "size": "sm", "color": "#888888", "flex": 3},
                    {"type": "text", "text": value, "size": "md", "color": color, "weight": "bold", "flex": 5},
                ],
            }

        def separator():
            return {"type": "separator", "margin": "md"}

        def ad_channel_box(label: str, spend: Any) -> Dict[str, Any]:
            display = self._format_currency(spend) if spend is not None else "N/A"
            return {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#F5F5F5",
                "cornerRadius": "md",
                "paddingAll": "10px",
                "flex": 1,
                "contents": [
                    {"type": "text", "text": label, "size": "xs", "color": "#757575"},
                    {"type": "text", "text": display, "size": "sm", "weight": "bold", "color": "#111111"},
                ],
            }

        highlights = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "md",
            "contents": [
                self._highlight_chip("營收", revenue_wow),
                self._highlight_chip("CVR", cvr_wow),
                self._highlight_chip("Sessions", sessions_wow),
            ],
        }

        insight_text = self._build_insight_text(data)

        main_section = [
            {"type": "text", "text": "📊 每日營運快訊", "weight": "bold", "size": "lg"},
            {"type": "text", "text": f"{brand_name} · {report_date}", "size": "sm", "color": "#888888"},
            highlights,
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "backgroundColor": "#F1F8E9",
                "cornerRadius": "md",
                "paddingAll": "12px",
                "contents": [
                    {"type": "text", "text": "💡 關鍵洞察", "size": "sm", "color": "#689F38", "weight": "bold"},
                    {"type": "text", "text": insight_text, "size": "sm", "color": "#33691E", "wrap": True},
                ],
            },
            separator(),
            {"type": "text", "text": "今日摘要", "weight": "bold", "size": "md", "margin": "md"},
            metric_row("營收", self._format_currency(revenue)),
            metric_row("訂單數", f"{orders:,} 筆"),
            metric_row("Sessions", f"{sessions:,}"),
            metric_row("CVR", self._format_percentage(cvr)),
            metric_row("客單價", self._format_currency(aov)),
            separator(),
            {"type": "text", "text": "週對週變化", "weight": "bold", "size": "md", "margin": "md"},
            metric_row("營收 vs 上週", self._format_delta(revenue_wow), "#F76B1C"),
            metric_row("CVR vs 上週", self._format_delta(cvr_wow), "#0F9D58"),
            metric_row("Sessions vs 上週", self._format_delta(sessions_wow), "#4285F4"),
            separator(),
            {"type": "text", "text": "廣告表現", "weight": "bold", "size": "md", "margin": "md"},
            metric_row("花費", self._format_currency(ad_spend) if ad_spend is not None else "N/A"),
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": [
                    ad_channel_box("Google Ads", google_ads_spend),
                    ad_channel_box("Meta Ads", meta_ads_spend),
                ],
            },
            metric_row("ROAS", f"{roas:.2f}x" if roas is not None else "N/A"),
            separator(),
            {"type": "text", "text": "月度進度", "weight": "bold", "size": "md", "margin": "md"},
            metric_row("目標達成率", self._format_percentage(mtd_achievement_rate)),
            metric_row("月達成營收", self._format_currency(mtd_revenue)),
            metric_row("預估營收", self._format_currency(mtd_projected_revenue)),
            metric_row("月目標", self._format_currency(monthly_target)),
        ]

        if ga4_warning:
            main_section.append(separator())
            main_section.append(
                {
                    "type": "text",
                    "text": f"⚠️ {ga4_warning}",
                    "size": "xs",
                    "color": "#FF6F61",
                    "wrap": True,
                }
            )

        footer_contents = [
            {
                "type": "button",
                "style": "primary",
                "color": "#1E88E5",
                "height": "sm",
                "action": {
                    "type": "uri",
                    "label": "查看完整報表",
                    "uri": self.dashboard_url,
                },
            }
        ]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "backgroundColor": "#1E3A5F",
                "contents": [
                    {"type": "text", "text": f"{brand_name} · 日報", "color": "#FFFFFF", "size": "lg", "weight": "bold"},
                    {"type": "text", "text": report_date, "color": "#BBDEFB", "size": "xs"},
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": main_section,
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer_contents,
            },
        }

        return bubble

    def _build_messages(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        report_date = data["report_date"]
        brand_name = self.brand_name or data.get("brand_name") or data.get("client_id", "營運品牌")
        revenue = self._format_currency(data["revenue"])
        mtd_rate = self._format_percentage(data["mtd_achievement_rate"])
        fallback_text = f"{brand_name} {report_date} 營收 {revenue}，目標達成率 {mtd_rate}"

        messages = [
            {"type": "text", "text": fallback_text},
            {
                "type": "flex",
                "altText": f"{brand_name} 每日營運日報 · {report_date}",
                "contents": self._build_flex_contents(data),
            },
        ]
        return messages

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def send(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        發送 LINE 推播

        Args:
            data: DailyAggregationGenerator 回傳的 JSON

        Returns:
            (成功與否, 訊息)
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        messages = self._build_messages(data)

        errors: List[str] = []
        for target in self.target_ids:
            payload = {"to": target, "messages": messages}
            response = requests.post(LINE_PUSH_ENDPOINT, headers=headers, json=payload, timeout=10)
            if response.status_code != 200:
                errors.append(f"{target}: HTTP {response.status_code} {response.text}")

        if errors:
            return False, "；".join(errors)
        return True, f"LINE 推播成功（{len(self.target_ids)} 位/群）"

