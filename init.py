import conf
import global_redis

def _init():
    configC = conf.Config()
    configC.configInit()
    global_redis._init()