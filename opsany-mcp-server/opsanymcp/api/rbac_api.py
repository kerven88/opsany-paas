from opsanymcp.api.base import BaseObj
from opsanymcp.constants import APIEndpoints


class RbacApi(BaseObj):
    rbac_get_all_user = APIEndpoints.rbac_get_all_user

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

    def opsany_rbac_get_or_search_all_user(self, **kwarg):
        limit = kwarg.get("limit")
        try:
            limit = int(limit) or 100
        except Exception:
            limit = 100
        if self.this_request.bk_role not in [1]:
            return self.to_json(False, "只有管理员权限可以获取到全部用户信息！")
        extend = kwarg.get("extend")
        params = {
            "bk_username": self.this_request.super_username,
            "username": kwarg.get("username"),
            "chname": kwarg.get("chname"),
            "search_username": kwarg.get("search_username"),
            "search_chname": kwarg.get("search_chname"),
            "search_username_or_chname": kwarg.get("search_username_or_chname"),
            "extend": extend,
        }
        if extend:
            self.user_headers.update(self.extend_headers)
        status, user_list, mess = self.this_request._request(self.rbac_get_all_user, "GET", params=params, body={})
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

    def opsany_rbac_get_my_user_info(self, **kwarg):
        extend = kwarg.get("extend")
        params = {
            "bk_username": self.this_request.super_username,
            "username": self.this_request.bk_username,
            "extend": extend,
        }
        if extend:
            self.user_headers.update(self.extend_headers)
        status, user_list, mess = self.this_request._request(self.rbac_get_all_user, "GET", params=params, body={})
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
