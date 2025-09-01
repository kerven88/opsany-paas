# -*- coding: utf-8 -*-
from urllib import parse

import mongoengine
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = 'PRODUCT'

# 只对正式环境日志级别进行配置，可以在这里修改
LOG_LEVEL = 'ERROR'

# 工单外部连接是否认证 True 免认证 False 强认证
WORK_ORDER_URL_APPROVE_NO_AUTH = True

# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')


# 正式环境数据库可以在这里配置

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': APP_CODE,  # 数据库名
            'USER': APP_CODE,  # 数据库用户
            'PASSWORD': os.getenv("MYSQL_PASSWORD", "MYSQL_OPSANY_WORKBENCH_PASSWORD"),  # 数据库密码
            'HOST': os.getenv("MYSQL_HOST", "MYSQL_SERVER_IP"),  # 数据库主机
            'PORT': int(os.getenv("MYSQL_PORT", "MYSQL_SERVER_PORT")),  # 数据库端口
            'OPTIONS': {
                "init_command": "SET default_storage_engine=INNODB;\
                                 SET sql_mode='STRICT_TRANS_TABLES';",
            }

        },
    }
)

# MongoDB Config
MONGO_CONN = mongoengine.connect(
        db=APP_CODE,                                 # 需要进行操作的数据库名称
        alias='default',                          # 必须定义一个default数据库
        host=os.getenv("MONGO_HOST", "MONGO_SERVER_IP"),
        port=int(os.getenv("MONGO_PORT", "MONGO_SERVER_PORT")),
        username=APP_CODE,
        password=os.getenv("MONGO_PASSWORD", "MONGO_WORKBENCH_PASSWORD"),
        connect=False
        # authentication_source="admin",           # 进行身份认证的数据库，通常这个数据库为admin
)

# 认证接口本地缓存时间(牵扯到接口反应时间和RBAC菜单授权生效时间)
AUTH_API_CACHE_EXPIRATION = 60 * 5

# Redis Config
REDIS_HOST = os.getenv("REDIS_HOST", "REDIS_SERVER_IP")
REDIS_PORT = os.getenv("REDIS_PORT", "REDIS_SERVER_PORT")
REDIS_USERNAME = parse.quote(os.getenv("REDIS_USERNAME", "REDIS_SERVER_USER") or "")  
REDIS_PASSWORD = parse.quote(os.getenv("REDIS_PASSWORD", "REDIS_SERVER_PASSWORD")) 

# Redis Celery AMQP
BROKER_URL = 'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'.format(REDIS_USERNAME=REDIS_USERNAME, REDIS_PASSWORD=REDIS_PASSWORD, REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT)

# Reids Cache
CACHES.update(
    {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://{}:{}@{}:{}/10".format(REDIS_USERNAME, REDIS_PASSWORD, REDIS_HOST, REDIS_PORT),
             # 'TIMEOUT': 86400,  # 1天
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # "CONNECTION_POOL_KWARGS": {"max_connections": 1000},
                # "PASSWORD": REDIS_PASSWORD,
            }
        }
    },
)

# Elastic APM
ELASTIC_APM = {
  'ENABLED': 'false',
  'SERVICE_NAME': 'opsany-saas-workbench',
  'SECRET_TOKEN': 'APM_SECRET_TOKEN',
  'SERVER_URL': 'https://APM_SERVER_HOST:8200',
  'VERIFY_SERVER_CERT': 'false',
  'ENVIRONMENT': 'prod',
}

# Elastic frontend APM
FRONTEND_ELASTIC_APM = {
    'FRONTEND_SERVICE_NAME': 'opsany-saas-workbench-frontend',
    'FRONTEND_SERVER_URL': 'https://APM_SERVER_HOST:8200',
    "FRONTEND_ENABLED": 'false',
    'FRONTEND_ENVIRONMENT': 'prod',
}

YUN_PIAN_URL = os.getenv("YUN_PIAN_URL", "YUN_PIAN_URL")
YUN_PIAN_APIKEY = os.getenv("YUN_PIAN_APIKEY", "YUN_PIAN_APIKEY")
YUN_PIAN_HS_CODE = os.getenv("YUN_PIAN_HS_CODE", "YUN_PIAN_HS_CODE")
YUN_PIAN_ALERT_TPL_ID = os.getenv("YUN_PIAN_ALERT_TPL_ID", "YUN_PIAN_ALERT_TPL_ID")
YUN_PIAN_SERVER_CHECK_TPL_ID = os.getenv("YUN_PIAN_SERVER_CHECK_TPL_ID", "YUN_PIAN_SERVER_CHECK_TPL_ID")

# 内网环境映射时可修改为映射IP
DING_TALK_API_DOMAIN = "https://api.dingtalk.com"
DING_TALK_OAPI_DOMAIN = "https://oapi.dingtalk.com"
# 支持在请求头传一个参数用作内网认证
DING_TALK_API_HEADER_CODE = "hs-code"  # 请求头参数
DING_TALK_API_HEADER_DATA = "DING_TALK_API_HEADER_DATA"  # 请求头数据-API
DING_TALK_OAPI_HEADER_DATA = "DING_TALK_OAPI_HEADER_DATA"  # 请求头数据-OAPI

# 工单处理后当前免登录链接过期时间(天)
WORK_ORDER_FREE_LINK_VALID_TIME = 30
