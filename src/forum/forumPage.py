# coding=utf-8

import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
from src.content import content
import re
from src.logger import logger


class ForumPage:
    def __init__(self, url, header, ip, page, area):
        self.url = url
        self.page = page
        self.header = header
        self.ip = ip
        self.area = area

    def _getForumPage(self):
        values = {"mod": "forumdisplay", "fid": "2", "filter": "sortid", "sortid": "3", "searchsort": "1",
                  "area": self.area, "page": self.page}

        headers = self.header
        data = parse.urlencode(values)

        proxy_support = urllib.request.ProxyHandler({'http': self.ip})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        try:
            request = urllib.request.Request(
                self.url + '?' + data, headers=headers)

            response = urllib.request.urlopen(request)

            if response.status != 200:
                raise Exception("get ip failed", response.status)

            page = response.read()
            response.close()

            soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
            contents = soup.find_all(href=re.compile('forum.php?mod=viewthread&amp;tid='))

            contentArray = []
            for i in contents:
                if 'href' in i.attrs:
                    tmp_jump_url = i.attrs['href']

                    r = re.compile('tid=(.*?)&')
                    m = r.search(tmp_jump_url)
                    tid = 0
                    if m:
                        tid = m.group(1)

                    jump_url = tmp_jump_url.replace('amp;', '')

                    simpleContent = content.Content()
                    contentArray.append(simpleContent.Simple(
                        title=i.text, jump_url=jump_url, tid=tid))

            return contentArray

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

    # ??????????????????????????????
    def getForumPageList(self):
        # refer = "https://www.xhg2009.com/forum.php?mod=forumdisplay&fid=2&filter=sortid&sortid=3&searchsort=1&area=1"

        # province = getProvince.GetProvince(url=url, user_agent=user_agent, refer=refer, cookie=cookie, accept=accept,
        # 								   accept_language=accept_language, page='1')
        # province.GetProvinceDict()

        pageArray = self._getForumPage()
        return pageArray
