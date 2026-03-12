# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs
from .toolkit.tools import base_api_url


class GetWorkOrderInst(Component):
    """
    apiMethod GET

    ### 功能描述

    获取工单实例列表

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数

    | 字段    | 类型     | 必选   | 描述       |
    | ----- | ------ | ---- | -------- |
    | current | string | 是  | 页码 |
    | pageSize | string | 是  | 每页数量 |
    | data_type | string | 否  | 是否分页 |
    | data | string | 否  | 工单标签搜索 |
    | order_by | string | 否  | 排序字段 |
    | order_type | string | 否  | 工单类型 |
    | status | dict | 否  | 工单状态 |
    | create_min_time | string | 否  | 最小时间 |
    | create_max_time | string | 否  | 最大时间 |
    | number | string | 否  | 工单编号 |
    | title | string | 否  | 工单标题 |
    | score | string | 否  | 打分 |
    | contents | string | 否  | 评价内容 |
    | follow | string | 否  | 是否跟踪 |
    | search_type | string | 否  | 搜索字段 |
    | search_data | string | 否  | 搜索数据 |

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
        current = forms.Field(required=False)
        pageSize = forms.Field(required=False)
        data_type = forms.Field(required=False)
        data = forms.Field(required=False)
        order_by = forms.Field(required=False)
        order_type = forms.Field(required=False)
        status = forms.Field(required=False)
        create_min_time = forms.Field(required=False)
        create_max_time = forms.Field(required=False)
        number = forms.Field(required=False)
        title = forms.Field(required=False)
        score = forms.Field(required=False)
        contents = forms.Field(required=False)
        follow = forms.Field(required=False)
        search_type = forms.Field(required=False)
        search_data = forms.Field(required=False)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["current", "pageSize", "data_type", "data", "order_by",
                                                          "order_type", "status", "create_min_time", "create_max_time",
                                                          "number", "title", "score", "contents", "follow",
                                                          "search_type", "search_data"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.get(
            host=configs.host,
            path='{}work-order-inst/'.format(base_api_url),
            params=params,
            data=None,
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
