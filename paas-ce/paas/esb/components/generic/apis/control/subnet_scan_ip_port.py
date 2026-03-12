# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs
from .toolkit.tools import base_api_url


class SubnetScanIpPort(Component):
    """
    apiMethod POST

    ### 功能描述

    扫描IP端口服务

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数

    | 字段    | 类型     | 必选   | 描述       |
    | ----- | ------ | ---- | -------- |
    | scan_type | str | 否  | 扫描类型 nmap|
    | proxy_id | int | 是  | 控制器ID 1 |
    | ip_start | str | 是  | 起始IP 192.168.0.111|
    | ip_end | str | 是  | 结束IP 192.168.0.200|
    | port_list | list | 否  | 端口范围 ["0-800", "8000"]|
    | timeout | int | 否  | 超时时间 600|
    | params | dict | 否  | 其他参数 {} |

    ### 请求参数示例

    ```python
    {
        "bk_app_code": "esb-test-app",
        "bk_app_secret": "xxx",
        "bk_token": "xxx-xxx-xxx-xxx-xxx",
        "host_id":  1
    }
    ```

    ### 返回结果示例

    ```python
    {
        "code": 200,
        "apicode": 20003,
        "result": true,
        "request_id": xxxxxxxxxxxxxxxxxxxxxxxx,
        "message": "相关信息更新成功",
        "data": [
            ...
        ]
    }
    ```
    """

    # 组件所属系统的系统名
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        scan_type = forms.Field(required=False)
        proxy_id = forms.Field(required=True)
        ip_start = forms.Field(required=True)
        ip_end = forms.Field(required=True)
        port_list = forms.Field(required=False)
        timeout = forms.Field(required=False)
        params = forms.Field(required=False)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["scan_type", "proxy_id", "ip_start", "ip_end", "port_list", "timeout", "params"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.post(
            host=configs.host,
            path='{}ip-port-scan/'.format(base_api_url),
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
