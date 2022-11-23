import os
import urllib.request
from bs4 import BeautifulSoup
import gzip
import time
import datetime
from src.config import conf, userAgent
from src.my_redis import global_redis
import random
from src.consts import consts
from src.logger import logger


class GetIP:
    def _getIP(self, pageNo, userAgent):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,zh-TW;q=0.4",
            "Cookie": "channelid=0; sid=1663399669310983",
            "Referer": "https://free.kuaidaili.com/free/inha/2/",
            "User-Agent": userAgent,
        }
        url = conf.get('ip_config', 'url') + str(pageNo)

        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            if response.status != 200:
                raise Exception("get ip failed", response.status)
            page = response.read()

            if 'Content-Encoding' in response.headers and response.headers['Content-Encoding'].lower() == 'gzip':
                data = gzip.decompress(page)
                dataString = data.decode(encoding='UTF-8')
            else:
                dataString = page
            response.close()

            soup = BeautifulSoup(dataString, 'html.parser',
                                 from_encoding='utf-8')
            ipContents = soup.find_all('tr')

            ipArray = []
            for i in ipContents:
                ipDict = {}
                ipText = i.find_all('td')
                for i in ipText:
                    if 'data-title' in i.attrs:
                        if i.attrs['data-title'] == '最后验证时间':
                            ipDict['最后验证时间'] = i.text
                        if i.attrs['data-title'] == '响应速度':
                            ipDict['响应速度'] = i.text
                        if i.attrs['data-title'] == 'IP':
                            ipDict['IP'] = i.text
                        if i.attrs['data-title'] == 'PORT':
                            ipDict['PORT'] = i.text

                threeDaysAgo = datetime.datetime.now() - datetime.timedelta(days=3)
                timeStamp = int(time.mktime(threeDaysAgo.timetuple()))
                takeTimeStamp = 0
                speed = 10

                if '最后验证时间' in ipDict:
                    takeTime = ipDict['最后验证时间']
                    takeTimeStamp = time.mktime(
                        time.strptime(takeTime, '%Y-%m-%d %H:%M:%S'))

                if '响应速度' in ipDict:
                    speedStr = ipDict['响应速度'].rstrip('秒')
                    speed = float(speedStr)

                if takeTimeStamp >= timeStamp and speed <= 1:
                    ipStr = ''
                    portStr = ''
                    if 'IP' in ipDict:
                        ipStr = ipDict['IP']
                    if 'PORT' in ipDict:
                        portStr = ipDict['PORT']
                    if ipStr != '' and portStr != '':
                        ipArray.append(ipStr + ':' + portStr)

            # 最后验证时间大于限定时间，直接返回
            # if takeTimeStamp < timeStamp:
            # 	return ipArray

            # print(i)
            # print(i.attrs)

            print(len(ipArray))
            return ipArray

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

    # 获得IP列表

    def getIPContent(self):
        fileDir = conf.get('ip_config', 'dir')
        filePath = fileDir

        if not os.path.exists(filePath):
            os.makedirs(filePath, mode=0o755, exist_ok=True)
        fileName = conf.get('ip_config', 'name')
        need_ip = False
        try:
            if os.path.exists(filePath + '/' + fileName):
                file_object = open(filePath + '/' + fileName,
                                   'r', encoding='utf-8')

                last_time = global_redis.get(consts.REDIS_KEY_IP_LAST_TIME)
                if last_time:
                    # 7天更新一次
                    get_ip_time = time.mktime(
                        time.strptime(last_time, '%Y-%m-%d %H:%M:%S'))
                    threeSevenAgo = datetime.datetime.now() - datetime.timedelta(days=7)
                    timeStamp = int(time.mktime(threeSevenAgo.timetuple()))
                    if get_ip_time < timeStamp:
                        need_ip = True
                else:
                    need_ip = True
                file_object.close()
            else:
                need_ip = True

            if need_ip:
                agent = userAgent.UserAgent()
                user_agent = agent.getUserAgent()
                ips = []
                for i in range(1, 16):
                    time.sleep(5)
                    ipArray = self._getIP(i, userAgent=user_agent)
                    if len(ipArray) > 0:
                        for i in ipArray:
                            if i not in ips:
                                ips.append(i)

                get_time = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                global_redis.set(consts.REDIS_KEY_IP_LAST_TIME, get_time)
                fw = open(filePath + '/' + fileName, 'w', encoding='utf-8')

                for i in ips:
                    fw.write(i)
                    fw.write('\n')
                fw.close()

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))

    # 获得随机IP

    def getRandIP(self):
        filePath = conf.get('ip_config', 'dir')
        fileName = conf.get('ip_config', 'name')
        ips = []
        ip = ''

        try:
            if os.path.exists(filePath + '/' + fileName):
                file_object = open(filePath + '/' + fileName, 'r')
                lines = file_object.readlines()
                for i in range(1, len(lines)):
                    line = lines[i].rstrip('\n')
                    ips.append(line)
                file_object.close()
            if len(ips) > 0:
                ip = random.choice(ips)
            return ip

        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))
