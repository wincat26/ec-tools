"""
PyEcharts 圖表生成模組
負責將資料轉換為互動式圖表 HTML
"""
import sys
import os

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, Funnel
from pyecharts.commons.utils import JsCode
from config.charts import (
    CHART_THEME,
    COLOR_PALETTE,
    TRAFFIC_SOURCE_COLORS,
    CHART_CONFIG,
    TITLE_CONFIG,
    LABEL_CONFIG,
    LEGEND_CONFIG,
    TOOLBOX_CONFIG,
    FUNNEL_CONFIG,
    TIMESERIES_CONFIG,
)


class ChartGenerator:
    """圖表生成器"""
    
    def __init__(self):
        self.theme = CHART_THEME
    
    def generate_weekly_comparison_chart(self, comparison_data):
        """
        生成本週關鍵摘要變化圖表
        
        Args:
            comparison_data: 包含本週與上週資料的字典
            
        Returns:
            str: 圖表的 HTML 字串
        """
        this_week = comparison_data['this_week']
        last_week = comparison_data['last_week']
        changes = comparison_data['changes']
        
        # 建立組合圖表（柱狀圖 + 折線圖）
        bar = (
            Bar(init_opts=opts.InitOpts(theme=self.theme, width=CHART_CONFIG['width'], height=CHART_CONFIG['height']))
            .add_xaxis(['營收變化', '訂單數變化'])
            .add_yaxis(
                "變化百分比 (%)",
                [
                    changes['revenue'],
                    changes['orders'],
                ],
                itemstyle_opts=opts.ItemStyleOpts(
                    color=JsCode(
                        """
                        function(params) {
                            return params.value >= 0 ? '#52C41A' : '#F5222D';
                        }
                        """
                    )
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="本週關鍵摘要（與上週比較）",
                    subtitle=f"營收變化: {changes['revenue']:+.2f}% | 訂單變化: {changes['orders']:+.2f}%",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['title_font_size']),
                    subtitle_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['subtitle_font_size']),
                ),
                toolbox_opts=opts.ToolboxOpts(**TOOLBOX_CONFIG),
                yaxis_opts=opts.AxisOpts(
                    name="變化百分比 (%)",
                    axislabel_opts=opts.LabelOpts(formatter="{value}%"),
                ),
                tooltip_opts=opts.TooltipOpts(
                    formatter=JsCode(
                        """
                        function(params) {
                            return params.name + '<br/>' +
                                   params.seriesName + ': ' + 
                                   params.value + '%';
                        }
                        """
                    )
                ),
            )
        )
        
        return bar.render_embed()
    
    def generate_traffic_source_chart(self, traffic_df):
        """
        生成流量來源分析圖表（餅圖 + 柱狀圖組合）
        
        Args:
            traffic_df: 包含流量來源資料的 DataFrame
            
        Returns:
            dict: 包含餅圖和柱狀圖的 HTML
        """
        if traffic_df.empty:
            return {
                'pie': '<p>暫無資料</p>',
                'bar': '<p>暫無資料</p>',
            }
        
        # 準備資料
        sources = traffic_df['traffic_source'].tolist()
        sessions = traffic_df['sessions'].tolist()
        revenue = traffic_df['revenue'].tolist()
        # 根據流量來源分類取得對應顏色
        color_map = {
            '1. 直接流量': TRAFFIC_SOURCE_COLORS.get('直接流量', COLOR_PALETTE['primary']),
            '2. 自然搜尋': TRAFFIC_SOURCE_COLORS.get('自然搜尋', COLOR_PALETTE['info']),
            '3. 付費廣告': TRAFFIC_SOURCE_COLORS.get('付費廣告', COLOR_PALETTE['danger']),
            '4. 會員經營': TRAFFIC_SOURCE_COLORS.get('會員經營', COLOR_PALETTE['success']),
            '5. AI 助理': TRAFFIC_SOURCE_COLORS.get('AI 來源', COLOR_PALETTE['info']),
            '6. 社群媒體': TRAFFIC_SOURCE_COLORS.get('社群經營', COLOR_PALETTE['warning']),
            '7. 參照連結': TRAFFIC_SOURCE_COLORS.get('參照連結', COLOR_PALETTE['info']),
            '8. 其他': TRAFFIC_SOURCE_COLORS.get('其他', COLOR_PALETTE['gray']),
        }
        colors = [color_map.get(source, COLOR_PALETTE['gray']) for source in sources]
        
        # 生成餅圖（按 Sessions）
        pie = (
            Pie(init_opts=opts.InitOpts(theme=self.theme, width=CHART_CONFIG['width'], height=CHART_CONFIG['height']))
            .add(
                "",
                [list(z) for z in zip(sources, sessions)],
                radius=["30%", "70%"],
                center=["50%", "50%"],
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="流量來源分布（Sessions）",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['title_font_size']),
                ),
                legend_opts=opts.LegendOpts(
                    orient="vertical",
                    pos_left="left",
                    textstyle_opts=opts.TextStyleOpts(font_size=LEGEND_CONFIG['font_size']),
                ),
                toolbox_opts=opts.ToolboxOpts(**TOOLBOX_CONFIG),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    formatter="{b}: {c} ({d}%)",
                    font_size=LABEL_CONFIG['font_size'],
                    position="outside",  # 標籤放在外面，避免與圖表重疊
                ),
                itemstyle_opts=opts.ItemStyleOpts(
                    color=JsCode(
                        """
                        function(params) {
                            var colors = %s;
                            return colors[params.dataIndex] || '#8C8C8C';
                        }
                        """ % colors
                    )
                ),
            )
        )
        
        # 生成柱狀圖（按營收）
        bar = (
            Bar(init_opts=opts.InitOpts(theme=self.theme, width=CHART_CONFIG['width'], height=CHART_CONFIG['height']))
            .add_xaxis(sources)
            .add_yaxis(
                "營收 (元)",
                revenue,
                itemstyle_opts=opts.ItemStyleOpts(
                    color=JsCode(
                        """
                        function(params) {
                            var colors = %s;
                            return colors[params.dataIndex] || '#8C8C8C';
                        }
                        """ % colors
                    )
                ),
                label_opts=opts.LabelOpts(
                    is_show=True,
                    position="top",  # 標籤放在柱狀圖上方
                    formatter=JsCode("function(params) { return params.value.toLocaleString(); }")
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="各流量來源營收表現",
                    subtitle="包含 CVR、AOV 等指標",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['title_font_size']),
                    subtitle_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['subtitle_font_size']),
                ),
                toolbox_opts=opts.ToolboxOpts(**TOOLBOX_CONFIG),
                yaxis_opts=opts.AxisOpts(
                    name="營收 (元)",
                    axislabel_opts=opts.LabelOpts(
                        formatter=JsCode("function(value) { return (value / 1000).toFixed(1) + 'K'; }")
                    ),
                ),
                tooltip_opts=opts.TooltipOpts(
                    formatter=JsCode(
                        """
                        function(params) {
                            var data = %s;
                            var idx = params.dataIndex;
                            return params.name + '<br/>' +
                                   '營收: ' + params.value.toLocaleString() + ' 元<br/>' +
                                   'Sessions: ' + data[idx].sessions + '<br/>' +
                                   'CVR: ' + data[idx].cvr + '%%<br/>' +
                                   'AOV: ' + data[idx].aov.toFixed(0) + ' 元';
                        }
                        """ % traffic_df.to_dict('records')
                    )
                ),
            )
        )
        
        return {
            'pie': pie.render_embed(),
            'bar': bar.render_embed(),
        }
    
    def generate_aov_distribution_chart(self, aov_data, dimension='overall'):
        """
        生成平均訂單金額分布圖表
        
        Args:
            aov_data: 包含件數分布和價格帶的字典
            dimension: 分析維度（'overall', 'new', 'returning'）
            
        Returns:
            dict: 包含件數分布和價格帶圖表的 HTML
        """
        # 購物車件數分布（柱狀圖）
        item_data = aov_data.get('item_distribution', [])
        if item_data:
            item_labels = [item['item_count'] for item in item_data]
            item_counts = [item['order_count'] for item in item_data]
            item_avg = [item['avg_amount'] for item in item_data]
            
            item_chart = (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width=CHART_CONFIG['width'], height=CHART_CONFIG['height']))
                .add_xaxis(item_labels)
                .add_yaxis(
                    "訂單數",
                    item_counts,
                    yaxis_index=0,
                )
                .add_yaxis(
                    "平均訂單金額",
                    item_avg,
                    yaxis_index=1,
                    label_opts=opts.LabelOpts(
                        is_show=True,
                        formatter="{c} 元",
                        font_size=LABEL_CONFIG['font_size'],
                    ),
                )
                .extend_axis(
                    yaxis=opts.AxisOpts(
                        name="平均訂單金額 (元)",
                        type_="value",
                        position="right",
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"購物車件數分布（{dimension}）",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['title_font_size']),
                    ),
                    toolbox_opts=opts.ToolboxOpts(**TOOLBOX_CONFIG),
                    yaxis_opts=opts.AxisOpts(name="訂單數"),
                    tooltip_opts=opts.TooltipOpts(
                        formatter=JsCode(
                            """
                            function(params) {
                                var data = %s;
                                var idx = params.dataIndex;
                                if (params.seriesName === '訂單數') {
                                    return params.name + '<br/>' +
                                           '訂單數: ' + params.value + '<br/>' +
                                           '平均訂單金額: ' + data[idx].avg_amount.toFixed(0) + ' 元';
                                }
                                return params.name + '<br/>平均訂單金額: ' + params.value + ' 元';
                            }
                            """ % item_data
                        )
                    ),
                )
            )
            item_html = item_chart.render_embed()
        else:
            item_html = '<p>暫無資料</p>'
        
        # 價格帶分布（堆疊柱狀圖）
        price_data = aov_data.get('price_band_distribution', [])
        if price_data:
            price_labels = [price['price_band'] for price in price_data]
            price_counts = [price['order_count'] for price in price_data]
            
            price_chart = (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width=CHART_CONFIG['width'], height=CHART_CONFIG['height']))
                .add_xaxis(price_labels)
                .add_yaxis(
                    "訂單數",
                    price_counts,
                    stack="price_band",
                    itemstyle_opts=opts.ItemStyleOpts(
                        color=JsCode(
                            """
                            function(params) {
                                var colors = ['#52C41A', '#FAAD14', '#F5222D'];
                                return colors[params.dataIndex] || '#8C8C8C';
                            }
                            """
                        )
                    ),
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"價格帶結構（{dimension}）",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['title_font_size']),
                    ),
                    toolbox_opts=opts.ToolboxOpts(**TOOLBOX_CONFIG),
                    yaxis_opts=opts.AxisOpts(name="訂單數"),
                    tooltip_opts=opts.TooltipOpts(
                        formatter=JsCode(
                            """
                            function(params) {
                                var data = %s;
                                var idx = params.dataIndex;
                                return params.name + '<br/>' +
                                       '訂單數: ' + params.value + '<br/>' +
                                       '平均訂單金額: ' + data[idx].avg_amount.toFixed(0) + ' 元';
                            }
                            """ % price_data
                        )
                    ),
                )
            )
            price_html = price_chart.render_embed()
        else:
            price_html = '<p>暫無資料</p>'
        
        return {
            'item_distribution': item_html,
            'price_band': price_html,
        }
    
    def generate_conversion_funnel_chart(self, funnel_data):
        """
        生成轉換漏斗圖表
        
        Args:
            funnel_data: 包含漏斗階層資料的字典
            
        Returns:
            str: 漏斗圖的 HTML 字串
        """
        overall = funnel_data.get('overall', {})
        steps = overall.get('steps', [])
        
        if not steps:
            return '<p>暫無漏斗資料</p>'
        
        # 準備漏斗資料（計算相對於第一個階段的轉換率）
        first_step_count = steps[0]['count'] if steps else 1
        funnel_items = []
        conversion_rates = []
        for step in steps:
            # 計算相對於第一個階段（訪客）的轉換率
            conversion_rate = (step['count'] / first_step_count * 100) if first_step_count > 0 else 0
            funnel_items.append([step['label'], step['count']])
            conversion_rates.append(round(conversion_rate, 2))
        
        # 生成漏斗圖（使用 sort='descending' 讓漏斗從大到小）
        funnel = (
            Funnel(init_opts=opts.InitOpts(
                theme=self.theme,
                width=FUNNEL_CONFIG['width'],
                height=FUNNEL_CONFIG['height']
            ))
            .add(
                "轉換漏斗",
                funnel_items,
                sort_="descending",  # 從大到小排序，形成漏斗效果
                gap=2,  # 階層間距
                label_opts=opts.LabelOpts(
                    position="inside",
                    formatter=JsCode(
                        """
                        function(params) {
                            var rates = %s;
                            var idx = params.dataIndex;
                            var conversionRate = rates[idx] || 0;
                            return params.name + ': ' + params.value.toLocaleString() + ' (' + conversionRate.toFixed(2) + '%%')';
                        }
                        """ % conversion_rates
                    ),
                    font_size=LABEL_CONFIG['font_size'],
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="全站轉換漏斗",
                    subtitle="從訪客到成交的核心轉換率（百分比為相對於訪客數的轉換率）",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['title_font_size']),
                    subtitle_textstyle_opts=opts.TextStyleOpts(font_size=TITLE_CONFIG['subtitle_font_size']),
                ),
                toolbox_opts=opts.ToolboxOpts(**TOOLBOX_CONFIG),
                tooltip_opts=opts.TooltipOpts(
                    formatter=JsCode(
                        """
                        function(params) {
                            var total = %s;
                            var current = params.value;
                            var rate = total > 0 ? (current / total * 100).toFixed(2) : 0;
                            return params.name + '<br/>' +
                                   '數量: ' + current.toLocaleString() + '<br/>' +
                                   '轉換率（相對於訪客）: ' + rate + '%%';
                        }
                        """ % (first_step_count)
                    )
                ),
            )
        )
        
        return funnel.render_embed()

