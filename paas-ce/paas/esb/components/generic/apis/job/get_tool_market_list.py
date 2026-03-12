# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs


class GetToolMarketList(Component):
    """
    apiMethod GET

    ### 功能描述

    获取工具市场中的作业或脚本

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数

    | 字段    | 类型   | 必选 | 描述      |
    | -----  | ------ | ---- | ------- |
    | data_type  | str  |  否  | 工具类型 job：作业 script：脚本 all: 全部 |
    | id     | int    |  否  | 指定ID作业或脚本 |
    | job_id     | int    |  否  | 指定作业ID获取作业详情 |
    | script_id     | int    |  否  | 指定脚本ID获取脚本详情 |
    | script_name     | str    |  否  | 脚本名称 |
    | create_user     | str    |  否  | 创建人 用户名或中文名 |
    | visible     | str    |  否  | 可见范围 1：私有 2：公开 |
    | script_type     | str    |  否  | 脚本类型(脚本参数)： sh, py, ps1, bat|
    | search_type     | str    |  否  | 搜索 |
    | search_data     | str    |  否  | 搜索 |
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
        data_type = forms.CharField(required=False)
        id = forms.IntegerField(required=False)
        job_id = forms.IntegerField(required=False)
        script_id = forms.IntegerField(required=False)
        script_name = forms.CharField(required=False)
        create_user = forms.CharField(required=False)
        visible = forms.CharField(required=False)
        script_type = forms.CharField(required=False)
        search_type = forms.CharField(required=False)
        search_data = forms.CharField(required=False)


        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["data_type", "id", "job_id", "script_id", "script_name",
                                                          "create_user", "visible", "script_type", "search_type",
                                                          "search_data"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.get(
            host=configs.host,
            path='{}tool-market-list/'.format(configs.base_api_url),
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
