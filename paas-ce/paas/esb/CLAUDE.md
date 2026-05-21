# ESB API网关开发指南

## 服务说明

ESB(Enterprise Service Bus)是PaaS平台的API网关服务，将底层原子平台或第三方系统接口封装成统一API供SaaS应用调用。

- **端口**: 8002
- **Python**: 3.12
- **Django**: 4.2.16
- **数据库**: MySQL
- **缓存**: Redis

## 目录结构

```
esb/
├── account/          # 账号管理
├── api/             # API接口
├── app/             # 应用
├── app_env/          # 应用环境
├── bk_app/          # 蓝鲸应用
├── blueking/         # 蓝鲸组件
├── common/          # 公共模块
├── components/       # ESB组件(核心)
├── conf/            # 配置
├── engine/          # 引擎
├── esb/             # ESB核心
├── guide/           # 指南
├── healthz/         # 健康检查
├── home/            # 首页
├── release/         # 发布
├── resource/        # 资源
├── saas/            # SaaS
├── user_center/      # 用户中心
├── manage.py        # Django管理脚本
├── requirements.txt # 依赖
├── settings.py      # 设置入口
└── urls.py         # URL路由
```

## 配置管理

- 环境变量: `BK_ENV` (development/testing/production)
- 配置文件: `conf/settings_{env}.py`

## 依赖

```
Django==4.2.16
dj-static==0.0.6
pycryptodome==3.20.0
requests==2.32.3
pymysql==1.1.1
gunicorn==23.0.0
xlrd==2.0.1
xlwt==1.3.0
gevent==24.2.1
greenlet==3.0.3
pytz==2024.2
python-dateutil==2.6.0
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
pyjwt==2.9.0
six==1.16.0
urllib3==2.2.3
django-cors-headers==4.3.0
```

## ESB组件开发

### 组件目录
组件目录: `esb/components/generic/apis/`

### 开发新组件
1. 在对应模块目录下创建新的Python文件
2. 继承 `esb.utils.BaseApiView` 或类似基类
3. 实现 `get_api_method` 方法
4. 在ESB管理后台注册组件

## 运行命令

```bash
cd paas-ce/paas/esb
python manage.py runserver 8002
```