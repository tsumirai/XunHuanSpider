import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome()  # 声明浏览器

    def _log_in(self):
        self.browser.implicitly_wait(30)  # 隐性等待 在规定的时间内，最长等待s秒
        self.browser.get(
            'https://www.xhg141.com/forum.php?mod=forumdisplay&fid=2&sortid=3&sortid=3&filter=sortid&searchsort=1&area=1&page=1')  # 打开设置的网址

        user_login_button = self.browser.find_element(
            by=By.CLASS_NAME, value='qx_user_a')
        user_login_button.click()

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
