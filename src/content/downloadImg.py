import os
import requests
from src.logger import logger


class DownloadImg:
    def downloadImg(self, img_url, filePath, header, ip):
        try:
            if not os.path.exists(filePath):
                os.makedirs(filePath, mode=0o755, exist_ok=True)

            imageNameArray = img_url.split('/')
            if len(imageNameArray) == 0:
                raise Exception("image name error")
            imageName = imageNameArray[len(imageNameArray) - 1]

            proxyIP = {
                'http': 'http://' + ip,
            }
            r = requests.get(img_url, headers=header, proxies=proxyIP)
            if r.status_code == 200:
                with open(filePath + imageName, 'wb') as f:
                    f.write(r.content)
            else:
                logger.error(img_url+"图片获取失败")

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

        finally:
            f.close()

    def saveImg(self, img_url, filePath, image_content):
        try:
            if not os.path.exists(filePath):
                os.makedirs(filePath, mode=0o755, exist_ok=True)
            imageNameArray = img_url.split('/')
            if len(imageNameArray) == 0:
                raise Exception("image name error")
            imageName = imageNameArray[len(imageNameArray) - 1]
            with open(filePath + imageName, 'wb') as f:
                f.write(image_content)
        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

        finally:
            f.close()
