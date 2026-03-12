url_startswith = "/api/c/compapi/"

url_cmdb_startswith = url_startswith + "cmdb/"
url_rbac_startswith = url_startswith + "rbac/"
url_control_startswith = url_startswith + "control/"
url_workbench_startswith = url_startswith + "workbench/"
url_job_startswith = url_startswith + "job/"


class APIEndpoints:
    check_api_token = "/login/accounts/is_login/"
    cmdb_get_resource_fields_api = url_cmdb_startswith + "get_model_field/"
    cmdb_get_resource_api = url_cmdb_startswith + "model_data_get/"
    cmdb_api_resources_api = url_cmdb_startswith + "get_cmdb_model_tree/"
    rbac_get_all_user = url_rbac_startswith + "get_all_user/"
    monitor_alert_info = url_control_startswith + "problem_info/"
    workbench_work_order_inst_list = url_workbench_startswith + "get_work_order_inst/"
    job_get_tool_market_list = url_job_startswith + "get_tool_market_list/"
    job_run_job_by_id = url_job_startswith + "run_job_by_id/"
    job_run_script_by_id = url_job_startswith + "run_script_by_id/"
    job_run_script_by_script = url_job_startswith + "run_script_by_script/"
    job_get_run_result_by_log_id = url_job_startswith + "get_run_result_by_log_id/"
    control_get_managed_host_list = url_control_startswith + "get_control_agent_info/"
