import inspect

from opsanymcp.api.base_api import BaseObj


class MonitorApi(BaseObj):
    def opsany_monitor_alert_info(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
        page = kwargs.get("page", 1)
        page_size = kwargs.get("page_size", 50)
        host_name = kwargs.get("host_name")
        problem = kwargs.get("name")
        level_id = kwargs.get("severity")

        filter = {
            "host_name": host_name,
            "problem": problem,
            "level_id": level_id,
        }
        body = {"page": page, "pageSize": page_size, "filter": filter}
        status, data_list, mess = self.call(fun_name, "POST", params={}, body=body, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "eventid": "事件ID",
            "name": "告警名称",
            "objectid": "时间对象ID",
            "clock": "告警时间",
            "ns": "告警持续时间",
            "r_eventid": "恢复时间ID",
            "r_clock": "恢复时间",
            "r_ns": "恢复持续时间",
            "acknowledged": "是否确认",
            "severity": "告警级别(0: 未分类 1: 信息 2: 警告 3: 一般严重 4: 严重 5: 灾难)",
            "cause_eventid": "原因时间ID",
            "suppressed": "是否被抑制",
            "hostid": "Zabbix主机ID",
            "host": "Zabbix主机名",
            "host_id": "管控平台实例ID",
            "host_name": "实例唯一标识",
            "zabbix_host_id": "Zabbix主机ID",
            "show_name": "实例名称",
            "group_full_name": "实例分组完整名称",
            "host_type": "主机模型code(cmdb模型名称)",
            "host_type_name": "主机模型名称(cmdb模型名称)",
            "network_code": "网络设备模型code(cmdb模型code)",
            "network_name": "网络设备模型名称(cmdb模型名称)",
            "device_type": "实例类型 host：主机 network： 网络设备",
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
