"""
HTML 報告組合模組
將所有圖表整合成完整的 HTML 報告
"""
import os
import sys
from datetime import datetime
from jinja2 import Template

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.charts import COLOR_PALETTE
from src.ai.summary import generate_weekly_summary
from src.utils.formatters import format_number, format_percentage, format_currency


class ReportBuilder:
    """報告建構器"""
    
    def __init__(self, template_dir=None, output_dir='./output'):
        # 預設模板目錄為 src/reports/templates
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src', 'reports', 'templates')
        self.template_dir = template_dir
        self.output_dir = output_dir
        
        # 確保輸出目錄存在
        os.makedirs(self.output_dir, exist_ok=True)
    
    def build_report(self, data_dict, charts_dict, brand_name='豆油伯'):
        """
        組合完整的 HTML 報告
        
        Args:
            data_dict: 包含所有資料的字典
            charts_dict: 包含所有圖表 HTML 的字典
            brand_name: 品牌名稱
            
        Returns:
            str: 生成的報告檔案路徑
        """
        # 讀取 HTML 模板
        template_path = os.path.join(self.template_dir, 'report_template.html')
        
        if not os.path.exists(template_path):
            # 如果模板不存在，使用預設模板
            html_content = self._generate_default_template()
        else:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = Template(f.read())
                # 生成 AI 摘要（暫時使用規則式，後續可整合 LLM）
                ai_summary = generate_weekly_summary(data_dict, use_llm=False)
                
                # 取得報告時間範圍
                report_period = data_dict.get('report_period', {})
                start_date = report_period.get('start_date', '')
                end_date = report_period.get('end_date', '')
                
                html_content = template.render(
                    brand_name=brand_name,
                    output_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                    report_start_date=start_date,
                    report_end_date=end_date,
                    data=data_dict,
                    charts=charts_dict,
                    colors=COLOR_PALETTE,
                    ai_summary=ai_summary,
                    format_number=format_number,
                    format_percentage=format_percentage,
                    format_currency=format_currency,
                )
        
        # 儲存報告
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'weekly_report_{timestamp}.html'
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_default_template(self):
        """生成預設的 HTML 模板"""
        return """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>電商週報 - {{ brand_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header h1 {
            color: {{ colors.primary }};
            margin-bottom: 10px;
        }
        .header .meta {
            color: #666;
            font-size: 14px;
        }
        .section {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid {{ colors.primary }};
        }
        .chart-container {
            margin: 20px 0;
            min-height: 400px;
        }
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .kpi-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .kpi-card .label {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .kpi-card .value {
            font-size: 32px;
            font-weight: bold;
            color: {{ colors.primary }};
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>電商週報 - {{ brand_name }}</h1>
            <div class="meta">生成時間：{{ report_date }}</div>
        </div>
        
        <!-- GMV 基本指標 -->
        <div class="section">
            <h2>GMV 基本指標</h2>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="label">成交營收</div>
                    <div class="value">{{ "%.0f"|format(data.gmv_metrics.net_revenue) }}</div>
                </div>
                <div class="kpi-card">
                    <div class="label">總營業額</div>
                    <div class="value">{{ "%.0f"|format(data.gmv_metrics.gross_revenue) }}</div>
                </div>
                <div class="kpi-card">
                    <div class="label">取消率</div>
                    <div class="value">{{ "%.2f"|format(data.gmv_metrics.cancel_rate) }}%</div>
                </div>
            </div>
        </div>
        
        <!-- 本週關鍵摘要 -->
        {% if charts.weekly_comparison %}
        <div class="section">
            <h2>本週關鍵摘要</h2>
            <div class="chart-container">
                {{ charts.weekly_comparison|safe }}
            </div>
        </div>
        {% endif %}
        
        <!-- 流量分析 -->
        {% if charts.traffic_source %}
        <div class="section">
            <h2>流量分析</h2>
            <div class="chart-container">
                {{ charts.traffic_source.pie|safe }}
            </div>
            <div class="chart-container">
                {{ charts.traffic_source.bar|safe }}
            </div>
        </div>
        {% endif %}
        
        <!-- AOV 分析 -->
        {% if charts.aov_distribution %}
        <div class="section">
            <h2>平均訂單金額分析</h2>
            <div class="chart-container">
                {{ charts.aov_distribution.item_distribution|safe }}
            </div>
            <div class="chart-container">
                {{ charts.aov_distribution.price_band|safe }}
            </div>
        </div>
        {% endif %}
        
        <!-- 轉換漏斗 -->
        {% if charts.conversion_funnel %}
        <div class="section">
            <h2>轉換率漏斗分析</h2>
            <div class="chart-container">
                {{ charts.conversion_funnel|safe }}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
        """

