from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import os
import time

DRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver-win64', 'chromedriver.exe')

URL = 'https://www.facebook.com/'

POST_URL = 'https://www.facebook.com/,https://www.google.com/'

EMAIL = 'egg790508@hotmail.com'

PASSWORD = 'Eggsy7955168~'

WAIT_MIN = 3

class Facebook_Crawler():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # Options 設定
        self.prefs = {
            'profile.default_content_setting_values': 
                {
                    'notifications': 2
                }
            }
        self.options.add_experimental_option('prefs', self.prefs) # 關閉訊息通知
        self.options.add_experimental_option('detach', True) # 避免自動關閉瀏覽器
        self.options.add_argument('--log-level=1') # https://stackoverflow.com/questions/78530683/created-tensorflow-lite-xnnpack-delegate-for-cpu-message-randomly-appears-when
        self.driver = webdriver.Chrome(options=self.options, service=Service(DRIVER_PATH))
        self.login_state = False

    def login(self):
        self.driver.get(URL)
        print('開始登入')
        # 搜尋 帳號/密碼 輸入框
        username = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, 'email')))
        password = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, 'pass')))
        submit = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.NAME, 'login')))
        username.send_keys(EMAIL)
        password.send_keys(PASSWORD)
        time.sleep(5)
        submit.click()
        print(f'請在{WAIT_MIN}分鐘內驗證登入!!!')
        try:
            # 尋找首頁的Search Bar (確定登入成功到達首頁)
            self.search = WebDriverWait(self.driver, int(WAIT_MIN*60)).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type=search]')))
            print('登入成功')
            self.login_state = True

        except:
            print('登入失敗')
            self.driver.quit()
        
    def post(self):
        self.login()
        time.sleep(5)

        if self.login_state:
            print('開始搜尋')
            self.search.click()
            # search.clear()
            self.search.send_keys('按讚')
            time.sleep(10)
            self.search.send_keys(Keys.RETURN)
            time.sleep(30)
            print('搜尋完畢')
            self.driver.quit()

if __name__ == '__main__':
    fb = Facebook_Crawler()
    fb.post()