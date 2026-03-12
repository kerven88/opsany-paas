#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opsanymcp import load_yaml_config
from opsanymcp.api import Resource, ResourceType, ResourceFields


def test_config_loading():
    """测试配置文件加载"""
    print("测试配置文件加载...")
    print("-" * 60)
    
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml")
    print(f"配置文件路径: {config_path}")
    
    status, config = load_yaml_config(config_path)
    
    if status:
        print("✓ 配置文件加载成功")
        print(f"  API URL: {config.get('apiService', {}).get('url')}")
        print(f"  App Code: {config.get('apiService', {}).get('bk_app_code')}")
        print(f"  Server Host: {config.get('server', {}).get('host')}")
        print(f"  Server Port: {config.get('server', {}).get('port')}")
    else:
        print(f"✗ 配置文件加载失败: {config}")
    
    print()
    return status, config


def test_api_classes(config):
    """测试 API 类实例化"""
    print("测试 API 类实例化...")
    print("-" * 60)
    
    try:
        resource_type = ResourceType(config)
        print("✓ ResourceType 实例化成功")
    except Exception as e:
        print(f"✗ ResourceType 实例化失败: {e}")
        return False
    
    try:
        resource_fields = ResourceFields(config)
        print("✓ ResourceFields 实例化成功")
    except Exception as e:
        print(f"✗ ResourceFields 实例化失败: {e}")
        return False
    
    try:
        resource = Resource(config)
        print("✓ Resource 实例化成功")
    except Exception as e:
        print(f"✗ Resource 实例化失败: {e}")
        return False
    
    print()
    return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("OpsAny MCP Server 单元测试")
    print("=" * 60)
    print()
    
    # 测试配置加载
    status, config = test_config_loading()
    if not status:
        print("配置加载失败，跳过后续测试")
        return
    
    # 测试 API 类实例化
    if not test_api_classes(config):
        print("API 类实例化失败，跳过后续测试")
        return

    print("=" * 60)
    print("所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
