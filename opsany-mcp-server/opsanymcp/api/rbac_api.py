import inspect

from opsanymcp.api.base_api import BaseObj


class RbacApi(BaseObj):

    user_headers = {
        "id": "用户ID",
        "username": "用户名",
        "chname": "中文名称",
        "phone": "联系电话",
        "email": "电子邮箱",
        "department_id": "部门ID",
        "position": "所任职位",
        "description": "用户描述",
        "joined_time": "创建时间",
        "bk_role": "用户类型(0: 普通用户 1: 管理员 2: 开发者)",
        "is_activate": "账号状态(True:启用 False:禁用)",
    }

    extend_headers = {
        "dep_full_name": "所属完整部门",
        "dep_name": "所属部门",
        "google_auth_status": "开启MFA认证(True:启用 False:禁用))",
        "google_auth_seven_days_free": "MFA开启7天免认证(True:启用 False:禁用)",
        "auth_folder_name": "用户组织目录",
        "auth_type": "认证类型",
        "auth_type_name": "认证类型名称",
        "domain": "登录域",
    }

    def opsany_rbac_get_or_search_all_user(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 30)
        limit = kwargs.get("limit")
        try:
            limit = int(limit) or 100
        except Exception:
            limit = 100
        if self.bk_role not in [1]:
            return self.to_json(False, "只有管理员权限可以获取到全部用户信息！")
        extend = kwargs.get("extend")
        params = {
            "bk_username": self.super_username,
            "username": kwargs.get("username"),
            "chname": kwargs.get("chname"),
            "search_username": kwargs.get("search_username"),
            "search_chname": kwargs.get("search_chname"),
            "search_username_or_chname": kwargs.get("search_username_or_chname"),
            "extend": extend,
        }
        if extend:
            self.user_headers.update(self.extend_headers)
        status, user_list, mess = self.call(fun_name, "GET", params=params, body={})
        if not status:
            return self.to_json(False, mess)

        if self.real_data_type == "table_header":
            result = {"columns": self.user_headers, "rows": user_list}
        else:
            result = []
            new_user_list = []
            for i in user_list:
                new_user_list.append([str(i.get(h) or "") for h in self.user_headers])
            for row in new_user_list:
                row_dict = dict(zip(self.user_headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_rbac_get_my_user_info(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 60)
        extend = kwargs.get("extend")
        params = {
            "bk_username": self.super_username,
            "username": self.bk_username,
            "extend": extend,
        }
        if extend:
            self.user_headers.update(self.extend_headers)
        status, user_list, mess = self.call(fun_name, "GET", params=params, body={}, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)

        if self.real_data_type == "table_header":
            result = {"columns": self.user_headers, "rows": user_list}
        else:
            result = []
            new_user_list = []
            for i in user_list:
                new_user_list.append([str(i.get(h) or "") for h in self.user_headers])
            for row in new_user_list:
                row_dict = dict(zip(self.user_headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_rbac_create_user(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 60)
        user_info_list = kwargs.get("user_info_list") or []
        body = {
            "user_info_list": user_info_list,
        }
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
                new_user_list.append([str(i.get(h) or "") for h in self.user_headers])
            for row in new_user_list:
                row_dict = dict(zip(self.user_headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_rbac_update_user(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 60)
        user_info_list = kwargs.get("user_info_list")
        body = {
            "user_info_list": user_info_list,
        }
        status, user_list, mess = self.call(fun_name, "POST", params={}, body=body, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)

        result_headers = {
            "success_dict": "修改成功信息",
            "error_dict": "修改失败信息",
        }

        if self.real_data_type == "table_header":
            result = {"columns": result_headers, "rows": user_list}
        else:
            result = []
            new_user_list = []
            for i in user_list:
                new_user_list.append([str(i.get(h) or "") for h in self.user_headers])
            for row in new_user_list:
                row_dict = dict(zip(self.user_headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)

    def opsany_rbac_delete_user(self, **kwargs):
        fun_name = inspect.currentframe().f_code.co_name
        tool_timeout = kwargs.pop("tool_timeout", 60)
        user_info_list = kwargs.get("user_info_list")
        body = {
            "user_info_list": user_info_list,
        }
        status, user_list, mess = self.call(fun_name, "POST", params={}, body=body, timeout=tool_timeout)
        if not status:
            return self.to_json(False, mess)

        result_headers = {
            "success_dict": "删除成功信息",
            "error_dict": "删除失败信息",
        }

        if self.real_data_type == "table_header":
            result = {"columns": result_headers, "rows": user_list}
        else:
            result = []
            new_user_list = []
            for i in user_list:
                new_user_list.append([str(i.get(h) or "") for h in self.user_headers])
            for row in new_user_list:
                row_dict = dict(zip(self.user_headers.values(), row))
                result.append(row_dict)
        if not result:
            return self.to_json(False, "获取当前资源数据为空", result)
        return self.to_json(True, mess, result)
