"""
enum: 限定参数的值必须是数组中的某一个。例如，"enum": ["add", "subtract", "multiply", "divide"]。
minimum / maximum: 为 number 或 integer 类型设置最小值和最大值。
minLength / maxLength: 为 string 类型设置最小和最大长度。
pattern: 使用正则表达式来验证字符串的格式，常用于邮箱、电话号码等。
items: 当属性类型为 array 时，items 用于定义数组中每个元素的类型和结构。

string: 字符串
number: 数字（包括浮点数）
integer: 整数
boolean: 布尔值 (true 或 false)
array: 数组
object: 对象（嵌套结构）
null: 空值
"""


TOOL_CMDB_DICT = {
    "opsany_cmdb_api_resources": {
        "name": "opsany_cmdb_api_resources",
        "description": "资源平台，获取全部资源模型, 包括资源类型名称，资源类型标识，资源分组名称，资源分组标识，资源名称，资源标识，资源简称，资源实例总数，字段总数, 当不要求获取资源实例总数，字段总数时output为空！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "output": {
                    "type": "string",
                    "description": "资源实例总数和字段总数:使用参数：extend, 默认为空字符串。",
                    "default": ""
                },
                "limit": {
                    "type": "integer",
                    "description": "返回的资源模型数量限制",
                    "default": 100
                },
                "resource_type": {
                    "type": "string",
                    "description": "返回的资源模型类型，zc：资产模型 zz：组织模型 yw：业务模型 gl：其他 如 zc zc,zz zc,zz,yw,gl。",
                    "default": "zc,zz,yw,gl"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            }
        }
    },
    "opsany_cmdb_get_resource_fields": {
        "name": "opsany_cmdb_get_resource_fields",
        "description": """资源平台，获取指定资源的字段信息，获取资源仓库数据，创建修改资源仓库数据时需要拉取字段信息；
        字段描述：
        1. 字段类型(type_name)
            str : 字符串, 
            textarea: 多行文本,
            int: 整数,
            float: 浮点型,
            date: 日期,
            expiredDate: 到期时间,
            richText: 富文本,
            dropDown: 下拉菜单,
            composite: 复合数据, 数据类型为List，元素为Dict。
            复合数据: 复合数据, 数据类型为List，元素为Dict。
            file: 附件,
            password: 密码,
            link: 链接 可以访问的链接地址，以字符串保存,
            引用: 从属/连接 is_relationship_field=1 从属 is_relationship_field=2 连接
        2. 字段相关配置(attribute)
            关系类型: 1 普通关系 2 连接关系
            
        """,
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_code": {"type": "string", "description": "资源类型标识"},
                "field_type": {"type": "string", "description": "字段类型， 默认 01： 0 普通字段 1 连接关系字段 2 从属关系字段，案例： 0 01 012。"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
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
                "model_code": {"type": "string", "description": "资源类型（必填）"},
                "resource_id": {"type": "string", "description": "资源 ID（可选）"},
                "search": {"type": "string", "description": "搜索关键词（可选）"},
                "link_data": {"type": "string", "description": "是否获取连接关系数据"},
                "fields": {"type": "string", "description": "要显示的字段，逗号分隔（可选），默认显示前8个字段 只作为查询获取可以使用默认最少字段，显示全部使用all。"},
                "page": {"type": "integer", "description": "页码（默认为 1）", "default": 1},
                "limit": {"type": "integer", "description": "每页数量（默认为 20）", "default": 20},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 60},
            },
            "required": ["model_code"]
        }
    },
    "opsany_cmdb_get_resource_link_inst_count": {
        "name": "opsany_cmdb_get_resource_link_inst_count",
        "description": "资源平台，获取某一资源的所有关联关系数据字段和实例总数，包括从属关系(is_relationship_field=1)和关联关系(is_relationship_field=2)！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "integer", "description": "资源ID（必填）"},
                "field_code": {"type": "string", "description": "关联关系字段（必填），opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系字段！"},
                # "search": {"type": "string", "description": "搜索关键词（可选）"},
                "current": {"type": "integer", "description": "页码， 打开第几页", "default": 1},
                "pageSize": {"type": "integer", "description": "页数，每页多少条！", "default": 20},
                "search_type": {"type": "integer", "description": "搜索字段"},
                "search_data": {"type": "integer", "description": "搜索数据"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 60},
            },
            "required": ["code", "field_code"]
        }
    },
    "opsany_cmdb_get_resource_link_inst_list": {
        "name": "opsany_cmdb_get_resource_link_inst_list",
        "description": "资源平台，获取资源仓库某一数据的指定关联关系字段数据列表, 包括opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "integer", "description": "资源ID（必填）"},
                "field_code": {"type": "string", "description": "关联关系字段（必填），opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系字段！"},
                "current": {"type": "integer", "description": "页码， 打开第几页", "default": 1},
                "pageSize": {"type": "integer", "description": "页数，每页多少条！", "default": 20},
                "search_type": {"type": "integer", "description": "搜索字段"},
                "search_data": {"type": "integer", "description": "搜索数据"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 60},
            },
            "required": ["code", "field_code"]
        }
    },
    "opsany_cmdb_get_can_add_link_inst_list": {
        "name": "opsany_cmdb_get_can_add_link_inst_list",
        "description": "资源平台，添加资源的关联关系字段数据时，拉取指定关联关系字段的待添加数据列表(拉取关联关系对端模型数据，已过滤添加过的数据)，包括opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "integer", "description": "资源ID（必填）"},
                "field_code": {"type": "string",
                               "description": "关联关系字段（必填），opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系字段！"},
                "current": {"type": "integer", "description": "页码， 打开第几页", "default": 1},
                "pageSize": {"type": "integer", "description": "页数，每页多少条！", "default": 20},
                "search_type": {"type": "integer", "description": "搜索字段"},
                "search_data": {"type": "integer", "description": "搜索数据"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 60},
            },
            "required": ["code", "field_code"]
        }
    },
    "opsany_cmdb_resource_add_link_inst": {
        "name": "opsany_cmdb_resource_add_link_inst",
        "description": "资源平台，资源仓库给指定数据添加关联关系字段数据，opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系， 使用该工具操作。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "integer", "description": "资源ID（必填）"},
                "model_code": {"type": "string", "description": "资源类型（必填）"},
                "field_code": {"type": "string", "description": "关联关系字段（必填），opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系字段！"},
                "target_code_list": {"type": "array", "description": "目标实例ID, [10, 11, 12]！"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 60},
            },
            "required": ["code", "model_code", "field_code", "target_code_list"]
        }
    },
    "opsany_cmdb_resource_remove_link_inst": {
        "name": "opsany_cmdb_resource_remove_link_inst",
        "description": "资源平台，资源仓库给指定数据移除关联关系字段数据，opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系， 使用该工具操作。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "integer", "description": "资源ID（必填）"},
                "model_code": {"type": "string", "description": "资源类型（必填）"},
                "field_code": {"type": "string", "description": "关联关系字段（必填），opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系字段！"},
                "target_code": {"type": "array", "description": "目标实例ID, [10, 11, 12]！"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 60},
            },
            "required": ["code", "model_code", "field_code", "target_code"]
        }
    },

    "opsany_cmdb_create_resource": {
        "name": "opsany_cmdb_create_resource",
        "description": "资源平台，资源仓库新建数据，需要获取该模型字段后整理数据, data数据中仅支持普通字段(is_relationship_field="")和从属关系字段(is_relationship_field=1)，创建关联关系请使用opsany_cmdb_resource_add_link_inst工具。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_code": {"type": "string", "description": "资源类型（必填）"},
                "import_type": {"type": "string", "description": "导入来源"},
                "parent_inst": {"type": "string", "description": "从属关系资源ID，从属关系资源ID 从字段接口中is_relationship_field=1，attribute.引用模型为上级模型, 设置从属关系为空：set_null 设置从属关系：上级模型数据ID。"},
                "data": {
                    "type": "object",
                    "description": """数据对象，根据model_code拉取到的opsany_cmdb_get_resource_fields字段，创建数据;
                    案例：
                    model_code为SERVER, 获取到的字段为 SERVER_name，SERVER_VISIBLE_NAME，SERVER_HOSTNAME，SERVER_INTERNAL_IP等，
                    根据获取到的字段类型和attribute规则生成数据，key为字段标识(code)，value为数据
                    {
                        "SERVER_name": "linux-node1",
                        "SERVER_VISIBLE_NAME": "linux-node1",
                        "SERVER_HOSTNAME": "linux-node1",
                        "SERVER_INTERNAL_IP": "192.168.0.111",
                    }
                    """
                },
            },
            "required": ["model_code", "data"]
        }
    },
    "opsany_cmdb_update_resource": {
        "name": "opsany_cmdb_update_resource",
        "description": """资源平台，资源仓库新建数据，需要获取该模型字段后整理数据, 
                       data数据中仅支持普通字段(is_relationship_field="")和从属关系字段(is_relationship_field=1)，
                       修改关联关系(is_relationship_field=2)请使用opsany_cmdb_resource_add_link_inst或opsany_cmdb_resource_remove_link_inst或工具。
                       """,
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_code": {"type": "string", "description": "资源类型（必填）"},
                "code": {"type": "integer", "description": "资源ID"},
                "parent_inst": {"type": "string", "description": "从属关系资源ID，从属关系资源ID 从字段接口中is_relationship_field=1，attribute.引用模型为上级模型, 设置从属关系为空：set_null 设置从属关系：上级模型数据ID。"},
                "data": {
                    "type": "object",
                    "description": """数据对象，根据model_code拉取到的opsany_cmdb_get_resource_fields字段，创建数据，从属关系字段单独使用parent_inst传参，不在data内写该字段;
                    案例：
                    model_code为SERVER, 获取到的字段为 SERVER_name，SERVER_VISIBLE_NAME，SERVER_HOSTNAME，SERVER_INTERNAL_IP等，
                    根据获取到的字段类型和attribute规则生成数据，key为字段标识(code)，value为数据
                    {
                        "SERVER_name": "linux-node1",
                        "SERVER_VISIBLE_NAME": "linux-node1",
                        "SERVER_HOSTNAME": "linux-node1",
                        "SERVER_INTERNAL_IP": "192.168.0.111",
                    }
                    """
                },
            },
            "required": ["model_code", "code", "data"]
        }
    },
    "opsany_cmdb_delete_resource": {
        "name": "opsany_cmdb_delete_resource",
        "description": "资源平台，资源仓库删除数据，需要传入资源ID。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_code": {"type": "string", "description": "资源类型（必填）"},
                "code": {"type": "integer", "description": "资源ID"},
            },
            "required": ["model_code", "code"]
        }
    },
}

TOOL_RBAC_DICT = {
    "opsany_rbac_get_or_search_all_user": {
        "name": "opsany_rbac_get_or_search_all_user",
        "description": """统一权限平台，获取平台全部用户信息，仅支持管理员用户查看，普通用户可能会返回没有操作权限；支持用户名精准查找，中文名精准查找，
                       用户名模糊搜索，中文名称模糊搜索，中文名或用户名联合模糊搜索，支持扩展字段，包括部门用户认证来源等全部字段，使用 all。""",
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
                    "default": "all",
                    "description": "扩展字段，包括部门用户认证来源等全部字段，使用 all。"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 60},
            },
            "required": []
        }
    },
    "opsany_rbac_get_my_user_info": {
        "name": "opsany_rbac_get_my_user_info",
        "description": "统一权限平台，获取自己的用户信息，当前用户信息，我是谁，支持扩展字段，包括部门用户认证来源等全部字段，使用 all。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "extend": {"type": "string", "description": "扩展字段，包括部门用户认证来源等全部字段，使用 all。"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": []
        }
    },
    "opsany_rbac_create_user": {
        "name": "opsany_rbac_create_user",
        "description": """
        统一权限平台，批量创建用，仅支持管理员用户操作，普通用户可能会返回没有操作权限；仅支持创建普通用户，创建管理员请前往统一权限平台操作！
        仅支持修改普通用户信息，暂时仅支持修改启用禁用
        参考案例:
            {
                "user_info_list": [
                    {
                        "username": "staff01", 
                        "chname": "用户01",
                        "password": "123456.coM",
                        "phone": "183xxxx",
                        "email": "xxx@xxx",
                    }
                ]
            }
        """,
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_info_list": {
                    "type": "array",
                    "description": """
                    用户信息列表, 元素为Dict类型数据字段包括
                        username, 用户名，字符串类型，必填；
                        chname, 中文名，字符串类型，必填；
                        password, 密码，字符串类型，必填；
                        phone, 手机号，字符串类型，不必填；
                        email, 邮箱，字符串类型，不必填；
                        position, 职位，字符串类型，不必填；
                        description, 描述信息，字符串类型，不必填；
                    """,
                    "items": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string", "description": "用户名, 用户名只能输入数字、字母、下划线。"},
                            "chname": {"type": "string", "description": "中文名"},
                            "password": {"type": "string", "description": "密码, 密码只支持数字、字母或!@#$%^*()_-+=，长度在8-20个字符，且必须保证包含大小写字母和数字。"},
                            "phone": {"type": "string", "description": "手机号"},
                            "email": {"type": "string", "description": "邮箱"},
                            "position": {"type": "string", "description": "职位"},
                            "description": {"type": "string", "description": "描述信息"}
                        },
                        "required": ["username", "chname", "password"]
                    }
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间, 每增加一条建议延长5秒。", "default": 60},
            },
            "required": ["user_info_list"],
        }
    },
    "opsany_rbac_update_user": {
        "name": "opsany_rbac_update_user",
        "description": """统一权限平台，批量修改用户，仅支持管理员用户操作，普通用户可能会返回没有操作权限；
        仅支持修改普通用户信息，暂时仅支持修改启用禁用
        参考案例:
            {
                "user_info_list": [
                    {
                        "username": "staff01", "is_activate": true
                    }
                ]
            }
        """,
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_info_list": {
                    "type": "array",
                    "description": """用户信息列表, 元素为Dict类型数据字段包括
                        is_activate, 启用禁用，布尔值，必填；
                """,
                    "items": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string", "description": "用户名"},
                            "is_activate": {"type": "boolean", "description": "启用禁用"},
                        },
                        "required": ["username", "is_activate"]
                    }
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间, 每增加一条建议延长5秒。", "default": 30},
            },
            "required": ["user_info_list"],

        }
    },
    "opsany_rbac_delete_user": {
        "name": "opsany_rbac_delete_user",
        "description": """
            统一权限平台，批量删除用户，仅支持管理员用户操作，普通用户可能会返回没有操作权限；仅支持删除普通用户，和被禁用的用户，
            当要删除的用户是启用状态，需要用户确认是否禁用后删除，参考案例
            {
                "user_info_list": ["staff01"]
            }
            """,
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_info_list": {
                    "type": "array",
                    "description": """username 用户名列表""",
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间, 每增加一条建议延长5秒。", "default": 60},

            },
            "required": ["user_info_list"]
        }
    },
}

TOOL_MONITOR_DICT = {
    "opsany_monitor_alert_info": {
        "name": "opsany_monitor_alert_info",
        "description": "基础监控，获取基础监控平台的实例告警，需要管控平台监控并纳管后，实例包括管控平台主机，网络设备！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "string", "description": "页码， 打开第几页"},
                "pageSize": {"type": "string", "description": "页数，每页多少条"},
                "host_name": {"type": "string", "description": "主机唯一标识和实例名称模糊搜索"},
                "name": {"type": "string", "description": "告警名称模糊搜索"},
                "severity": {"type": "string", "description": "根据告警级别搜索，0: 未分类 1: 信息 2: 警告 3: 一般严重 4: 严重 5: 灾难。"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间, 告警过多建议增加超时时间。", "default": 30},
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
                    "description": "页码， 打开第几页！"
                },
                "pageSize": {
                    "type": "string",
                    "description": "页数，每页多少条！"
                },
                "data": {
                    "type": "string",
                    "description": "工单的分类，全部工单: all 待办工单: will 我的已办工单:already 我提交的工单: self ！"
                },
                "order_by": {
                    "type": "string",
                    "description": "排序字段"
                },
                "status": {
                    "type": "string",
                    "description": "工单状态，0: 正在进行 1: 已经结束 2 ！"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": []
        }
    },
    "opsany_workbench_work_order_folder": {
        "name": "opsany_workbench_work_order_folder",
        "description": "工作台，ITSM平台，获取全部服务分类，用来搜索指定分类下的工单！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": []
        }
    },
    "opsany_workbench_work_order_temp": {
        "name": "opsany_workbench_work_order_temp",
        "description": "工作台，ITSM平台，获取全部服务目录，包含全部服务，用来提单使用，会拉取授权的全部服务和服务相关字段！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "服务id，通过模板id获取到该服务项的详情和表单字段，获取单条需要使用form_fields字段，带上表单字段，以便提单！"
                },
                "form_fields": {
                    "type": "boolean",
                    "description": "是否包含表单字段"
                },
                "current": {
                    "type": "integer",
                    "description": "页码，打开第几页。"
                },
                "pageSize": {
                    "type": "integer",
                    "description": "页数，每页多少条。"
                },
                "folder_id": {
                    "type": "string",
                    "description": "服务分类ID，搜索指定分类的服务, all: 全部分类 或分类id。"
                },
                "data_type": {
                    "type": "string",
                    "description": "服务类型，all： 全部类型 tags：我的收藏 request：请求管理 change：变更管理 event：事件管理 issues：问题管理 recently：最近提单。"
                },
                "name_or_describe": {
                    "type": "string",
                    "description": "模糊搜索， 主要搜索 名称(name)和描述(describe)。"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": []
        }
    },
    "opsany_workbench_work_order_submit": {
        "name": "opsany_workbench_work_order_submit",
        "description": "工作台，ITSM平台，提单，根据opsany_workbench_work_order_temp拉取到的服务id和表单字段(field_list)提单！",
        "inputSchema": {
            "type": "object",
            "properties": {
                "submit_from": {
                    "type": "string",
                    "description": "提交来源"
                },
                "work_order_id": {
                    "type": "integer",
                    "description": "服务ID"
                },
                "follow": {
                    "type": "boolean",
                    "description": "是否跟踪，当使用true，工单有状态变更会通知提单人。"
                },
                "field_dict": {
                    "type": "object",
                    "description": """表单内容，字段内容来服务项(opsany_workbench_work_order_temp field_list)中的字段!
                    field_type 字段描述：
                        select 下拉菜单：需要传入 field_list.other_info.selectOptions 中的选项数据，如{"key": "1"}
                        cascader 级联惨淡：需要传入 field_list.other_info.cascaderOptions 中的选项数据，如 {"key": "first_layer"}, {"key": "second_layer"}, {"key": "third_layer"}]
                        radio 单选： field_list.other_info.selectOptions 中的选项数据，如 {"key": "one"}
                        checkbox 多选： field_list.other_info.selectOptions 中的选项数据，如 [{"key": "one"},  {"key": "two"}]
                    """
                }
            },
            "required": ["submit_from", "work_order_id", "field_dict"]
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
                    "description": "工具市场类型：job: 作业 script: 脚本 all: 全部，作业名称字段为 name，描述字段为 describe；脚本名称字段为 script_name，描述字段为 version_remarks。"
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
                    "description": "查询某一条作业详情，包括 作业名称 创建人 创建时间 步骤列表，步骤内脚本信息等。"
                },
                "script_id": {
                    "type": "integer",
                    "description": "查询某一条脚本详情，包括 脚本名称 创建人 创建时间 脚本内容等。"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": []
        }
    },
    "opsany_job_get_job_list": {
        "name": "opsany_job_get_job_list",
        "description": "作业平台 获取作业平台作业列表，只需要作业ID就可以执行的作业列表，作业名称字段为 name，描述字段为 describe！",
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
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": []
        }
    },
    "opsany_job_get_script_list": {
        "name": "opsany_job_get_script_list",
        "description": "作业平台 获取作业平台脚本列表，该脚本执行需要脚本ID执行主机等参数，脚本名称字段为 script_name，描述字段为 version_remarks！",
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
                    "description": "查询某一条脚本详情，包括 脚本名称 创建人 创建时间 脚本信息等。"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
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
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
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
                    "description": "脚本执行超时时间, 默认120s",
                    "default": 120
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
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
                "script": {"type": "string", "description": "脚本内容, 直接输入脚本内容。"},
                "parameter": {"type": "string", "description": "脚本参数", "default": ""},
                "run_describe": {"type": "string", "description": "执行原因"},
                "timeout": {"type": "integer", "description": "超时时间, 默认120s", "default": 120},
                "tool_timeout": {"type": "integer", "description": "脚本执行超时时间", "default": 30},
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
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": ["log_id"]
        }
    },
}

TOOL_CONTROL_DICT = {
    "opsany_control_get_managed_host_list": {
        "name": "opsany_control_get_managed_host_list",
        "description": """管控平台 获取管控平台纳管的主机列表，
                       该数据来自资源平台主机组内三个模型的数据(SERVER,CLOUD_SERVER,VIRTUAL_SERVER)！""",
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
                                   "查询全部忽略该字段，查询多个使用逗号隔开)。"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 30},
            },
            "required": []
        }
    },
    "opsany_control_get_controller_list": {
        "name": "opsany_control_get_controller_list",
        "description": "管控平台 获取管控平台控制器(Proxy)列表，纳管主机时使用，将主机纳管在该控制器下。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "根据控制名称搜索"},
                "id": {"type": "integer", "description": "根据控制ID获取控制器详情"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 10},
            },
            "required": []
        }
    },
    "opsany_control_get_host_group_list": {
        "name": "opsany_control_get_host_group_list",
        "description": "管控平台 获取管控平台主机分组列表，纳管主机时使用，将主机添加至该分组，分组支持嵌套。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 10},
            }
        }
    },
    "opsany_control_get_zabbix_list": {
        "name": "opsany_control_get_zabbix_list",
        "description": "管控平台 获取管控平台监控插件 基础监控插件ZabbixServer列表，纳管主机添加监基础控插件时使用，将主机使用该插件监控，可在基础监控平台查看。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 10},
            }
        }
    },
    "opsany_control_get_prometheus_list": {
        "name": "opsany_control_get_prometheus_list",
        "description": "管控平台 获取管控平台监控插件 应用监控插件PrometheusServer列表，纳管主机添加应用监控插件时使用，将主机使用该插件监控，可在应用监控平台查看。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 10},
            }
        }
    },
    "opsany_control_get_dashboard_list": {
        "name": "opsany_control_get_dashboard_list",
        "description": "管控平台 获取管控平台监控大屏列表，纳管主机添加监控插件时使用，根据标签判断 将主机使用该插件监控，可在应用监控平台查看。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dashboard_type": {"type": "string", "description": "大屏类型 Prometheus 或 Zabbix，选择监控插件时使用！"},
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 10},
            },
            "required": ["dashboard_type"]
        }
    },
    "opsany_control_get_zabbix_temp_list": {
        "name": "opsany_control_get_zabbix_temp_list",
        "description": "管控平台 获取管控平台Zabbix监控模板列表，纳管主机添加Zabbix监控插件时使用。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "zabbix_id": {
                    "type": "string", "description": "通过opsany_control_get_zabbix_list获取Zabbix实例ID，选择监控插件时使用！"
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间", "default": 20},
            },
            "required": ["zabbix_id"]
        }
    },
    "opsany_control_create_host": {
        "name": "opsany_control_create_host",
        "description": "管控平台 添加纳管主机，需要输入主机唯一标识， 主机IP,主机端口，系统用户，需要选择控制器，选择操作系统，管控方式，分组主机类型等，也可以添加Zabbix监控插件或Prometheus监控插件，需要传入指定参数。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "host_info_list": {
                    "type": "array",
                    "description": "批量纳管主机列表，主机信息在列表中。",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "主机唯一标识(执行脚本等操作需要传入该唯一标识)！"},
                            "show_name": {"type": "string", "description": "主机显示名！"},
                            "ip": {"type": "string", "description": "主机IP地址！"},
                            "system_type": {
                                "type": "string",
                                "enum": ["Linux", "Windows"],
                                "default": "password",
                                "description": "主机操作系统，仅支持Linux Windows！"
                            },
                            "controller_id": {
                                "type": "integer",
                                "description": "控制器，选择控制器ID根据工具 opsany_control_get_controller_list 获取到的ID(字段为id)！"
                            },
                            "control_type": {
                                "type": "integer", "enum": [1, 2, 3, 4],
                                "default": 1,
                                "description": "管控方式，主机纳管方式包含四种 1: SSH 2: Agent 3: SSH/Agent 4: Agent/SSH。"
                            },
                            "ssh_port": {
                                "type": "string",
                                "default": "22",
                                "description": "主机端口，当主机操作系统为Linux时需要输入SSH端口，端口范围为1-65535，默认 22！",
                            },
                            "login_port": {
                                "type": "string",
                                "description": "主机远程登录端口，当主机操作系统为Windows时需要输入RDP端口, 端口范围为1-65535，默认 3389！",
                            },
                            "username": {
                                "type": "string",
                                "default": "root",
                                "description": "主机系统用户, 登录或纳管主机使用的主机系统用户！"
                            },
                            "group_id": {
                                "type": "integer",
                                "description": "主机分组，分组id根据工具 opsany_control_get_host_group_list 获取戴的ID(字段为code)，当分组结构为 第一层/第二层/第三层 指向的是嵌套到第三层的分组！"
                            },
                            "ssh_type": {
                                "type": "string",
                                "enum": ["password"],
                                "default": "password",
                                "description": "密码类型，默认 password！",
                            },
                            "password": {
                                "type": "string",
                                "description": "密码，主机密码！"
                            },
                            "host_type": {
                                "type": "string",
                                "enum": ["SERVER", "VIRTUAL_SERVER"],
                                "description": "主机类型，创建主机成功后会将主机同步至CMDB(资源平台)主机模型内，支持两种主机类型： 物理机: SERVER 虚拟机: VIRTUAL_SERVER！",
                            },
                            "privilege": {
                                "type": "boolean",
                                "description": "特权提升(sudo)，是否开启特权提升 当system_type(操作系统)选择Linux 且 control_type(管控方式)包含SSH，true 或 false！"
                            },
                            "privilege_type": {
                                "type": "string",
                                "enum": ["sudo", "su"],
                                "description": "特权类型，两个选项 sudo 或 su, 当 privilege 为 true 时使用！"
                            },
                            "privilege_username": {
                                "type": "string",
                                "description": "特权用户名, 当 privilege 为 true 时使用！"
                            },
                            "privilege_password": {
                                "type": "string",
                                "description": "特权密码, 当 privilege 为 true 时使用！"
                            },
                            "monitor_type": {
                                "type": "string",
                                "enum": ["Zabbix", "Prometheus"],
                                "description": """
                                选择监控插件， 支持主机安装监控插件， 根据监控插件进行监控，支持 Zabbix 或 Prometheus
                                当选择Zabbix需要传入参数:
                                    1. controller_zabbix(ZabbixServer)
                                    2. template_list(Zabbix监控模板)！
                                    3. dashboard_dict(大屏需要拉取dashboard_type=Zabbix数据)
                                当选择Prometheus需要传入参数:
                                    1. controller_prom(PrometheusServer)
                                    3. dashboard_dict(大屏需要拉取dashboard_type=prometheus)
                                """,
                            },
                            "controller_zabbix": {
                                "type": "string",
                                "description": "选择监控插件实例，当monitor_type参数使用Zabbix时需要传入该参数！"
                            },
                            "controller_prom": {
                                "type": "string",
                                "description": "选择监控插件实例，当monitor_type参数使用Prometheus时需要传入该参数！"
                            },
                            "bind_port": {
                                "type": "integer",
                                "default": 9101,
                                "description": "选择监控插件实例，当monitor_type参数使用Prometheus时，且需要自定义端口时需要传入该参数！"
                            },
                            "is_bastion": {
                                "type": "boolean",
                                "default": "false",
                                "description": "是否将资源同步到堡垒机！"
                            },
                            "is_bastion_group": {
                                "type": "boolean",
                                "default": "false",
                                "description": "是否将资源同步到堡垒机，并将主机分组同步至堡垒机分组，false: 同步到堡垒机默认分组， 当is_bastion是true时使用！"
                            },
                            "reinstall_zabbix_agent": {
                                "type": "boolean",
                                "default": "true",
                                "description": "选择监控插件实例，当monitor_type参数使用Zabbix时，是否需要自动安装监控插件！"
                            },
                            "reinstall_prom_exporter": {
                                "type": "boolean",
                                "default": "true",
                                "description": "选择监控插件实例，当monitor_type参数使用Prometheus时，是否需要自动安装监控插件！"
                            },
                            "template_list": {
                                "type": "array",
                                "description": "Zabbix监控模板列表，包含模板名称和ID，当monitor_type参数使用Zabbix时需要传入该参数。",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "temp_name": {
                                            "type": "string",
                                            "description": "模板名称"
                                        },
                                        "temp_id": {
                                            "type": "string",
                                            "description": "模板ID"
                                        }
                                    },
                                    "required": ["temp_name", "temp_id"]
                                }
                            },
                            "dashboard_dict": {
                                "type": "object",
                                "description": "Grafana大屏信息，当使用monitor_type参数时需要传入大屏！",
                                "properties": {
                                    "uid": {
                                        "type": "string",
                                        "description": "大屏唯一标识符"
                                    },
                                    "title": {
                                        "type": "string",
                                        "description": "大屏标题"
                                    },
                                    "url": {
                                        "type": "string",
                                        "description": "大屏访问URL"
                                    },
                                    "tags": {
                                        "type": "array",
                                        "description": "大屏标签列表",
                                        "items": {
                                            "type": "string"
                                        }
                                    }
                                },
                                "required": ["uid", "title", "url", "tags"]
                            }
                        },
                        "required": ["name", "show_name", "ip", "system_type", "controller_id", "control_type",
                                     "username", "group_id", "host_type"]
                    }
                },
                "tool_timeout": {"type": "integer", "description": "工具请求超时时间，每增加一台建议延长2秒。", "default": 30},
            },
            "required": ["host_info_list"],
        }
    },
}

# TOOL_DICT = TOOL_CMDB_DICT | TOOL_MONITOR_DICT | TOOL_WORKBENCH_DICT | TOOL_JOB_DICT | TOOL_CONTROL_DICT
TOOL_DICT = TOOL_CMDB_DICT | TOOL_RBAC_DICT | TOOL_MONITOR_DICT | TOOL_WORKBENCH_DICT | TOOL_JOB_DICT | TOOL_CONTROL_DICT
TOOL_DICT.pop("opsany_workbench_work_order_folder", None)
TOOL_DICT.pop("opsany_job_run_script_by_script", None)
TOOL_LIST = list(TOOL_DICT.values())


if __name__ == '__main__':
    print(TOOL_LIST)
