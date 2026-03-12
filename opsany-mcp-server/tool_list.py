TOOL_CMDB_DICT = {
    "opsany_cmdb_api_resources": {
        "name": "opsany_cmdb_api_resources",
        "description": "资源平台，获取全部资源模型, 包括资源类型名称，资源类型标识，资源分组名称，资源分组标识，资源名称，资源标识，资源简称，资源实例总数，字段总数, 当不要求获取资源实例总数，字段总数时output为空！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "output": {
                    "type": "string",
                    "description": "资源实例总数和字段总数:使用参数：extend, 默认为空字符串",
                    "default": ""
                },
                "limit": {
                    "type": "integer",
                    "description": "返回的资源模型数量限制",
                    "default": 100
                },
            }
        }
    },
    "opsany_cmdb_get_resource_fields": {
        "name": "opsany_cmdb_get_resource_fields",
        "description": "资源平台，获取指定资源的字段信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_code": {
                    "type": "string",
                    "description": "资源类型标识"
                },
            },
            "required": ["model_code"]
        }
    },
    "opsany_cmdb_get_resource": {
        "name": "opsany_cmdb_get_resource",
        "description": "资源平台，获取资源仓库数据",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_code": {
                    "type": "string",
                    "description": "资源类型（必填）"
                },
                "resource_id": {
                    "type": "string",
                    "description": "资源 ID（可选）"
                },
                "search": {
                    "type": "string",
                    "description": "搜索关键词（可选）"
                },
                "fields": {
                    "type": "string",
                    "description": "要显示的字段，逗号分隔（可选）"
                },
                "page": {
                    "type": "integer",
                    "description": "页码（默认为 1）",
                    "default": 1
                },
                "limit": {
                    "type": "integer",
                    "description": "每页数量（默认为 20）",
                    "default": 20
                },
            },
            "required": ["model_code"]
        }
    }
}

TOOL_RBAC_DICT = {
    "opsany_rbac_get_or_search_all_user": {
        "name": "opsany_rbac_get_or_search_all_user",
        "description": "统一权限平台，获取平台全部用户信息， 支持用户名精准查找，中文名精准查找，"
                       "用户名模糊搜索，中文名称模糊搜索，中文名或用户名联合模糊搜索，支持扩展字段，包括部门用户认证来源等全部字段，使用 all",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "用户名精准查找"
                },
                "chname": {
                    "type": "string",
                    "description": "中文名精准查找"
                },
                "search_username": {
                    "type": "string",
                    "description": "用户名模糊搜索"
                },
                "search_chname": {
                    "type": "string",
                    "description": "中文名称模糊搜索"
                },
                "search_username_or_chname": {
                    "type": "string",
                    "description": "中文名或用户名联合模糊搜索"
                },
                "extend": {
                    "type": "string",
                    "description": "扩展字段，包括部门用户认证来源等全部字段，使用 all"
                },
            },
            "required": []
        }
    },
    "opsany_rbac_get_my_user_info": {
        "name": "opsany_rbac_get_my_user_info",
        "description": "统一权限平台，获取自己的用户信息，当前用户信息，我是谁，支持扩展字段，包括部门用户认证来源等全部字段，使用 all",
        "inputSchema": {
            "type": "object",
            "properties": {
                "extend": {
                    "type": "string",
                    "description": "扩展字段，包括部门用户认证来源等全部字段，使用 all"
                },
            },
            "required": []
        }
    }
}


TOOL_MONITOR_DICT = {
    "opsany_monitor_alert_info": {
        "name": "opsany_monitor_alert_info",
        "description": "基础监控，获取管理平台监控纳管后，基础监控平台的实例告警，实例包括管控平台主机，网络设备！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "string",
                    "description": "页码， 打开第几页"
                },
                "pageSize": {
                    "type": "string",
                    "description": "页数，每页多少条"
                },
                "host_name": {
                    "type": "string",
                    "description": "主机唯一标识和实例名称模糊搜索"
                },
                "name": {
                    "type": "string",
                    "description": "告警名称模糊搜索"
                },
                "severity": {
                    "type": "string",
                    "description": "根据告警级别搜索，0: 未分类 1: 信息 2: 警告 3: 一般严重 4: 严重 5: 灾难"
                },
            },
            "required": []
        }
    }
}

TOOL_WORKBENCH_DICT = {
    "opsany_workbench_work_order_inst": {
        "name": "opsany_workbench_work_order_inst",
        "description": "工作台，ITSM平台，获取全部工单，待办工单，我的已办工单，我提交的工单！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current": {
                    "type": "string",
                    "description": "页码， 打开第几页"
                },
                "pageSize": {
                    "type": "string",
                    "description": "页数，每页多少条"
                },
                "data": {
                    "type": "string",
                    "description": "工单的分类，全部工单: all 待办工单: will 我的已办工单:already 我提交的工单: self"
                },
                "order_by": {
                    "type": "string",
                    "description": "排序字段"
                },
                "status": {
                    "type": "string",
                    "description": "工单状态，0: 正在进行 1: 已经结束 2"
                },
            },
            "required": []
        }
    },
}

TOOL_JOB_DICT = {
    "opsany_job_get_tool_market_list": {
        "name": "opsany_job_get_tool_market_list",
        "description": "作业平台 获取作业平台工具市场，包括作业列表和脚本列表！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_type": {
                    "type": "string",
                    "description": "工具市场类型：job: 作业 script: 脚本 all: 全部"
                },
                "script_name": {
                    "type": "string",
                    "description": "模糊搜索脚本或作业名称"
                },
                "create_user": {
                    "type": "string",
                    "description": "模糊搜索创建人"
                },
                "job_id": {
                    "type": "integer",
                    "description": "查询某一条作业详情，包括 作业名称 创建人 创建时间 步骤列表，步骤内脚本信息等"
                },
                "script_id": {
                    "type": "integer",
                    "description": "查询某一条脚本详情，包括 脚本名称 创建人 创建时间 脚本内容等"
                },
            },
            "required": []
        }
    },
    "opsany_job_get_job_list": {
        "name": "opsany_job_get_job_list",
        "description": "作业平台 获取作业平台作业列表，只需要作业ID就可以执行的作业列表！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "模糊搜索作业名称。"
                },
                "create_user": {
                    "type": "string",
                    "description": "模糊搜索创建人，支持用户名中文名联合模糊搜索。"
                },
                "job_id": {
                    "type": "integer",
                    "description": "查询某一条作业详情，包括 作业名称 创建人 创建时间 步骤列表，步骤内脚本信息等。"
                },
            },
            "required": []
        }
    },
    "opsany_job_get_script_list": {
        "name": "opsany_job_get_script_list",
        "description": "作业平台 获取作业平台脚本列表，该脚本执行需要脚本ID执行主机等参数！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_name": {
                    "type": "string",
                    "description": "模糊搜索脚本或作业名称"
                },
                "create_user": {
                    "type": "string",
                    "description": "模糊搜索创建人，支持用户名中文名联合模糊搜索。"
                },
                "script_id": {
                    "type": "integer",
                    "description": "查询某一条脚本详情，包括 脚本名称 创建人 创建时间 脚本信息等"
                },
            },
            "required": []
        }
    },
    "opsany_job_run_job_by_id": {
        "name": "opsany_job_run_job_by_id",
        "description": "作业平台 根据作业ID执行作业， 返回的为任务ID, 可以根据任务ID获取执行结果, 根据返回的字段flag判断是否执行完成 True: 完成 False: 未完成。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "integer",
                    "description": "作业ID"
                }
            },
            "required": ["job_id"]
        }
    },
    "opsany_job_run_script_by_id": {
        "name": "opsany_job_run_script_by_id",
        "description": "作业平台 根据脚本ID执行脚本， 返回的为任务ID, 可以根据任务ID获取执行结果！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_id": {
                    "type": "integer",
                    "description": "作业ID"
                },
                "server": {
                    "type": "string",
                    "description": "主机唯一标识, 当有多条时用逗号隔开，该主机为管控平台纳管的主机。"
                },
                "parameter": {
                    "type": "string",
                    "description": "脚本参数",
                    "default": ""
                },
                "run_describe": {
                    "type": "string",
                    "description": "执行原因"
                },
                "time_out": {
                    "type": "integer",
                    "description": "超时时间, 默认120s",
                    "default": 120

                },
            },
            "required": ["script_id", "server"]
        }
    },
    "opsany_job_run_script_by_script": {
        "name": "opsany_job_run_script_by_script",
        "description": "作业平台 输入脚本内容和主机信息执行脚本， 返回的为任务ID, 可以根据任务ID获取执行结果！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_name": {
                    "type": "string",
                    "description": "任务名称，简短的任务名称，后续执行任务会根据该名称拼接执行记录， 作业平台，执行历史可查看 不输入会自动生成。",
                    "default": "MCP生成"
                },
                "server_type": {
                    "type": "string",
                    "description": "字段server数据的主机类型，默认为主机唯一标识(host_name), "
                                   "host_name: 主机唯一标识"
                                   "ip: 主机IP 当选择使用主机IP地址执行时。"
                },
                "server": {
                    "type": "string",
                    "description": "主机唯一标识或主机IP, 当有多条时用逗号隔开，该主机为管控平台纳管的主机, 没有纳管会被忽略，纳管异常会执行失败。"
                },
                "script_type": {
                    "type": "string",
                    "description": "脚本类型, 生成脚本文件的后缀 默认 sh，如：Shell: sh  PowerShell:ps1 Python:py Bat:bat"
                },
                "script": {
                    "type": "string",
                    "description": "脚本内容, 直接输入脚本内容。"
                },
                "parameter": {
                    "type": "string",
                    "description": "脚本参数",
                    "default": ""
                },
                "run_describe": {
                    "type": "string",
                    "description": "执行原因"
                },
                "timeout": {
                    "type": "integer",
                    "description": "超时时间, 默认120s",
                    "default": 120

                },
            },
            "required": ["server"]
        }
    },
    "opsany_job_get_run_result_by_log_id": {
        "name": "opsany_job_get_run_result_by_log_id",
        "description": "作业平台 获取执行的作业或脚本结果， 根据返回的任务ID获取！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "log_id": {
                    "type": "integer",
                    "description": "执行作业或脚本后返回的任务ID"
                },
            },
            "required": ["log_id"]
        }
    },

}

TOOL_CONTROL_DICT = {
    "opsany_control_get_managed_host_list": {
        "name": "opsany_control_get_managed_host_list",
        "description": "管控平台 获取管控平台纳管的主机列表，"
                       "该数据来自资源平台主机组内三个模型的数据(SERVER,CLOUD_SERVER,VIRTUAL_SERVER)！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "host_name_search": {
                    "type": "string",
                    "description": "根据主机唯一标识模糊搜索纳管主机"
                },
                "show_name_search": {
                    "type": "string",
                    "description": "根据主机名称模糊搜索纳管主机"
                },
                "ip_search": {
                    "type": "string",
                    "description": "根据主机名唯一标识模糊搜索纳管主机"
                },
                "id": {
                    "type": "integer",
                    "description": "根据主机ID查询纳管主机, 精准查询。"
                },
                "host_name": {
                    "type": "string",
                    "description": "根据主机ID查询纳管主机, 精准查询。"
                },
                "show_name": {
                    "type": "string",
                    "description": "根据主机ID查询纳管主机, 精准查询。"
                },
                "ip": {
                    "type": "string",
                    "description": "根据主机IP查询纳管主机, 精准查询。"
                },
                "system_type": {
                    "type": "string",
                    "description": "根据主机系统类型查询纳管主机，查询全部忽略该字段，Linux Windows"
                },
                "host_type": {
                    "type": "string",
                    "description": "查根据主机类型查询纳管主机(对应资源平台主机组内模型SERVER,CLOUD_SERVER,VIRTUAL_SERVER，"
                                   "查询全部忽略该字段，查询多个使用逗号隔开)"
                },
            },
            "required": []
        }
    },

}

TOOL_DICT = TOOL_CMDB_DICT | TOOL_RBAC_DICT | TOOL_MONITOR_DICT | TOOL_WORKBENCH_DICT | TOOL_JOB_DICT | TOOL_CONTROL_DICT
TOOL_LIST = list(TOOL_DICT.values())

