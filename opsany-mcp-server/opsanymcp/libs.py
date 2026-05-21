import json
import os
from pathlib import Path
from typing import Optional

from starlette.requests import Request
from starlette.responses import Response

import yaml

import urllib3
urllib3.disable_warnings()


def load_yaml_config(config_path=None) -> tuple:
    if not config_path:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_config_path = os.path.join(current_dir, "config", "config.yaml")
        user_config_path = os.path.join(str(Path.home()), ".opsany-mcp-server", "config")
        if os.path.exists(project_config_path):
            config_path = project_config_path
        elif os.path.exists(user_config_path):
            config_path = user_config_path
        else:
            config_path = project_config_path
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        if not isinstance(config, dict):
            return False, f"错误: 配置文件 config 格式不正确"

        api_service = config.get("apiService")
        if not isinstance(api_service, dict):
            return False, f"错误: 配置文件 config.apiService 格式不正确"
        if not all([k in api_service for k in ["url", "bk_app_code", "bk_app_secret"]]):
            return False, f"错误: 配置文件 config.apiService 缺少必要项"
        return True, config
    except FileNotFoundError:
        return False, f"错误: 配置文件 '{config_path}' 不存在"
    except yaml.YAMLError as e:
        return False, f"错误: 无法解析 YAML 文件 '{config_path}': {e}"
    except Exception as e:
        return False, f"错误: 未知的错误: {str(e)}"


def check_auth(request, expected_token: Optional[str]) -> Optional[Response]:
    """检查 Bearer Token，失败返回 401"""
    if isinstance(request, Request):
        auth_token = request.headers.get("mcp-auth-token", "")
    else:
        auth_token = dict(request.get("headers", [])).get(b"mcp-auth-token", b"").decode("utf-8")
    if not auth_token:
        return Response(
            content=json.dumps({"error": "Missing Authorization header: mcp-auth-token"}),
            status_code=401,
            media_type="application/json",
        )

    if auth_token != expected_token:
        return Response(
            content=json.dumps({"error": "Invalid mcp auth token"}),
            status_code=401,
            media_type="application/json",
        )
    return None

