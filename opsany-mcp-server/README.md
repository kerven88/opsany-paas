# OpsAny MCP Server

基于 OpsAny 平台的 MCP (Model Context Protocol) Server，提供通过 MCP 协议访问 OpsAny 平台资源、工单、脚本等能力。

## 功能特性

根据你提供的文档，我为你整理了所有工具的名称（Name）与描述（Description）。为了方便阅读，我已将其按功能平台分类列出：

- **opsany_cmdb_api_resources**: 资源平台，获取全部资源模型, 包括资源类型名称，资源类型标识，资源分组名称，资源分组标识，资源名称，资源标识，资源简称，资源实例总数，字段总数, 当不要求获取资源实例总数，字段总数时output为空！
- **opsany_cmdb_get_resource_fields**: 资源平台，获取指定资源的字段信息，获取资源仓库数据，创建修改资源仓库数据时需要拉取字段信息。
- **opsany_cmdb_get_resource**: 资源平台，获取资源仓库数据。
- **opsany_cmdb_get_resource_link_inst_count**: 资源平台，获取某一资源的所有关联关系数据字段和实例总数，包括从属关系(is_relationship_field=1)和关联关系(is_relationship_field=2)！
- **opsany_cmdb_get_resource_link_inst_list**: 资源平台，获取资源仓库某一数据的指定关联关系字段数据列表。
- **opsany_cmdb_get_can_add_link_inst_list**: 资源平台，添加资源的关联关系数据时，拉取指定关联关系字段的待添加数据列表(拉取关联关系对端模型数据，已过滤添加过的数据)。
- **opsany_cmdb_resource_add_link_inst**: 资源平台，资源仓库给指定数据添加关联关系数据。
- **opsany_cmdb_resource_remove_link_inst**: 资源平台，资源仓库给指定数据移除关联关系数据。
- **opsany_cmdb_create_resource**: 资源平台，资源仓库新建数据，需要获取该模型字段后整理数据, 创建普通字段需要将字段数据写入data。
- **opsany_cmdb_update_resource**: 资源平台，资源仓库修改数据，需要获取该模型字段后整理数据，修改普通字段需要将字段数据写入data！
- **opsany_cmdb_delete_resource**: 资源平台，资源仓库删除数据，需要传入资源ID。
- **opsany_rbac_get_or_search_all_user**: 统一权限平台，获取平台全部用户信息，仅支持管理员用户查看，普通用户可能会返回没有操作权限；支持用户名精准查找，中文名精准查找，用户名模糊搜索，中文名称模糊搜索，中文名或用户名联合模糊搜索，支持扩展字段，包括部门用户认证来源等全部字段，使用 all。
- **opsany_rbac_get_my_user_info**: 统一权限平台，获取自己的用户信息，当前用户信息，我是谁，支持扩展字段，包括部门用户认证来源等全部字段，使用 all。
- **opsany_rbac_create_user**: 统一权限平台，批量创建用，仅支持管理员用户操作，普通用户可能会返回没有操作权限；仅支持创建普通用户，创建管理员请前往统一权限平台操作！
- **opsany_rbac_update_user**: 统一权限平台，批量修改用户，仅支持管理员用户操作，普通用户可能会返回没有操作权限；仅支持修改普通用户信息，暂时仅支持修改启用禁用。
- **opsany_rbac_delete_user**: 统一权限平台，批量删除用户，仅支持管理员用户操作，普通用户可能会返回没有操作权限；仅支持删除普通用户，和被禁用的用户。
- **opsany_monitor_alert_info**: 基础监控，获取基础监控平台的实例告警，需要管控平台监控并纳管后，实例包括管控平台主机，网络设备！
- **opsany_workbench_work_order_inst**: 工作台，ITSM平台，获取全部工单，待办工单，我的已办工单，我提交的工单！
- **opsany_workbench_work_order_temp**: 工作台，ITSM平台，获取全部服务目录，包含全部服务，用来提单使用，会拉取授权的全部服务和服务相关字段！
- **opsany_workbench_work_order_submit**: 工作台，ITSM平台，提单，根据opsany_workbench_work_order_temp拉取到的服务id和表单字段(field_list)提单！
- **opsany_job_get_tool_market_list**: 作业平台 获取作业平台工具市场，包括作业列表和脚本列表！
- **opsany_job_get_job_list**: 作业平台 获取作业平台作业列表，只需要作业ID就可以执行的作业列表！
- **opsany_job_get_script_list**: 作业平台 获取作业平台脚本列表，该脚本执行需要脚本ID执行主机等参数！
- **opsany_job_run_job_by_id**: 作业平台 根据作业ID执行作业， 返回的为任务ID, 可以根据任务ID获取执行结果, 根据返回的字段flag判断是否执行完成 True: 完成 False: 未完成。
- **opsany_job_run_script_by_id**: 作业平台 根据脚本ID执行脚本， 返回的为任务ID, 可以根据任务ID获取执行结果！
- **opsany_job_get_run_result_by_log_id**: 作业平台 获取执行的作业或脚本结果， 根据返回的任务ID获取！
- **opsany_control_get_managed_host_list**: 管控平台 获取管控平台纳管的主机列表，该数据来自资源平台主机组内三个模型的数据(SERVER,CLOUD_SERVER,VIRTUAL_SERVER)！
- **opsany_control_get_controller_list**: 管控平台 获取管控平台控制器(Proxy)列表，纳管主机时使用，将主机纳管在该控制器下。
- **opsany_control_get_host_group_list**: 管控平台 获取管控平台主机分组列表，纳管主机时使用，将主机添加至该分组，分组支持嵌套。
- **opsany_control_get_zabbix_list**: 管控平台 获取管控平台监控插件 基础监控插件ZabbixServer列表，纳管主机添加监基础控插件时使用，将主机使用该插件监控，可在基础监控平台查看。
- **opsany_control_get_prometheus_list**: 管控平台 获取管控平台监控插件 应用监控插件PrometheusServer列表，纳管主机添加应用监控插件时使用，将主机使用该插件监控，可在应用监控平台查看。
- **opsany_control_get_dashboard_list**: 管控平台 获取管控平台监控大屏列表，纳管主机添加监控插件时使用，根据标签判断 将主机使用该插件监控，可在应用监控平台查看。
- **opsany_control_get_zabbix_temp_list**: 管控平台 获取管控平台Zabbix监控模板列表，纳管主机添加Zabbix监控插件时使用。
- **opsany_control_create_host**: 管控平台 添加纳管主机，需要输入主机唯一标识， 主机IP,主机端口，系统用户，需要选择控制器，选择操作系统，管控方式，分组主机类型等，也可以添加Zabbix监控插件或Prometheus监控插件，需要传入指定参数。


## 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd opsany-mcp-server
```

2. 创建虚拟环境并安装依赖：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 配置

在项目目录下创建 `config/config.yaml` 文件（参考config.yaml.example）：

```yaml
apiVersion: v1
apiService:
  url: https://DOMAIN_NAME
  bk_app_code: cmdb
  bk_app_secret: CMDB_SECRET_KEY
  super_username: admin  # 管理员用户名 用作部分API接口内部调用
  api_version: 4.0.2  # esb api服务版本
server:
  host: 0.0.0.0
  port: 8020
  auth_token: "MCP_AUTH_TOKEN"  # MCP Server的认证Token，安装时自动生成，调用时需要添加在Header中。
  version: 2.3.2
config:
  resourceIdDefaultField: "code,VISIBLE_NAME,name"
  resourceIdFieldSearch: false
  resourceDefaultLimit: 20
  apiResourcesDefaultLimit: 100


```

## 使用

### 启动服务器

```bash
python server.py
```


或覆盖主机和端口：

```bash
python server.py --host 0.0.0.0 --port 8020
```

### MCP 工具

# OpsAny 平台 API 文档

---

### 1. CMDB（配置管理数据库）接口

#### 1.1 获取全部资源模型信息
**接口名称**：`opsany_cmdb_api_resources`
**功能描述**：获取平台中全部资源模型信息，包括资源类型名称、资源类型标识、资源分组名称等。若未传 `output=extend`，则不会返回“资源实例总数”和“字段总数”。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **output** | String | 否 | `""` | 若需获取资源实例总数与字段总数，请传 `"extend"`；否则留空。 |
| **limit** | Integer | 否 | `100` | 返回的资源模型数量上限。 |
| **resource_type** | String | 否 | `zc,zz,yw,gl` | 资源模型类型：`zc`(资产) `zz`(组织) `yw`(业务) `gl`(其他)，支持多选。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |


#### 1.2 获取指定资源字段信息
**接口名称**：`opsany_cmdb_get_resource_fields`
**功能描述**：获取指定资源模型的字段定义详情（如字段类型、配置）。在创建/修改数据前，必须调用此接口拉取字段信息以符合校验规则。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **model_code** | String | **是** | - | 资源类型标识（Code）。 |
| **field_type** | String | 否 | `01` | 字段类型过滤：`0`(普通) `1`(连接) `2`(从属)，支持组合如 `012`。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 1.3 获取资源仓库数据
**接口名称**：`opsany_cmdb_get_resource`
**功能描述**：分页查询资源仓库中的具体实例数据。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **model_code** | String | **是** | - | 资源类型标识（必填）。 |
| **resource_id** | String | 否 | - | 资源 ID，精准查询单条数据。 |
| **search** | String | 否 | - | 搜索关键词，用于模糊匹配。 |
| **link_data** | String | 否 | - | 是否获取连接关系数据。 |
| **fields** | String | 否 | 前8个字段 | 指定返回的字段列表，多个用逗号分隔；显示全部传 `"all"`。 |
| **page** | Integer | 否 | `1` | 页码。 |
| **limit** | Integer | 否 | `20` | 每页数量。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

---

#### 1.4 获取资源关联关系实例总数
**接口名称**：`opsany_cmdb_get_resource_link_inst_count`
**功能描述**：获取某一资源的所有关联关系数据字段和实例总数，包括从属关系（`is_relationship_field=1`）和关联关系（`is_relationship_field=2`）。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **code** | Integer | **是** | - | 资源 ID。 |
| **field_code** | String | **是** | - | 关联关系字段（需为 `is_relationship_field=2` 的字段）。 |
| **current** | Integer | 否 | `1` | 页码，打开第几页。 |
| **pageSize** | Integer | 否 | `20` | 页数，每页多少条。 |
| **search_type** | Integer | 否 | - | 搜索字段。 |
| **search_data** | Integer | 否 | - | 搜索数据。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

---

#### 1.5 获取资源关联关系实例列表
**接口名称**：`opsany_cmdb_get_resource_link_inst_list`
**功能描述**：资源平台，获取资源仓库某一数据的指定关联关系字段数据列表, 包括opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **code** | Integer | **是** | - | 资源 ID。 |
| **field_code** | String | **是** | - | 关联关系字段（需为 `is_relationship_field=2` 的字段）。 |
| **current** | Integer | 否 | `1` | 页码，打开第几页。 |
| **pageSize** | Integer | 否 | `20` | 页数，每页多少条。 |
| **search_type** | Integer | 否 | - | 搜索字段。 |
| **search_data** | Integer | 否 | - | 搜索数据。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

---

#### 1.6 获取可添加的关联关系数据列表
**接口名称**：`opsany_cmdb_get_can_add_link_inst_list`
**功能描述**：资源平台，添加资源的关联关系字段数据时，拉取指定关联关系字段的待添加数据列表(拉取关联关系对端模型数据，已过滤添加过的数据)，包括opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **code** | Integer | **是** | - | 资源 ID。 |
| **field_code** | String | **是** | - | 关联关系字段（需为 `is_relationship_field=2` 的字段）。 |
| **current** | Integer | 否 | `1` | 页码，打开第几页。 |
| **pageSize** | Integer | 否 | `20` | 页数，每页多少条。 |
| **search_type** | Integer | 否 | - | 搜索字段。 |
| **search_data** | Integer | 否 | - | 搜索数据。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

---

#### 1.7 添加资源关联关系数据
**接口名称**：`opsany_cmdb_resource_add_link_inst`
**功能描述**：资源平台，资源仓库给指定数据添加关联关系字段数据，opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系， 使用该工具操作。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **code** | Integer | **是** | - | 资源 ID。 |
| **model_code** | String | **是** | - | 资源类型。 |
| **field_code** | String | **是** | - | 关联关系字段（需为 `is_relationship_field=2` 的字段）。 |
| **target_code_list** | Array | **是** | - | 目标实例 ID 列表，例如 `[10, 11, 12]`。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

---

#### 1.8 移除资源关联关系数据
**接口名称**：`opsany_cmdb_resource_remove_link_inst`
**功能描述**：资源平台，资源仓库给指定数据移除关联关系字段数据，opsany_cmdb_get_resource_fields接口中is_relationship_field=2的字段为关联关系， 使用该工具操作。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **code** | Integer | **是** | - | 资源 ID。 |
| **model_code** | String | **是** | - | 资源类型。 |
| **field_code** | String | **是** | - | 关联关系字段（需为 `is_relationship_field=2` 的字段）。 |
| **target_code** | Array | **是** | - | 目标实例 ID 列表，例如 `[10, 11, 12]`。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |


#### 1.9 创建资源实例
**接口名称**：`opsany_cmdb_create_resource`
**功能描述**：在资源仓库中新建一条数据。必须先获取模型字段后整理数据，普通字段数据写入 `data`。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **model_code** | String | **是** | - | 资源类型（必填）。 |
| **import_type** | String | 否 | - | 导入来源。 |
| **parent_inst** | String | 否 | - | 从属关系资源 ID；置空传 `set_null`。 |
| **data** | Object | **是** | - | 数据对象。Key 为字段标识 (code)，Value 为具体数据。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

#### 1.10 更新资源实例
**接口名称**：`opsany_cmdb_update_resource`
**功能描述**：更新资源仓库中的现有数据。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **model_code** | String | **是** | - | 资源类型（必填）。 |
| **code** | Integer | **是** | - | 资源 ID。 |
| **parent_inst** | String | 否 | - | 从属关系资源 ID（不在 data 内写）。 |
| **data** | Object | **是** | - | 数据对象。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

#### 1.11 删除资源实例
**接口名称**：`opsany_cmdb_delete_resource`
**功能描述**：从资源仓库中删除指定数据。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **model_code** | String | **是** | - | 资源类型（必填）。 |
| **code** | Integer | **是** | - | 资源 ID。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

---


### 2. RBAC（统一权限）接口

#### 2.1 获取全部用户信息
**接口名称**：`opsany_rbac_get_or_search_all_user`
**功能描述**：获取平台全部用户信息（仅管理员）。支持精准查找、模糊搜索及扩展字段（部门、认证来源等）。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **username** | String | 否 | - | 用户名精准查找。 |
| **chname** | String | 否 | - | 中文名精准查找。 |
| **search_username** | String | 否 | - | 用户名模糊搜索。 |
| **search_chname** | String | 否 | - | 中文名称模糊搜索。 |
| **search_username_or_chname** | String | 否 | - | 中文名或用户名联合模糊搜索。 |
| **extend** | String | 否 | `all` | 扩展字段，包括部门用户认证来源等全部字段。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

#### 2.2 获取当前用户信息
**接口名称**：`opsany_rbac_get_my_user_info`
**功能描述**：获取当前登录用户（自己）的详细信息。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **extend** | String | 否 | - | 扩展字段，包括部门用户认证来源等全部字段，使用 `"all"`。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 2.3 创建用户
**接口名称**：`opsany_rbac_create_user`
**功能描述**：批量创建用户（仅管理员）。仅支持创建普通用户。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **user_info_list** | Array | **是** | - | 用户信息列表（数组）。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

*   **`user_info_list` 元素结构 (Object)**:
    *   `username` (String, 必填): 用户名。
    *   `chname` (String, 必填): 中文名。
    *   `password` (String, 必填): 密码 (8-20位, 大小写字母+数字)。
    *   `phone` (String): 手机号。
    *   `email` (String): 邮箱。
    *   `position` (String): 职位。
    *   `description` (String): 描述。

#### 2.4 更新用户信息
**接口名称**：`opsany_rbac_update_user`
**功能描述**：批量修改用户信息（仅管理员）。目前仅支持修改启用/禁用状态。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **user_info_list** | Array | **是** | - | 用户信息列表。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

*   **`user_info_list` 元素结构 (Object)**:
    *   `username` (String): 用户名。
    *   `is_activate` (Boolean, 必填): 启用禁用状态。

#### 2.5 删除用户
**接口名称**：`opsany_rbac_delete_user`
**功能描述**：批量删除用户（仅管理员）。仅支持删除普通用户或被禁用的用户。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **user_info_list** | Array | **是** | - | 用户名列表 (Array)。 |
| **tool_timeout** | Integer | 否 | `60` | 工具请求超时时间（秒）。 |

---


### 3. Monitor（基础监控）接口

#### 3.1 获取实例告警信息
**接口名称**：`opsany_monitor_alert_info`
**功能描述**：获取基础监控平台的实例告警信息（需管控平台纳管）。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **page** | String | 否 | - | 页码。 |
| **pageSize** | String | 否 | - | 每页条数。 |
| **host_name** | String | 否 | - | 主机唯一标识/实例名称模糊搜索。 |
| **name** | String | 否 | - | 告警名称模糊搜索。 |
| **severity** | String | 否 | - | 告警级别：`0`(未分类) `1`(信息) `2`(警告) `3`(一般严重) `4`(严重) `5`(灾难)。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

---

### 4. Workbench（工作台/ITSM）接口

#### 4.1 获取工单列表
**接口名称**：`opsany_workbench_work_order_inst`
**功能描述**：获取全部工单、待办、已办或我提交的工单。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **current** | String | 否 | - | 页码。 |
| **pageSize** | String | 否 | - | 每页条数。 |
| **data** | String | 否 | - | 分类：`all`(全部) `will`(待办) `already`(已办) `self`(我提交的)。 |
| **order_by** | String | 否 | - | 排序字段。 |
| **status** | String | 否 | - | 工单状态：`0`(进行中) `1`(已结束)。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 4.2 获取服务分类
**接口名称**：`opsany_workbench_work_order_folder`
**功能描述**：获取全部服务分类，用于搜索指定分类下的工单。
**请求参数**：
*(无特定业务参数)*

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 4.3 获取服务目录/模板
**接口名称**：`opsany_workbench_work_order_temp`
**功能描述**：获取全部服务目录及表单字段，用于提单前获取字段详情。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **id** | Integer | 否 | - | 服务 ID，获取单条详情。 |
| **form_fields** | Boolean | 否 | - | 是否包含表单字段（提单必选）。 |
| **current** | Integer | 否 | - | 页码。 |
| **pageSize** | Integer | 否 | - | 每页条数。 |
| **folder_id** | String | 否 | - | 服务分类 ID (`all` 或具体 ID)。 |
| **data_type** | String | 否 | - | 服务类型：`all`, `tags`, `request`, `change` 等。 |
| **name_or_describe** | String | 否 | - | 名称或描述模糊搜索。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 4.4 提交工单
**接口名称**：`opsany_workbench_work_order_submit`
**功能描述**：根据服务 ID 和表单字段提交新工单。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **submit_from** | String | **是** | - | 提交来源。 |
| **work_order_id** | Integer | **是** | - | 服务 ID。 |
| **follow** | Boolean | 否 | - | 是否跟踪（状态变更通知）。 |
| **field_dict** | Object | **是** | - | 表单内容。Key 为字段 ID，Value 为数据。下拉/级联等需传入 `{"key": "value"}` 格式。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

---

### 5. Job（作业平台）接口

#### 5.1 获取工具市场列表
**接口名称**：`opsany_job_get_tool_market_list`
**功能描述**：获取作业平台工具市场（作业列表和脚本列表）。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **data_type** | String | 否 | - | 类型：`job`(作业) `script`(脚本) `all`(全部)。 |
| **script_name** | String | 否 | - | 脚本或作业名称模糊搜索。 |
| **create_user** | String | 否 | - | 创建人模糊搜索。 |
| **job_id** | Integer | 否 | - | 查询特定作业详情。 |
| **script_id** | Integer | 否 | - | 查询特定脚本详情。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 5.2 获取作业列表
**接口名称**：`opsany_job_get_job_list`
**功能描述**：获取仅需作业 ID 即可执行的作业列表。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **name** | String | 否 | - | 作业名称模糊搜索。 |
| **create_user** | String | 否 | - | 创建人模糊搜索。 |
| **job_id** | Integer | 否 | - | 查询特定作业详情。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 5.3 获取脚本列表
**接口名称**：`opsany_job_get_script_list`
**功能描述**：获取脚本列表（执行需脚本 ID 及主机等参数）。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **script_name** | String | 否 | - | 脚本名称模糊搜索。 |
| **create_user** | String | 否 | - | 创建人模糊搜索。 |
| **script_id** | Integer | 否 | - | 查询特定脚本详情。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 5.4 根据 ID 执行作业
**接口名称**：`opsany_job_run_job_by_id`
**功能描述**：根据作业 ID 执行作业，返回任务 ID。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **job_id** | Integer | **是** | - | 作业 ID。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

#### 5.5 根据 ID 执行脚本
**接口名称**：`opsany_job_run_script_by_id`
**功能描述**：根据脚本 ID 在指定主机上执行脚本。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **script_id** | Integer | **是** | - | 脚本 ID。 |
| **server** | String | **是** | - | 主机唯一标识（多台用逗号隔开）。 |
| **parameter** | String | 否 | `""` | 脚本参数。 |
| **run_describe** | String | 否 | - | 执行原因。 |
| **time_out** | Integer | 否 | `120` | 脚本执行超时时间（秒）。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |


#### 5.6 获取执行结果
**接口名称**：`opsany_job_get_run_result_by_log_id`
**功能描述**：根据任务 ID 获取作业或脚本的执行结果。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **log_id** | Integer | **是** | - | 执行后返回的任务 ID。 |
| **tool_timeout** | Integer | 否 | `30` | 工具请求超时时间（秒）。 |

---

### 6. Control（管控平台）接口

---

#### 6.1 获取纳管主机列表
**接口名称**：`opsany_control_get_managed_host_list`
**功能描述**：获取管控平台纳管的主机列表，数据来自资源平台主机组内三个模型的数据(SERVER, CLOUD_SERVER, VIRTUAL_SERVER)。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **host_name_search** | String | 否 | - | 根据主机唯一标识模糊搜索纳管主机。 |
| **show_name_search** | String | 否 | - | 根据主机名称模糊搜索纳管主机。 |
| **ip_search** | String | 否 | - | 根据主机名唯一标识模糊搜索纳管主机。 |
| **id** | Integer | 否 | - | 根据主机ID查询纳管主机，精准查询。 |
| **host_name** | String | 否 | - | 根据主机ID查询纳管主机，精准查询。 |
| **show_name** | String | 否 | - | 根据主机ID查询纳管主机，精准查询。 |
| **ip** | String | 否 | - | 根据主机IP查询纳管主机，精准查询。 |
| **system_type** | String | 否 | - | 根据主机系统类型查询，Linux 或 Windows。 |
| **host_type** | String | 否 | - | 根据主机类型查询，支持 SERVER, CLOUD_SERVER, VIRTUAL_SERVER，多个使用逗号隔开。 |
| **tool_timeout** | Integer | 否 | 30 | 工具请求超时时间。 |

---

#### 6.2 获取控制器列表
**接口名称**：`opsany_control_get_controller_list`
**功能描述**：获取管控平台控制器(Proxy)列表，用于纳管主机时指定控制器。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **name** | String | 否 | - | 根据控制名称搜索。 |
| **id** | Integer | 否 | - | 根据控制ID获取控制器详情。 |
| **tool_timeout** | Integer | 否 | 10 | 工具请求超时时间。 |

---

#### 6.3 获取主机分组列表
**接口名称**：`opsany_control_get_host_group_list`
**功能描述**：获取管控平台主机分组列表，用于纳管主机时添加至该分组（支持嵌套）。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **tool_timeout** | Integer | 否 | 10 | 工具请求超时时间。 |

---

#### 6.4 获取 Zabbix 监控列表
**接口名称**：`opsany_control_get_zabbix_list`
**功能描述**：获取管控平台基础监控插件 ZabbixServer 列表，用于纳管主机时添加基础监控插件。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **tool_timeout** | Integer | 否 | 10 | 工具请求超时时间。 |

---

#### 6.5 获取 Prometheus 监控列表
**接口名称**：`opsany_control_get_prometheus_list`
**功能描述**：获取管控平台应用监控插件 PrometheusServer 列表，用于纳管主机时添加应用监控插件。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **tool_timeout** | Integer | 否 | 10 | 工具请求超时时间。 |

---

#### 6.6 获取监控大屏列表
**接口名称**：`opsany_control_get_dashboard_list`
**功能描述**：获取管控平台监控大屏列表，根据标签判断将主机使用该插件监控。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **dashboard_type** | String | **是** | - | 大屏类型，必填：Prometheus 或 Zabbix。 |
| **tool_timeout** | Integer | 否 | 10 | 工具请求超时时间。 |

---

#### 6.7 获取 Zabbix 模板列表
**接口名称**：`opsany_control_get_zabbix_temp_list`
**功能描述**：获取管控平台 Zabbix 监控模板列表，纳管主机添加 Zabbix 监控插件时使用。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **zabbix_id** | String | **是** | - | 通过 `opsany_control_get_zabbix_list` 获取 Zabbix 实例 ID。 |
| **tool_timeout** | Integer | 否 | 20 | 工具请求超时时间。 |

---

#### 6.8 创建纳管主机
**接口名称**：`opsany_control_create_host`
**功能描述**：添加纳管主机，支持批量纳管，并可配置 Zabbix 或 Prometheus 监控插件。
**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **host_info_list** | Array | **是** | - | 批量纳管主机列表，主机信息在列表中。 |
| **tool_timeout** | Integer | 否 | 30 | 工具请求超时时间，每增加一台建议延长 2 秒。 |

**`host_info_list` 数组内对象参数详情**：

*   **基础信息**：
    *   `name` (String, **必填**): 主机唯一标识。
    *   `show_name` (String, **必填**): 主机显示名。
    *   `ip` (String, **必填**): 主机 IP 地址。
    *   `system_type` (String, **必填**): 操作系统，仅支持 `Linux` 或 `Windows`。
    *   `controller_id` (Integer, **必填**): 控制器 ID（通过 `opsany_control_get_controller_list` 获取）。
    *   `control_type` (Integer, **必填**): 管控方式，1: SSH, 2: Agent, 3: SSH/Agent, 4: Agent/SSH。
    *   `group_id` (Integer, **必填**): 主机分组 ID（通过 `opsany_control_get_host_group_list` 获取）。
    *   `host_type` (String, **必填**): 主机类型，`SERVER` (物理机) 或 `VIRTUAL_SERVER` (虚拟机)。
    *   `username` (String, 可选): 主机系统用户，默认 `root`。
    *   `password` (String, 可选): 主机密码。

*   **端口配置**：
    *   `ssh_port` (String): SSH 端口，Linux 默认 `22`。
    *   `login_port` (String): RDP 端口，Windows 默认 `3389`。

*   **特权提升 (Sudo/Su)**：
    *   `privilege` (Boolean): 是否开启特权提升。
    *   `privilege_type` (String): 特权类型，`sudo` 或 `su`。
    *   `privilege_username` (String): 特权用户名。
    *   `privilege_password` (String): 特权密码。

*   **监控插件配置**：
    *   `monitor_type` (String): 监控类型，`Zabbix` 或 `Prometheus`。
    *   `controller_zabbix` (String): monitor_type 为 Zabbix 时必填。
    *   `controller_prom` (String): monitor_type 为 Prometheus 时必填。
    *   `bind_port` (Integer): Prometheus 自定义端口，默认 `9101`。
    *   `template_list` (Array): Zabbix 模板列表（包含 temp_name 和 temp_id）。
    *   `dashboard_dict` (Object): 大屏信息（uid, title, url, tags）。

*   **其他配置**：
    *   `is_bastion` (Boolean): 是否同步到堡垒机。
    *   `is_bastion_group` (Boolean): 是否同步分组到堡垒机。
    *   `reinstall_zabbix_agent` (Boolean): 是否自动安装 Zabbix 插件。
    *   `reinstall_prom_exporter` (Boolean): 是否自动安装 Prometheus 插件。
---


## 在 TRAE 中配置使用

### 1. 启动 MCP Server

首先启动 OpsAny MCP Server：

```bash
cd opsany-mcp-server
python server.py --config config/config.yaml
```

服务器启动后会显示：

```
Starting OpsAny MCP Server on 192.168.0.111:8020
```

### 2. 在 TRAE 中配置 MCP Server

1. 打开 TRAE IDE
2. 进入 **设置** → **MCP Servers**
3. 点击 **添加 MCP Server**
4. 填写配置信息：

```json
{
    "name": "opsany-mcp-server",
    "url": "http://192.168.0.111:8020/sse",
    "headers": {
        "username": "username",
        "user-api-token": "7IecXVZHrk7t0jQ6lAUwBSULnScfVrRJpM7ZtPi5Wk73Fw",
        "mcp-auth-token": "7e84a67d-e97a-4986-a5c9-393837089c12"
  }
}
```

- username： OpsAny当前用户名
- user-api-token： OpsAny工作台-个人设置 创建的API Token
- mcp-auth-token： config.yaml配置中auth_token值


5. 点击 **保存** 并 **连接**

### 3. 验证连接

在 TRAE 的聊天界面中输入测试命令：

```
请使用 api_resources 工具获取所有可用的资源模型
```

如果连接成功，将返回所有资源模型的列表。


### 6. 常见问题排查

#### 连接失败

- 确认 MCP Server 正在运行
- 检查配置的 URL 是否正确（应为 `http://192.168.0.11:8020/sse`）
- 查看服务器日志确认是否有错误

#### 认证失败

- 检查 `config.yaml` 中的 API 凭证是否正确
- 确认 OpsAny 平台地址可访问
- 验证用户权限是否足够

#### 数据返回为空

- 确认 OpsAny 平台中有相关资源数据
- 检查搜索关键词是否正确
- 尝试不使用搜索参数获取全部数据

## 开发

项目结构：

```
opsany-mcp-server/
├── opsanymcp/               # 核心模块
│   ├── api/                 # API 接口
│   │   ├── __init__.py
│   │   ├── base.py          # API核心组件
│   │   ├── cmdb_api.py      # 资源平台API
│   │   ├── monitor_api.py   # 基础监控API
│   │   ├── rbac_api.py      # 统一权限API
│   │   └── workbench_api.py # 工作台API
│   ├── __init__.py
│   ├── constants.py         # 常量定义
│   └── libs.py              # 工具函数
├── config/                  # 配置文件
│   └── config.yaml          # 配置文件
├── server.py                # MCP Server 主入口
├── tool_list.py             # MCP 工具列表
└── requirements.txt         # Python 依赖
```

## 许可证

MIT License
