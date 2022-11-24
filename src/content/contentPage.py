# coding=utf-8
from bs4 import BeautifulSoup
from src import content
import requests
from src.config import conf
from src.content import downloadImg, saveTxt, content, uploadImg
from src.logger import logger
import re


class SinglePage:
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

        proxyIP = {
            'http': 'http://' + self.ip,
        }

        try:
            response = requests.get(
                url, headers=self.header, proxies=proxyIP)
            response.encoding = 'utf-8'

            # if response.status != 200:
            # 	raise Exception("get ip failed", response.status)
            #

            soup = BeautifulSoup(
                response.text, 'html.parser', from_encoding='utf-8')
            title = soup.find_all('meta', attrs={"name": 'keywords'})
            # thread = soup.find_all('span')
            miss_show = soup.find_all('div', class_='miss-show')
            contentText = soup.find_all('td', class_='t_f')
            pics = soup.find_all('div', class_='mbn savephotop')
            other_pics = soup.find_all('img', class_='zoom')
            contentDetail = content.Content()

            contentData = ''
            titleData = ''

            contactData = ''
            imageData = []
            for i in title:
                titleData = i.attrs['content'].replace('凤楼信息', '')

            for i in miss_show:
                reg = re.compile(r'QQ/微信:(.*)切记！未见面不要先给钱，见面满意后付款!')

                m = re.search(reg, i.text)
                if m:
                    contactData = m.group(1)
                else:
                    contactData = i.text

            for i in contentText:
                tempData = i.find(text=True).strip()
                if tempData != '':
                    contentData = tempData
                else:
                    if len(i.contents) > 1 and len(i.contents[1]) > 0:
                        contentData = i.contents[1].contents[0].text

            for i in pics:
                img = i.find_all('img')
                for j in img:
                    image_url = self.img_url + j.attrs['file']
                    imageData.append(image_url)

            for i in other_pics:
                image_url = self.img_url + i.attrs['file']
                if image_url not in imageData:
                    imageData.append(image_url)

            complete = contentDetail.Complete(
                titleData, contentData, imageData, contactData, url, self.tid)
            return complete

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

    # 获得具体帖子内容
    def _getSinglePage(self):
        # refer = "https://www.xhg2009.com/forum.php?mod=forumdisplay&fid=2&filter=sortid&sortid=3&searchsort=1&area=1"

        singleData = self._getSinglePageContent()
        return singleData

        # 上传图片
        upImg = uploadImg.UploadImg()
        for img in singleData['image_urls']:
            upImg.uploadImg(img, self.header, self.ip, self.tid)

        # 下载图片
        downImg = downloadImg.DownloadImg()

        fileDir = conf.get('image', 'dir')
        filePath = fileDir + singleData['title'] + '/'

        for down_img in singleData['image_urls']:
            downImg.downloadImg(down_img, filePath, self.header, self.ip)

        txt = saveTxt.SaveTxt()
        txt.saveTxt(singleData, filePath)
