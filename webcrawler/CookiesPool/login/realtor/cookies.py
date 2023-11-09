from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
import time


class RealtorCookies():
    def __init__(self, username, password, browser):
        #login page
        self.url = 'https://www.realtor.com/myaccount'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'raas_email')))
        submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        username.send_keys(self.username)
        time.sleep(3)
        submit.click()
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'raas_password')))
        submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        time.sleep(3)
        password.send_keys(self.password)
        submit.click()
        time.sleep(1)

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return WebDriverWait(self.browser, 30).until(
                EC.text_to_be_present_in_element((By.ID, 'raas_password_helper'), 'Email and/or Password do not match'))
        except TimeoutException:
            return False
    
    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.LINK_TEXT, 'Sign out'))))
        except TimeoutException:
            return False

    def main(self):
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        

if __name__ == "__main__":
    driver = Driver(uc=True)
    print(RealtorCookies("serel33664@othao.com", "Nimbus_nova@123456", driver).main())