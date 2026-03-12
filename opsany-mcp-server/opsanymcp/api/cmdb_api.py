from opsanymcp.api.base import BaseObj
from opsanymcp.constants import APIEndpoints


class CMDBApi(BaseObj):
    cmdb_api_resources_api = APIEndpoints.cmdb_api_resources_api
    cmdb_get_resource_fields_api = APIEndpoints.cmdb_get_resource_fields_api
    cmdb_get_resource_api = APIEndpoints.cmdb_get_resource_api

    def opsany_cmdb_api_resources(self, **kwargs):
        limit = kwargs.get("limit", 100)
        output = kwargs.get("output", "")
        try:
            limit = int(limit) or 100
        except Exception:
            limit = 100

        params = {"tree": "3"}
        if output =="extend":
            params["model_type"] = "resource_count,field_count"
        status, model_list, mess = self.this_request._request(self.cmdb_api_resources_api, "GET", params=params, body={})
        if not status:
            return self.to_json(False, mess)
        headers = {
            "model_type_name": "资源类型名称",
            "model_type_code": "资源类型标识",
            "model_group_name": "资源分组名称",
            "model_group_code": "资源分组标识",
            "model_name": "资源名称",
            "model_code": "资源标识",
        }
        if output =="extend":
            headers.update({"resource_count": "资源实例总数", "field_count": "基本属性(字段数量)", "parent_field_count": "从属关系(字段数量)", "link_field_count": "连接关系(字段数量)"})
        dict_data_list = []
        list_data_list = []
        for type_dict in model_list:
            type_name = type_dict.get("value")
            type_code = type_dict.get("key")
            group_children = type_dict.get("children") or []
            for group in group_children:
                group_name = group.get("value")
                group_code = group.get("key")
                children = group.get("children") or []
                for child in children:
                    value =  child.get("value")
                    key =  child.get("key")
                    res_dict = {
                        "model_type_name": type_name,
                        "model_type_code": type_code,
                        "model_group_name": group_name,
                        "model_group_code": group_code,
                        "model_name": value,
                        "model_code": key,
                    }
                    base_li = [type_name, type_code, group_name, group_code, child.get("value"), key]
                    if output == "extend":
                        res_dict.update(**child)
                        base_li.extend([
                            str(child.get("resource_count") or 0),
                            str(child.get("field_count") or 0),
                            str(child.get("parent_field_count") or 0),
                            str(child.get("link_field_count") or 0)
                        ]
                    )
                    list_data_list.append(base_li)
                    dict_data_list.append(res_dict)
        list_data_list = list_data_list[:limit]
        dict_data_list = dict_data_list[:limit]
        if not list_data_list:
            return self.to_json(False, mess)
        result = []
        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": dict_data_list}
        else:
            for row in list_data_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_cmdb_get_resource_fields(self, **kwargs):
        model_code = kwargs.get("model_code")
        if not model_code:
            return self.to_json(False, "resource parameter is required")
        params = {
            "model_code": model_code,
        }
        params.update(self.base_params)
        status, field_list, mess = self.this_request._request(self.cmdb_get_resource_fields_api, "GET", params=params, body={})
        if not status:
            return self.to_json(False, f"获取当前资源 {model_code} 字段失败: {mess}，请使用 api-resources 获取支持的资源！")
        headers = {
            "model_name": "资源名称",
            "model_code": "资源标识",
            "name": "字段名称",
            "code": "字段标识",
            "index": "字段序号",
            "type_name": "字段类型",
            "field_group_code": "字段类分组",
            "is_relationship_field": "字段属性",
            "attribute": "字段相关配置",
        }
        dict_data_list = []
        list_data_list = []
        if self.real_data_type == "table_header":
            result = {"columns": headers, "rows": field_list}
        else:
            result = []
            for field in field_list:
                l = []
                for k, v in headers.items():
                    v = str(field.get(k))
                    if k == "is_relationship_field":
                        if v == "": v = "基本属性"
                        elif v == "1": v = "从属关系"
                        elif v == "2": v = "连接关系"
                    l.append(v)
                list_data_list.append(l)
            for row in list_data_list:
                row_dict = dict(zip(headers.values(), row))
                result.append(row_dict)
        return self.to_json(True, mess, result)

    def opsany_cmdb_get_resource(self, **kwargs):
        model_code = kwargs.get("model_code")
        resource_id = kwargs.get("resource_id")
        search = kwargs.get("search")
        fields = kwargs.get("fields")
        page = kwargs.get("page", 1)
        limit = kwargs.get("limit", 20)
        if model_code is None:
            return self.to_json(False, "model_code parameter is required")

        headers = []
        field_code_list = []
        params = {
            "model_code": model_code,
            "page": page,
            "per_page": limit,
        }
        if resource_id and ("=" in resource_id) and self.resource_id_field_search:
            find_fields, find_value = resource_id.split("=")[:2]
            if resource_id:
                params["find_fields"] = find_fields
                params["find_value"] = find_value

        elif resource_id:
            resource_id_field = self.resource_id_default_field.split(",")
            new_list = []
            for i in resource_id_field:
                if i == "code": new_list.append(i)
                else: new_list.append(model_code + "_" + i)
            params["find_fields"] = ",".join(new_list)
            params["find_value"] = resource_id
        if search:
            params["search_type"] = "all"
            params["search_data"] = search

        params.update(self.base_params)
        fields_status, field_list, fields_mess = self.this_request._request(self.cmdb_get_resource_fields_api, "GET", params=params, body={})
        if not fields_status:
            return self.to_json(False, f"获取当前资源 {model_code} 字段失败: {fields_mess}，请使用 api-resources 获取支持的资源！")

        data_status, data_dict, data_mess = self.this_request._request(self.cmdb_get_resource_api, "GET", params=params, body={})
        if not data_status:
            return self.to_json(False,f"获取当前资源 {model_code} 数据失败: {data_mess}，请使用 api-resources 获取支持的资源！")

        if not data_dict:
            return self.to_json(False,f"获取当前资源 {model_code} 获取数据为空！")

        list_data_list = []

        if not fields:
            new_field_list = field_list[:8]
        else:
            new_field_list = []
            fields = fields.split(",")
            for i in field_list:
                if i.get("code") in fields:
                    new_field_list.append(i)

        current = data_dict.get("current")
        page_size = data_dict.get("pageSize")
        total = data_dict.get("total")
        data_list = data_dict.get("data", [])
        total_pages = (total + page_size - 1) // page_size
        mess = f"第 {current} 页，共 {total_pages} 页；当前页 {len(data_list)} 条，总共 {total} 条。"

        if self.real_data_type == "table_header":
            result = {"columns": new_field_list, "rows": data_dict}
        else:
            for field in field_list:
                field_code = field.get("code")
                field_name = field.get("name")
                if (fields and (field_code not in fields)) and (fields and (field_name not in fields)):
                    continue
                is_relationship_field = field.get("is_relationship_field")
                if is_relationship_field:
                    continue
                headers.append([field_name, field_code])
                field_code_list.append(field_code)
            headers.insert(0, ["序号", "code"])
            data_list.insert(0, headers)
            result = data_list
        return self.to_json(True, mess, result)
