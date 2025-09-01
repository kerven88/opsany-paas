# -*- coding: utf-8 -*-
"""
"""
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs


class KeepStrategyBastion(Component):
    """
    apiMethod POST

    ### 功能描述

    配置堡垒机各类日志保留天数
 

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数
    | 字段    | 类型     | 必选   | 描述       |
    | ----- | ------ | ---- | -------- |
    | data_type | string | 是  | 操作类型 clean message |
    | strategy_operation_log | dict | 否  | 操作审计 |
    | strategy_session_log | dict | 否  | 会话审计 |
    | strategy_command_log | dict | 否  | 命令审计 |
    | params | dict | 否  | 参数 |

    ### 请求参数示例

    ### 返回结果示例

    ```python
 	{
        "bk_app_code": "esb-test-app",
        "bk_app_secret": "xxx",
        "bk_token": "xxx-xxx-xxx-xxx-xxx",
    }
    ```
    """

    # 组件所属系统的系统名
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        data_type = forms.CharField()
        strategy_operation_log = forms.Field(required=False)
        strategy_session_log = forms.Field(required=False)
        strategy_command_log = forms.Field(required=False)
        params = forms.Field(required=False)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["data_type", "strategy_operation_log", "strategy_session_log", "strategy_command_log", "params"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.post(
            host=configs.host,
            path=configs.base_api_url + 'keep-strategy/',
            data=json.dumps(params),
            cookies=self.request.wsgi_request.COOKIES,
        )

        # 对结果进行解析
        code = response['code']
        if code == 200:
            result = {
                'code': response['code'],
                'api_code': response['successcode'],
                'message': response['message'],
                'result': True,
                'data': response['data'],
            }
        else:
            result = {
                'api_code': response['errcode'],
                'result': False,
                'message': response['message']
            }

        # 设置组件返回结果，payload为组件实际返回结果
        self.response.payload = result
