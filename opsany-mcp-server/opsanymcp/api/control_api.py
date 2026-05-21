import inspect

from opsanymcp.api.base_api import BaseObj


class ControlApi(BaseObj):
    def opsany_control_get_managed_host_list(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
        host_name_search = kwargs.get('host_name_search')
        show_name_search = kwargs.get('show_name_search')
        ip_search = kwargs.get('ip_search')
        id = kwargs.get('id')
        host_type = kwargs.get('host_type')
        host_name = kwargs.get('host_name')
        show_name = kwargs.get('show_name')
        ip = kwargs.get('ip')
        system_type = kwargs.get("system_type")
        group_type = kwargs.get("group_type")
        group_level = kwargs.get("group_level")
        body = {"token_data": self.api_token}

        if show_name_search: body["show_name"] = show_name_search
        if host_name_search: body["name"] = host_name_search
        if ip_search: body["ip"] = ip_search
        if system_type: body["system_type"] = system_type
        if group_type: body["group_type"] = group_type
        if system_type: body["system_type"] = system_type
        if host_type: body["host_type"] = host_type
        if group_level: body["group_level"] = group_level

        if id:
            body["search_type"] = "search_id_list"
            body["search_data"] = id
        elif host_name:
            body["search_type"] = "search_name_list"
            body["search_data"] = host_name
        elif ip:
            body["search_type"] = "search_ip_list"
            body["search_data"] = ip
        elif show_name:
            body["search_type"] = "search_show_name_list"
            body["search_data"] = show_name
        status, data_list, mess = self.call(fun_name, "POST", {}, body=body, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "normal": "正常主机数",
            "not_normal": "不正常主机数",
            "agent_info.ip": "主机ID",
            "agent_info.host_name": "主机唯一标识",
            "agent_info.show_name": "主机显示名",
            "agent_info.system_type": "系统类型",
            "agent_info.system_details": "系统类型描述",
            "agent_info.ssh_agent_state": "可执行状态",
            "agent_info.ssh_agent_state.id": "可执行状态ID",
            "agent_info.ssh_agent_state.state": "可执行状态",
            "agent_info.agent_state": "Agent状态",
            "agent_info.agent_state.id": "Agent状态ID",
            "agent_info.agent_state.state": "Agent状态",
            "agent_info.ssh_state": "SSH状态",
            "agent_info.ssh_state.id": "SSH状态ID",
            "agent_info.ssh_state.state": "SSH状态",
            "agent_info.control_type": "纳管方式",
            "agent_info.control_type.id": "纳管方式ID",
            "agent_info.control_type.state": "纳管方式",
            "agent_info.group": "主机分组",
            "agent_info.controller_name": "控制名称",
            "agent_info.controller_id": "控制器ID",
        }

        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": data_list}
        else:
            result = []
            new_user_list = []
            for i in data_list:
                new_user_list.append([str(i.get(h) or "") for h in headers])
            for row in new_user_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_control_get_controller_list(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 10)
        name = kwargs.get('name')
        id = kwargs.get('id')
        params = {}
        if name:
            params["search_type"] = "name"
            params["search_data"] = name
        if id:
            params["search_type"] = "id"
            params["search_data"] = id

        status, data_list, mess = self.call(fun_name, "GET", params, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "id": "ID",
            "name": "控制器名称",
            "type": "控制器类型",
            "state1": "内网控制器状态",
            "state2": "外网控制器状态",
            "proxy_description": "控制器描述",
        }
        if id and data_list:
            headers.update({
                "proxy_url": "内网控制器地址",
                "proxy_public_url": "外网控制器地址",
                "proxy_agent_count": "纳管主机数量",
                "proxy_network_count": "纳管网络设备数量",
                "proxy_prom_count": "纳管Prometheus实例数量",
                "proxy_ip_count": "纳管IP地址数量",
                "proxy_database_count": "纳管数据库数量",
                "proxy_web_count": "纳管Web服务数量",
                "proxy_middleware_count": "纳管中间件数量",
            })


        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": data_list}
        else:
            result = []
            new_user_list = []
            for i in data_list:
                new_user_list.append([str(i.get(h) or "") for h in headers])
            for row in new_user_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_control_get_host_group_list(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 60)
        name = kwargs.get('name')
        id = kwargs.get('id')
        params = {}
        if name:
            params["search_type"] = "name"
            params["search_data"] = name
        if id:
            params["search_type"] = "id"
            params["search_data"] = id
        status, data_list, mess = self.call(fun_name, "GET", params, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "code": "ID",
            "name": "分组名称",
            "self_count": "当前组内主机实例数量",
            "count": "主机实例数量",
            "children": "子分组",
        }

        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": data_list}
        else:
            result = []
            new_user_list = []
            for i in data_list:
                new_user_list.append([str(i.get(h) or "") for h in headers])
            for row in new_user_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_control_get_zabbix_list(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 10)
        name = kwargs.get('name')
        id = kwargs.get('id')
        params = {}
        if name:
            params["search_type"] = "name"
            params["search_data"] = name
        if id:
            params["search_type"] = "id"
            params["search_data"] = id
        status, data_list, mess = self.call(fun_name, "GET", params, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "id": "ID",
            "name": "实例名称",
            "group_name": "Zabbix组名",
            "description": "描述",
            "default": "是否默认",
            "version": "Zabbix版本",
            "zabbix_state": "状态",
        }

        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": data_list}
        else:
            result = []
            new_user_list = []
            for i in data_list:
                new_user_list.append([str(i.get(h) or "") for h in headers])
            for row in new_user_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_control_get_prometheus_list(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 10)
        body = {"output": "all"}
        status, data_list, mess = self.call(fun_name, "POST", {}, body=body, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "id": "ID",
            "name": "实例组名称",
            "group_name": "Zabbix组名",
            "description": "实例组描述",
            "prom_list": "Prometheus实例列表",
            "prom_list.id": "Prometheus实例ID",
            "prom_list.name": "状态",
            "prom_list.built_in": "是否内置",
            "prom_list.description": "描述",
            "prom_list.default": "默认值",
            "prom_list.prom_state": "Prometheus状态",
            "prom_list.consul_state": "Consul状态",
        }

        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": data_list}
        else:
            result = []
            new_user_list = []
            for i in data_list:
                new_user_list.append([str(i.get(h) or "") for h in headers])
            for row in new_user_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_control_get_dashboard_list(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 10)
        dashboard_type = kwargs.get("dashboard_type")
        params_data = {}
        if dashboard_type:
            params_data["dashboard_type"] = dashboard_type
        status, data_list, mess = self.call(fun_name, "POST", params_data, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "folder_title": "分组名称",
            "dashboard_list": "大屏列表",
            "dashboard_list.uid": "Zabbix组名",
            "dashboard_list.title": "实例组描述",
            "dashboard_list.url": "Prometheus实例列表",
            "prom_list.tags": "Prometheus实例ID",
        }

        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": data_list}
        else:
            result = []
            new_user_list = []
            for i in data_list:
                new_user_list.append([str(i.get(h) or "") for h in headers])
            for row in new_user_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_control_get_zabbix_temp_list(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 20)
        zabbix_id = kwargs.get("zabbix_id")
        params_data = {}
        if zabbix_id:
            params_data["zabbix_id"] = zabbix_id
        status, data_list, mess = self.call(fun_name, "GET", params_data, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "templateid": "模板ID",
            "name": "模板名称",
            "items.uid": "模板uid",
            "triggers": "模板触发器",
            "graphs": "模板图表",
            "templategroups": "模板分组",
            "templates": "继承模板",
            "hosts": "关联主机数",
            "tags": "标签",
        }

        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": data_list}
        else:
            result = []
            new_user_list = []
            for i in data_list:
                new_user_list.append([str(i.get(h) or "") for h in headers])
            for row in new_user_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_control_create_host(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
        host_name = kwargs.get("host_name")
        body = kwargs
        status, user_list, mess = self.call(fun_name, "POST", params={}, body=body, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)

        result_headers = {
            "success_dict": "创建成功信息",
            "error_dict": "创建失败信息",
        }

        if self.real_data_type == "table_header":
            result = {"columns": result_headers, "rows": user_list}
        else:
            result = []
            new_user_list = []
            for i in user_list:
                new_user_list.append([str(i.get(h) or "") for h in result_headers])
            for row in new_user_list:
                row_dict = dict(zip(result_headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)
