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
        self.shortWait = WebDriverWait(self.browser, 5)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password
        self.reTry = 3

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        try:
            self.browser.delete_all_cookies()
            self.browser.get(self.url)
        except Exception as e:
            print('timeout waiting')
    
    def inputUserName(self):
        """
        输入用户名
        :return: None
        """
        try:
            username = self.wait.until(EC.presence_of_element_located((By.ID, 'raas_email')))
            submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            time.sleep(3)
            username.send_keys(self.username)
            time.sleep(5)
            submit.click()
        except Exception as e:
            pass
    
    def inputPassword(self):
        """
        输入密码
        :return: None
        """
        try:
            password = self.wait.until(EC.presence_of_element_located((By.ID, 'raas_password')))
            submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            time.sleep(3)
            password.send_keys(self.password)
            time.sleep(5)
            submit.click()
        except Exception as e:
            pass

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return self.shortWait.until(
                EC.text_to_be_present_in_element((By.ID, 'raas_password_helper'), 'Email and/or Password do not match'))
        except Exception as e:
            return False
    
    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                self.shortWait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="success-screen-cta"]'))))
        except Exception as e:
            return False
    
    def pass_bot_verify(self):
        """
        通过人机检测
        :return:
        """
        try:
            needVery = True
            def check_bot_verify():
                global needVery
                h2List = self.shortWait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2')))
                for e in h2List:
                    if 'Please verify you are a human' in e.text:
                        needVery = True
                        return True
                return False
            while check_bot_verify():
                button = self.shortWait.until(EC.presence_of_element_located((By.ID, 'px-captcha')))
                #按钮没加载出来刷新
                if button.size['height'] != 120:
                    self.open()
                    break
                #长按10秒
                actions = ActionChains(self.browser)
                actions.click_and_hold(button).perform()
                time.sleep(10)
            return needVery
        except Exception as e:
            return False
    
    def loginFlow(self):
        self.inputUserName()
        self.inputPassword()

    def main(self):
        self.open()
        self.loginFlow()
        count = self.reTry
        while count > 0 and self.pass_bot_verify():
            count -= 1
            self.loginFlow()
        if self.login_successfully():
            cookies = self.browser.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        return {
            'status': 10,
            'content': 'other'
        }
        

if __name__ == "__main__":
    driver = Driver(uc=True, disable_ws=True, devtools=True)
    print(RealtorCookies("pixime9052@othao.com", "Nimbus_nova@123456", driver).main())