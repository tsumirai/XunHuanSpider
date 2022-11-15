# coding=utf-8
from src.config import conf
from src.glb import global_redis
from requests.cookies import cookiejar_from_dict
from src.logIn import log_in
from src.content import allContent
from src.forum import forumPage
from src.getIp import getIP
from src.config import global_config, userAgent


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
    configC = conf.Config()
    configC.configInit()
    # global_redis._init()

    logIn = log_in.Login('zailid', 'hatsune3190')
    cookie = logIn.get_cookie()

    url = global_config.get_value('xunhuan.url')

    agent = userAgent.UserAgent()
    user_agent = agent.getUserAgent()
    # print(user_agent)

    ipFunc = getIP.GetIP()
    ipFunc.getIPContent()
    ip = ipFunc.getRandIP()
    print(ip)

    headers = getHeaders(url, user_agent, cookie)
    sPage = allContent.AllContent(url, ip, headers)
    print(sPage)
    i = 1
    # for i in range(1, 4):
    fPage = forumPage.ForumPage(url, headers, ip, i, 1)
    pageArray = fPage.getForumPageList()
    print(len(pageArray))
    print(pageArray)
    sPage.getAllSinglePageContent(pageArray)

    logIn.closeBrowser()
