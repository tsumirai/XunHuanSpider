import redis
from src.config import conf


def _init():
    global _global_pool
    _global_pool = redis.ConnectionPool(host=conf.get(
        'redis', 'host'), port=conf.get('redis', 'port'), decode_responses=True)


def set(key, value):
    r = redis.Redis(connection_pool=_global_pool)
    res = r.set(key, value)
    return res


def get(key):
    r = redis.Redis(connection_pool=_global_pool)
    value = r.get(key)
    return value
