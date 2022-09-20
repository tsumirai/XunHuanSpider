# coding=utf-8

import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
import province
import content


class CountryPage:
	def __init__(self, url, header, ip, page, area):
		self.url = url
		self.page = page
		self.header = header
		self.ip = ip
		self.area = area

	def getCountryPage(self):
		values = {"mod": "forumdisplay", "fid": "2", "filter": "sortid", "sortid": "3", "searchsort": "1",
				  "area": self.area, "page": self.page}

		headers = self.header
		data = parse.urlencode(values)

		proxy_support = urllib.request.ProxyHandler({'http': self.ip})
		opener = urllib.request.build_opener(proxy_support)
		urllib.request.install_opener(opener)

		print(self.url + '?' + data)

		try:
			request = urllib.request.Request(self.url + '?' + data, headers=headers)
			# print(request.data)
			response = urllib.request.urlopen(request)

			if response.status != 200:
				raise Exception("get ip failed", response.status)

			page = response.read()
			response.close()
			# print(page.decode("unicode_escape"))

			soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
			contents = soup.find_all('a', attrs={'class': 's xst'})
			# print(contents)
			contentArray = []
			for i in contents:
				# print(i.attrs)
				# print(i.text)
				if 'href' in i.attrs:
					tmp_jump_url = i.attrs['href']
					# print(tmp_jump_url)
					jump_url = tmp_jump_url.replace('amp;', '')
					# print(jump_url)
					simpleContent = content.Content()
					contentArray.append(simpleContent.Simple(title=i.text, jump_url=jump_url))

			return contentArray
		# print(i)

		# for k, v in contentDict.items():
		# 	print(k)
		# 	print(v)

		except Exception as result:
			print(result.__traceback__.tb_frame.f_globals['__file__'])
			print(result.__traceback__.tb_lineno)
			print(repr(result))
