from lib2to3.pgen2.token import OP
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from src.config import conf


class Login:
    def __init__(self, username, password, ip):
        self.username = username
        self.password = password

        if ip:
            chrome_option = Options()
            chrome_option.add_argument('--proxy-server=https://'+ip)

            self.browser = webdriver.Chrome(options=chrome_option)  # 声明浏览器
        else:
            self.browser = webdriver.Chrome()

    def _log_in(self):
        self.browser.implicitly_wait(30)  # 隐性等待 在规定的时间内，最长等待s秒
        url = conf.get('xunhuan','url')
        # self.browser.get(url+'forum.php'+
        #     '?mod=forumdisplay&fid=2&sortid=3&sortid=3&filter=sortid&searchsort=1&area=1&page=1')  # 打开设置的网址

        self.browser.get(url+
            'member.php?mod=logging&action=login')  # 打开设置的网址

        # user_login_button = self.browser.find_element(
        #     by=By.CLASS_NAME, value='pnavbar-nav')
        # user_login_button.click()

        # 输入用户名
        username = self.browser.find_element(
            by=By.NAME, value='username')
        username.send_keys(self.username)

        # 输入密码
        password = self.browser.find_element(by=By.NAME, value='password')
        password.send_keys(self.password)

        # 点击登录按钮
        login_button = self.browser.find_element(
            by=By.NAME, value='loginsubmit')
        login_button.submit()

        time.sleep(4)
        self.browser.refresh()  # 刷新网页
        time.sleep(4)

        cookie = self.browser.get_cookies()  # 获得cookie

        return cookie

    def get_cookie(self):
        cookie = self._log_in()
        cookieStr = [item['name'] + '=' + item['value'] for item in cookie]
        return '; '.join(item for item in cookieStr)

    def closeBrowser(self):
        self.browser.quit()
