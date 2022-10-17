# coding=utf-8

import singlePage
import countryPage
import getProvince
import downloadImg
import saveTxt
import userAgent
import getIP
import time
from concurrent.futures import ThreadPoolExecutor
import os
import datetime
import random
import global_var
import conf
import init
import global_redis


# 设置header
def getHeaders(url, user_agent):
	temp_url = url.replace('https://', '')
	temp_url = temp_url.replace('/forum.php', '')
	authority = temp_url
	refer = url + "?mod=forumdisplay&fid=2"
	cookie = "PHPSESSID=3860ir8b2p5eq24avl0h7k4mt3; " \
			 "eqST_2132_saltkey=lOI0eD2o; " \
			 "eqST_2132_lastvisit=1663313799; " \
			 "eqST_2132_sendmail=1; " \
			 "eqST_2132_sid=gguPGN; " \
			 "eqST_2132_ulastactivity=261be2KHxUoYaI3kmKqkJlGwBIyDrjhrZJ2tmlcnS0PLplbbzwgT; " \
			 "eqST_2132_lastcheckfeed=75874%7C1663317436; " \
			 "eqST_2132_lip=111.197.238.222%2C1663316443; " \
			 "eqST_2132_auth=8e3frf78YzDPnxeQfZj8rwuKEA%2F94muDGBbQWWP5eZC%2FXY7j%2F6RnlXubzwFKMw6TNwXHPITitf6ZJmUWFO6cDPUwMQ; " \
			 "eqST_2132_tshuz_accountlogin=75874; eqST_2132_member_login_status=1; " \
			 "eqST_2132_nofavfid=1; eqST_2132_onlineusernum=547; eqST_2132_atarget=1; " \
			 "eqST_2132_visitedfid=2; eqST_2132_st_t=75874%7C1663317549%7C4d91339027d6808bf7f27d6fc8a0ac9c; " \
			 "eqST_2132_forum_lastvisit=D_2_1663317549; eqST_2132_viewid=tid_124258; " \
			 "eqST_2132_st_p=75874%7C1663317561%7Cddf1eb7283eb9af76ffafcabd06ae7c4; eqST_2132_lastact=1663317562%09misc.php%09patch"
	# cookie = "PHPSESSID=3860ir8b2p5eq24avl0h7k4mt3; eqST_2132_saltkey=lOI0eD2o; eqST_2132_lastvisit=1663313799; eqST_2132_sendmail=1; eqST_2132_sid=gguPGN; eqST_2132_ulastactivity=261be2KHxUoYaI3kmKqkJlGwBIyDrjhrZJ2tmlcnS0PLplbbzwgT; eqST_2132_lastcheckfeed=75874%7C1663317436; eqST_2132_lip=111.197.238.222%2C1663316443; eqST_2132_auth=8e3frf78YzDPnxeQfZj8rwuKEA%2F94muDGBbQWWP5eZC%2FXY7j%2F6RnlXubzwFKMw6TNwXHPITitf6ZJmUWFO6cDPUwMQ; eqST_2132_tshuz_accountlogin=75874; eqST_2132_member_login_status=1; eqST_2132_nofavfid=1; eqST_2132_onlineusernum=547; eqST_2132_atarget=1; eqST_2132_visitedfid=2; eqST_2132_st_t=75874%7C1663317549%7C4d91339027d6808bf7f27d6fc8a0ac9c; eqST_2132_forum_lastvisit=D_2_1663317549; eqST_2132_viewid=tid_124258; eqST_2132_st_p=75874%7C1663317561%7Cddf1eb7283eb9af76ffafcabd06ae7c4; eqST_2132_lastact=1663317562%09misc.php%09patch; eqST_2132_forum_lastvisit=D_2_1663332814; eqST_2132_lastact=1663399363%09forum.php%09viewthread; eqST_2132_lip=111.197.238.222%2C1663343525; eqST_2132_sid=o5fk6K; eqST_2132_st_p=75874%7C1663399363%7Cb0750ae89743ab2cc568b3e91faaa4d7; eqST_2132_st_t=75874%7C1663332814%7C6f667a8a1a5bfa712899695cbd605c5d; eqST_2132_ulastactivity=d680o2aedO%2FS0VZBBgknjmHggoqdpyQ8HPw1WiCifXp6T1isno53; eqST_2132_viewid=tid_124258"
	cache_control = 'max-age=0'
	accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
	accept_language = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,zh-TW;q=0.4"
	headers = {"authority": authority, "accept": accept, "accept-language": accept_language,
			   "cache-control": cache_control, "cookie": cookie,
			   "user-agent": user_agent,
			   "refer": refer}
	return headers


# 根据页数获得帖子列表
def getForumPageContent(url, ip, page, headers, area):
	# refer = "https://www.xhg2009.com/forum.php?mod=forumdisplay&fid=2&filter=sortid&sortid=3&searchsort=1&area=1"

	# province = getProvince.GetProvince(url=url, user_agent=user_agent, refer=refer, cookie=cookie, accept=accept,
	# 								   accept_language=accept_language, page='1')
	# province.GetProvinceDict()

	country = countryPage.CountryPage(url=url, header=headers, ip=ip,
									  page=page, area=area)
	pageArray = country.getCountryPage()
	return pageArray


# 获得所有帖子内容
def getAllSinglePageContent(url, pageArray, ip, thread_pool, headers):
	for v in pageArray:
		# 设置随机时间，防止请求过于频繁被反
		sleep_time = random.randint(5, 10)
		time.sleep(sleep_time)
		# 多线程
		thread_pool.submit(getSinglePageContent, url,
						   ip, v['jump_url'], v['tid'], headers)


# 获得具体帖子内容
def getSinglePageContent(url, ip, jump_url, tid, headers):
	# refer = "https://www.xhg2009.com/forum.php?mod=forumdisplay&fid=2&filter=sortid&sortid=3&searchsort=1&area=1"

	single = singlePage.SinglePage(url=url, ip=ip,
								   jump_url=jump_url, tid=tid, header=headers)
	singleData = single.getSinglePageContent()

	# 下载图片
	downImg = downloadImg.DownloadImg()

	# print(v['title'])
	# print(v['content'])
	# print(v['qq'])
	# print(v['wx'])
	# print(v['image_urls'])
	fileDir = global_var.get_value('image.dir')
	filePath = fileDir + singleData['title'] + '/'

	for img in singleData['image_urls']:
		downImg.downloadImg(img, filePath, headers, ip)

	txt = saveTxt.SaveTxt()
	txt.saveTxt(singleData, filePath)


# 获得IP列表
def getIPContent():
	configC = conf.Config()
	fileDir = global_var.get_value('ip_config.dir')
	filePath = fileDir
	if not os.path.exists(filePath):
		os.makedirs(filePath, mode=0o755, exist_ok=True)
	fileName = global_var.get_value('ip_config.name')
	need_ip = False
	try:
		if os.path.exists(filePath + '/' + fileName):
			file_object = open(filePath + '/' + fileName,
							   'r', encoding='utf-8')
			last_time = ''
			last_time = global_redis.get('ip_last_time')

			if last_time:
				# 7天更新一次
				get_ip_time = time.mktime(
					time.strptime(last_time, '%Y-%m-%d %H:%M:%S'))
				threeSevenAgo = datetime.datetime.now() - datetime.timedelta(days=7)
				timeStamp = int(time.mktime(threeSevenAgo.timetuple()))
				if get_ip_time < timeStamp:
					need_ip = True
			else:
				need_ip = True
			file_object.close()
		else:
			need_ip = True

		if need_ip:
			agent = userAgent.UserAgent()
			user_agent = agent.getUserAgent()
			ips = []
			for i in range(1, 16):
				time.sleep(5)
				ipArray = getIP.GetIP().getIP(i, userAgent=user_agent)
				if len(ipArray) > 0:
					for i in ipArray:
						if i not in ips:
							ips.append(i)

			get_time = time.strftime(
				'%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
			global_redis.set('last_time', get_time)
			fw = open(filePath + '/' + fileName, 'w', encoding='utf-8')

			for i in ips:
				fw.write(i)
				fw.write('\n')
			fw.close()

	except Exception as result:
		print(result.__traceback__.tb_frame.f_globals['__file__'])
		print(result.__traceback__.tb_lineno)
		print(repr(result))


# 获得随机IP
def getRandIP():
	filePath = global_var.get_value('ip_config.dir')
	fileName = global_var.get_value('ip_config.name')
	ips = []
	ip = ''

	try:
		if os.path.exists(filePath + '/' + fileName):
			file_object = open(filePath + '/' + fileName, 'r')
			lines = file_object.readlines()
			for i in range(1, len(lines)):
				line = lines[i].rstrip('\n')
				ips.append(line)
			file_object.close()
		if len(ips) > 0:
			ip = random.choice(ips)
		return ip

	except Exception as result:
		print(result.__traceback__.tb_frame.f_globals['__file__'])
		print(result.__traceback__.tb_lineno)
		print(repr(result))

# 设置tid最大值的缓存
def setMaxTidRedis(pageArray):
	for v in pageArray:
		


if __name__ == '__main__':
	init._init()

	url = global_var.get_value('xunhuan.url')

	global_redis.set("url", url)
	print(global_redis.get('url'))

# agent = userAgent.UserAgent()
# user_agent = agent.getUserAgent()
# # print(user_agent)

# getIPContent()
# ip = getRandIP()
# # print(ip)

# headers = getHeaders(url, user_agent)
# # 设置线程池
# thread_pool = ThreadPoolExecutor(max_workers=5)

# for i in range(1, 4):
# 	pageArray = getForumPageContent(url, ip, i, headers, 1)
# 	print(len(pageArray))
# 	print(pageArray)
# 	getAllSinglePageContent(url, pageArray, ip, thread_pool, headers)

# thread_pool.shutdown(wait=True)

# getSinglePageContent(url, ip, 'forum.php?mod=viewthread&tid=124294&extra=page%3D3%26filter%3Dsortid%26sortid%3D3',headers)
