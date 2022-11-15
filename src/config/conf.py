import configparser
import os
import sys

from src.config import global_config


class Config:
	# def updateConfig(self,key,value):
	#     config = configparser.ConfigParser()
	#     path = './config.ini'
	#     config.read(path)
	#     config.set('ip_config',key,value)
	#     config.write(open(path,'w'))

	def configInit(self):
		config = configparser.ConfigParser()
		# 获取绝对路径
		abs_path = os.path.abspath(__file__)
		# 获取目录路径
		dir_name = os.path.dirname(abs_path)  # 2

		path = dir_name + r'/config.ini'

		if not os.path.exists(path):
			raise FileNotFoundError("配置文件不存在")
		config.read(path)

		# config = toml.load("./config.toml")
		# print(config)

		global_config._init()
		global_config.set_value('xunhuan.url', config.get('xunhuan', 'url'))
		global_config.set_value('ip_config.dir', config.get('ip_config', 'dir'))
		global_config.set_value('ip_config.name', config.get('ip_config', 'name'))
		global_config.set_value('ip_config.url', config.get('ip_config', 'url'))
		global_config.set_value('image.dir', config.get('image', 'dir'))
		global_config.set_value('redis.host', config.get('redis', 'host'))
		global_config.set_value('redis.port', config.get('redis', 'port'))
