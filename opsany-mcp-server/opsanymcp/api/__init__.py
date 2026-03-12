from opsanymcp.api.base import BaseObj
from opsanymcp.api.cmdb_api import CMDBApi
from opsanymcp.api.control_api import ControlApi
from opsanymcp.api.job_api import JobApi
from opsanymcp.api.rbac_api import RbacApi
from opsanymcp.api.monitor_api import MonitorApi
from opsanymcp.api.workbench_api import WorkbenchApi


__all__ = ["BaseObj", "CMDBApi", "RbacApi", "MonitorApi", "WorkbenchApi", "JobApi", "ControlApi"]


API_CLASS_DICT = {
    "opsany_cmdb": CMDBApi,
    "opsany_rbac": RbacApi,
    "opsany_monitor": MonitorApi,
    "opsany_workbench": WorkbenchApi,
    "opsany_job": JobApi,
    "opsany_control": ControlApi,
}

_SORTED_PREFIXES = sorted(API_CLASS_DICT.keys(), key=len, reverse=True)

def get_opsany_api(name, config, username, api_token):

    api_class = BaseObj
    for prefix in _SORTED_PREFIXES:
        if name.startswith(prefix):
            api_class = API_CLASS_DICT[prefix]
            break
    api = api_class(name, config, username, api_token)
    # 检查请求状态
    if not api.request_status:
        return False, api, api.to_json(False, api.request_message)
    return True, api, "Success"
