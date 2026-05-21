# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs
from .toolkit.tools import base_api_url


class GetWorkOrderEvent(Component):
    """
    apiMethod GET

    ### 功能描述

    获取告警转工单列表

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数

    | 字段    | 类型     | 必选   | 描述       |
    | ----- | ------ | ---- | -------- |
    | id    | int | 否 | 工单模板ID 根据工单获取工单详情包括字段数据 |
    | event_type    | int | 否 | 告警类型 |
    | username    | string | 否 | 用户名 |
    | form_fields    | bool | 否 | 是否包含字段内容，当获取少量数据时使用，防止数据过大 |
    | folder_id    | int | 否 | 目录ID 空获取全部 |
    | data_type    | string | 否    | 工单类型，all： 全部类型 tags：我的收藏 request：请求管理 change：变更管理 event：事件管理 issues：问题管理 recently：最近提单|
    | name_or_describe   | string | 否    | 名字和描述模糊搜索 |

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
        id = forms.Field(required=False)
        event_type = forms.Field(required=False)
        username = forms.Field(required=False)
        folder_id = forms.Field(required=False)
        data_type = forms.Field(required=False)
        form_fields = forms.Field(required=False)
        name_or_describe = forms.Field(required=False)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["id", "event_type", "username", "folder_id", "data_type", "form_fields", "name_or_describe"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.get(
            host=configs.host,
            path='{}work-order-event/'.format(base_api_url),
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
