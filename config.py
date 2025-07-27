from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class CozeConfig(BaseModel):
    """Coze平台配置"""
    base_url: str = "http://localhost:8888"
    token: str = "pat_1b47ac59af6180272392fbed556e7b91b4684e6e2338d13f4063cf23840615f2"
    mcp_port: int = int(os.getenv("MCP_PORT", 8000))
    
    @property
    def api_url(self) -> str:
        """获取完整的API URL"""
        if self.base_url.startswith('http'):
            return f"{self.base_url}/v1/workflow/run"
        else:
            return f"http://{self.base_url}/v1/workflow/run"
    
    @property
    def headers(self) -> dict:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

# 全局配置实例
coze_config = CozeConfig()