import httpx
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from config import coze_config

class WorkflowRequest(BaseModel):
    """工作流请求参数"""
    workflow_id: str
    parameters: Optional[Dict[str, Any]] = None
    bot_id: Optional[str] = None
    ext: Optional[Dict[str, str]] = None
    is_async: Optional[bool] = False
    app_id: Optional[str] = None

class WorkflowResponse(BaseModel):
    """工作流响应"""
    code: int
    msg: str = "Unknown error"
    data: Optional[str] = None
    execute_id: Optional[str] = None
    debug_url: Optional[str] = None
    detail: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, Any]] = None

class CozeWorkflowClient:
    """Coze工作流客户端"""
    
    def __init__(self):
        self.config = coze_config
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def run_workflow(self, request: WorkflowRequest) -> WorkflowResponse:
        """执行工作流"""
        try:
            # 构建请求数据
            payload = {
                "workflow_id": request.workflow_id
            }
            
            if request.parameters:
                payload["parameters"] = request.parameters
            if request.bot_id:
                payload["bot_id"] = request.bot_id
            if request.ext:
                payload["ext"] = request.ext
            if request.is_async is not None:
                payload["is_async"] = request.is_async
            if request.app_id:
                payload["app_id"] = request.app_id
            
            # 发送请求
            response = await self.client.post(
                self.config.api_url,
                headers=self.config.headers,
                json=payload
            )
            
            # 检查HTTP状态码
            if response.status_code != 200:
                return WorkflowResponse(
                    code=response.status_code,
                    msg=f"HTTP错误: {response.status_code} - {response.text}"
                )
            
            # 解析响应
            try:
                response_data = response.json()
                # print(f"原始响应数据: {response_data}")  # 调试信息
                
                # 确保必要字段存在
                if 'code' not in response_data:
                    response_data['code'] = -1
                if 'msg' not in response_data or response_data['msg'] is None:
                    response_data['msg'] = "响应格式错误"
                
                # 处理可能为None的字段
                for field in ['data', 'execute_id', 'debug_url', 'detail', 'usage']:
                    if field in response_data and response_data[field] is None:
                        response_data[field] = None  # 保持None值
                
                return WorkflowResponse(**response_data)
            except Exception as parse_error:
                return WorkflowResponse(
                    code=-1,
                    msg=f"响应解析错误: {str(parse_error)}"
                )
            
        except httpx.RequestError as e:
            return WorkflowResponse(
                code=-1,
                msg=f"请求错误: {str(e)}"
            )
        except Exception as e:
            return WorkflowResponse(
                code=-1,
                msg=f"未知错误: {str(e)}"
            )
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()