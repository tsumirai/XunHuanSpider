import requests
from src.logger import logger
from src.config import conf
import random
import string
from requests_toolbelt import MultipartEncoder
import json
import datetime
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


class UploadImg:
    def uploadImg(self, content, image_content, index):
        try:
            # proxyIP = {
            #     'http': 'http://' + ip,
            # }
            # r = requests.get(img_url, headers=header, proxies=proxyIP)
            # if r.status_code == 200:
            image_url = conf.get('image', 'host')
            token = conf.get('image', 'key')

            img_url = content['image_urls'][index]
            tid = content['tid']
            imageNameArray = img_url.split('/')
            if len(imageNameArray) == 0:
                raise Exception("image name error")
            source_image_name = imageNameArray[len(imageNameArray) - 1]
            reg = re.compile(r'\.(.*)')
            m = re.search(reg, source_image_name)
            expand_name = '.jpg'
            if m:
                expand_name = m.group(1)

            image_name = str(tid)+'-'+str(index+1)+'.'+str(expand_name)
            fields = {"file": (image_name, image_content)}
            boundary = '----WebKitFormBoundary' \
                + ''.join(random.sample(string.ascii_letters +
                                        string.digits, 16))
            m = MultipartEncoder(fields=fields, boundary=boundary)
            headers = {
                "Content-Type": m.content_type,
                "Accept": "application/json",
                "Authorization": token
            }

            for i in range(0, 3):  # 重试3次
                req = requests.post(
                    url=image_url, headers=headers, data=m, timeout=10)
                if req.status_code == 200:
                    json_data = json.loads(req.text)
                    logger.info(str(json_data))
                    if json_data['status']:
                        if "data" in json_data and "links" in json_data["data"] and 'url' in json_data["data"]['links']:
                            image_url_data = json_data["data"]['links']['url']
                            logger.info(str(image_url_data))
                            return image_url_data

                    else:
                        message = json['message']
                        logger.error(img_url+"图片上传失败"+message)
            # else:
            #     logger.error(img_url+"图片获取失败")

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))
