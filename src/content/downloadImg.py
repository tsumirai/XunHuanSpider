import os
import requests
from src.glb import logger


class DownloadImg:
	def downloadImg(self, img_url, filePath, header, ip):
		try:
			if not os.path.exists(filePath):
				os.makedirs(filePath, mode=0o755, exist_ok=True)
			# request = urllib.request.Request(img_url, headers=header)
			imageNameArray = img_url.split('/')
			if len(imageNameArray) == 0:
				raise Exception("image name error")
			imageName = imageNameArray[len(imageNameArray) - 1]

			# urllib.request.urlretrieve(img_url, filePath + imageName)
			# print(img_url)
			proxyIP = {
				'http': 'http://' + ip,
			}
			r = requests.get(img_url, headers=header, proxies=proxyIP)
			if r.status_code == 200:
				with open(filePath + imageName, 'wb') as f:
					f.write(r.content)
			else:
				print("图片获取失败")

		except Exception as result:
			print(result.__traceback__.tb_frame.f_globals['__file__'])
			print(result.__traceback__.tb_lineno)
			print(repr(result))
			logger.error(result.__traceback__.tb_frame.f_globals['__file__']+':'+logger.error(
            result.__traceback__.tb_lineno))
        	logger.error(repr(result))

# with open(filePath + imageName, 'wb')as f:
# 	f.write(response.content)
# 	f.close()
