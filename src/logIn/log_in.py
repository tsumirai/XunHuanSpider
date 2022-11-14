import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class Login:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.browser = webdriver.Chrome(
			executable_path=r'C:\Users\sakuraba\.conda\envs\DownloadFromXunhuan\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe')  # 声明浏览器

	def _log_in(self):
		self.browser.implicitly_wait(30)  # 隐性等待 在规定的时间内，最长等待s秒
		self.browser.get(
			'https://www.xhg141.com/forum.php?mod=forumdisplay&fid=2&sortid=3&sortid=3&filter=sortid&searchsort=1&area=1&page=1')  # 打开设置的网址

		user_login_button = self.browser.find_element_by_class_name('qx_user_a')
		user_login_button.click()

		# 输入用户名
		username = self.browser.find_element_by_name('username')
		username.send_keys(self.username)

		# 输入密码
		password = self.browser.find_element_by_name('password')
		password.send_keys(self.password)

		# 点击登录按钮
		login_button = self.browser.find_element_by_name('loginsubmit')
		login_button.submit()

		time.sleep(4)
		self.browser.refresh()  # 刷新网页
		time.sleep(4)

		cookie = self.browser.get_cookies()  # 获得cookie

		# print(cookie)

		# 打印网页源代码
		# print(browser.page_source.encode('utf-8').decode())
		# browser.quit()
		return cookie

	def get_cookie(self):
		cookie = self._log_in()
		cookieStr = [item['name'] + '=' + item['value'] for item in cookie]
		return '; '.join(item for item in cookieStr)

	# for c in cookie:
	# 	self.cookie[c['name']] = c['value']

	def closeBrowser(self):
		self.browser.quit()
