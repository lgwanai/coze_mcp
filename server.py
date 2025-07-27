#!/usr/bin/env python3
"""
Coze工作流MCP服务 - 官方版本
使用官方MCP Python SDK中的FastMCP
"""

import asyncio
import json
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from coze_client import CozeWorkflowClient, WorkflowRequest
from config import coze_config

# 创建FastMCP实例
mcp = FastMCP("CozeWorkflow", port=coze_config.mcp_port)

# 全局客户端实例
workflow_client = None

@mcp.tool()
async def run_coze_workflow(
    workflow_id: str,
    parameters: Optional[Dict[str, Any]] = None,
    bot_id: Optional[str] = None,
    is_async: Optional[bool] = False,
    app_id: Optional[str] = None
) -> str:
    """
    执行Coze工作流
    
    Args:
        workflow_id: 工作流ID
        parameters: 工作流输入参数，格式为键值对
        bot_id: 关联的智能体ID（可选）
        is_async: 是否异步执行（可选，默认False）
        app_id: 应用ID（可选）
    
    Returns:
        工作流执行结果的JSON字符串
    """
    global workflow_client
    
    if workflow_client is None:
        workflow_client = CozeWorkflowClient()
    
    try:
        # 创建请求对象
        request = WorkflowRequest(
            workflow_id=workflow_id,
            parameters=parameters,
            bot_id=bot_id,
            is_async=is_async,
            app_id=app_id
        )
        
        # 执行工作流
        response = await workflow_client.run_workflow(request)
        
        # 返回结果
        return json.dumps({
            "code": response.code,
            "msg": response.msg,
            "data": response.data,
            "execute_id": response.execute_id,
            "debug_url": response.debug_url,
            "usage": response.usage
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "code": -1,
            "msg": f"执行失败: {str(e)}",
            "data": None
        }, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_workflow_status(
    execute_id: str
) -> str:
    """
    查询异步工作流执行状态（预留接口）
    
    Args:
        execute_id: 异步执行ID
    
    Returns:
        执行状态信息
    """
    # 注意：这里只是预留接口，实际需要根据Coze平台的查询API实现
    return json.dumps({
        "code": 0,
        "msg": "查询状态功能待实现",
        "execute_id": execute_id,
        "status": "pending"
    }, ensure_ascii=False, indent=2)

@mcp.resource("coze://workflow/{workflow_id}")
async def get_workflow_info(workflow_id: str) -> str:
    """
    获取工作流信息资源
    
    Args:
        workflow_id: 工作流ID
    
    Returns:
        工作流基本信息
    """
    return f"""# 工作流信息

**工作流ID**: {workflow_id}

**描述**: 这是一个Coze平台的工作流，可以通过run_coze_workflow工具执行。

**使用方法**:
```python
# 执行工作流
result = await run_coze_workflow(
    workflow_id="{workflow_id}",
    parameters={{"key": "value"}}
)
```

**注意事项**:
- 工作流必须已发布才能执行
- 某些工作流可能需要关联智能体ID
- 支持同步和异步执行模式
"""

@mcp.prompt()
async def create_workflow_execution_prompt(
    workflow_id: str,
    task_description: str
) -> str:
    """
    创建工作流执行提示词
    
    Args:
        workflow_id: 工作流ID
        task_description: 任务描述
    
    Returns:
        执行提示词
    """
    return f"""请执行以下Coze工作流任务：

**任务描述**: {task_description}
**工作流ID**: {workflow_id}

请使用run_coze_workflow工具执行此工作流，并根据任务需求设置合适的参数。

执行步骤：
1. 分析任务需求，确定需要的输入参数
2. 调用run_coze_workflow工具
3. 解析执行结果
4. 如果需要，可以访问debug_url查看详细执行过程
"""

if __name__ == "__main__":
    # 使用FastMCP启动服务
    print("启动Coze工作流MCP服务 (FastMCP版本)...")
    
    # 客户端将在首次工具调用时按需初始化
    # 启动FastMCP服务器
    print(f"启动FastMCP服务器 on port {coze_config.mcp_port}...")
    mcp.run(transport="sse")