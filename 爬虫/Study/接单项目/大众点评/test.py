import csv
import random
import re
import time

from lxml import etree
from seleniumwire import webdriver
import requests


def get_cookies(ur, head):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # 等效在cmd中：chrome --remote-debugging-port=9222
    options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
    options.add_argument(f'User-Agent={head}')
    driver = webdriver.Chrome(options=options)
    driver.get(ur)
    cookie_lst = driver.get_cookies()
    li = []
    for cookies in cookie_lst:
        name = cookies['name']
        value = cookies['value']
        li.append(f'{name}={value}')
    cookies = '; '.join(li)
    time.sleep(1)
    driver.quit()
    return cookies


if __name__ == '__main__':
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    url = 'https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97'
    cookie = get_cookies(url, header)
    # print(cookie)
    headers = {
        'User-Agent': header,
        'Host': 'www.dianping.com',
        'Cookie': cookie
    }

    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    print(resp.text)


