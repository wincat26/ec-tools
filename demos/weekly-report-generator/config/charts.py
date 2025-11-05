"""
PyEcharts 圖表樣式設定
統一管理圖表的主題、顏色、字體等樣式
"""
from pyecharts.globals import ThemeType


# 圖表主題設定
CHART_THEME = ThemeType.MACARONS  # 可選：MACARONS, WONDERLAND, ROMANTIC 等

# 顏色配置（對應電商品牌色彩）
COLOR_PALETTE = {
    'primary': '#4A90E2',      # 主色：藍色
    'success': '#52C41A',      # 成功：綠色
    'warning': '#FAAD14',      # 警告：橘色
    'danger': '#F5222D',       # 危險：紅色
    'info': '#1890FF',         # 資訊：淺藍
    'gray': '#8C8C8C',         # 灰色
}

# 流量來源顏色對應（對應 data.html 的 8 種分類）
TRAFFIC_SOURCE_COLORS = {
    '直接流量': '#4A90E2',
    '付費廣告': '#F5222D',
    '會員經營': '#52C41A',
    'AI 來源': '#722ED1',
    '自然搜尋': '#13C2C2',
    '社群經營': '#FA8C16',
    '參照連結': '#1890FF',
    '其他': '#8C8C8C',
}

# 圖表通用設定
CHART_CONFIG = {
    'width': '100%',
    'height': '400px',
}

# 標題設定
TITLE_CONFIG = {
    'title_font_size': 16,
    'subtitle_font_size': 14,
}

# 標籤設定
LABEL_CONFIG = {
    'font_size': 12,
}

# 圖例設定
LEGEND_CONFIG = {
    'font_size': 12,
}

# 工具箱設定
TOOLBOX_CONFIG = {
    'feature': {
        'saveAsImage': {'show': True},  # 儲存為圖片
        'restore': {'show': True},      # 還原
        'dataView': {'show': True},     # 資料視圖
    },
}

# 漏斗圖設定
FUNNEL_CONFIG = {
    'width': '100%',
    'height': '500px',
    'label_font_size': 14,
    'gap': 20,  # 漏斗階層間距
}

# 時間序列圖設定（折線圖）
TIMESERIES_CONFIG = {
    'width': '100%',
    'height': '350px',
    'smooth': True,  # 平滑曲線
    'symbol_size': 6,
}

