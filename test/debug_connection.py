#!/usr/bin/env python3
"""
调试连接问题
"""

import asyncio
import httpx
import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import coze_config

async def test_mcp_server():
    """测试MCP服务器连接"""
    print("=== 测试MCP服务器连接 ===")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/sse/")
            print(f"✅ MCP服务器响应: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            return True
    except Exception as e:
        print(f"❌ MCP服务器连接失败: {e}")
        return False

async def test_coze_api():
    """测试Coze API连接"""
    print("\n=== 测试Coze API连接 ===")
    print(f"API URL: {coze_config.api_url}")
    print(f"Token: {coze_config.token[:20]}...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 简单的GET请求测试连接
            response = await client.get(coze_config.base_url)
            print(f"✅ Coze平台连接: {response.status_code}")
            
            # 测试工作流API
            payload = {
                "workflow_id": "7531773147675099136",
                "parameters": {"test": "debug"}
            }
            
            response = await client.post(
                coze_config.api_url,
                headers=coze_config.headers,
                json=payload
            )
            
            print(f"工作流API响应: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            
            return response.status_code == 200
            
    except httpx.ConnectError as e:
        print(f"❌ 连接错误: {e}")
        return False
    except httpx.TimeoutException as e:
        print(f"❌ 超时错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

async def test_network_basic():
    """测试基本网络连接"""
    print("\n=== 测试基本网络连接 ===")
    
    # 测试本地端口
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8888")
            print(f"✅ localhost:8888 响应: {response.status_code}")
    except Exception as e:
        print(f"❌ localhost:8888 连接失败: {e}")
    
    # 测试MCP端口
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000")
            print(f"✅ localhost:8000 响应: {response.status_code}")
    except Exception as e:
        print(f"❌ localhost:8000 连接失败: {e}")

if __name__ == "__main__":
    print("🔍 开始连接调试...")
    
    asyncio.run(test_network_basic())
    asyncio.run(test_mcp_server())
    asyncio.run(test_coze_api())
    
    print("\n🏁 调试完成")