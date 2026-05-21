# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs
from .toolkit.tools import base_api_url


class PostCreateHost(Component):
    """
    apiMethod POST

    ### 功能描述

    创建主机

    ### 请求参数
    {{ common_args_desc }}

    #### 接口参数
    | 字段 | 类型 | 必选 | 描述 |
    | :--- | :--- | :--- | :--- |
    | host_info_list | list | 是 | 批量导入的主机列表 元素为Dict包含以下字段 |
    | name | str | 是 | 主机唯一标识(执行脚本等操作需要传入该唯一标识)！ |
    | show_name | str | 是 | 主机显示名！ |
    | ip | str | 是 | 主机IP地址！ |
    | system_type | str | 是 | 主机操作系统，仅支持Linux Windows！ |
    | controller_id | int | 是 | 控制器，选择控制器ID根据工具 opsany_control_get_controller_list 获取到的ID(字段为id)！ |
    | control_type | int | 是 | 管控方式，主机纳管方式包含四种 1: SSH 2: Agent 3: SSH/Agent 4: Agent/SSH |
    | ssh_port | str | 否 | 主机端口，当主机操作系统为Linux时需要输入SSH端口，端口范围为1-65535，默认 22！ |
    | login_port | str | 否 | 主机远程登录端口，当主机操作系统为Linux时需要输入RDP端口, 端口范围为1-65535，默认 3389！ |
    | username | str | 是 | 主机系统用户, 登录或纳管主机使用的主机系统用户！ |
    | group_id | str | 是 | 主机分组，分组id根据工具 opsany_control_get_host_group_list 获取戴的ID(字段为code)，当分组结构为 第一层/第二层/第三层 指向的是嵌套到第三层的分组！ |
    | ssh_type | str | 否 | 密码类型，默认 password！ |
    | password | str | 否 | 密码，主机密码！ |
    | host_type | str | 是 | 主机类型，创建主机成功后会将主机同步至CMDB(资源平台)主机模型内，支持两种主机类型： 物理机: SERVER 虚拟机: VIRTUAL_SERVER ！ |
    | privilege | str | 否 | 特权提升(sudo)，是否开启特权提升 当system_type(操作系统)选择Linux 且 control_type(管控方式)包含SSH！ |
    | privilege_type | str | 否 | 特权类型，两个选项 sudo 或 su！ |
    | privilege_username | str | 否 | 特权用户名！ |
    | privilege_password | str | 否 | 特权密码！ |
    | template_list | list | 否 | Zabbix监控模板列表，包含模板名称和ID |
    | dashboard_dict | dict | 否 | Grafana大屏信息字典 |


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
        host_info_list = forms.Field(required=True)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            return self.get_cleaned_data_when_exist(keys=["host_info_list"])

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        params = self.form_data

        # 设置当前操作者
        params['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.post(
            host=configs.host,
            path='{}create-host/'.format(base_api_url),
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
