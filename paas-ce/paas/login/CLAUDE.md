# Login 统一登录服务开发指南

## 服务说明

Login是PaaS平台的统一登录服务，提供用户认证、MFA多因素认证等功能。

- **端口**: 8003
- **Python**: 3.12
- **Django**: 4.2.16
- **数据库**: MySQL
- **缓存**: Redis

## 目录结构

```
login/
├── api/               # API接口
├── bkaccount/         # 蓝鲸账号
├── common/            # 公共模块
├── conf/             # 配置
├── config/            # 环境配置
├── ee_official_login/  # 企业登录
├── healthz/          # 健康检查
├── login/            # 登录核心
├── static/           # 静态文件
├── templates/         # 模板
├── manage.py          # Django管理脚本
├── requirements.txt   # 依赖
├── settings.py        # 设置入口
└── urls.py           # URL路由
```

## 配置管理

- 环境变量: `BKPAAS_ENVIRONMENT` (dev/stag/prod) 或 `BK_ENV` (development/testing/production)
- 配置文件: `config/{env}.py`

## 依赖

```
Django==4.2.16
Mako==1.0.6
mysqlclient==1.4.6
PyMySQL==1.0.2
redis==4.2.0
django_redis==5.0.0
celery==5.5.3
kombu==5.5.4
importlib-metadata==7.0
django-cors-headers==3.2.1
channels==4.0.0
channels-redis==4.0.0
requests==2.25.0
paramiko==3.5.0
sshtunnel==0.4.0
kubernetes==26.1.0
cryptography==3.4.7
pycryptodomex==3.9.8
grafana-api==1.0.3
uvicorn==0.35.0
gevent==24.11.1
gunicorn==23.0.0
websockets==15.0.1
```

## 运行命令

```bash
cd paas-ce/paas/login
python manage.py runserver 8003
```