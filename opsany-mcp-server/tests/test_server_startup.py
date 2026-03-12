#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import signal
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import main


async def test_server_startup():
    """测试服务器启动"""
    print("=" * 60)
    print("测试 OpsAny MCP Server 启动")
    print("=" * 60)
    print()
    
    # 修改 sys.argv 来模拟命令行参数
    sys.argv = ["server.py", "--host", "127.0.0.1", "--port", "8001"]
    
    print("尝试启动服务器...")
    print("按 Ctrl+C 停止服务器")
    print()
    
    try:
        await main()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_server_startup())
