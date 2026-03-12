from opsanymcp.api.base import BaseObj
from opsanymcp.constants import APIEndpoints


class ControlApi(BaseObj):
    control_get_managed_host_list = APIEndpoints.control_get_managed_host_list

    def opsany_control_get_managed_host_list(self, **kwargs):
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
        body = {"token_data": self.this_request.api_token}

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
        status, data_list, mess = self.this_request._request(self.control_get_managed_host_list, "POST", params={}, body=body)
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
