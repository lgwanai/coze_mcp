#!/usr/bin/env python3
"""
测试Coze工作流客户端
"""

import asyncio
import json
import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from coze_client import CozeWorkflowClient, WorkflowRequest

async def test_workflow_client():
    """测试工作流客户端"""
    client = CozeWorkflowClient()
    
    try:
        # 测试工作流执行
        print("测试工作流执行...")
        
        request = WorkflowRequest(
            workflow_id="7531773147675099136",
            parameters={
                "test_param": "hello world",
                "user_id": "test_user_123"
            }
        )
        
        response = await client.run_workflow(request)
        
        print(f"响应代码: {response.code}")
        print(f"响应消息: {response.msg}")
        print(f"响应数据: {response.data}")
        print(f"调试URL: {response.debug_url}")
        
        if response.usage:
            print(f"Token使用情况: {response.usage}")
        
        return response.code == 0
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False
    finally:
        await client.close()

async def test_async_workflow():
    """测试异步工作流执行"""
    client = CozeWorkflowClient()
    
    try:
        print("\n测试异步工作流执行...")
        
        request = WorkflowRequest(
            workflow_id="7531773147675099136",
            parameters={
                "test_param": "async test",
                "user_id": "async_user_123"
            },
            is_async=True
        )
        
        response = await client.run_workflow(request)
        
        print(f"异步响应代码: {response.code}")
        print(f"异步响应消息: {response.msg}")
        print(f"执行ID: {response.execute_id}")
        
        return response.code == 0
        
    except Exception as e:
        print(f"异步测试失败: {e}")
        return False
    finally:
        await client.close()

if __name__ == "__main__":
    print("开始测试Coze工作流客户端...")
    
    # 运行测试
    sync_result = asyncio.run(test_workflow_client())
    async_result = asyncio.run(test_async_workflow())
    
    print("\n测试结果:")
    print(f"同步工作流测试: {'通过' if sync_result else '失败'}")
    print(f"异步工作流测试: {'通过' if async_result else '失败'}")
    
    if sync_result and async_result:
        print("\n所有测试通过！")
    else:
        print("\n部分测试失败，请检查配置和网络连接。")