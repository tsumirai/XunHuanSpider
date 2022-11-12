from src.glb import global_redis
from src.config import conf


def _init():
	configC = conf.Config()
	configC.configInit()
	global_redis._init()
