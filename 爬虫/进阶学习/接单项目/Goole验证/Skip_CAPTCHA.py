import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

import sys
import os

import requests

from twocaptcha import TwoCaptcha

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class SkipCAPTCHA:
    def __init__(self):
        self.API_KEY = 'f64c64f6dee56400f02c9cf224a969c5'
        self.key = os.getenv('APIKEY_2CAPTCHA', self.API_KEY)
        self.solver = TwoCaptcha(self.key)
        self.site_xpath1 = '//div[contains(@id, "recaptcha") and @data-sitekey]'
        self.site_xpath2 = '//form/script[contains(text(), "sitekey")]'
        self.textarea_xpath = '//textarea[@id="g-recaptcha-response"]'
        self.submit_xpath = self.textarea_xpath + '/ancestor::form'
        self.enterprise = 0
        self.picture_xpath = None
        self.img = './normal.png'

    def get_chrome_driver(self):
        # s = input('请先在cmd中打开, 然后输入yes:')
        s = 'a'
        options = webdriver.ChromeOptions()
        if s.lower() == 'y':
            # 反爬
            # 方式一
            # 等效在cmd中：chrome --remote-debugging-port=9222
            options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
            # options.add_argument('--headless')
            chrome_driver = webdriver.Chrome(chrome_options=options)
        else:
            # 方式二
            proxy = 'http://104.223.212.161:65432'

            options.add_argument(f'--proxy-server={proxy}')
            # options.add_argument('--headless')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('disable-infobars')
            options.add_argument("service_args = ['–ignore - ssl - errors = true', '–ssl - protocol = TLSv1']")
            chrome_driver = webdriver.Chrome(chrome_options=options)
            chrome_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
            })
        return chrome_driver

    def get_site_key(self, chrome_driver, sitekey_xpath):
        time.sleep(0.5)
        if 'script' not in sitekey_xpath:
            if 'data-sitekey' in sitekey_xpath:
                sitekey_attr = 'data-sitekey'
                site_key = chrome_driver.find_element(By.XPATH, sitekey_xpath).get_attribute(sitekey_attr)
                print(f'site_key: {site_key}')
            elif 'data-s' in sitekey_xpath:
                data_s_attr = 'data-s'
                site_key = chrome_driver.find_element(By.XPATH, sitekey_xpath).get_attribute(data_s_attr)
                print(f'data-s: {site_key}')
            else:
                site_key = None
        else:
            site_key = re.search(rf'sitekey: "(.*?)",',
                                 chrome_driver.find_element(By.XPATH, sitekey_xpath).get_attribute('innerHTML'),
                                 re.S).group(1)
            print(f'site_key: {site_key}')
        return site_key

    def get_token(self, chrome_driver, site_key, data_s, picture_xpath):
        # 九宫格验证
        if not picture_xpath:
            if data_s:
                self.enterprise = 1
                try:
                    result = self.solver.recaptcha(
                        sitekey=site_key,
                        url=chrome_driver.current_url,
                        enterprise=self.enterprise,
                        datas=data_s
                    )
                    token = result['code']
                except Exception as e:
                    token = None
                    if str(e) == 'ERROR_CAPTCHA_UNSOLVABLE':
                        print('重新获取token值')
                        time.sleep(5)
                        self.get_token(chrome_driver, site_key, data_s, self.picture_xpath)
                    # sys.exit(e)
            else:
                try:
                    result = self.solver.recaptcha(
                        sitekey=site_key,
                        url=chrome_driver.current_url
                    )
                    token = result['code']
                except Exception as e:
                    token = None
                    if str(e) == 'ERROR_CAPTCHA_UNSOLVABLE':
                        print('重新获取token值')
                        time.sleep(5)
                        self.get_token(chrome_driver, site_key, data_s, self.picture_xpath)
                # sys.exit(e)
        # 图片验证
        else:
            chrome_driver.find_element(By.XPATH, picture_xpath).screenshot(self.img)
            try:
                result = self.solver.normal(self.img)
            except Exception as e:
                sys.exit(e)
            else:
                token = result['code']

        return token

    def set_textarea(self, chrome_driver, textarea_xpath, token):
        print(f'令牌信息：{token}')
        textarea = chrome_driver.find_element(By.XPATH, textarea_xpath)
        if textarea:
            # 显示textarea
            chrome_driver.execute_script('arguments[0].style.display="block";', textarea)
            # 填充textarea
            chrome_driver.execute_script(f'''arguments[0].value="{token}"''', textarea)
            time.sleep(1)

    def submit_form(self, chrome_driver, submit_xpath):
        if 'name="continue"' in chrome_driver.page_source:
            form_element = chrome_driver.find_element(By.XPATH, submit_xpath)
            chrome_driver.execute_script('arguments[0].submit()', form_element)
            # chrome_driver.execute_script('document.getElementById("captcha-form").submit()')
            time.sleep(2)
            # chrome_driver.refresh()
            # print(chrome_driver.page_source)
            # print(chrome_driver.current_url)
        elif 'id="captcha-form"' in chrome_driver.page_source:
            form_element = chrome_driver.find_element(By.XPATH, submit_xpath)
            chrome_driver.execute_script('arguments[0].click()', form_element)
            time.sleep(1)
        else:
            submit_element = chrome_driver.find_element(By.XPATH, submit_xpath)
            if 'form' in submit_xpath:
                submit_element.submit()
            else:
                try:
                    chrome_driver.execute_script("arguments[0].click()", submit_element)
                except Exception as e:
                    sys.exit('JS点击提交失败：' + str(e))

    def google_search(self):
        if self.solver.balance() > 0.00299:
            driver = self.get_chrome_driver()
            driver.get('https://www.google.com/')
            # time.sleep(2)
            # keyword = input('请输入你要搜索的内容：')
            keyword = 'https://seasoneqpt.com/'
            search_element = driver.find_element(By.XPATH, '//form[@role="search"]//input[@class="gLFyf"]')
            search_element.send_keys(keyword)
            search_element.send_keys(Keys.ENTER)
            time.sleep(1)

            # 测试九宫格
            while 'name="continue"' not in driver.page_source:
                driver.refresh()

            # 测试图形验证码
            # while 'id="captcha"' not in driver.page_source:
            #     driver.back()
            #     self.google_search()

            # 九宫格人机验证
            if 'sorry/index' in driver.current_url and 'reCAPTCHA' in driver.page_source:
                time.sleep(1)
                site_key = self.get_site_key(driver, self.site_xpath1)
                datas_xpath = self.site_xpath1.replace('data-sitekey', 'data-s')
                datas = self.get_site_key(driver, datas_xpath)
                token = self.get_token(driver, site_key, datas, self.picture_xpath)
                # textarea中填写token
                self.set_textarea(driver, self.textarea_xpath, token)
                self.submit_form(driver, self.submit_xpath)
            # 图形验证码
            elif 'sorry/index' in driver.current_url and 'id="captcha"' in driver.page_source:
                time.sleep(1)
                self.picture_xpath = '//form[@id="captcha-form"]/img'
                token = self.get_token(driver, None, None, self.picture_xpath)
                self.textarea_xpath = '//form[@id="captcha-form"]/input[@name="captcha"]'
                self.submit_xpath = '//form[@id="captcha-form"]/input[@type="submit"]'
                # textarea中填写token
                self.set_textarea(driver, self.textarea_xpath, token)
                self.submit_form(driver, self.submit_xpath)
        else:
            print(f'余额不足请充值')


if __name__ == '__main__':
    skip_captcha = SkipCAPTCHA()
    skip_captcha.google_search()
