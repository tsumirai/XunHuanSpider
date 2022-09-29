import toml
import global_var
import configparser

global config

class Config:
    def updateConfig(self,key,value):
        config = configparser.ConfigParser()
        path = './config.ini'
        config.read(path)
        config.set('ip_config',key,value)
        config.write(open(path,'w'))

    def configInit(self):
        config = configparser.ConfigParser()
        path = './config.ini'
        config.read(path)

        # config = toml.load("./config.toml")
        # print(config)

        global_var._init()
        global_var.set_value('xunhuan.url',config['xunhuan']['url'])
        global_var.set_value('ip_config.dir',config['ip_config']['dir'])
        global_var.set_value('ip_config.name',config['ip_config']['name'])
        global_var.set_value('ip_config.url',config['ip_config']['url'])
        global_var.set_value('image.dir',config['image']['dir'])

