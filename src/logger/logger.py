from loguru import logger
import os
from src.config import conf


def _init():
    filePath = conf.get('log', 'dir')
    if not os.path.exists(filePath):
        os.makedirs(filePath, mode=0o755, exist_ok=True)
    logger.add(
        filePath+"xunhuan.log", format="{time}|{level}|{message}", filter=lambda x: '[INFO]' in x['message'], level="INFO")
    logger.add(
        filePath + "xunhuan.log.wf", format="{time}|{level}|{message}-", filter=lambda x: '[ERROR]' in x['message'], level="ERROR")


def info(value):
    logger.info('[INFO]'+value)


def error(value):
    logger.error('[ERROR]'+value)
