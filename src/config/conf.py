import configparser
from src.config import global_config

global config


class Config:
	# def updateConfig(self,key,value):
	#     config = configparser.ConfigParser()
	#     path = './config.ini'
	#     config.read(path)
	#     config.set('ip_config',key,value)
	#     config.write(open(path,'w'))

	def configInit(self):
		config = configparser.ConfigParser()
		path = 'config.ini'
		config.read(path)

		# config = toml.load("./config.toml")
		# print(config)

		global_config._init()
		global_config.set_value('xunhuan.url', config['xunhuan']['url'])
		global_config.set_value('ip_config.dir', config['ip_config']['dir'])
		global_config.set_value('ip_config.name', config['ip_config']['name'])
		global_config.set_value('ip_config.url', config['ip_config']['url'])
		global_config.set_value('image.dir', config['image']['dir'])
		global_config.set_value('redis.host', config['redis']['host'])
		global_config.set_value('redis.port', config['redis']['port'])
