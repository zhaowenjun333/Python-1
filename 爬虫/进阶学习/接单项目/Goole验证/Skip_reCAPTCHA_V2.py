# coding=utf8
import random
import re
import time
from selenium import webdriver
import string
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

import sys
import os

import requests
from lxml import etree
from urllib.parse import urljoin

from twocaptcha import TwoCaptcha

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class SkipV2:
    def __init__(self, api_key, site_xpath1, site_xpath2, textarea_xpath, submit_xpath):
        self.API_KEY = api_key
        self.key = os.getenv('APIKEY_2CAPTCHA', self.API_KEY)
        self.solver = TwoCaptcha(self.key)
        self.site_xpath1 = site_xpath1
        self.site_xpath2 = site_xpath2
        self.textarea_xpath = textarea_xpath
        self.submit_xpath = submit_xpath
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'
        self.api_url = f'https://2captcha.com/in.php?key={self.API_KEY}&method=userrecaptcha'
        self.token_url = f'https://2captcha.com/res.php?key={self.API_KEY}&action=get'
        self.img = './normal.png'

    def get_chrome_driver(self):
        # s = input('请先在cmd中打开, 然后输入yes:')
        s = 'y'
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
            options.add_argument('--headless')
            options.add_argument(f'--proxy-server={proxy}')
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
        time.sleep(1)
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

    # 手动获取
    def get_content(self, url):
        resp = self.session.get(url)
        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        return resp.text

    def get_token(self, site_key, data_s, chrome_driver):
        if not data_s:
            api_url = f'{self.api_url}&googlekey={site_key}&pageurl={chrome_driver.current_url}'
        else:
            api_url = f'{self.api_url}&googlekey={site_key}&data-s={data_s}&pageurl={chrome_driver.current_url}'
        # print(api_url)

        token_id = self.get_content(api_url).split('|')[-1]
        print(f'token_id: {token_id}')
        # time.sleep(1)
        token_url = f'{self.token_url}&id={token_id}'
        # print(token_url)
        token = self.get_content(token_url).split('|')[-1]
        # print(f'第一次获取到的token：{token}')

        time.sleep(0.5)
        while token == 'CAPCHA_NOT_READY':
            token = self.get_content(token_url).split('|')[-1]
            # print(token)
            time.sleep(0.5)
        return token

    def set_textarea(self, chrome_driver, textarea_xpath, token):
        print(f'令牌信息：{token}')
        textarea = chrome_driver.find_element(By.XPATH, textarea_xpath)
        if textarea:
            # 显示textarea
            chrome_driver.execute_script('arguments[0].style.display="block";', textarea)
            # 填充textarea
            chrome_driver.execute_script(f'''arguments[0].value="{token}"''', textarea)
            time.sleep(0.5)

    def submit_form(self, chrome_driver, submit_xpath, token):
        if 'name="continue"' in chrome_driver.page_source:
            form_element = chrome_driver.find_element(By.XPATH, submit_xpath)
            chrome_driver.execute_script('arguments[0].submit()', form_element)
            # chrome_driver.execute_script('document.getElementById("captcha-form").submit()')
            time.sleep(0.5)
            # chrome_driver.refresh()
            # print(chrome_driver.page_source)
            # print(chrome_driver.current_url)
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
            print(f'当前余额：{self.solver.balance()}')
            driver = self.get_chrome_driver()
            driver.get('https://www.google.com/')
            # time.sleep(2)
            # keyword = input('请输入你要搜索的内容：')
            keyword = 'https://seasoneqpt.com/'
            search_element = driver.find_element(By.XPATH, '//form[@role="search"]//input[@class="gLFyf"]')
            search_element.send_keys(keyword)
            search_element.send_keys(Keys.ENTER)
            # time.sleep(1)
            # 测试九宫格
            while 'name="continue"' not in driver.page_source:
                driver.refresh()

            # 测试图形验证码
            # while 'id="captcha"' not in driver.page_source:
            #     driver.back()
            #     self.google_search()

            if 'sorry/index' in driver.current_url and 'reCAPTCHA' in driver.page_source:
                time.sleep(0.5)
                site_key = self.get_site_key(driver, self.site_xpath1)
                data_s_xpath = self.site_xpath1.replace('data-sitekey', 'data-s')
                data_s = self.get_site_key(driver, data_s_xpath)
                # 获取token令牌信息
                token = self.get_token(site_key, data_s, driver)
                # textarea中填写token
                self.set_textarea(driver, self.textarea_xpath, token)
                self.submit_form(driver, self.submit_xpath, token)
            elif 'sorry/index' in driver.current_url and 'id="captcha"' in driver.page_source:
                time.sleep(0.5)
                pic_xpath = '//form[@id="captcha-form"]/img'
                picture = driver.find_element(By.XPATH, pic_xpath).screenshot(self.img)
                api_key = os.getenv('APIKEY_2CAPTCHA', self.API_KEY)
                solver = TwoCaptcha(api_key)
                try:
                    result = solver.normal(self.img)
                except Exception as e:
                    sys.exit(e)
                else:
                    token = result['code']
                    # input_number = driver.find_element(By.XPATH, '//form[@id="captcha-form"]/input[@name="captcha"]')
                    self.textarea_xpath = '//form[@id="captcha-form"]/input[@name="captcha"]'
                    self.submit_xpath = '//form[@id="captcha-form"]'
                    # textarea中填写token
                    self.set_textarea(driver, self.textarea_xpath, token)
                    self.submit_form(driver, self.submit_xpath, token)
        else:
            print(f'余额不足请充值')

    def run(self):
        driver = self.get_chrome_driver()
        page_url = 'https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3D111%26sxsrf%3DAJOqlzWrR3_4Yr7Bhldu8Z7IJEgDT1dUXg%253A1675129781385%26source%3Dhp%26ei%3DtXPYY6TTFKvC0PEPkp6S8A0%26iflsig%3DAK50M_UAAAAAY9iBxVeLCp_2JEIDtq8J1mE2qwKEvtI6%26ved%3D0ahUKEwjkgcfc2PD8AhUrITQIHRKPBN4Q4dUDCAk%26uact%3D5%26oq%3D111%26gs_lcp%3DCgdnd3Mtd2l6EAMyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECcyBwgjEOoCECdQ9gVYtAhgqwpoAXAAeACAAQCIAQCSAQCYAQCgAQGwAQo%26sclient%3Dgws-wiz&q=EgQtIRMQGJLo4Z4GIighDKDDIHF53Dl6hmr-CqEpZJagGwaLpPVS5Y1FFIa__KT2BaBsPcH_MgJjbg'
        # page_url = 'https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3D111%26sxsrf%3DAJOqlzUYt_2uUjztUmav4PzZqwsE-GQ7BQ%253A1674973580611%26ei%3DjBHWY5H9JKGuptQPv7O_sAU%26ved%3D0ahUKEwiR857qkuz8AhUhl4kEHb_ZD1YQ4dUDCBE%26uact%3D5%26oq%3D111%26gs_lcp%3DCgxnd3Mtd2l6LXNlcnAQAzIECCMQJzIHCC4Q1AIQQzIECAAQQzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoECC4QQ0oECEEYAEoECEYYAFAAWJ4CYJcEaABwAHgAgAH8AYgB2AWSAQMyLTOYAQCgAQHAAQE%26sclient%3Dgws-wiz-serp&q=EgQtIRMQGJ2j2J4GIihnb7tQ4_YL607qXBsYFnPDJ-FRUkmBmbrbQKrvWen0tH37D4DLJ0FNMgJjbg'
        driver.get(page_url)
        code = None
        if 'sorry/index' in page_url and 'reCAPTCHA' in driver.page_source:
            site_key = self.get_site_key(driver, self.site_xpath1)
            data_s_xpath = self.site_xpath1.replace('data-sitekey', 'data-s')
            data_s = self.get_site_key(driver, data_s_xpath)
        elif 'sorry/index' in driver.current_url and 'id="captcha"' in driver.page_source:
            time.sleep(1)
            pic_xpath = '//form[@id="captcha-form"]/img'
            picture = driver.find_element(By.XPATH, pic_xpath).screenshot(self.img)
            api_key = os.getenv('APIKEY_2CAPTCHA', self.API_KEY)

            solver = TwoCaptcha(api_key)
            try:
                result = solver.normal(self.img)
            except Exception as e:
                sys.exit(e)
            else:
                site_key = None
                data_s = None
                code = result['code']
                self.textarea_xpath = '//form[@id="captcha-form"]/input[@name="captcha"]'
                self.submit_xpath = '//form[@id="captcha-form"]'
        else:
            site_key = self.get_site_key(driver, self.site_xpath2)
            data_s = None

        # 获取token令牌信息
        if site_key and not code:
            token = self.get_token(site_key, data_s, driver)
        else:
            token = code
        # textarea中填写token
        self.set_textarea(driver, self.textarea_xpath, token)
        self.submit_form(driver, self.submit_xpath, token)


if __name__ == '__main__':
    t1 = time.time()
    API_KEY = 'f64c64f6dee56400f02c9cf224a969c5'
    siteXpath1 = '//div[contains(@id, "recaptcha") and @data-sitekey]'
    siteXpath2 = '//form/script[contains(text(), "sitekey")]'
    textareaXpath = '//textarea[@id="g-recaptcha-response"]'
    submitXpath = textareaXpath + '/ancestor::form'
    skip_v2 = SkipV2(API_KEY, siteXpath1, siteXpath2, textareaXpath, submitXpath)
    # skip_v2.run()
    skip_v2.google_search()
    t2 = time.time()
    print(t2 - t1)
