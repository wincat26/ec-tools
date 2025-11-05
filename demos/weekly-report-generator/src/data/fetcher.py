"""
BigQuery 資料查詢模組
負責從 BigQuery 查詢所需的電商資料
根據實際資料表結構 (lv1_order_master, lv1_order 等) 調整查詢邏輯
"""
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# 添加專案根目錄到路徑
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from config.bigquery import BigQueryConfig, TABLES
from src.utils.date_utils import get_week_range, get_last_week_range, get_last_last_week_range


class DataFetcher:
    """資料查詢器"""
    
    def __init__(self):
        self.bq_config = BigQueryConfig()
        self.client = self.bq_config.get_client()
    
    def fetch_gmv_metrics(self, start_date=None, end_date=None):
        """
        查詢 GMV 基本指標
        
        Args:
            start_date: 開始日期（datetime.date），如果為 None 則使用本週週一
            end_date: 結束日期（datetime.date），如果為 None 則使用本週週日
            
        Returns:
            dict: 包含成交營收、總營業額、取消率等指標
        """
        if start_date is None or end_date is None:
            start_date, end_date = get_last_week_range()
        
        # 使用 lv1_order_master 表（訂單主檔）
        table_ref = self.bq_config.get_table_ref(TABLES['lv1_order_master'])
        
        query = f"""
        SELECT
            -- 成交總額：所有訂單的 ord_rev
            SUM(ord_rev) as net_revenue,
            -- 總營業額：排除取消訂單的 ord_rev
            SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) as gross_revenue,
            -- 交易會員數
            COUNT(DISTINCT user_id) as unique_users,
            -- 成交訂單總量：所有訂單數
            COUNT(DISTINCT ord_id) as completed_orders,
            -- 總訂單總量：排除取消的訂單數
            SUM(CASE WHEN bhv1 <> '取消' THEN 1 ELSE 0 END) as total_orders,
            -- 取消訂單數
            COUNT(DISTINCT CASE WHEN bhv1 = '取消' THEN ord_id END) as cancelled_orders,
            -- 取消訂單總額
            SUM(CASE WHEN bhv1 = '取消' THEN ord_rev ELSE 0 END) as cancelled_revenue
        FROM `{table_ref}`
        WHERE DATE(dt) BETWEEN DATE('{start_date}') AND DATE('{end_date}')
            AND touch_class = 'ec'  -- 只查詢電商通路
        """
        
        result = self.bq_config.query(query).to_dataframe()
        
        if result.empty or result.iloc[0].get('total_orders') is None:
            return {
                'net_revenue': 0,
                'gross_revenue': 0,
                'unique_users': 0,
                'completed_orders': 0,
                'total_orders': 0,
                'cancelled_orders': 0,
                'cancelled_revenue': 0,
                'cancel_rate': 0.0,
            }
        
        row = result.iloc[0]
        # 注意：根據 SQL 邏輯
        # completed_orders = 所有訂單數（包含取消）
        # total_orders = 排除取消的訂單數
        # cancelled_orders = 取消的訂單數
        completed_orders = int(row.get('completed_orders') or 0)  # 成交訂單總量（所有訂單）
        total_orders = int(row.get('total_orders') or 0)  # 總訂單總量（排除取消）
        cancelled_orders = int(row.get('cancelled_orders') or 0)
        # 取消率 = 取消訂單數 / 所有訂單數
        cancel_rate = (cancelled_orders / completed_orders * 100) if completed_orders > 0 else 0.0
        
        return {
            'net_revenue': float(row.get('net_revenue') or 0),  # 成交總額（所有 ord_rev）
            'gross_revenue': float(row.get('gross_revenue') or 0),  # 總營業額（排除取消的 ord_rev）
            'unique_users': int(row.get('unique_users') or 0),  # 交易會員數
            'completed_orders': completed_orders,  # 成交訂單總量（所有訂單數）
            'total_orders': total_orders,  # 總訂單總量（排除取消的訂單數）
            'cancelled_orders': cancelled_orders,  # 取消訂單數
            'cancelled_revenue': float(row.get('cancelled_revenue') or 0),  # 取消訂單總額
            'cancel_rate': round(cancel_rate, 2),
        }
    
    def fetch_weekly_comparison(self):
        """
        查詢上週（上週一到上週日）與上上週（上上週一到上上週日）的比較資料
        
        Returns:
            dict: 包含上週與上上週的指標，以及變化百分比
        """
        # 計算上週範圍（上週一到上週日）- 這是觀察週
        this_week_monday, this_week_sunday = get_last_week_range()
        
        # 計算上上週範圍（上上週一到上上週日）- 這是對比週
        last_week_monday, last_week_sunday = get_last_last_week_range()
        
        # 查詢上週資料（觀察週）
        this_week = self.fetch_gmv_metrics(this_week_monday, this_week_sunday)
        
        # 查詢上上週資料（對比週）
        last_week = self.fetch_gmv_metrics(last_week_monday, last_week_sunday)
        
        # 計算變化百分比
        def calc_change(current, previous):
            if previous == 0:
                return 100.0 if current > 0 else 0.0
            return round(((current - previous) / previous) * 100, 2)
        
        return {
            'this_week': this_week,  # 實際上是上週
            'last_week': last_week,  # 實際上是上上週
            'changes': {
                'revenue': calc_change(this_week['net_revenue'], last_week['net_revenue']),
                'orders': calc_change(this_week['completed_orders'], last_week['completed_orders']),
            }
        }
    
    def fetch_traffic_analysis(self, start_date=None, end_date=None):
        """
        查詢流量分析資料
        
        整合 GA4 events_* 表和 Shopline 訂單表，透過 transaction_id JOIN ord_id
        計算各流量來源的 Sessions、CVR、AOV、營收
        
        Args:
            start_date: 開始日期（datetime.date），如果為 None 則使用本週週一
            end_date: 結束日期（datetime.date），如果為 None 則使用本週週日
            
        Returns:
            DataFrame: 各流量來源的 Sessions、CVR、AOV、營收
        """
        from src.utils.traffic_classifier import classify_traffic_source_sql
        
        if start_date is None or end_date is None:
            start_date, end_date = get_last_week_range()
        
        # 生成日期字串列表（用於 GA4 表的分區查詢）
        date_suffixes = []
        current_date = start_date
        while current_date <= end_date:
            date_suffixes.append(current_date.strftime('%Y%m%d'))
            current_date += timedelta(days=1)
        date_suffix_str = "','".join(date_suffixes)
        
        # GA4 事件表
        ga4_table_ref = self.bq_config.get_ga4_table_ref('events_*')
        
        # Shopline 訂單表
        order_master_table = self.bq_config.get_table_ref(TABLES['lv1_order_master'])
        
        # 流量分類 SQL
        # traffic_source 可以直接存取 source 和 medium
        # session_traffic_source_last_click 需要從 manual_campaign 或 cross_channel_campaign 取得
        traffic_classification_sessions = classify_traffic_source_sql('traffic_source.source', 'traffic_source.medium')
        traffic_classification_purchases = classify_traffic_source_sql(
            'COALESCE(session_traffic_source_last_click.manual_campaign.source, session_traffic_source_last_click.cross_channel_campaign.source, "(direct)")',
            'COALESCE(session_traffic_source_last_click.manual_campaign.medium, session_traffic_source_last_click.cross_channel_campaign.medium, "(none)")'
        )
        
        # 分兩步查詢，避免位置問題
        # 步驟 1: 查詢 GA4 Sessions
        ga4_sessions_query = f"""
        SELECT
            {traffic_classification_sessions} as traffic_category,
            COUNT(DISTINCT CONCAT(
                user_pseudo_id, 
                '-', 
                COALESCE(
                    CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS STRING),
                    CAST((SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'session_id') AS STRING),
                    ''
                )
            )) as sessions
        FROM `{ga4_table_ref}`
        WHERE _TABLE_SUFFIX IN ('{date_suffix_str}')
            AND event_name = 'session_start'
        GROUP BY traffic_category
        """
        
        # 步驟 2: 查詢 GA4 Purchases 和 JOIN Shopline 訂單
        # 注意：使用 UNION ALL 來查詢不同位置的資料表，然後在 Python 中 JOIN
        ga4_purchases_query = f"""
        SELECT DISTINCT
            (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') as transaction_id,
            {traffic_classification_purchases} as traffic_category
        FROM `{ga4_table_ref}`
        WHERE _TABLE_SUFFIX IN ('{date_suffix_str}')
            AND event_name = 'purchase'
            AND (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') IS NOT NULL
        """
        
        shopline_orders_query = f"""
        SELECT
            ord_id,
            SUM(CASE WHEN bhv1 <> '取消' THEN ord_rev ELSE 0 END) as revenue,
            AVG(CASE WHEN bhv1 <> '取消' THEN ord_rev END) as aov
        FROM `{order_master_table}`
        WHERE DATE(dt) BETWEEN DATE('{start_date}') AND DATE('{end_date}')
            AND touch_class = 'ec'
            AND bhv1 <> '取消'
        GROUP BY ord_id
        """
        
        try:
            # 查詢 GA4 Sessions
            sessions_df = self.bq_config.query(ga4_sessions_query).to_dataframe()
            
            # 查詢 GA4 Purchases
            purchases_df = self.bq_config.query(ga4_purchases_query).to_dataframe()
            
            # 查詢 Shopline 訂單
            orders_df = self.bq_config.query(shopline_orders_query).to_dataframe()
            
            # 在 Python 中 JOIN
            if purchases_df.empty or orders_df.empty:
                return pd.DataFrame(columns=['traffic_source', 'sessions', 'conversions', 'cvr', 'aov', 'revenue'])
            
            # JOIN purchases 和 orders
            traffic_orders = purchases_df.merge(
                orders_df,
                left_on='transaction_id',
                right_on='ord_id',
                how='inner'
            )
            
            if traffic_orders.empty:
                return pd.DataFrame(columns=['traffic_source', 'sessions', 'conversions', 'cvr', 'aov', 'revenue'])
            
            # 按流量來源聚合
            traffic_agg = traffic_orders.groupby('traffic_category').agg({
                'transaction_id': 'count',
                'revenue': 'sum',
                'aov': 'mean'
            }).reset_index()
            traffic_agg.columns = ['traffic_category', 'conversions', 'revenue', 'aov']
            
            # 合併 Sessions 資料
            if not sessions_df.empty:
                result_df = sessions_df.merge(
                    traffic_agg,
                    on='traffic_category',
                    how='outer'
                )
            else:
                result_df = traffic_agg.copy()
                result_df['sessions'] = 0
            
            # 計算 CVR
            result_df['cvr'] = result_df.apply(
                lambda row: round((row['conversions'] / row['sessions'] * 100), 2) if row['sessions'] > 0 else 0.0,
                axis=1
            )
            
            # 重新命名並填充空值
            result_df['traffic_source'] = result_df['traffic_category'].fillna('8. 其他')
            result_df = result_df.fillna(0)
            
            # 選擇需要的欄位
            result_df = result_df[[
                'traffic_source', 'sessions', 'conversions', 'cvr', 'aov', 'revenue'
            ]].sort_values('revenue', ascending=False)
            
            return result_df
            
        except Exception as e:
            print(f"⚠️  查詢流量分析時發生錯誤: {str(e)}")
            # 如果查詢失敗，返回空 DataFrame
            return pd.DataFrame(columns=['traffic_source', 'sessions', 'conversions', 'cvr', 'aov', 'revenue'])
        
        try:
            df = self.bq_config.query(query).to_dataframe()
            
            if df.empty:
                return pd.DataFrame(columns=['traffic_source', 'sessions', 'conversions', 'cvr', 'aov', 'revenue'])
            
            # 確保所有欄位都有值
            df = df.fillna(0)
            
            return df
            
        except Exception as e:
            print(f"⚠️  查詢流量分析時發生錯誤: {str(e)}")
            # 如果查詢失敗，返回空 DataFrame
            return pd.DataFrame(columns=['traffic_source', 'sessions', 'conversions', 'cvr', 'aov', 'revenue'])
    
    def fetch_aov_analysis(self, start_date=None, end_date=None, dimension='overall'):
        """
        查詢平均訂單金額分析
        
        Args:
            start_date: 開始日期（datetime.date），如果為 None 則使用本週週一
            end_date: 結束日期（datetime.date），如果為 None 則使用本週週日
            dimension: 分析維度（'overall', 'new', 'returning'）
            
        Returns:
            dict: 包含購物車件數分布和價格帶結構
        """
        if start_date is None or end_date is None:
            start_date, end_date = get_last_week_range()
        
        # 使用 lv1_order 表（訂單明細）計算購物車件數
        order_table = self.bq_config.get_table_ref(TABLES['lv1_order'])
        order_master_table = self.bq_config.get_table_ref(TABLES['lv1_order_master'])
        
        # 根據維度加入條件（需要判斷新客/回購客）
        dimension_join = ""
        if dimension == 'new':
            # TODO: 需要判斷是否為首次購買，可能需要 JOIN lv1_user 表
            dimension_join = "AND o.user_id IN (SELECT user_id FROM (SELECT user_id, MIN(DATE(dt)) as first_order_date FROM `{order_master_table}` GROUP BY user_id) WHERE DATE(dt) = first_order_date)"
        elif dimension == 'returning':
            dimension_join = "AND o.user_id NOT IN (SELECT user_id FROM (SELECT user_id, MIN(DATE(dt)) as first_order_date FROM `{order_master_table}` GROUP BY user_id) WHERE DATE(dt) = first_order_date)"
        
        # 查詢購物車件數分布（從訂單明細計算每個訂單的件數）
        query_items = f"""
        WITH order_items AS (
            SELECT
                ord_id,
                COUNT(*) as item_count,
                SUM(ord_price * ord_qty) as order_total
            FROM `{order_table}`
            WHERE DATE(dt) BETWEEN DATE('{start_date}') AND DATE('{end_date}')
                AND touch_class = 'ec'
            GROUP BY ord_id
        )
        SELECT
            CASE 
                WHEN item_count = 1 THEN '1件'
                WHEN item_count = 2 THEN '2件'
                WHEN item_count = 3 THEN '3件'
                ELSE '4件以上'
            END as item_count,
            COUNT(*) as order_count,
            AVG(order_total) as avg_amount
        FROM order_items
        GROUP BY item_count
        ORDER BY 
            CASE item_count
                WHEN '1件' THEN 1
                WHEN '2件' THEN 2
                WHEN '3件' THEN 3
                ELSE 4
            END
        """
        
        df_items = self.bq_config.query(query_items).to_dataframe()
        
        # 查詢價格帶結構（從訂單主檔）
        query_price = f"""
        SELECT
            CASE 
                WHEN ord_rev < 500 THEN '低價帶 (<500)'
                WHEN ord_rev < 1500 THEN '中價帶 (500-1500)'
                ELSE '高價帶 (≥1500)'
            END as price_band,
            COUNT(*) as order_count,
            AVG(ord_rev) as avg_amount
        FROM `{order_master_table}`
        WHERE DATE(dt) BETWEEN DATE('{start_date}') AND DATE('{end_date}')
            AND touch_class = 'ec'
            AND bhv1 <> '取消'  -- 只計算成交訂單
        GROUP BY price_band
        ORDER BY 
            CASE price_band
                WHEN '低價帶 (<500)' THEN 1
                WHEN '中價帶 (500-1500)' THEN 2
                ELSE 3
            END
        """
        
        df_price = self.bq_config.query(query_price).to_dataframe()
        
        return {
            'item_distribution': df_items.to_dict('records') if not df_items.empty else [],
            'price_band_distribution': df_price.to_dict('records') if not df_price.empty else [],
        }
    
    def fetch_conversion_funnel(self, start_date=None, end_date=None):
        """
        查詢轉換漏斗資料
        
        Args:
            start_date: 開始日期（datetime.date），如果為 None 則使用本週週一
            end_date: 結束日期（datetime.date），如果為 None 則使用本週週日
            
        Returns:
            dict: 包含全站漏斗、商品分區漏斗、活動分區漏斗
        """
        if start_date is None or end_date is None:
            start_date, end_date = get_last_week_range()
        
        # 查詢 GA4 事件表
        ga4_table_ref = self.bq_config.get_ga4_table_ref('events_*')
        
        # 計算日期範圍的字串格式（用於 _TABLE_SUFFIX）
        date_suffixes = []
        current_date = start_date
        while current_date <= end_date:
            date_suffixes.append(current_date.strftime('%Y%m%d'))
            current_date += timedelta(days=1)
        
        # 查詢 GA4 漏斗事件
        query = f"""
        SELECT
            COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) as visitors,
            COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) as view_item,
            COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) as add_to_cart,
            COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN user_pseudo_id END) as begin_checkout,
            COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_pseudo_id END) as purchase
        FROM `{ga4_table_ref}`
        WHERE _TABLE_SUFFIX IN ('{"','".join(date_suffixes)}')
        """
        
        try:
            result = self.bq_config.query(query).to_dataframe()
            
            if result.empty:
                return {
                    'overall': {
                        'steps': [
                            {'label': '訪客', 'count': 0},
                            {'label': '商品瀏覽', 'count': 0},
                            {'label': '加入購物車', 'count': 0},
                            {'label': '開始結帳', 'count': 0},
                            {'label': '完成購買', 'count': 0},
                        ]
                    },
                    'products': [],
                    'campaigns': [],
                }
            
            row = result.iloc[0]
            
            return {
                'overall': {
                    'steps': [
                        {'label': '訪客', 'count': int(row['visitors'] or 0)},
                        {'label': '商品瀏覽', 'count': int(row['view_item'] or 0)},
                        {'label': '加入購物車', 'count': int(row['add_to_cart'] or 0)},
                        {'label': '開始結帳', 'count': int(row['begin_checkout'] or 0)},
                        {'label': '完成購買', 'count': int(row['purchase'] or 0)},
                    ]
                },
                'products': [],  # TODO: 實作商品分區漏斗
                'campaigns': [],  # TODO: 實作活動分區漏斗
            }
            
        except Exception as e:
            print(f"⚠️  查詢 GA4 漏斗資料時發生錯誤: {str(e)}")
            return {
                'overall': {
                    'steps': [
                        {'label': '訪客', 'count': 0},
                        {'label': '商品瀏覽', 'count': 0},
                        {'label': '加入購物車', 'count': 0},
                        {'label': '開始結帳', 'count': 0},
                        {'label': '完成購買', 'count': 0},
                    ]
                },
                'products': [],
                'campaigns': [],
            }
