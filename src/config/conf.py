import configparser
import os
from posixpath import dirname


def _init():
    global _global_config
    _global_config = configparser.ConfigParser()
    # 获取绝对路径
    abs_path = os.path.abspath(__file__)
    # 获取目录路径
    dir_name = os.path.dirname(abs_path)  # 2

    path = dir_name + r'/../../config/config.ini'

    if not os.path.exists(path):
        raise FileNotFoundError("配置文件不存在")
    _global_config.read(path)


def get(section, key):
    return _global_config.get(section, key)
