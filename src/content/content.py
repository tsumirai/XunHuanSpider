import requests
from src.logger import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.content import uploadImg, downloadImg, saveTxt
from src.config import conf


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
        # 设置线程池
        thread_pool = ThreadPoolExecutor(max_workers=5)
        for v in contentList:
            thread_pool.submit(self._getImgContent, v, header, ip)
        thread_pool.shutdown(wait=True)

        # 上传图片
        thread_pool = ThreadPoolExecutor(max_workers=3)
        upImg = uploadImg.UploadImg()
        for v in contentList:
            for img in v['image_urls']:
                if img in self.image_content:
                    new_img_url = thread_pool.submit(
                        upImg.uploadImg, img, self.image_content[img], ip, 0)
                    v['new_image_urls'].append(new_img_url.result())

        thread_pool.shutdown(wait=True)

        # 下载图片
        downImg = downloadImg.DownloadImg()

        fileDir = conf.get('image', 'dir')
        for singleData in contentList:
            filePath = fileDir + singleData['title'] + '/'

            for down_img in singleData['image_urls']:
                if down_img in self.image_content:
                    downImg.saveImg(down_img, filePath,
                                    self.image_content[down_img])

            txt = saveTxt.SaveTxt()
            txt.saveTxt(singleData, filePath)

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
