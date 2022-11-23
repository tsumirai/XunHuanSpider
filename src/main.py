# coding=utf-8

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from src.content import content
from src import mysql
from src.mysql import global_mysql
from src.config import conf
from requests.cookies import cookiejar_from_dict
from src.logIn import log_in
from src.content import allContent
from src.forum import forumPage
from src.getIp import getIP
from src.config import userAgent
from src.my_redis import global_redis
from src.logger import logger
from src.model import xunhuan
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine


# 设置header

def getHeaders(url, user_agent, cookie):
    temp_url = url.replace('https://', '')
    temp_url = temp_url.replace('/forum.php', '')
    authority = temp_url
    refer = url + "?mod=forumdisplay&fid=2"
    cookie = cookie
    cache_control = 'max-age=0'
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    accept_language = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,zh-TW;q=0.4"
    headers = {"authority": authority, "accept": accept, "accept-language": accept_language,
               "cache-control": cache_control, "cookie": cookie,
               "user-agent": user_agent,
               "refer": refer}
    return headers


if __name__ == '__main__':
    try:
        conf._init()
        global_redis._init()
        logger._init()
        global_mysql._init()

        logIn = log_in.Login('zailid', 'hatsune3190')
        cookie = logIn.get_cookie()

        url = conf.get('xunhuan', 'url')

        agent = userAgent.UserAgent()
        user_agent = agent.getUserAgent()

        ipFunc = getIP.GetIP()
        ipFunc.getIPContent()
        ip = ipFunc.getRandIP()

        headers = getHeaders(url, user_agent, cookie)
        sPage = allContent.AllContent(url, ip, headers)

        i = 1
        # for i in range(1, 4):
        fPage = forumPage.ForumPage(url, headers, ip, i, 1)
        pageArray = fPage.getForumPageList()
        logger.info("总数量为："+str(len(pageArray)))
        single_list = sPage.getAllSinglePageContent(pageArray)

        # 处理图片
        pImg = content.Content()
        pImg.processContent(single_list, headers, ip)
        for v in single_list:
            print(v)

    except Exception as result:
        logger.error(
            result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

    finally:
        logIn.closeBrowser()
