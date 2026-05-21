# PaaS 主服务开发指南

## 服务说明

PaaS主服务是整个平台的核心，包含开发中心和工作台功能。

- **端口**: 8001
- **Python**: 3.12
- **Django**: 4.2.16
- **数据库**: MySQL
- **缓存**: Redis

## 目录结构

```
paas/
├── apps/              # SaaS应用代码
├── common/           # 公共模块
├── components/       # 组件
├── configs/         # 配置文件
├── esb/             # ESB组件
├── healthz/         # 健康检查
├── lib/             # 工具库
├── manage.py         # Django管理脚本
├── requirements.txt  # 依赖
├── settings.py       # 设置入口
├── urls.py          # URL路由
└── wsgi.py         # WSGI入口
```

## 配置管理

- 环境变量: `BK_ENV` (development/testing/production)
- 配置文件: `conf/settings_{env}.py`

## 依赖

```
Django==4.2.16
pymysql==1.1.1
requests==2.32.3
gunicorn==23.0.0
uWSGI==2.0.26
gevent==24.2.1
```

## 运行命令

```bash
cd paas-ce/paas/paas
python manage.py runserver 8001
```

## 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```