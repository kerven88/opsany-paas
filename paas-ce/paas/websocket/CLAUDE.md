# Websocket 堡垒机服务开发指南

## 服务说明

Websocket是PaaS平台的堡垒机服务，提供Web界面连接到目标设备，支持RDP、SSH、Telnet、MySQL、Redis协议。

- **端口**: 8004
- **Python**: 3.7 (需要升级到 3.12)
- **Django**: 4.2.16
- **数据库**: MySQL
- **缓存**: Redis

## 目录结构

```
websocket/
├── bastion/           # 堡垒机核心
│   ├── component/    # 业务组件
│   ├── core/        # 核心组件
│   │   ├── guacamole/ # Guacamole协议
│   │   └── terminal/ # 终端
│   ├── migrations/  # 迁移
│   ├── models.py  # 数据模型
│   └── routing.py # Websocket路由
├── config/           # 配置
├── manage.py         # Django管理脚本
├── requirements.txt # 依赖
├── settings.py       # 设置入口
└── wsgi.py        # WSGI入口
```

## 配置管理

- 环境变量: `BK_ENV` (development/testing/production)
- 配置文件: `conf/settings_{env}.py`

## 依赖

```
Django==4.2.16
requests==2.32.3
jinja2==3.1.4
sqlalchemy==2.0.38
pymysql==1.1.1
redis==7.1.0
thrift==0.10.0
gevent==24.2.1
pytz==2024.2
MarkupSafe==2.0.1
pycrypto==2.6.1
markdown==3.7
gunicorn==23.0.0
uWSGI==2.0.26
PyYAML==5.1
arrow==0.10.0
Pygments==2.15.0
```

## ⚠️ 待升级事项

**websocket项目当前使用Python 3.7，需要升级到3.12**

### 升级检查点
1. 检查requirements.txt中所有依赖是否支持Python 3.12
2. 检查asgi.py配置(需要使用daphne或uvicorn)
3. 检查channels版本兼容性
4. 测试所有Websocket连接(RDP/SSH/Telnet/MySQL/Redis)

## 运行命令

```bash
cd paas-ce/paas/websocket
python manage.py runserver 8004
```

## Websocket协议

- 使用Django Channels
- 支持WebSocket连接: ws://host:8004/ws/
- 路由: bastion/routing.py