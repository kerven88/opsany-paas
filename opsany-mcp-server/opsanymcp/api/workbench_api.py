from opsanymcp.api.base import BaseObj
from opsanymcp.constants import APIEndpoints


class WorkbenchApi(BaseObj):
    workbench_work_order_inst_list = APIEndpoints.workbench_work_order_inst_list

    def opsany_workbench_work_order_inst(self, **kwargs):
        params = {
            "current": kwargs.get("current", 1),
            "pageSize": kwargs.get("pageSize", 20),
            "data_type": kwargs.get("data_type", "page"),
            "data": kwargs.get("data", "will"),
            "order_by": kwargs.get("order_by"),
            "order_type": kwargs.get("order_type"),
            "status": kwargs.get("status"),
            "create_min_time": kwargs.get("create_min_time"),
            "create_max_time": kwargs.get("create_max_time"),
            "number": kwargs.get("number"),
            "title": kwargs.get("title"),
            "score": kwargs.get("score"),
            "contents": kwargs.get("contents"),
            "follow": kwargs.get("follow"),
            "search_type":  kwargs.get("search_type"),
            "search_data": kwargs.get("search_data"),
        }
        status, data_list, mess = self.this_request._request(self.workbench_work_order_inst_list, "GET", params=params, body={})
        if not status:
            return self.to_json(False, mess)
        headers = {
            "id": "工单ID",
            "number": "工单编号",
            "title": "工单标题",
            "status": "工单状态",
            "error": "工单错误信息",
            "work_order_name": "工单模板名称",
            "work_order_type_name": "工单类型名称",
            "create_user_username": "提单人用户名",
            "create_user_ch_name": "提单人中文名",
            "create_time": "提单时间",
            "sla_first_resp_time": "SLA协议首次响应时间",
            "first_resp_time": "实际响应时间",
            "first_resp_second": "实际响应时间(单位秒)",
            "sla_resolved_time": "SLA协议解决时间",
            "resolved_time": "实际解决时间",
            "resolved_second": "实际解决时间(单位秒)",
            "first_resp_status": "是否符合响应协议",
            "resolved_status": "是否符合处理协议",
            "current_step.step_name": "当前进度(当前节点)",
            "current_step.index": "当前进度序号",
            "current_step.step_type": "当前节点类型",
            "current_step.step_handler.username": "节点处理人用户名",
            "current_step.step_handler.ch_name": "节点处理人中文名",
            "current_step.step_handler.handle_status": "是否处理",
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
