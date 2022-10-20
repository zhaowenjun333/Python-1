# 爬虫 大众点评上全国的宠物店名字 地址 电话等信息

import re
import threading
import time
import random

import xlwt
from lxml import etree

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import requests
from queue import Queue
import csv


class DZProducer(threading.Thread):


    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        # self.driver = d
        # self.wait = w

    def run(self):
        while True:
            if self.page_q.empty():
                break
            (url, page_num) = self.page_q.get()
            # print(url)
            self.parse_page(url, page_num)

    def get_head(self, ur):
        user_agent_lst = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_lst)

        # chrome_options = webdriver.ChromeOptions()
        # # chrome_options.add_argument('--headless')
        # # 等效在cmd中：chrome --remote-debugging-port=9222
        # chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
        # chrome_options.add_argument(f'User-Agent={user_agent}')
        # driver = webdriver.Chrome(options=chrome_options)
        # driver.get(ur)
        # cookie_lst = driver.get_cookies()
        # li = []
        # for cookies in cookie_lst:
        #     name = cookies['name']
        #     value = cookies['value']
        #     li.append(f'{name}={value}')
        # cookie = '; '.join(li)
        # time.sleep(1)
        # driver.quit()
        headers = {
            'User-Agent': user_agent,
            'Host': 'www.dianping.com',
            'Cookie': 'fspop=test; cy=1; cye=shanghai; _lxsdk_cuid=183f6b7b77ac8-0576b2000857a6-26021f51-144000-183f6b7b77bc8; _lxsdk=183f6b7b77ac8-0576b2000857a6-26021f51-144000-183f6b7b77bc8; _hc.v=1d14c5e5-9369-774b-3393-4955af60834d.1666291579; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666291579; s_ViewType=10; lgtoken=0ae2f3f34-0188-4b18-b288-76c6bf3c512b; WEBDFPID=u098vy4w172w5wvz0w16y2z649uv8u1v816u3y039w3979583vx686zz-1981651688000-1666291687315WGCSEGSfd79fef3d01d5e9aadc18ccd4d0c95071444; dplet=c8a5a40d68db99102961b0c323115f40; dper=d337bc7d6fb74b0bba231d0f6194495b5d6d2925707fef8bab8b95b7a79b84fee42437ffec6de7c0f8b4bb408f70f90a6d4ab1c719cd9a564866b26b9d0862be181b78cba2668e3f1589fee0bf0007c421a730307cb720ca7bf5bb12981f9f38; ll=7fd06e815b796be3df069dec7836c3df; ua=Gean; ctu=f038cc6e62074d02d2dccf4f1fee29143d98513ff2966d55a74c2481aac9d5da; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1666291712; _lxsdk_s=183f6b7b77c-e4e-d02-b49%7C%7C74'
        }
        return headers

    def parse_page(self, url, page_num):
        headers = self.get_head(url)
        # print(f'headers: {headers}')
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()
        html_element = etree.HTML(html)
        shops = html_element.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
        shops_type = re.findall('<div class="tag-addr">.*?<span class="tag">(.*?)</span>', html, re.S)
        # print(shops_type)
        for num in range(len(shops)):
            url = shops[num].xpath('.//div[@class="tit"]/a/@href')[0]
            shop_type = shops_type[num].replace('<svgmtsi class="tagName">', '').replace('</svgmtsi>', '')
            for k, v in tagName_dict.items():
                shop_type = shop_type.replace(k, v)
            self.parse_second(url, shop_type, num, page_num, headers)

    def parse_second(self, url, shop_type, num, page_num, headers):
        item = {}
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()
        # 宠物店名称
        shop_name = re.match('.*?<h1 class="shop-name">(.*?)<a class="qr-contrainer"', html, re.S).group(1)
        shop_name = shop_name.replace('<e class="address">', '').replace('</e>', '').replace(' ', '') \
            .replace('<dclass="num">', '').replace('</d>', '')
        for k, v in address_dict.items():
            shop_name = shop_name.replace(k, v)
        for k, v in num_dict.items():
            shop_name = shop_name.replace(k, v)
        # print(shop_name)
        item['宠物店名称'] = shop_name
        # 类型
        item['宠物店类型'] = shop_type

        # # 评分
        # grade = self.grade_num(url)
        # item['评分'] = grade

        # 评价数量
        comment_num = re.match('.*?<span id="reviewCount" class="item">(.*?)</span>', html, re.S).group(1)
        comment_num = comment_num.replace('<d class="num">', '').replace('</d>', '').replace(' ', '')
        for k, v in num_dict.items():
            comment_num = comment_num.replace(k, v)
        item['评价数量'] = comment_num
        # 费用
        price = re.match('.*?<span id="avgPriceTitle" class="item">.*?: (.*?)</span>', html, re.S).group(1)
        price = price.replace('<d class="num">', '').replace('</d>', '')
        for k, v in num_dict.items():
            price = price.replace(k, v)
        item['费用'] = price
        # 地址
        position = re.match('.*?<span class="item" itemprop="street-address" id="address">(.*?)'
                            '</span>', html, re.S).group(1)
        position = position.replace('<e class="address">', '').replace('</e>', '') \
            .replace('<d class="num">', '').replace('</d>', '').strip(' ')
        for k, v in address_dict.items():
            position = position.replace(k, v)
        for k, v in num_dict.items():
            position = position.replace(k, v)
        item['地址'] = position
        # 电话号码
        tel = re.match('.*?<span class="info-name">电话：</span>(.*?)</p>', html, re.S).group(1)
        if '无' in tel:
            tel = '无'
        else:
            tel = tel.replace('<d class="num">', '').replace('</d>', '').replace('&nbsp; ', '').strip(' ')
            for k, v in num_dict.items():
                tel = tel.replace(k, v)
        item['电话号码'] = tel
        self.info_q.put((item, num, page_num))
        print(item)
        # print('-----' * 30)

    # def grade_num(self, url):
    #     global grade
    #     self.driver.get(url)
    #     time.sleep(1)
    #     # self.wait.until(
    #     #     ec.text_to_be_present_in_element((By.CLASS_NAME, 'info-name'), '特色：')
    #     # )
    #     print('尝试获取评分')
    #     try:
    #         grade = self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'mid-score'))).text
    #     except Exception as e:
    #         self.grade_num(url)
    #     if grade:
    #         return grade


class DZConsumer(threading.Thread):
    def __init__(self, info_q, s, c):
        super().__init__()
        self.info_q = info_q
        self.sheet = s
        self.col = c

    def saveData(self, item, num, page_num):
        for column in range(len(self.col)):
            row = (page_num-1)*15 + num + 1
            data = self.col[column]
            self.sheet.write(row, column, item[data])

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info, num, page_num = self.info_q.get()
            self.saveData(info, num, page_num)
            # print('----' * 40)


if __name__ == '__main__':
    ti1 = time.time()

    # chrome_options = Options()
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # chrome_options.add_argument(
    #     'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"')
    # driver = webdriver.Chrome(options=chrome_options)
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #                 Object.defineProperty(navigator, 'webdriver', {
    #                   get: () => undefined
    #                 })
    #               """
    # })
    # wait = WebDriverWait(driver, 100)

    # with open('./89代理.txt', 'r', encoding='utf-8') as f:
    #     proxies_list = [eval(i.strip(',\n')) for i in f.readlines()]
    # print(proxies_list)

    with open('./get_dicts/address.txt', 'r', encoding='utf-8') as address_txt:
        address_dict = eval(address_txt.readline())
    with open('./get_dicts/num.txt', 'r', encoding='utf-8') as num_txt:
        num_dict = eval(num_txt.readline())
    with open('./get_dicts/tagName.txt', 'r', encoding='utf-8') as tagName_txt:
        tagName_dict = eval(tagName_txt.readline())

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    for page in range(1, 5):
        page_url = f'https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97/p{page}'
        page_queue.put((page_url, page))

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = DZProducer(page_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('全国宠物店信息', cell_overwrite_ok=True)
    col = ('宠物店名称', '宠物店类型', '评价数量', '费用', '地址', '电话号码')
    for c in range(len(col)):
        sheet.write(0, c, col[c])

    c_lst = []
    # 创建五个消费者
    for j in range(5):
        t2 = DZConsumer(info_queue, sheet, col)
        t2.start()
        c_lst.append(t2)

    for c in c_lst:
        c.join()

    book.save('./全国宠物店信息.xls')
    print('关闭文件')
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
