import json

from opsanymcp.libs import Request


class BaseObj:
    def __init__(self, name, config, username=None, api_token=None):
        self.name = name
        self.username = username
        self.api_token = api_token
        self.this_request = Request(config, username, api_token)
        self.resource_id_default_field = config.get('resourceIdDefaultField') or "code,VISIBLE_NAME,name"
        self.resource_id_field_search = config.get('resourceIdFieldSearch') or False
        self.real_data_type =config.get('realDataType') or "table_header"
        self.request_status, self.request_message = self.this_request.status, self.this_request.message
        self.base_params = {
            "username": self.username,
        }

    def to_json(self, success=False, msg="", result=None, ensure_ascii=False, indent=2):
        res_data = {"success": success, "error": msg, "data": result}
        return json.dumps(res_data, ensure_ascii=ensure_ascii, indent=indent)

    def run(self, arguments: dict):
        fun = getattr(self, self.name, None)
        if fun:
            try:
                return fun(**arguments)
            except Exception as e:
                return self.to_json(False, f"Tool {self.name} error, arguments {arguments}, msg: {e}")
        return self.to_json(False, f"Unknown OpsAny Tool: {self.name}")

