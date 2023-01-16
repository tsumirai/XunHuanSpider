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
            contentDetail = content.Content()
            # thread = soup.find_all('span')
            # miss_show = soup.find_all('div', class_='Profile')
            contactData = ''
            miss_show = soup.find(class_='font-weight-bold',text=re.compile(r'QQ/微信：(.*)'))
            if miss_show.next_sibling:
                contactData = miss_show.next_sibling.text.replace('未见人就要定金、押金、路费的100%是骗子，请点击举报，删帖处理','')
            contentText = soup.find_all('td', class_='t_f')
            pics = soup.find_all('img', class_='el-image__inner p_no_uid el-image__preview')
            other_pics = soup.find_all('img', class_='el-image__inner el-image__preview')

            contentData = ''
            titleData = ''
            
            imageData = []
            for i in title:
                titleData = i.attrs['content'].replace('凤楼信息', '')

            # for i in miss_show:
            #     contactDetail = i.find_next(class_='font-weight-bold',text=re.compile(r'QQ/微信：(.*)'))
            #     print(contactDetail.next_sibling)
                
            #     reg = re.compile(r'QQ/微信：(.*)\n\n')

            #     m = re.search(reg, i.text)
            #     if m:
            #         contactData = m.group(1)
            #     else:
            #         contactData = i.text

            for i in contentText:
                tempData = i.find(text=True).strip()
                if tempData != '':
                    contentData = tempData
                else:
                    if len(i.contents) > 1 and len(i.contents[1]) > 0:
                        contentData = i.contents[1].contents[0].text

            for i in pics:
                addImgUrl = i.attrs['src']
                image_url = self.img_url + addImgUrl
                if image_url not in imageData:
                    imageData.append(image_url)

            for i in other_pics:
                image_url = self.img_url + i.attrs['src']
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

