# coding=utf-8
from src.config import global_config, userAgent
from src.getIp import getIP
from src.forum import forumPage
from src.content import allContent
from src.logIn import log_in
from requests.cookies import cookiejar_from_dict
from src.glb import global_redis
from src.config import conf


# 设置header
def getHeaders(url, user_agent, cookie):
	temp_url = url.replace('https://', '')
	temp_url = temp_url.replace('/forum.php', '')
	authority = temp_url
	refer = url + "?mod=forumdisplay&fid=2"
	cookie = cookie
	# cookie = "PHPSESSID=3860ir8b2p5eq24avl0h7k4mt3; eqST_2132_saltkey=lOI0eD2o; eqST_2132_lastvisit=1663313799; eqST_2132_sendmail=1; eqST_2132_sid=gguPGN; eqST_2132_ulastactivity=261be2KHxUoYaI3kmKqkJlGwBIyDrjhrZJ2tmlcnS0PLplbbzwgT; eqST_2132_lastcheckfeed=75874%7C1663317436; eqST_2132_lip=111.197.238.222%2C1663316443; eqST_2132_auth=8e3frf78YzDPnxeQfZj8rwuKEA%2F94muDGBbQWWP5eZC%2FXY7j%2F6RnlXubzwFKMw6TNwXHPITitf6ZJmUWFO6cDPUwMQ; eqST_2132_tshuz_accountlogin=75874; eqST_2132_member_login_status=1; eqST_2132_nofavfid=1; eqST_2132_onlineusernum=547; eqST_2132_atarget=1; eqST_2132_visitedfid=2; eqST_2132_st_t=75874%7C1663317549%7C4d91339027d6808bf7f27d6fc8a0ac9c; eqST_2132_forum_lastvisit=D_2_1663317549; eqST_2132_viewid=tid_124258; eqST_2132_st_p=75874%7C1663317561%7Cddf1eb7283eb9af76ffafcabd06ae7c4; eqST_2132_lastact=1663317562%09misc.php%09patch; eqST_2132_forum_lastvisit=D_2_1663332814; eqST_2132_lastact=1663399363%09forum.php%09viewthread; eqST_2132_lip=111.197.238.222%2C1663343525; eqST_2132_sid=o5fk6K; eqST_2132_st_p=75874%7C1663399363%7Cb0750ae89743ab2cc568b3e91faaa4d7; eqST_2132_st_t=75874%7C1663332814%7C6f667a8a1a5bfa712899695cbd605c5d; eqST_2132_ulastactivity=d680o2aedO%2FS0VZBBgknjmHggoqdpyQ8HPw1WiCifXp6T1isno53; eqST_2132_viewid=tid_124258"
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

	# ipFunc = getIP.GetIP()
	# ipFunc.getIPContent()
	# ip = ipFunc.getRandIP()
	# print(ip)

	ip = '101.200.127.149:3129'
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
