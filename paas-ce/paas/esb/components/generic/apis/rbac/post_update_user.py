# -*- coding: utf-8 -*-
"""
"""
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs


class PostUpdateUser(Component):
    """
    apiMethod POST

    ### 功能描述

    批量编辑用户

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数

    | 字段           | 类型   | 必选 | 描述       |
    | -----          | ------ | ---- | --------   |
    | user_info_list | list |  是  | 批量创建用户   |
    | user_info_list.username  | string |  是  | 用户名  |
    | user_info_list.is_activate  | bool |  是  | 启用禁用  |
    ...
    ### 请求参数示例

    ```python
    {
        "bk_app_code": "xxxx",
        "bk_app_secret": "xxx",
        "bk_token": "xxx-xxx-xxx-xxx-xxx",
        "user_info_list":  [{"username": "huxingqi"}]",
    }
    ```

    ### 返回结果示例


    """

    # 组件所属系统的系统名
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        user_info_list = forms.Field(required=False)


        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["user_info_list"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        data = self.form_data
        # 设置当前操作者
        params = {"operator": self.current_user.username}
        data.update(params)
        # 请求系统接口
        response = self.outgoing.http_client.post(
            host=configs.host,
            path=configs.base_api_url + 'update-user/',
            data = json.dumps(data),
            params = params,
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
                'data': response.get("data", None),
            }
        else:
            result = {
                'code': response.get('code'),
                'api_code': response.get('errcode') or response.get('code'),
                'result': False,
                'message': response['message']
            }

        # 设置组件返回结果，payload为组件实际返回结果
        self.response.payload = result
