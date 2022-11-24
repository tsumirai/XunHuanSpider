# coding=utf-8

import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
from src.forum import province


class GetProvince:
    def __init__(self, url, header, page):
        self.url = url
        self.page = page
        self.header = header

    def GetProvinceDict(self):
        values = {"mod": "forumdisplay", "fid": "2", "filter": "sortid", "sortid": "3", "searchsort": "1",
                  "area": self.page}

        headers = self.header
        data = parse.urlencode(values).encode('utf-8')

        request = urllib.request.Request(self.url, data, headers)
        response = urllib.request.urlopen(request)

        if response.status != 200:
            raise Exception("get ip failed", response.status)

        page = response.read()
        # print(page.decode("unicode_escape"))
        response.close()

        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        provinces = soup.find_all('a', attrs={'class': 'xi2'})
        provinceDict = {}
        # print(provinces)
        for i in provinces:
            if 'href' in i.attrs:
                jump_url = i.attrs['href']
                jump_urls = jump_url.split('&area=')
                if len(jump_urls) > 1:
                    area_id = jump_urls[1]
                    provinceDict[i.text] = province.Province(
                        name=i.text, area_id=area_id, jump_url=jump_url)

        for k, v in provinceDict.items():
        	print(k)
        	print(v.name, v.area_id, v.jump_url)
