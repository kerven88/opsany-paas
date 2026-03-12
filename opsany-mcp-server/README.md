# OpsAny MCP Server

基于 OpsAny 平台的 MCP (Model Context Protocol) Server，提供通过 MCP 协议访问 OpsAny 平台资源、工单、脚本等能力。

## 功能特性

- **opsany_cmdb_api_resources**: 资源平台，获取全部资源模型, 包括资源类型名称，资源类型标识，资源分组名称，资源分组标识，资源名称，资源标识，资源简称，资源实例总数，字段总数, 当不要求获取资源实例总数，字段总数时output为空！
- **opsany_cmdb_get_resource_fields**: 获取指定资源的字段信息
- **opsany_cmdb_get_resource**: 获取资源数据，支持搜索、分页等功能
- **opsany_rbac_get_or_search_all_user**: 统一权限平台，获取平台全部用户信息， 支持用户名精准查找，中文名精准查找
- **opsany_rbac_get_my_user_info**: 统一权限平台，获取自己的用户信息，当前用户信息，我是谁，支持扩展字段，包括部门用户认证来源等全部字段，使用 all
- **opsany_monitor_alert_info**: 基础监控，获取管理平台监控纳管后，基础监控平台的实例告警，实例包括管控平台主机，网络设备！
- **opsany_workbench_work_order_inst**: 工作台，ITSM平台，获取全部工单，待办工单，我的已办工单，我提交的工单！
- **opsany_job_get_tool_market_list**: 作业平台 获取作业平台工具市场，包括作业列表和脚本列表！
- **opsany_job_get_job_list**: 作业平台 获取作业平台作业列表，只需要作业ID就可以执行的作业列表！
- **opsany_job_get_script_list**: 作业平台 获取作业平台脚本列表，该脚本执行需要脚本ID执行主机等参数！
- **opsany_job_run_job_by_id**: 作业平台 根据作业ID执行作业， 返回的为任务ID, 可以根据任务ID获取执行结果, 根据返回的字段flag判断是否执行完成。
- **opsany_job_run_script_by_id**: 作业平台 根据脚本ID执行脚本， 返回的为任务ID, 可以根据任务ID获取执行结果！
- **opsany_job_run_script_by_script**: 作业平台 输入脚本内容和主机信息执行脚本， 返回的为任务ID, 可以根据任务ID获取执行结果！
- **opsany_job_get_run_result_by_log_id**: 作业平台 获取执行的作业或脚本结果， 根据返回的任务ID获取！
- **opsany_control_get_managed_host_list**: 管控平台 获取管控平台纳管的主机列表！

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

## 1. CMDB（配置管理数据库）接口

### 1.1 获取全部资源模型信息  
**接口名称**：`opsany_cmdb_api_resources`  
**描述**：获取平台中全部资源模型信息，包括资源类型名称、资源类型标识、资源分组名称、资源分组标识、资源名称、资源标识、资源简称等。  
> ⚠️ 若未传 `output=extend`，则不会返回“资源实例总数”和“字段总数”，相关字段将为空。

**请求参数**：

| 参数名   | 类型    | 必填 | 默认值 | 描述 |
|----------|---------|------|--------|------|
| `output` | string  | 否   | `""`   | 若需获取资源实例总数与字段总数，请传 `"extend"`；否则留空 |
| `limit`  | integer | 否   | `100`  | 返回的资源模型数量上限 |

---

### 1.2 获取指定资源类型的字段信息  
**接口名称**：`opsany_cmdb_get_resource_fields`  
**描述**：根据资源类型标识（`model_code`），获取该资源类型的所有字段定义（如字段名、类型、是否必填等）。

**请求参数**：

| 参数名       | 类型   | 必填 | 描述                                 |
|--------------|--------|------|------------------------------------|
| `model_code` | string | 是   | 资源类型标识（例如：`SERVER`、`CLOUD_SERVER`） |

---

### 1.3 获取资源仓库数据（资源实例列表）  
**接口名称**：`opsany_cmdb_get_resource`  
**描述**：查询指定资源类型下的实例数据，支持按 ID 精确查询、关键词模糊搜索、字段筛选及分页。

**请求参数**：

| 参数名        | 类型    | 必填 | 默认值 | 描述 |
|---------------|---------|------|--------|------|
| `model_code`  | string  | 是   | —      | 资源类型标识 |
| `resource_id` | string  | 否   | —      | 资源实例 ID（精确匹配） |
| `search`      | string  | 否   | —      | 全局关键词模糊搜索（作用于所有可搜索字段） |
| `fields`      | string  | 否   | —      | 要返回的字段列表，逗号分隔（如：`name,ip,status`） |
| `page`        | integer | 否   | `1`    | 页码（从 1 开始） |
| `limit`       | integer | 否   | `20`   | 每页返回数量 |

---

## 2. RBAC（统一权限平台）接口

### 2.1 查询用户信息  
**接口名称**：`opsany_rbac_get_or_search_all_user`  
**描述**：获取平台全部用户信息，支持多种搜索方式，并可扩展返回部门、认证来源等完整字段。  
**请求参数**：  

| 参数名                        | 类型   | 必填 | 描述 |
|------------------------------|--------|------|------|
| `username`                   | string | 否   | 用户名（精准匹配） |
| `chname`                     | string | 否   | 中文名（精准匹配） |
| `search_username`            | string | 否   | 用户名模糊搜索 |
| `search_chname`              | string | 否   | 中文名模糊搜索 |
| `search_username_or_chname`  | string | 否   | 用户名或中文名联合模糊搜索 |
| `extend`                     | string | 否   | 若需返回完整用户信息（含部门、认证来源等），请传 `"all"` |

> 💡 建议一次只使用一种搜索参数，避免逻辑冲突。

---

### 2.2 获取当前用户信息  
**接口名称**：`opsany_rbac_get_my_user_info`  
**描述**：获取当前登录用户的基本信息及扩展信息。  
**请求参数**：

| 参数名   | 类型   | 必填 | 描述 |
|----------|--------|------|------|
| `extend` | string | 否   | 若需返回完整信息（含部门、认证来源等），请传 `"all"` |

---

## 3. Monitor（基础监控）接口

### 3.1 查询告警信息  
**接口名称**：`opsany_monitor_alert_info`  
**描述**：获取已纳管的主机或网络设备产生的告警信息，支持分页、关键词及告警级别过滤。  
**请求参数**：

| 参数名        | 类型   | 必填 | 描述 |
|---------------|--------|------|------|
| `page`        | string | 否   | 页码（字符串格式，如 `"1"`） |
| `pageSize`    | string | 否   | 每页条数（字符串格式，如 `"20"`） |
| `host_name`   | string | 否   | 主机唯一标识或实例名称（模糊匹配） |
| `name`        | string | 否   | 告警名称（模糊匹配） |
| `severity`    | string | 否   | 告警级别：<br>`"0"`: 未分类<br>`"1"`: 信息<br>`"2"`: 警告<br>`"3"`: 一般严重<br>`"4"`: 严重<br>`"5"`: 灾难 |

---

## 4. Workbench（工作台 / ITSM）接口

### 4.1 查询工单列表  
**接口名称**：`opsany_workbench_work_order_inst`  
**描述**：获取不同类别的工单列表，包括全部、待办、已办及本人提交的工单。  
**请求参数**：

| 参数名      | 类型   | 必填 | 描述 |
|-------------|--------|------|------|
| `current`   | string | 否   | 页码（如 `"1"`） |
| `pageSize`  | string | 否   | 每页数量（如 `"10"`） |
| `data`      | string | 否   | 工单分类：<br>`"all"`: 全部工单<br>`"will"`: 待办工单<br>`"already"`: 我的已办工单<br>`"self"`: 我提交的工单 |
| `order_by`  | string | 否   | 排序字段（如 `"create_time"`） |
| `status`    | string | 否   | 工单状态：<br>`"0"`: 进行中<br>`"1"`: 已结束<br>`"2"`: （保留状态） |

---

## 5. Job（作业平台）接口

### 5.1 查询作业平台工具市场列表  
**接口名称**：`opsany_job_get_tool_market_list`  
**描述**：获取作业平台工具市场中的作业列表和脚本列表，支持按类型、名称、创建人等条件进行筛选，也可查询单条作业或脚本的详细信息。  
**请求参数**：

| 参数名         | 类型    | 必填 | 描述 |
|----------------|---------|------|------|
| `data_type`    | string  | 否   | 工具市场类型：<br>`"job"`: 仅作业<br>`"script"`: 仅脚本<br>`"all"`: 全部（默认） |
| `script_name`  | string  | 否   | 模糊搜索脚本或作业名称 |
| `create_user`  | string  | 否   | 模糊搜索创建人 |
| `job_id`       | integer | 否   | 查询指定作业的详情，包括作业名称、创建人、创建时间、步骤列表及各步骤中的脚本信息 |
| `script_id`    | integer | 否   | 查询指定脚本的详情，包括脚本名称、创建人、创建时间、脚本内容等 |


### 5.2 查询作业列表  
**接口名称：** `opsany_job_get_job_list`  
**描述：** 获取作业平台中可通过作业ID直接执行的作业列表，支持模糊搜索及详情查询。  
**请求参数：**  

| 参数名        | 类型    | 必填 | 描述 |
|---------------|---------|------|------|
| `name`        | string  | 否   | 模糊搜索作业名称 |
| `create_user` | string  | 否   | 模糊搜索创建人（支持中文名） |
| `job_id`      | integer | 否   | 查询指定作业的完整详情，包括步骤与脚本信息 |


### 5.3 查询脚本列表
**接口名称：** `opsany_job_get_script_list`  
**描述：** 获取作业平台中的脚本列表，脚本执行需配合主机等参数；支持模糊搜索及详情查询。  
**请求参数：**  

| 参数名         | 类型    | 必填 | 描述 |
|----------------|---------|------|------|
| `script_name`  | string  | 否   | 模糊搜索脚本名称 |
| `create_user`  | string  | 否   | 模糊搜索创建人（支持中文名） |
| `script_id`    | integer | 否   | 查询指定脚本的完整详情，包括脚本内容、创建人、创建时间等 |


### 5.4 执行作业
**接口名称：** `opsany_job_run_job_by_id`  
**描述：** 根据作业ID执行作业，返回任务ID，可用于后续查询执行结果。  
**请求参数：**  

| 参数名   | 类型    | 必填 | 描述 |
|----------|---------|------|------|
| `job_id` | integer | 是   | 要执行的作业ID |


### 5.5 执行脚本（通过脚本ID）
**接口名称：** `opsany_job_run_script_by_id`  
**描述：** 根据脚本ID在指定主机上执行脚本，返回任务ID用于查询执行结果。  
**请求参数：**  

| 参数名          | 类型    | 必填 | 描述 |
|-----------------|---------|------|------|
| `script_id`     | integer | 是   | 要执行的脚本ID |
| `server`        | string  | 是   | 主机唯一标识，多个用逗号分隔（必须为已纳管主机） |
| `parameter`     | string  | 否   | 脚本执行参数（默认为空） |
| `run_describe`  | string  | 否   | 执行原因说明 |
| `time_out`      | integer | 否   | 超时时间（秒），默认120秒 |



### 5.6 执行脚本（通过脚本内容）  
**接口名称：** `opsany_job_run_script_by_script`  
**描述：** 直接传入脚本内容和目标主机信息执行脚本，返回任务ID用于查询结果。  
**请求参数：**  

| 参数名           | 类型    | 必填 | 描述 |
|------------------|---------|------|------|
| `task_name`      | string  | 否   | 任务名称（默认为“MCP生成”） |
| `server_type`    | string  | 否   | 主机标识类型：<br>`"host_name"`（默认）或 `"ip"` |
| `server`         | string  | 是   | 主机唯一标识或IP，多个用逗号分隔（必须为已纳管主机） |
| `script_type`    | string  | 否   | 脚本类型（文件后缀）：<br>`"sh"`（默认）、`"ps1"`、`"py"`、`"bat"` 等 |
| `script`         | string  | 是   | 要执行的脚本内容 |
| `parameter`      | string  | 否   | 脚本执行参数（默认为空） |
| `run_describe`   | string  | 否   | 执行原因说明 |
| `timeout`        | integer | 否   | 超时时间（秒），默认120秒 |


### 5.7 查询执行结果
**接口名称：** `opsany_job_get_run_result_by_log_id`  
**描述：** 根据任务ID（log_id）查询作业或脚本的执行结果。  
**请求参数：**  

| 参数名   | 类型    | 必填 | 描述 |
|----------|---------|------|------|
| `log_id` | integer | 是   | 执行作业或脚本后返回的任务ID |


## 6. Control（管控平台）接口


### 6.1 查询纳管主机列表
**接口名称**：`opsany_control_get_managed_host_list`  
**描述**：获取管控平台中已纳管的主机列表，数据来源于资源平台的 SERVER、CLOUD_SERVER、VIRTUAL_SERVER 三种主机模型。  
****请求参数：****  

| 参数名              | 类型    | 必填 | 描述 |
|---------------------|---------|------|------|
| `host_name_search`  | string  | 否   | 按主机唯一标识模糊搜索 |
| `show_name_search`  | string  | 否   | 按主机显示名称模糊搜索 |
| `ip_search`         | string  | 否   | 按主机IP模糊搜索 |
| `id`                | integer | 否   | 按主机ID精准查询 |
| `host_name`         | string  | 否   | 按主机唯一标识精准查询 |
| `show_name`         | string  | 否   | 按主机显示名称精准查询 |
| `ip`                | string  | 否   | 按主机IP精准查询 |
| `system_type`       | string  | 否   | 按系统类型筛选：<br>`"Linux"`、`"Windows"` |
| `host_type`         | string  | 否   | 按主机类型筛选（对应资源平台模型）：<br>`"SERVER"`、`"CLOUD_SERVER"`、`"VIRTUAL_SERVER"`，多个用逗号分隔 |


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
