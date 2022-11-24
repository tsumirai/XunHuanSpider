import os
import requests
from src.logger import logger
import re
from src.config import conf


class DownloadImg:
    def downloadImg(self, img_url, filePath, header, ip, index, tid):
        try:
            if not os.path.exists(filePath):
                os.makedirs(filePath, mode=0o755, exist_ok=True)

            imageNameArray = img_url.split('/')
            if len(imageNameArray) == 0:
                raise Exception("image name error")
            # imageName = imageNameArray[len(imageNameArray) - 1]

            source_image_name = imageNameArray[len(imageNameArray) - 1]
            reg = re.compile(r'\.(.*)')
            m = re.search(reg, source_image_name)
            expand_name = '.jpg'
            if m:
                expand_name = m.group(1)

            imageName = str(tid)+'-'+str(index+1)+'.'+str(expand_name)

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

    def saveImg(self, content, image_content, index, filePath):
        try:
            if not os.path.exists(filePath):
                os.makedirs(filePath, mode=0o755, exist_ok=True)
            img_url = content['image_urls'][index]
            tid = content['tid']
            imageNameArray = img_url.split('/')
            if len(imageNameArray) == 0:
                raise Exception("image name error")
            # imageName = imageNameArray[len(imageNameArray) - 1]
            source_image_name = imageNameArray[len(imageNameArray) - 1]
            reg = re.compile(r'\.(.*)')
            m = re.search(reg, source_image_name)
            expand_name = '.jpg'
            if m:
                expand_name = m.group(1)

            imageName = str(tid)+'-'+str(index+1)+'.'+str(expand_name)
            # imageName = str(tid)+'-'+str(index+1)
            with open(filePath + imageName, 'wb') as f:
                f.write(image_content)
        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

        finally:
            f.close()
