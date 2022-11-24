import requests
from src.logger import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.content import uploadImg, downloadImg, saveTxt
from src.config import conf
from src.mysql import global_mysql
from src.my_redis import global_redis
from src.consts import consts
from src.model import xunhuan


class Content:
    def __init__(self) -> None:
        self.image_content = {}

    def Simple(self, jump_url, title, tid):
        dict = {}
        dict['title'] = title
        dict['jump_url'] = jump_url
        dict['tid'] = tid
        return dict

    def Complete(self, title, content, imageUrls, contact, url, tid):
        dict = {}
        dict['title'] = title
        dict['content'] = content
        dict['image_urls'] = imageUrls
        dict['contact'] = contact
        dict['tid'] = tid
        dict['url'] = url
        dict['new_image_urls'] = []
        return dict

    def processContent(self, contentList, header, ip):
        save_data = []
        # 设置线程池
        thread_pool = ThreadPoolExecutor(max_workers=5)
        for v in contentList:
            thread_pool.submit(self._getImgContent, v, header, ip)
        thread_pool.shutdown(wait=True)

        # 上传图片
        thread_pool = ThreadPoolExecutor(max_workers=3)
        upImg = uploadImg.UploadImg()
        for v in contentList:
            for index in range(len(v['image_urls'])):
                if v['image_urls'][index] in self.image_content:
                    new_img_url = thread_pool.submit(
                        upImg.uploadImg, v, self.image_content[v['image_urls'][index]], index)
                    if new_img_url.result():
                        v['new_image_urls'].append(new_img_url.result())

        thread_pool.shutdown(wait=True)

        # 下载图片
        thread_pool = ThreadPoolExecutor(max_workers=5)

        for singleData in contentList:
            thread_pool.submit(self._saveContentData, singleData)
        thread_pool.shutdown(wait=True)
        
        # 落库
        max_tid_redis = global_redis.get(consts.REDIS_KEY_MAX_TID)
        max_tid = 0
        if max_tid_redis:
            max_tid = int(max_tid_redis)
        for v in contentList:
            logger.info(str(v))
            image_url = ';'.join(v['image_urls'])
            new_image_url = ';'.join(v['new_image_urls'])
            save_content = xunhuan.Xunhuan(v['tid'], v['title'], v['content'],
                                           image_url, v['contact'], new_image_url, v['url'])
            save_data.append(save_content)
            if int(v['tid']) > max_tid:
                max_tid = int(v['tid'])
        global_mysql.add_all(save_data)

        global_redis.set(consts.REDIS_KEY_MAX_TID, max_tid)

    def _getImgContent(self, content, header, ip):
        try:
            proxyIP = {
                'http': 'http://' + ip,
            }
            for img_url in content['image_urls']:
                r = requests.get(img_url, headers=header, proxies=proxyIP)
                if r.status_code == 200:
                    self.image_content[img_url] = r.content
                else:
                    logger.error(img_url+" 图片获取失败")

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

    def _saveContentData(self, content):
        downImg = downloadImg.DownloadImg()
        fileDir = conf.get('image', 'dir')
        filePath = fileDir + str(content['tid'])+'-'+content['title'] + '/'

        for index in range(len(content['image_urls'])):
            if content['image_urls'][index] in self.image_content:
                downImg.saveImg(
                    content, self.image_content[content['image_urls'][index]], index, filePath)

        txt = saveTxt.SaveTxt()
        txt.saveTxt(content, filePath)
