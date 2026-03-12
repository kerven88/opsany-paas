import json
import os
from pathlib import Path
from typing import Optional
from starlette.responses import Response

import yaml
from requests import request
import urllib3
from opsanymcp import APIEndpoints

urllib3.disable_warnings()


class Request:
    def __init__(self, config, username, api_token):
        self.api_service = config.get("apiService")
        self.url = self.api_service.get("url")
        self.super_username = self.api_service.get("super_username")
        self.username = username
        self.bk_username = username
        self.is_bk_username = False
        self.bk_role = 0
        self.api_token = api_token
        self.headers = {"Content-Type": "application/json; charset=utf-8", "User-Agent": "OpsAny MCP Server v1"}
        self.bk_app_code = self.api_service.get("bk_app_code")
        self.bk_app_secret = self.api_service.get("bk_app_secret")
        self.status, self.message = self.check_user()

    def check_user(self):
        if not self.username:
            return False, "MCP Client headers缺少参数用户名(username)"
        if not self.api_token:
            return False, "MCP Client headers缺少参数APIToken(user-api-token), 工作台-个人设置-API Token"

        check_url = APIEndpoints.check_api_token
        params = {"bk_token": self.api_token, "request_api_from": "esb", "username": self.bk_username}
        err_title = "用户认证失败: {}"
        try:
            url = str(self.url) + check_url
            res = request("GET", url, data={}, params=params, headers=self.headers, timeout=5, verify=False)
            try:
                json_data = res.json()
                message = json_data.get("message") or "Success"
                if json_data.get("result"):
                    user_dict = json_data.get("data") or {}
                    if isinstance(user_dict, dict):
                        if self.bk_username == user_dict.get("username"):
                            self.bk_role = user_dict.get("bk_role") or 0
                            return True, message
                        else:
                            return False, err_title.format("无效的令牌，请检查后重试！")
                    else:
                        return False, err_title.format(message)
                else:
                    return False, err_title.format(message) + "(工作台-个人设置-API Token，创建并获取Token)"
            except Exception as e:
                return False, err_title.format(str(res.content.decode()))
        except Exception as e:
            return False, err_title.format(str(e))

    def _request(self, url_path, method, params, body, headers=None, timeout=10):
        if not headers:
            headers = self.headers
        url = str(self.url) + url_path
        base_params = {
            "bk_app_code": self.bk_app_code,
            "bk_app_secret": self.bk_app_secret,
        }
        if self.is_bk_username:
            base_params["bk_username"] = self.bk_username
        else:
            base_params["bk_token"] = self.api_token
            headers["Cookie"] = f"bk_token={self.api_token};opsany_language=chinese_simplified"
        params.update(base_params)
        body.update(base_params)
        try:
            res = request(method, url, data=json.dumps(body), params=params, headers=headers, timeout=timeout, verify=False)
            try:
                json_data = res.json()
                result = json_data.get("result")
                message = json_data.get("message")
                data = json_data.get("data")
                if not result:
                    return False, [], message
                return True, data, message or "Success"
            except Exception as e:
                return False, [], f"HTTP 响应解析失败: {res.content.decode()}"
        except Exception as e:
            return False, [], f"HTTP 请求失败: {str(url)} {str(e)}"


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

