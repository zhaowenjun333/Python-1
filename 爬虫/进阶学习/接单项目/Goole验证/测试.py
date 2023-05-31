# coding=utf8
# callback
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


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
    chrome_driver = webdriver.Chrome(chrome_options=options)
    return chrome_driver


def run():
    session = requests.session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    session.headers.update(headers)
    driver = get_chrome_driver()
    driver.get('https://www.google.com/')
    time.sleep(2)
    # keyword = input('请输入你要搜索的内容：')
    keyword = 'https://seasoneqpt.com/'
    search_element = driver.find_element(By.XPATH, '//form[@role="search"]//input[@class="gLFyf"]')
    search_element.send_keys(keyword)
    search_element.send_keys(Keys.ENTER)
    while 'name="continue"' not in driver.page_source:
        driver.refresh()
    if 'sorry/index' in driver.current_url and 'reCAPTCHA' in driver.page_source:
        time.sleep(1)
        site_key = driver.find_element(By.XPATH, site_xpath).get_attribute('data-sitekey')
        # print(site_key)
        data_s = driver.find_element(By.XPATH, data_s_xpath).get_attribute('data-s')
        # api_url = f'https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={site_key}&data-s={data_s}&pageurl={driver.current_url}'
        # soft_id = session.get(api_url).text.split('|')[-1]
        # print(soft_id)
        api_key = os.getenv('APIKEY_2CAPTCHA', API_KEY)

        solver = TwoCaptcha(api_key)

        try:
            result = solver.recaptcha(
                sitekey=site_key,
                url=driver.current_url,
                enterprise=1,
                datas=data_s
                )

        except Exception as e:
            sys.exit(e)

        else:
            sys.exit('solved: ' + str(result))


if __name__ == '__main__':
    API_KEY = 'f64c64f6dee56400f02c9cf224a969c5'
    site_xpath = '//div[contains(@id, "recaptcha") and @data-sitekey]'
    data_s_xpath = site_xpath.replace('data-sitekey', 'data-s')
    run()
