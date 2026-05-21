import inspect

from opsanymcp.api.base_api import BaseObj


class WorkbenchApi(BaseObj):
    def opsany_workbench_work_order_inst(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
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
        status, data_list, mess = self.call(fun_name, "GET", params=params, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "id": "工单实例ID",
            "number": "工单实例编号",
            "title": "工单实例标题",
            "status": "工单实例状态",
            "error": "工单实例错误信息",
            "work_order_name": "工单名称",
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

    def opsany_workbench_work_order_folder(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
        params = {}
        status, data_list, mess = self.call(fun_name, "GET", params=params, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "id": "服务分类ID",
            "name": "服务分类名称",
            "children": "服务子分类",
            "order_count": "服务数量",
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

    def opsany_workbench_work_order_temp(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
        params = {
            "id": kwargs.get("id"),
            "current": kwargs.get("current", 1),
            "pageSize": kwargs.get("pageSize", 10),
            "folder_id": kwargs.get("folder_id"),
            "form_fields": kwargs.get("form_fields"),
            "data_type": kwargs.get("data_type"),
            "name_or_describe": kwargs.get("name_or_describe"),
        }
        status, data_list, mess = self.call(fun_name, "GET", params=params, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "current": "当前页码",
            "pageSize": "每页数量",
            "total": "总数",
            "data.id": "服务ID",
            "data.name": "服务名称",
            "data.unique": "服务唯一标识",
            "data.describe": "服务描述",
            "data.create_time": "服务创建时间",
            "data.order_type": "服务类型",
            "data.order_type.id": "服务类型ID",
            "data.order_type.name": "服务类型名称",
            "data.order_type.key": "服务类型标识",
            "data.folder": "服务分类",
            "data.folder.id": "服务分类ID",
            "data.folder.name": "服务分类名称",
            "data.folder.field_list": "服务表单字段列表",
            "data.folder.field_list.id": "字段ID",
            "data.folder.field_list.field_from": "字段来源(1: 公共字段 2: 手动创建)",
            "data.folder.field_list.default": "默认值",
            "data.folder.field_list.describe": "字段描述",
            "data.folder.field_list.required": "是否必填",
            "data.folder.field_list.index": "字段序号",
            "data.folder.field_list.group_id": "字段组",
            "data.folder.field_list.layout": "字段布局 1：半行  2：整行",
            "data.folder.field_list.code": "字段标识(提单使用)",
            "data.folder.field_list.name": "字段名称",
            "data.folder.field_list.field_type": "字段类型",
            "data.folder.field_list.other_info": "字段约束",
            "data.folder.field_list.rule": "字段规则",
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

    def opsany_workbench_work_order_submit(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
        body = {
            "submit_from": kwargs.get("submit_from", "API提交"),
            "work_order_id": kwargs.get("work_order_id"),
            "follow": kwargs.get("follow"),
            "field_dict": kwargs.get("field_dict"),
        }
        status, data_list, mess = self.call(fun_name, "POST", params={}, body=body, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)
        headers = {
            "id": "工单ID",
            "number": "工单编号",
            "title": "工单标题",
            "status": "工单状态",
            "error": "工单错误信息",
            "work_order_name": "服务名称",
            "work_order_type_name": "服务类型名称",
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
