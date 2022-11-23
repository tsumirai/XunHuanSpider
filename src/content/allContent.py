import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.content import contentPage
from src.logger import logger


class AllContent:
    def __init__(self, url, ip, header):
        self.url = url
        self.ip = ip
        self.img_url = url.replace('forum.php', '')
        self.header = header
        self.header['refer'] = header['refer'] + \
            '&filter=sortid&sortid=3&searchsort=1&area=1'

    # 获得所有帖子内容
    def getAllSinglePageContent(self, pageArray):
        # 设置线程池
        thread_pool = ThreadPoolExecutor(max_workers=5)
        single_list = []
        for v in pageArray:
            # 设置随机时间，防止请求过于频繁被反
            sleep_time = random.randint(5, 10)
            time.sleep(sleep_time)
            cPage = contentPage.SinglePage(
                self.url, self.ip, v['jump_url'], v['tid'], self.header)
            # cPage._getSinglePage()
            # 多线程
            single_data = thread_pool.submit(cPage._getSinglePage)
            single_list.append(single_data)

        thread_pool.shutdown(wait=True)

        logger.info("总执行数量为："+str(len(single_list)))
        single_list_data = []
        for future in as_completed(single_list):
            single_list_data.append(future.result())
        return single_list_data
