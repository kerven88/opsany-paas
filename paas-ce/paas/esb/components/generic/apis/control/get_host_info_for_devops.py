# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs
from .toolkit.tools import base_api_url


class GetHostInfoForDevops(Component):
    """
    apiMethod GET

    ### 功能描述

    获取指定应用关联的所有主机

    ### 请求参数
    
    {{ common_args_desc }}
    
    #### 接口参数

    | 字段    | 类型     | 必选   | 描述       |
    | ----- | ------ | ---- | -------- |
    | app_name_list | list or str | 是    |  应用唯一标识 |
    | search_type | string | 否    |  搜索条件 |
    | search_data | string | 否    |  搜索内容 |
    | prom_state | string | 否    |  可用性状态 |
    | alert | string | 否    |  未恢复告警 |
    | control_agent_id | string | 否    |  管控已添加主机的id |


    ### 返回结果示例

    ```python
    {
        "code": 200,
        "apicode": 20012,
        "result": true,
        "request_id": xxxxxxxxxxxxxxxxxxxxxxxx,
        "message": "获取相关信息成功"
    }
    ```
    """

    # 组件所属系统的系统名
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        app_name_list = forms.Field(required=True)
        search_type = forms.Field(required=False)
        search_data = forms.Field(required=False)
        prom_state = forms.Field(required=False)
        alert = forms.Field(required=False)
        control_agent_id = forms.Field(required=False)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["app_name_list", "search_type", "search_data", "prom_state",
                                                          "alert", "control_agent_id"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username
        # 请求系统接口
        response = self.outgoing.http_client.post(
            host=configs.host,
            path='{}get-host-info-for-devops/'.format(base_api_url),
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
                'data': response.get("data", None),
            }
        else:
            result = {
                'api_code': response['errcode'],
                'result': False,
                'message': response['message']
            }

        # 设置组件返回结果，payload为组件实际返回结果
        self.response.payload = result
