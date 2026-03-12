#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """测试 MCP Server 的基本功能"""
    
    print("开始测试 OpsAny MCP Server...")
    print("=" * 60)
    
    # 连接到 MCP Server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py", "--config", "config/config.yaml"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()
            print("✓ MCP Server 初始化成功")
            print()
            
            # 列出可用的工具
            tools = await session.list_tools()
            print(f"✓ 可用工具数量: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # 测试 api_resources 工具
            print("测试 api_resources 工具...")
            try:
                result = await session.call_tool("api_resources", {"limit": 10})
                if result.content:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("success"):
                            print(f"✓ api_resources 调用成功")
                            print(f"  返回数据条数: {len(data.get('data', []))}")
                        else:
                            print(f"✗ api_resources 调用失败: {data.get('error')}")
                    else:
                        print(f"✗ api_resources 返回格式异常")
                else:
                    print(f"✗ api_resources 没有返回内容")
            except Exception as e:
                print(f"✗ api_resources 调用异常: {str(e)}")
            print()
            
            # 测试 get_resource_fields 工具
            print("测试 get_resource_fields 工具...")
            try:
                result = await session.call_tool("get_resource_fields", {"resource": "SERVER"})
                if result.content:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("success"):
                            print(f"✓ get_resource_fields 调用成功")
                            print(f"  返回字段数量: {len(data.get('data', []))}")
                        else:
                            print(f"✗ get_resource_fields 调用失败: {data.get('error')}")
                    else:
                        print(f"✗ get_resource_fields 返回格式异常")
                else:
                    print(f"✗ get_resource_fields 没有返回内容")
            except Exception as e:
                print(f"✗ get_resource_fields 调用异常: {str(e)}")
            print()
            
            # 测试 get_resource 工具
            print("测试 get_resource 工具...")
            try:
                result = await session.call_tool("get_resource", {
                    "resource_type": "SERVER",
                    "limit": 5
                })
                if result.content:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("success"):
                            print(f"✓ get_resource 调用成功")
                            print(f"  返回数据条数: {len(data.get('data', []))}")
                            print(f"  消息: {data.get('message')}")
                        else:
                            print(f"✗ get_resource 调用失败: {data.get('error')}")
                    else:
                        print(f"✗ get_resource 返回格式异常")
                else:
                    print(f"✗ get_resource 没有返回内容")
            except Exception as e:
                print(f"✗ get_resource 调用异常: {str(e)}")
            print()
            
    print("=" * 60)
    print("测试完成！")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
