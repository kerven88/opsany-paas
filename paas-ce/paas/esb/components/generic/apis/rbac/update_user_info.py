# -*- coding: utf-8 -*-
"""
"""
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs


class UpdateUserInfo(Component):
    """
    apiMethod POST

    ### 功能描述

    更新用户信息

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数

    | 字段           | 类型   | 必选 | 描述       |
    | -----          | ------ | ---- | --------   |
    | username | string |  是  | 用户名   |
    | ch_name      | string |  是  | 中文名  |
    | phone    | string |  是  |  电话   |
    | email    | string |  是  | 电子邮箱   |
    | set_password    | string |  否  | 是否已设置密码   |
    | params    | string |  否  | 额外参数   |

    ### 请求参数示例

    ```python
    ```

    ### 返回结果示例

    ```python
    ```
    """

    # 组件所属系统的系统名
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        username = forms.Field()
        ch_name = forms.Field(required=False)
        phone = forms.Field(required=False)
        email = forms.Field(required=False)
        set_password = forms.BooleanField(required=False)
        params = forms.Field(required=False)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["username", "ch_name", "phone", "email", "set_password", "params"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data
        data = self.request.wsgi_request.body

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.post(
            host=configs.host,
            path=configs.base_api_url + 'update-user-info/',
            data = data,
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
