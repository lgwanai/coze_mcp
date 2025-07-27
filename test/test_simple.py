#!/usr/bin/env python3
"""
简化的MCP服务测试
"""

import asyncio
import httpx
import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_server_running():
    """测试服务器是否运行"""
    try:
        print("测试MCP服务器状态...")
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            # 尝试访问MCP SSE端点
            response = await client.get("http://localhost:8000/sse/")
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code in [200, 405, 426]:  # 426 Upgrade Required也是正常的
                print("✅ MCP服务器正在运行")
                return True
            else:
                print(f"❌ 服务器响应异常: {response.status_code}")
                return False
                
    except httpx.ConnectError:
        print("❌ 无法连接到服务器，请确认服务已启动")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

async def test_direct_workflow_call():
    """直接测试工作流调用功能"""
    try:
        print("\n测试直接工作流调用...")
        
        from coze_client import CozeWorkflowClient, WorkflowRequest
        
        client = CozeWorkflowClient()
        
        request = WorkflowRequest(
            workflow_id="7531773147675099136",
            parameters={
                "input": "测试MCP服务集成",
                "user_id": "mcp_integration_test"
            }
        )
        
        response = await client.run_workflow(request)
        
        print(f"工作流调用结果:")
        print(f"  代码: {response.code}")
        print(f"  消息: {response.msg}")
        print(f"  数据长度: {len(response.data) if response.data else 0}")
        print(f"  调试URL: {response.debug_url}")
        
        await client.close()
        
        return response.code == 0
        
    except Exception as e:
        print(f"❌ 直接调用测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始MCP服务集成测试...")
    print("="*50)
    
    # 运行测试
    server_result = asyncio.run(test_server_running())
    workflow_result = asyncio.run(test_direct_workflow_call())
    
    print("\n" + "="*50)
    print("📊 测试结果汇总:")
    print(f"  MCP服务器状态: {'✅ 通过' if server_result else '❌ 失败'}")
    print(f"  工作流调用功能: {'✅ 通过' if workflow_result else '❌ 失败'}")
    
    if server_result and workflow_result:
        print("\n🎉 所有测试通过！MCP服务运行正常。")
        print("\n📝 使用说明:")
        print("  1. MCP服务已在 http://localhost:8000/sse/ 启动")
        print("  2. 可以在支持MCP的客户端中配置此服务")
        print("  3. 使用 run_coze_workflow 工具执行Coze工作流")
    else:
        print("\n⚠️  部分测试失败，请检查:")
        if not server_result:
            print("  - MCP服务是否正确启动")
        if not workflow_result:
            print("  - Coze平台连接和配置")
            print("  - 工作流ID和参数是否正确")