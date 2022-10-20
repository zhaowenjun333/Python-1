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
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Host': 'www.dianping.com',
        'Cookie': 'fspop=test; cy=1; cye=shanghai; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=183e0d70e97c8-060a8f5fd8e7db-26021f51-144000-183e0d70e97c8; _lxsdk=183e0d70e97c8-060a8f5fd8e7db-26021f51-144000-183e0d70e97c8; _hc.v=5783cd9d-2c98-3e30-d79d-7f51816e0159.1665924534; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1665924534; s_ViewType=10; WEBDFPID=19xzxv6194785vyy1018z6vxv18807v3816v8772x439795853v6x4y3-1981289477164-1665929476449AWIAWSEfd79fef3d01d5e9aadc18ccd4d0c95071599; dplet=5905ae07ba9d09e02aebb3ac736abe06; dper=a3a8ff29e55beeb6b6f168c8f8febb3594805607c49b0b21ecb1d7cd584fd58669e0b1bcd9d690cda78cd3bda3a8bde3f91204186e974b061bb02b274a2910e753f3c6dfa378eb5a90e81364f2a67ccb051f56c6fade5dc3952cf35a2513a29b; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_5095982428; ctu=80250699b312b597868ffcb6836b0e6e5af2d6183bdd2f95ade9428455a6173a; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1665929497; _lxsdk_s=183e1222e94-f5a-b28-cbd%7C%7C52'
    }

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
            url = self.page_q.get()
            # print(url)
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()
        html_element = etree.HTML(html)
        shops = html_element.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
        shops_type = re.findall('<div class="tag-addr">.*?<span class="tag">(.*?)</span>', html, re.S)
        # print(shops_type)
        for info in range(len(shops)):
            url = shops[info].xpath('.//div[@class="tit"]/a/@href')[0]
            shop_type = shops_type[info].replace('<svgmtsi class="tagName">', '').replace('</svgmtsi>', '')
            for k, v in tagName_dict.items():
                shop_type = shop_type.replace(k, v)
            self.parse_second(url, shop_type)

    def parse_second(self, url, shop_type):
        item = {}
        resp = requests.get(url, headers=self.headers)
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
        self.info_q.put(item)
        print(item)
        print('-----' * 30)

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
    def __init__(self, info_q, heads, w):
        super().__init__()
        self.info_q = info_q
        self.heads = heads
        self.writer = w

    def saveData(self, item):
        rows = []
        for head in self.heads:
            rows.append(item[head])
        rows = tuple(rows)
        self.writer.writerow(rows)
        print("Over！")

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            # print(info)
            self.saveData(info)
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

    # f = open('./全国宠物店信息.csv', 'w+', encoding='utf-8-sig', newline='')
    # writer = csv.writer(f)
    # writer.writerow(header)

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    for page in range(1, 2):
        page_url = f'https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97/p{page}'
        page_queue.put(page_url)

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
    for j in range(15):
        t2 = DZConsumer(info_queue, header, writer)
        t2.start()
        c_lst.append(t2)

    for c in c_lst:
        c.join()

    f.close()
    book.save('./全国宠物店信息.xls')
    print('关闭文件')
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
