# coding=utf-8

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


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

        add_content = xunhuan.Xunhuan(
            12312, '测试', '测试用内容', 'http://ssafdafe', 901231293, 'ceshji')
        session = global_mysql.get_session()
        session.add(add_content)
        session.commit()

        # logIn = log_in.Login('zailid', 'hatsune3190')
        # cookie = logIn.get_cookie()
        # url = conf.get('xunhuan', 'url')

        # agent = userAgent.UserAgent()
        # user_agent = agent.getUserAgent()
        # # print(user_agent)

        # ipFunc = getIP.GetIP()
        # ipFunc.getIPContent()
        # ip = ipFunc.getRandIP()
        # print(ip)

        # headers = getHeaders(url, user_agent, cookie)
        # sPage = allContent.AllContent(url, ip, headers)
        # print(sPage)
        # i = 1
        # # for i in range(1, 4):
        # fPage = forumPage.ForumPage(url, headers, ip, i, 1)
        # pageArray = fPage.getForumPageList()
        # print(len(pageArray))
        # print(pageArray)
        # sPage.getAllSinglePageContent(pageArray)

    except Exception as result:
        print(result.__traceback__.tb_frame.f_globals['__file__'])
        print(result.__traceback__.tb_lineno)
        print(repr(result))
        # logger.error(result.__traceback__.tb_frame.f_globals['__file__']+':'+str(logger.error(
        #     result.__traceback__.tb_lineno)))
        # logger.error(repr(result))
    # finally:
    #     logIn.closeBrowser()
