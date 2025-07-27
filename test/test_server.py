#!/usr/bin/env python3
"""
测试官方MCP服务器
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_official_mcp_server():
    """测试官方MCP服务器"""
    print("=== 测试官方MCP服务器 ===")
    
    try:
        # 创建服务器参数
        server_params = StdioServerParameters(
            command="python",
            args=[str(project_root / "server.py")]
        )
        
        # 连接到服务器
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("✓ 成功连接到MCP服务器")
                
                # 初始化会话
                await session.initialize()
                print("✓ 会话初始化完成")
                
                # 列出可用工具
                tools_result = await session.list_tools()
                print(f"\n可用工具 ({len(tools_result.tools)})个):")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # 列出可用资源
                resources_result = await session.list_resources()
                print(f"\n可用资源 ({len(resources_result.resources)})个):")
                for resource in resources_result.resources:
                    print(f"  - {resource.uri}: {resource.name}")
                
                # 列出可用提示词
                prompts_result = await session.list_prompts()
                print(f"\n可用提示词 ({len(prompts_result.prompts)})个):")
                for prompt in prompts_result.prompts:
                    print(f"  - {prompt.name}: {prompt.description}")
                
                # 测试工具调用
                print("\n=== 测试工具调用 ===")
                
                # 测试get_workflow_status工具
                print("\n测试 get_workflow_status 工具:")
                try:
                    status_result = await session.call_tool(
                        "get_workflow_status",
                        {"execute_id": "test_execute_id_123"}
                    )
                    print(f"✓ 工具调用成功")
                    for content in status_result.content:
                        if hasattr(content, 'text'):
                            result_data = json.loads(content.text)
                            print(f"  结果: {json.dumps(result_data, ensure_ascii=False, indent=2)}")
                except Exception as e:
                    print(f"✗ 工具调用失败: {e}")
                
                # 测试资源获取
                print("\n=== 测试资源获取 ===")
                try:
                    resource_result = await session.read_resource(
                        "coze://workflow/test_workflow_123"
                    )
                    print(f"✓ 资源获取成功")
                    for content in resource_result.contents:
                        if hasattr(content, 'text'):
                            print(f"  内容: {content.text[:200]}...")
                except Exception as e:
                    print(f"✗ 资源获取失败: {e}")
                
                # 测试提示词
                print("\n=== 测试提示词 ===")
                try:
                    prompt_result = await session.get_prompt(
                        "create_workflow_execution_prompt",
                        {
                            "workflow_id": "test_workflow_123",
                            "task_description": "测试任务描述"
                        }
                    )
                    print(f"✓ 提示词获取成功")
                    if prompt_result.messages:
                        for message in prompt_result.messages:
                            if hasattr(message.content, 'text'):
                                print(f"  内容: {message.content.text[:200]}...")
                except Exception as e:
                    print(f"✗ 提示词获取失败: {e}")
                
                print("\n=== 测试完成 ===")
                
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    await test_official_mcp_server()

if __name__ == "__main__":
    asyncio.run(main())