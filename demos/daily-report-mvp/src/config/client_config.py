"""
客戶設定檔讀取模組
"""
import yaml
import os
from typing import Dict, Any, Optional


class ClientConfig:
    """客戶設定檔管理"""
    
    def __init__(self, config_path: str = None):
        """
        初始化客戶設定檔
        
        Args:
            config_path: 設定檔路徑（預設為 config/clients.yaml）
        """
        if config_path is None:
            # 預設路徑：相對於專案根目錄
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(current_dir, 'config', 'clients.yaml')
        
        self.config_path = config_path
        self.clients = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        載入設定檔
        
        Returns:
            dict: 客戶設定字典
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"客戶設定檔不存在：{self.config_path}\n"
                f"請複製 config/clients.yaml.example 為 config/clients.yaml 並填入實際值"
            )
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if 'clients' not in config:
            raise ValueError("設定檔格式錯誤：缺少 'clients' 鍵")
        
        # 建立以 client_id 為 key 的字典
        clients_dict = {}
        for client in config['clients']:
            client_id = client.get('client_id')
            if not client_id:
                raise ValueError("設定檔格式錯誤：客戶缺少 'client_id'")
            
            clients_dict[client_id] = client
        
        return clients_dict
    
    def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        取得客戶設定
        
        Args:
            client_id: 客戶 ID
            
        Returns:
            dict: 客戶設定，如果不存在則返回 None
        """
        return self.clients.get(client_id)
    
    def list_clients(self) -> list[str]:
        """
        列出所有客戶 ID
        
        Returns:
            list: 客戶 ID 列表
        """
        return list(self.clients.keys())

