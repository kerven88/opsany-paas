import aioredis
import json
from django.conf import settings

def get_async_redis_connection(alias="default"):
    redis_config = settings.CACHES[alias]
    conn = aioredis.from_url(
        f"redis://{redis_config['LOCATION']}",
        decode_responses=True
    )
    return conn

def get_redis_dict_data_async(conn, token):
    if not isinstance(conn, aioredis.Redis):
        conn = get_async_redis_connection(str(conn))
    data = conn.get(token)
    if not data:
        return None
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        try:
            return eval(data)
        except Exception:
            return data

def get_redis_str_data_async(conn, token):
    if not isinstance(conn, aioredis.Redis):
        conn = get_async_redis_connection(str(conn))
    return conn.get(token)

def set_redis_data_async(conn, key, value, ex=None):
    if not isinstance(conn, aioredis.Redis):
        conn = get_async_redis_connection(str(conn))
    conn.set(key, value, ex=ex)
    return True
