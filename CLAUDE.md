# OpsAny 项目开发指南

## 项目概览

OpsAny是基于腾讯蓝鲸bk-PaaS二次开发的运维PaaS平台，提供应用引擎、API网关、统一登录、前后台开发框架等模块，帮助开发者快速构建运维SaaS应用。

## 技术栈

- **Python**: 3.12 (paas服务), 3.7 (websocket服务，待升级)
- **Django**: 4.2.16
- **Go**: paasagent
- **数据库**: MySQL, MongoDB
- **缓存**: Redis

## 目录结构

```
opsany-paas/
├── paas-ce/                    # 核心PaaS服务代码
│   ├── paas/                  # Django项目(4个服务)
│   │   ├── appengine/         # 应用引擎 (端口8000)
│   │   ├── esb/              # API网关 (端口8002)
│   │   ├── login/             # 统一登录 (端口8003)
│   │   ├── paas/             # 开发中心&工作台 (端口8001)
│   │   └── websocket/         # 堡垒机服务 (端口8004)
│   ├── paasagent/            # Go语言Agent (端口4245/8085)
│   └── saas/                # SaaS应用目录
├── install/                   # 安装维护脚本
│   ├── install.config.example
│   ├── paas-install.sh       # PaaS平台安装
│   └── saas-ce-install.sh    # SaaS安装
├── kubernetes/               # K8S helm部署
│   ├── helm/opsany-base/    # 基础组件(MySQL/Redis/MongoDB)
│   └── helm/                # PaaS服务部署
├── opsctl/                  # CLI客户端
├── opsany-mcp-server/       # MCP Server
├── saas/                    # SaaS应用集合
└── docs/                    # 文档
```

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| paas | 8001 | 开发中心&web工作台 |
| appengine | 8000 | 应用引擎 |
| esb | 8002 | API网关 |
| login | 8003 | 统一登录服务 |
| websocket | 8004 | 堡垒机底层通信 |
| paasagent | 4245 | Agent服务 |
| paasagent | 8085 | Nginx端口 |

## 开发注意事项

### 1. Python版本要求
- 所有paas服务使用Python 3.12
- **websocket项目当前使用Python 3.7，未来需要升级到3.12**
- 参考其他服务（如paas/esb）的代码结构和依赖进行升级

### 2. Django版本
- 当前使用Django 4.2.16
- 升级时注意Django 5.x的兼容性变化

### 3. ESB组件开发
- 组件目录: `paas-ce/paas/esb/components/generic/`
- 每个API组件是一个单独的Python文件
- 遵循现有组件模式开发新接口

### 4. 数据库模型
- 使用Django ORM
- 迁移文件在各自app的migrations目录

### 5. 配置管理
- 环境变量: `BK_ENV` (development/testing/production)
- 配置文件在各服务的`conf/`目录

## 常用命令

```bash
# 运行Django服务
cd paas-ce/paas/paas && python manage.py runserver 8001
cd paas-ce/paas/esb && python manage.py runserver 8002
cd paas-ce/paas/login && python manage.py runserver 8003
cd paas-ce/paas/websocket && python manage.py runserver 8004
cd paas-ce/paas/appengine && python manage.py runserver 8000

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 安装SaaS
cd install && ./saas-ce-install.sh
```

## MCP Server

- 入口: `opsany-mcp-server/server.py`
- 工具列表: `opsany-mcp-server/tool_list.py`
- 配置: `opsany-mcp-server/config/`

## 参考文档

- 项目README: `README.md`
- 安装文档: `install/README.md`
- 各服务独立README:
  - `paas-ce/paas/appengine/README.md`
  - `paas-ce/paas/esb/README.md`
  - `paas-ce/paas/login/README.md`
  - `paas-ce/paas/websocket/README.md`