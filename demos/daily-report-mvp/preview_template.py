#!/usr/bin/env python3
"""
預覽 Google Chat 卡片模板
生成範例卡片並顯示結構
"""
import json
from datetime import date
from src.notification.google_chat import GoogleChatNotifier

# 建立範例資料
sample_data = {
    'client_id': 'client_A',
    'report_date': '2025-11-05',
    'monthly_target_revenue': 2000000,
    'revenue': 85000,
    'orders': 50,
    'aov': 1700.0,
    'cvr': 0.015,
    'sessions': 3333,
    'ad_spend': 10000,
    'roas': 8.5,
    'revenue_change_wow': 0.15,  # +15%
    'cvr_change_wow': -0.10,  # -10%
    'sessions_change_wow': 0.085,  # +8.5%
    'aov_change_wow': 0.05,  # +5%
    'mtd_revenue': 340000,
    'mtd_achievement_rate': 0.17,  # 17%
    'mtd_projected_revenue': 1020000,
}

# 建立推播器（使用假 Webhook URL）
notifier = GoogleChatNotifier("https://example.com/webhook")

# 生成卡片
card = notifier.create_card(sample_data)

print("=" * 80)
print("📊 Google Chat 卡片模板預覽")
print("=" * 80)
print()

# 顯示卡片結構
print("📋 卡片結構：")
print(json.dumps(card, indent=2, ensure_ascii=False))

print()
print("=" * 80)
print("📝 文字版預覽：")
print("=" * 80)
print()

# 文字版預覽
print(f"📊 每日數據彙整日報")
print(f"日期：{sample_data['report_date']}")
print()
print("📈 當日關鍵指標")
print(f"  • 總營收：${sample_data['revenue']:,} ({'+' if sample_data['revenue_change_wow'] > 0 else ''}{sample_data['revenue_change_wow']*100:.1f}%)")
print()
print("🔍 營收公式拆解")
print(f"  • 流量 (Sessions)：{sample_data['sessions']:,} ({'+' if sample_data['sessions_change_wow'] > 0 else ''}{sample_data['sessions_change_wow']*100:.1f}%)")
print(f"  • 轉換率 (CVR)：{sample_data['cvr']*100:.2f}% ({'+' if sample_data['cvr_change_wow'] > 0 else ''}{sample_data['cvr_change_wow']*100:.1f}%)")
print(f"  • 客單價 (AOV)：${sample_data['aov']:,.0f} ({'+' if sample_data['aov_change_wow'] > 0 else ''}{sample_data['aov_change_wow']*100:.1f}%)")
print()
print("📦 訂單資訊")
print(f"  • 訂單數：{sample_data['orders']:,} 筆")
print(f"  • 平均客單價：${sample_data['aov']:,.0f}")
print()
print("💰 廣告表現")
print(f"  • 廣告花費：${sample_data['ad_spend']:,}")
print(f"  • ROAS：{sample_data['roas']:.2f}x")
print()
print("🎯 當月目標達成")
print(f"  • 目標達成率：{sample_data['mtd_achievement_rate']*100:.1f}%")
print(f"  • 月迄今營收：${sample_data['mtd_revenue']:,}")
print(f"  • 預估當月營收：${sample_data['mtd_projected_revenue']:,}")
print(f"  • 當月目標：${sample_data['monthly_target_revenue']:,}")
remaining = sample_data['monthly_target_revenue'] - sample_data['mtd_revenue']
daily_needed = notifier._calculate_daily_target_needed(sample_data)
print(f"  • 每日平均需達成：${daily_needed:,.0f}")
print()
print("💡 關鍵洞察")
print("  📊 數據彙整完成，點擊下方按鈕深入分析營運狀況")
print()
print("📊 [深入分析] 按鈕")

