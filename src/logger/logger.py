from loguru import logger


def _init():
    logger.add(
        "xunhuan.log", format="{time}|{level}|{message}", filter=lambda x: '[INFO]' in x['message'], level="INFO")
    logger.add(
        "xunhuan.log.wf", format="{time}|{level}|{message}-", filter=lambda x: '[ERROR]' in x['message'], level="ERROR")


def info(value):
    logger.info('[INFO]'+value)


def error(value):
    logger.error('[ERROR]'+value)
