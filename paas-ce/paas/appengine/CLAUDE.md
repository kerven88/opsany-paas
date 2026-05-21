# AppEngine 应用引擎开发指南

## 服务说明

AppEngine是PaaS平台的应用引擎服务，负责SaaS应用的部署、运行和管理。

- **端口**: 8000
- **Python**: 3.12
- **Django**: 4.2.16
- **数据库**: MySQL

## 目录结构

```
appengine/
├── api/               # API接口
├── common/            # 公共模块
├── controller/        # 控制器(核心)
│   ├── settings_default.py  # 默认配置
│   └── settings_sample.py # 示例配置
├── manage.py          # Django管理脚本
├── requirements.txt   # 依赖
└── wsgi.py          # WSGI入口
```

## 配置管理

- 环境变量: `BK_ENV` 或通过controller/settings_default.py配置

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
cd paas-ce/paas/appengine
python manage.py runserver 8000
```

## SaaS部署流程

1. 通过Paas工作台上传SaaS包
2. AppEngine接收部署请求
3. 调用paasagent执行部署任务
4. 回写部署日志到AppEngine