---
name: opsany
description: 通过 opsany-mcp-server 连接 OpsAny 运维平台，实现 CMDB 资源查询和资源操作、工单管理、用户管理、作业执行及主机纳管等全栈运维操作。
---

# OpsAny

## 1. 概述

OpsAny SKILL 通过 opsany-mcp-server这个MCP Server 协议连接 OpsAny 平台，将 AI 对话能力与企业级运维平台打通。支持对配置管理数据库（CMDB）、作业平台、统一权限、基础监控等九大 SaaS 服务的数据查询与操作和日常运维工作。OpsAny平台是由多个服务组成的运维平台。

### 核心能力
- **工作台**： 运维工作台，支持自定义工单流程、自定义工单（表单、字段设计），是企业服务流程管理的入口。
- **堡垒机**： 运维堡垒机，支持4A审计，是企业手工运维的入口也是企业安全等保建设必备产品。
- **资产管理 (CMDB)**：查询资产模型、字段定义及实例数据，管理资产间的关联与从属关系。
- **管控平台**：自动添加主机至管控平台，完成对运维对象的纳管操作，通过SSH或者Agent两种方式进行控制，配置监控插件（Zabbix/Prometheus）及堡垒机同步。 。
- **作业执行**：通过 ID 或脚本内容执行作业，支持 Shell/Python 等脚本类型，并获取执行结果。
- **基础监控**： 完成对运维对象的多层级的监控工作，目前采集器采用Zabbix。
- **统一权限**：查询与管理平台用户信息（需管理员权限）。
- **云管平台**： 多云统一管理，支持阿里云、腾讯云、华为云、AWS、金山云，资产自动导入至CMDB（资源平台）。

## 2. 配置管理

### MCP 服务器配置

请在 MCP 客户端配置文件中添加以下配置，替换对应环境变量。

```json
{
  "mcpServers": {
    "opsany-mcp-server": {
      "url": "http://${DOMAIN_NAME}:8020/sse",
      "headers": {
        "username": "admin",
        "user-api-token": "${USER_ACCESS_TOKEN}",
        "mcp-auth-token": "${MCP_AUTH_TOKEN}"
      }
    }
  }
}
```

**参数说明：**
- `DOMAIN_NAME`：OpsAny 平台的访问域名或 IP 地址。
- `USER_ACCESS_TOKEN`：登录平台后，在“工作台 -> 个人设置 -> API Token”中创建。
- `MCP_AUTH_TOKEN`：MCP Server 的配置文件中的认证 Token（默认路径：`/data/opsany/conf/opsany-paas/mcp-server/config.yaml`）。

## 3. 工具明细 (Tools)

### 3.1 资源平台 (CMDB)
用于管理 IT 资源模型与数据。
- `opsany_cmdb_api_resources`: 获取全部资源模型（类型、分组、标识等）。
- `opsany_cmdb_get_resource_fields`: 获取指定资源模型的字段详情（类型、配置）。
- `opsany_cmdb_get_resource`: 查询资源实例数据，支持分页、关键词搜索。
- `opsany_cmdb_get_resource_link_inst_count`: 获取资源的关联/从属关系实例总数。
- `opsany_cmdb_get_resource_link_inst_list`: 获取资源指定关联关系的数据列表。
- `opsany_cmdb_get_can_add_link_inst_list`: 查询可添加的关联关系数据列表（去重过滤）。
- `opsany_cmdb_resource_add_link_inst`: 为资源添加关联关系数据。
- `opsany_cmdb_resource_remove_link_inst`: 移除资源的关联关系数据。
- `opsany_cmdb_create_resource`: 创建新的资源数据。
- `opsany_cmdb_update_resource`: 更新资源数据。
- `opsany_cmdb_delete_resource`: 删除资源数据。

### 3.2 统一权限 (RBAC)
用于管理平台用户。
- `opsany_rbac_get_or_search_all_user`: 获取或搜索全部用户信息（管理员权限）。
- `opsany_rbac_get_my_user_info`: 获取当前登录用户信息。
- `opsany_rbac_create_user`: 批量创建用户（管理员权限）。
- `opsany_rbac_update_user`: 批量更新用户状态（如启用/禁用）。
- `opsany_rbac_delete_user`: 批量删除用户（管理员权限）。

### 3.3 基础监控 (Monitor)
- `opsany_monitor_alert_info`: 获取监控告警信息，支持按主机、级别（严重/警告等）筛选。

### 3.4 工作台 (Workbench/ITSM)
用于工单服务管理。
- `opsany_workbench_work_order_inst`: 查询工单实例（待办、已办、全部）。
- `opsany_workbench_work_order_temp`: 获取服务目录及表单字段（用于提单）。
- `opsany_workbench_work_order_submit`: 提交新工单。

### 3.5 作业平台 (Job)
用于脚本与作业执行。
- `opsany_job_get_tool_market_list`: 获取工具市场（作业/脚本列表）。
- `opsany_job_get_job_list`: 获取可执行的作业列表。
- `opsany_job_get_script_list`: 获取脚本列表。
- `opsany_job_run_job_by_id`: 根据 ID 执行作业。
- `opsany_job_run_script_by_id`: 根据 ID 执行脚本。
- `opsany_job_get_run_result_by_log_id`: 根据任务 ID 获取执行结果。

### 3.6 管控平台 (Control)
用于主机纳管与环境配置。
- `opsany_control_get_managed_host_list`: 获取已纳管主机列表。
- `opsany_control_get_controller_list`: 获取控制器 (Proxy) 列表。
- `opsany_control_get_host_group_list`: 获取主机分组列表。
- `opsany_control_get_zabbix_list`: 获取 Zabbix 实例列表。
- `opsany_control_get_prometheus_list`: 获取 Prometheus 实例列表。
- `opsany_control_get_dashboard_list`: 获取监控大屏列表。
- `opsany_control_get_zabbix_temp_list`: 获取 Zabbix 模板列表。
- `opsany_control_create_host`: **核心操作**，添加主机纳管，支持配置 SSH/Agent、监控插件及堡垒机同步。

## 4. 场景案例

### 4.1 资源深度查询 (CMDB)
**场景：** 查询特定业务模型下的主机资源，并查看其关联的网络设备。

**步骤：**
1.  **发现模型**：调用 `opsany_cmdb_api_resources`，筛选 `resource_type` 为 `yw` (业务模型)，找到目标业务的 `model_code`。
2.  **查询资源**：使用 `opsany_cmdb_get_resource`，传入 `model_code` 和搜索关键词（如主机 IP），获取主机 ID (`resource_id`)。
3.  **查看关联**：
    *   调用 `opsany_cmdb_get_resource_fields` 获取该模型的字段，找到 `is_relationship_field=2` (关联关系) 的字段 `field_code`。
    *   调用 `opsany_cmdb_get_resource_link_inst_list`，传入主机 ID 和 `field_code`，获取关联的网络设备列表。

### 4.2 批量纳管主机 (管控平台)
**场景：** 将一批新服务器添加到运维平台，并自动安装监控插件。

**步骤：**
1.  **环境准备**：
    *   调用 `opsany_control_get_controller_list` 获取 `controller_id`。
    *   调用 `opsany_control_get_host_group_list` 获取目标分组 `group_id`。
    *   调用 `opsany_control_get_zabbix_list` 获取 `controller_zabbix` ID。
2.  **执行纳管**：调用 `opsany_control_create_host`。
    *   构造 `host_info_list` 数组，包含多台主机信息。
    *   配置 `monitor_type` 为 `Zabbix`。
    *   设置 `reinstall_zabbix_agent` 为 `true`。
    *   填写 `controller_zabbix` 和 `template_list` (Zabbix 模板 ID 列表)。

## 5. 相关资源
- [OpsAny官网](https://www.opsany.com/)
- [OpsAny官方文档](https://docs.opsany.com/)
- [MCP协议文档](https://spec.modelcontextprotocol.io/)
- [mcporter文档](https://mcporter.dev/)
```