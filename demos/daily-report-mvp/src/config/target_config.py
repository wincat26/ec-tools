"""
目標設定檔讀取模組
支援動態月份目標
"""
import yaml
import os
from datetime import date
from typing import Optional


class TargetConfig:
    """目標設定檔管理"""
    
    def __init__(self, config_path: str = None):
        """
        初始化目標設定檔
        
        Args:
            config_path: 設定檔路徑（預設為 config/targets.yaml）
        """
        if config_path is None:
            # 預設路徑：相對於專案根目錄
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(current_dir, 'config', 'targets.yaml')
        
        self.config_path = config_path
        self.targets = self._load_config()
    
    def _load_config(self) -> dict:
        """
        載入設定檔
        
        Returns:
            dict: 目標字典（key: YYYY-MM, value: 目標金額）
        """
        if not os.path.exists(self.config_path):
            # 如果目標檔不存在，返回空字典（使用客戶設定檔的預設值）
            return {}
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if 'targets' not in config:
            return {}
        
        return config['targets']
    
    def get_monthly_target(self, target_date: date, default: Optional[int] = None) -> Optional[int]:
        """
        取得指定月份的目標金額
        
        Args:
            target_date: 目標日期（用於判斷月份）
            default: 如果找不到目標時的預設值
            
        Returns:
            int: 目標金額（元），如果找不到則返回 default
        """
        # 格式化為 YYYY-MM
        month_key = target_date.strftime('%Y-%m')
        
        # 嘗試取得目標
        target = self.targets.get(month_key)
        
        if target is not None:
            return int(target)
        
        # 如果找不到，返回預設值
        return default
    
    def list_all_targets(self) -> dict:
        """
        列出所有目標
        
        Returns:
            dict: 所有目標（key: YYYY-MM, value: 目標金額）
        """
        return self.targets.copy()

