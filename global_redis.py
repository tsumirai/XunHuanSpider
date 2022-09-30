import redis
import global_var


def _init():
    global _global_pool
    _global_pool = redis.ConnectionPool(host=global_var.get_value(
        'redis.host'), port=global_var.get_value('redis.port'), decode_responses=True)


def set(key, value):
    r = redis.Redis(connection_pool=_global_pool)
    r.set(key, value)

def get(key):
    r = redis.Redis(connection_pool=_global_pool)
    value = r.get(key)
    return value
