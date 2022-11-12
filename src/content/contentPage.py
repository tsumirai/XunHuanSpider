# coding=utf-8
from bs4 import BeautifulSoup
from src import content
import requests
from src.config import global_config
from src.content import downloadImg, saveTxt, content


class SinglePage():
	def __init__(self, url, ip, jump_url, tid, header):
		self.url = url
		self.ip = ip
		self.jump_url = jump_url
		self.tid = tid
		self.img_url = url.replace('forum.php', '')
		self.header = header
		self.header['refer'] = header['refer'] + \
							   '&filter=sortid&sortid=3&searchsort=1&area=1'

	def _getSinglePageContent(self):
		url = self.url + '?' + self.jump_url.replace('forum.php?', '')
		# r = re.compile('tid=(.*?)&')
		# m = r.search(self.jump_url)
		# tid = 0
		# if m:
		# 	tid = m.group(1)
		# 	print(tid)

		# cj = cookiejar.CookieJar()
		# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
		# urllib.request.install_opener(opener)

		# proxy_support = urllib.request.ProxyHandler({'http': self.ip})
		# opener = urllib.request.build_opener(proxy_support)
		# urllib.request.install_opener(opener)
		#
		# request = urllib.request.Request(url, headers=self.header)
		# response = urllib.request.urlopen(request)

		proxyIP = {
			'http': 'http://' + self.ip,
		}

		try:
			response = requests.get(url, headers=self.header, proxies=proxyIP)
			response.encoding = 'utf-8'

			# if response.status != 200:
			# 	raise Exception("get ip failed", response.status)
			#
			# page = response.read()
			# print(page.decode("unicode_escape"))
			# response.close()

			soup = BeautifulSoup(
				response.text, 'html.parser', from_encoding='utf-8')
			title = soup.find_all('meta', attrs={"name": 'keywords'})
			thread = soup.find_all('span')
			contentText = soup.find_all('td', class_='t_f')
			pics = soup.find_all('div', class_='mbn savephotop')
			other_pics = soup.find_all('img', class_='zoom')
			contentDetail = content.Content()
			# print(company_item)
			# keyword = "name=\"keywords\""
			contentData = ''
			titleData = ''
			qqData = ''
			wxData = ''
			imageData = []
			for i in title:
				# print(i)
				# print(i.attrs)
				titleData = i.attrs['content'].replace('凤楼信息', '')
			# print(titleData)

			# print(thread)
			for i in thread:
				# print(i.text)
				if 'QQ：' in i.text:
					qq = i.text.split(' ')
					if len(qq) > 0:
						qqData = qq[0].replace('QQ：', '')
				elif 'QQ:' in i.text:
					qq = i.text.split(' ')
					if len(qq) > 0:
						qqData = qq[0].replace('QQ:', '')
				elif 'QQ ' in i.text:
					qq = i.text.split(' ')
					if len(qq) > 1:
						qqData = qq[1].replace('QQ', '')
				elif 'QQ' in i.text and 'QQ群' not in i.text:
					qq = i.text.split(' ')
					if len(qq) > 0:
						qqData = qq[0].replace('QQ', '')
				elif 'qq：' in i.text:
					qq = i.text.split(' ')
					if len(qq) > 0:
						qqData = qq[0].replace('qq：', '')
				elif 'qq:' in i.text:
					qq = i.text.split(' ')
					if len(qq) > 0:
						qqData = qq[0].replace('qq:', '')
				elif 'qq ' in i.text:
					qq = i.text.split(' ')
					if len(qq) > 1:
						qqData = qq[1].replace('qq', '')
				elif 'qq' in i.text and 'qq群' not in i.text:
					qq = i.text.split(' ')
					if len(qq) > 0:
						qqData = qq[0].replace('qq', '')
				# print(qqData)
				if '微信：' in i.text:
					wx = i.text.split(' ')
					if len(wx) > 0:
						wxData = wx[0].replace('微信：', '')
				elif '微信:' in i.text:
					wx = i.text.split(' ')
					if len(wx) > 0:
						wxData = wx[0].replace('微信:', '')
				elif '微信 ' in i.text:
					wx = i.text.split(' ')
					if len(wx) > 1:
						wxData = wx[1].replace('微信:', '')
				elif '微信' in i.text and '微信群' not in i.text:
					wx = i.text.split(' ')
					if len(wx) > 0:
						wxData = wx[0].replace('微信', '')

			for i in contentText:
				tempData = i.find(text=True).strip()
				if tempData != '':
					contentData = tempData
				else:
					if len(i.contents) > 1 and len(i.contents[1]) > 0:
						contentData = i.contents[1].contents[0].text
			# fontText = i.find_all('font')
			# for j in fontText:
			# 	if j.text != '':
			# 		contentData = j.text
			# 	else:
			# 		font2Text = j.find_all('font')
			# 		for k in font2Text:
			# 			if k.text != '':
			# 				contentData = k.text
			# 			else:
			# 				font3Text = k.find_all('font')
			# 				for f in font3Text:
			# 					if f.text != '':
			# 						contentData = f.text

			# print(contentData)
			# print(contentData)
			# print(content)

			for i in pics:
				img = i.find_all('img')
				for j in img:
					image_url = self.img_url + j.attrs['file']
					imageData.append(image_url)
			# print(imageData)
			# print(i)

			for i in other_pics:
				image_url = self.img_url + i.attrs['file']
				imageData.append(image_url)

			complete = contentDetail.Complete(
				titleData, contentData, imageData, qqData, wxData, url, self.tid)
			return complete

		except Exception as result:
			print(result.__traceback__.tb_frame.f_globals['__file__'])
			print(result.__traceback__.tb_lineno)
			print(repr(result))

	# 获得具体帖子内容
	def _getSinglePage(self):
		# refer = "https://www.xhg2009.com/forum.php?mod=forumdisplay&fid=2&filter=sortid&sortid=3&searchsort=1&area=1"

		singleData = self._getSinglePageContent()

		# 下载图片
		downImg = downloadImg.DownloadImg()

		# print(v['title'])
		# print(v['content'])
		# print(v['qq'])
		# print(v['wx'])
		# print(v['image_urls'])
		fileDir = global_config.get_value('image.dir')
		filePath = fileDir + singleData['title'] + '/'

		for img in singleData['image_urls']:
			downImg.downloadImg(img, filePath, self.header, self.ip)

		txt = saveTxt.SaveTxt()
		txt.saveTxt(singleData, filePath)
