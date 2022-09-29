import urllib.request
from bs4 import BeautifulSoup
import gzip
import time
import datetime
import global_var


class GetIP:
	def getIP(self, pageNo, userAgent):
		headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,zh-TW;q=0.4",
			"Cookie": "channelid=0; sid=1663399669310983",
			"Referer": "https://free.kuaidaili.com/free/inha/2/",
			"User-Agent": userAgent,
		}
		url = global_var.get_value('ip_config.url') + str(pageNo)

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

			soup = BeautifulSoup(dataString, 'html.parser', from_encoding='utf-8')
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
					takeTimeStamp = time.mktime(time.strptime(takeTime, '%Y-%m-%d %H:%M:%S'))

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
