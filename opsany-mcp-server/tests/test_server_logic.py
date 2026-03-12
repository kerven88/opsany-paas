#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opsanymcp import load_yaml_config
from opsanymcp.api import Resource, ResourceType, ResourceFields


async def test_server_logic():
    """测试服务器逻辑（不启动 HTTP 服务器）"""
    print("=" * 60)
    print("测试 OpsAny MCP Server 逻辑")
    print("=" * 60)
    print()
    
    # 加载配置
    print("1. 加载配置...")
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    status, config = load_yaml_config(config_path)
    if not status:
        print(f"✗ 配置加载失败: {config}")
        return
    print("✓ 配置加载成功")
    print()
    
    # 测试 api_resources
    print("2. 测试 api_resources...")
    try:
        res = ResourceType(config)
        status, headers, data, mess = res.get_resources_type(output=None, limit=5)
        if status:
            print(f"✓ api_resources 调用成功")
            print(f"  返回数据条数: {len(data)}")
            print(f"  消息: {mess}")
            if data:
                print(f"  示例数据: {data[0][:3]}")
        else:
            print(f"✗ api_resources 调用失败: {mess}")
    except Exception as e:
        print(f"✗ api_resources 调用异常: {str(e)}")
    print()
    
    # 测试 get_resource_fields
    print("3. 测试 get_resource_fields...")
    try:
        res = ResourceFields(config)
        status, headers, data, mess = res.get_resource_field("SERVER")
        if status:
            print(f"✓ get_resource_fields 调用成功")
            print(f"  返回字段数量: {len(data)}")
            if data:
                print(f"  示例字段: {data[0][:3]}")
        else:
            print(f"✗ get_resource_fields 调用失败: {mess}")
    except Exception as e:
        print(f"✗ get_resource_fields 调用异常: {str(e)}")
    print()
    
    # 测试 get_resource
    print("4. 测试 get_resource...")
    try:
        default_config = config.get('config') or {}
        resource_id_default_field = default_config.get('resourceIdDefaultField') or "code,VISIBLE_NAME,name"
        resource_id_field_search = default_config.get('resourceIdFieldSearch') or False
        
        res = Resource(config)
        status, headers, data, mess = res.get_resource(
            "SERVER", None, None, None, 1, 5,
            resource_id_default_field, resource_id_field_search
        )
        if status:
            print(f"✓ get_resource 调用成功")
            print(f"  返回数据条数: {len(data)}")
            print(f"  消息: {mess}")
            if data:
                print(f"  示例数据: {data[0][:3]}")
        else:
            print(f"✗ get_resource 调用失败: {mess}")
    except Exception as e:
        print(f"✗ get_resource 调用异常: {str(e)}")
    print()
    
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_server_logic())
