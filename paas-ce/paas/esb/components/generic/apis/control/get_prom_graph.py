# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs
from .toolkit.tools import base_api_url


class GetPromGraph(Component):
    """
    apiMethod POST

    ### 功能描述

    从Prometheus获取图表视图的指标数据

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数

    | 字段    | 类型     | 必选   | 描述       |
    | ----- | ------ | ---- | -------- |
    | prom_id | string | 是  | prometheus实例id |
    | query | string | 否  | 查询promQL语句 |
    | start | string | 否 | 查询开始时间戳 |
    | end | string | 否 | 查询结束时间戳 |
    | step | string | 否 | 查询步长 |
    | params | string | 否 | 其他查询参数 |


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
        prom_id = forms.Field(required=True)
        query = forms.Field(required=False)
        start = forms.Field(required=False)
        end = forms.Field(required=False)
        step = forms.Field(required=False)
        params = forms.Field(required=False)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["prom_id", "query", "start", "end", "step", "params"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.post(
            host=configs.host,
            path='{}get-prom-graph/'.format(base_api_url),
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
                'message': response['message'],
                'request_data': params
            }

        # 设置组件返回结果，payload为组件实际返回结果
        self.response.payload = result
