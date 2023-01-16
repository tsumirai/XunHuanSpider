# coding=utf-8
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)



from src.content import content
from src.logger import logger
from src.my_redis import global_redis
from src.config import userAgent
from src.getIp import getIP
from src.forum import forumPage
from src.content import allContent
from src.logIn import log_in
from requests.cookies import cookiejar_from_dict
from src.config import conf
from src.mysql import global_mysql
from src.consts import consts
from src.content import contentPage


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

        ipFunc = getIP.GetIP()
        ipFunc.getIPContent()
        ip = ipFunc.getRandIP()
        logger.info("ip is :"+ip)

        logIn = log_in.Login('zailid', 'hatsune3190', '')
        cookie = logIn.get_cookie()

        url = conf.get('xunhuan', 'url')+'forum.php'

        agent = userAgent.UserAgent()
        user_agent = agent.getUserAgent()

        headers = getHeaders(url, user_agent, cookie)

        # url = 'url = https://www.xhg072.com/'
        # temp_url = url.replace('https://', '')
        # temp_url = temp_url.replace('/forum.php', '')
        # authority = temp_url
        # refer = url + "?mod=forumdisplay&fid=2"
        # cookie = 'Hm_lvt_628b274bff594d6ada27c2b6221d5c1f=1673506520; eqST_2132_saltkey=D73a80aa; eqST_2132_lastvisit=1673585420; eqST_2132_sendmail=1; eqST_2132_viewid=tid_154587; eqST_2132_sid=LHbbv9; eqST_2132_ulastactivity=54b8cvbAlsa9biCidvIO3npR4m7rng9ZTxf6Y8SQEBXCJ9n4aeOT; eqST_2132_lastcheckfeed=75874%7C1673589038; eqST_2132_checkfollow=1; eqST_2132_lip=36.110.18.35%2C1673588551; eqST_2132_auth=8bf5D3qoOycB3xugE1W8O9Aajkeu%2FVBKKM%2Fz2byorg%2BWEahOUuuERaDCoHd6j6OUMvVezu8LAYgaeFdHK479ZQWXog; eqST_2132_tshuz_accountlogin=75874; eqST_2132_member_login_status=1; eqST_2132_st_p=75874%7C1673589041%7C1b94b07d3620f7f4cf9d60b287cc9ee9; eqST_2132_visitedfid=2; Hm_lpvt_628b274bff594d6ada27c2b6221d5c1f=1673589048; eqST_2132_lastact=1673589047%09misc.php%09patch'
        # cache_control = 'max-age=0'
        # accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        # accept_language = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,zh-TW;q=0.4"
        # headers = {"authority": authority, "accept": accept, "accept-language": accept_language,
        #         "cache-control": cache_control, "cookie": cookie,
        #         "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
        #         "refer": refer}
        # sPage = contentPage.SinglePage('https://www.xhg072.com/forum.php',
        #                 '172.24.221.146', 'mod=viewthread&tid=154587', '154587', headers)
        # sPage._getSinglePage()


        sPage = allContent.AllContent(url, ip, headers)

        max_page_num = conf.get('page', 'max_page_num')
        max_tid = global_redis.get(consts.REDIS_KEY_MAX_TID)
        manual_config = conf.get('page', 'manual')
        manual = False
        if manual_config == 'True':
            manual = True

        logger.info('max_page_num is:'+str(max_page_num))
        logger.info('max_tid is:'+str(max_tid))
        logger.info('manual is '+str(manual))

        start_page = 1
        end_page = int(max_page_num)+1
        if manual:
            start_page = int(conf.get('page', 'start_page_num'))
            end_page = start_page+int(conf.get('page', 'page_num'))

        if not max_tid:
            max_tid = 0

        # 获得页面数据
        for i in range(start_page, end_page):
            logger.info("第"+str(i)+'页')
            fPage = forumPage.ForumPage(url, headers, ip, i, 1)
            pageArray = fPage.getForumPageList()
            logger.info("页面内容总数量为："+str(len(pageArray)))

            getPageArray = []
            if not manual:
                for v in pageArray:
                    if int(v['tid']) > int(max_tid):
                        getPageArray.append(v)
            else:
                getPageArray = pageArray

            if len(getPageArray) > 0:
                # 获得页面里的内容数据
                single_list = sPage.getAllSinglePageContent(getPageArray)

                # 处理图片
                pImg = content.Content()
                pImg.processContent(single_list, headers, ip)
            else:
                break

    except Exception as result:
        logger.error(
            result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

    finally:
        logIn.closeBrowser() 

