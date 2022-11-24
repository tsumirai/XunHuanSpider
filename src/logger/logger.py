from loguru import logger
import os
from src.config import conf


def _init():
    filePath = conf.get('log', 'dir')
    if not os.path.exists(filePath):
        os.makedirs(filePath, mode=0o755, exist_ok=True)
    logger.add(
        filePath+"xunhuan.log", rotation='1 week', retention='7 days', format="{time}|{level}|{message}", filter=lambda x: '[INFO]' in x['message'], level="INFO")
    logger.add(
        filePath + "xunhuan.log.wf", rotation='1 week', retention='7 days', format="{time}|{level}|{message}-", filter=lambda x: '[ERROR]' in x['message'], level="ERROR")


def info(value):
    logger.info('[INFO]'+str(value))


def error(value):
    logger.error('[ERROR]'+str(value))
