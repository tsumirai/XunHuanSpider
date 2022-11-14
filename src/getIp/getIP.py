import os
import urllib.request
from bs4 import BeautifulSoup
import gzip
import time
import datetime
from src.config import global_config, userAgent
from src.glb import global_redis
import random


class GetIP:
	def _getIP(self, pageNo, userAgent):
		headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,zh-TW;q=0.4",
			"Cookie": "channelid=0; sid=1663399669310983",
			"Referer": "https://free.kuaidaili.com/free/inha/2/",
			"User-Agent": userAgent,
		}
		url = global_config.get_value('ip_config.url') + str(pageNo)

		try:
			request = urllib.request.Request(url, headers=headers)
			response = urllib.request.urlopen(request)
			if response.status != 200:
				raise Exception("get ip failed", response.status)
			page = response.read()

			if 'Content-Encoding' in response.headers and response.headers['Content-Encoding'].lower() == 'gzip':
				data = gzip.decompress(page)
				dataString = data.decode(encoding='UTF-8')
			else:
				dataString = page
			response.close()

			soup = BeautifulSoup(dataString, 'html.parser',
								 from_encoding='utf-8')
			ipContents = soup.find_all('tr')

			ipArray = []
			for i in ipContents:
				ipDict = {}
				ipText = i.find_all('td')
				for i in ipText:
					if 'data-title' in i.attrs:
						if i.attrs['data-title'] == '最后验证时间':
							ipDict['最后验证时间'] = i.text
						if i.attrs['data-title'] == '响应速度':
							ipDict['响应速度'] = i.text
						if i.attrs['data-title'] == 'IP':
							ipDict['IP'] = i.text
						if i.attrs['data-title'] == 'PORT':
							ipDict['PORT'] = i.text

				threeDaysAgo = datetime.datetime.now() - datetime.timedelta(days=3)
				timeStamp = int(time.mktime(threeDaysAgo.timetuple()))
				takeTimeStamp = 0
				speed = 10

				if '最后验证时间' in ipDict:
					takeTime = ipDict['最后验证时间']
					takeTimeStamp = time.mktime(
						time.strptime(takeTime, '%Y-%m-%d %H:%M:%S'))

				if '响应速度' in ipDict:
					speedStr = ipDict['响应速度'].rstrip('秒')
					speed = float(speedStr)

				# print(takeTimeStamp)
				# print(timeStamp)
				# print(speed)
				if takeTimeStamp >= timeStamp and speed <= 1:
					ipStr = ''
					portStr = ''
					if 'IP' in ipDict:
						ipStr = ipDict['IP']
					if 'PORT' in ipDict:
						portStr = ipDict['PORT']
					if ipStr != '' and portStr != '':
						ipArray.append(ipStr + ':' + portStr)

			# 最后验证时间大于限定时间，直接返回
			# if takeTimeStamp < timeStamp:
			# 	return ipArray

			# print(i)
			# print(i.attrs)

			print(ipArray)
			return ipArray

		except Exception as result:
			print(result.__traceback__.tb_frame.f_globals['__file__'])
			print(result.__traceback__.tb_lineno)
			print(repr(result))

	# 获得IP列表
	def getIPContent(self):
		fileDir = global_config.get_value('ip_config.dir')
		# 获取绝对路径
		abs_path = os.path.abspath(__file__)
		# 获取目录路径
		dir_name = os.path.dirname(abs_path)
		filePath = fileDir
		print(dir_name)
		if not os.path.exists(filePath):
			os.makedirs(filePath, mode=0o755, exist_ok=True)
		fileName = global_config.get_value('ip_config.name')
		need_ip = False
		try:
			if os.path.exists(filePath + '/' + fileName):
				file_object = open(filePath + '/' + fileName,
								   'r', encoding='utf-8')

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
					ipArray = self._getIP(i, userAgent=user_agent)
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
	def getRandIP(self):
		filePath = global_config.get_value('ip_config.dir')
		fileName = global_config.get_value('ip_config.name')
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
