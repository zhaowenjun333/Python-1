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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Host': 'www.dianping.com',
        'Cookie': '_lxsdk_cuid=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _lxsdk=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _hc.v=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198; s_ViewType=10; ctu=f038cc6e62074d02d2dccf4f1fee2914ce130122d343e9146f7edebe2a902766; fspop=test; WEBDFPID=vw0z7286x72v5yy8048ywvw1705486u1816789uwzz097958z1v0u6u7-1978067029903-1662707029572YGMKOUSfd79fef3d01d5e9aadc18ccd4d0c95073605; cy=1; cye=shanghai; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1662913957,1662914153,1662951906,1662958958; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; dplet=e9dee6d846cc7073d2f67141422da23e; dper=d337bc7d6fb74b0bba231d0f6194495b740cf959c046942394895cd7ac64c148ee04317626c1402340e78c26c2ab6991b9c61c04f489898d077678383aa06af3c3bfde13fd55c28732edd8209a144f8b2447a37070602d884ed275d9c4777278; ll=7fd06e815b796be3df069dec7836c3df; ua=Gean; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1662964769; _lxsdk_s=1833047b23e-e29-dd9-9fc%7C%7C655'
    }
    Cookie = {
        'Cookie': '_lxsdk_cuid=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _lxsdk=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _hc.v=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198; s_ViewType=10; ctu=f038cc6e62074d02d2dccf4f1fee2914ce130122d343e9146f7edebe2a902766; fspop=test; WEBDFPID=vw0z7286x72v5yy8048ywvw1705486u1816789uwzz097958z1v0u6u7-1978067029903-1662707029572YGMKOUSfd79fef3d01d5e9aadc18ccd4d0c95073605; cy=1; cye=shanghai; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1662913957,1662914153,1662951906,1662958958; dplet=7915105ca766b8b548b0e5b382c6daf8; dper=d337bc7d6fb74b0bba231d0f6194495b20f0b2cd353b4eb24a6e4c5d8225d625c77f38869048fa45971e3002641a81ade2c39b49bdd7aa8e881baf3802f9d0642eb4f001ecea3d8d440c467bfef8dbf263306bfd6ccbfcc928b23cd7f24e7411; ll=7fd06e815b796be3df069dec7836c3df; ua=Gean; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1662966557; _lxsdk_s=1833047b23e-e29-dd9-9fc%7C%7C1091'
    }

    def __init__(self, page_q, info_q, proxies_dicts, waite1):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        self.proxies_dicts = proxies_dicts
        self.wait = waite1
        self.s = requests.session()

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            print(url)
            self.parse_page(url)

    def parse_page(self, url):
        while True:
            resp = self.s.get(url, headers=self.headers, cookies=self.Cookie)
            resp.encoding = 'utf-8'
            html = resp.text
            # print(html)
            resp.close()
            html_element = etree.HTML(html)
            title = html_element.xpath('/html/head/title/text()')[0]
            if title == '403 Forbidden':
                print('403')
                continue
            else:
                shops = html_element.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
                shops_type = re.findall('<div class="tag-addr">.*?<span class="tag">(.*?)</span>', html, re.S)
                # print(shops_type)
                for info in range(len(shops)):
                    url = shops[info].xpath('.//div[@class="tit"]/a/@href')[0]
                    shop_type = shops_type[info].replace('<svgmtsi class="tagName">', '').replace('</svgmtsi>', '')
                    for k, v in tagName_dict.items():
                        shop_type = shop_type.replace(k, v)
                    self.parse_second(url, shop_type)
                break

    def parse_second(self, url, shop_type):
        item = {}
        driver.get(url)
        # html1 = driver.page_source
        # print(html1)
        resp = requests.get(url, random.choice(self.proxies_dicts), headers=self.headers)
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()
        # 宠物店名称
        shop_name = re.match('.*?<h1 class="shop-name">(.*?)<a class="qr-contrainer"', html, re.S).group(1)
        shop_name = shop_name.replace('<e class="address">', '').replace('</e>', '').replace(' ', '')\
            .replace('<dclass="num">', '').replace('</d>', '')
        for k, v in address_dict.items():
            shop_name = shop_name.replace(k, v)
        for k, v in num_dict.items():
            shop_name = shop_name.replace(k, v)
        # print(shop_name)
        item['宠物店名称'] = shop_name
        # 类型
        item['宠物店类型'] = shop_type

        # 评分
        time.sleep(0.5)
        # self.wait.until(
        #     ec.text_to_be_present_in_element((By.CLASS_NAME, 'phone-qr'), ' 手机扫码&nbsp;优惠买单 ')
        # )
        grade = driver.find_element(By.CLASS_NAME, 'mid-score').text
        item['评分'] = grade

        # 评价数量
        comment_num = re.match('.*?<span id="reviewCount" class="item.txt">(.*?)</span>', html, re.S).group(1)
        comment_num = comment_num.replace('<d class="num">', '').replace('</d>', '').replace(' ', '')
        for k, v in num_dict.items():
            comment_num = comment_num.replace(k, v)
        item['评价数量'] = comment_num
        # 费用
        price = re.match('.*?<span id="avgPriceTitle" class="item.txt">.*?: (.*?)</span>', html, re.S).group(1)
        price = price.replace('<d class="num">', '').replace('</d>', '')
        for k, v in num_dict.items():
            price = price.replace(k, v)
        item['费用'] = price
        # 地址
        position = re.match('.*?<span class="item.txt" itemprop="street-address" id="address">(.*?)'
                            '</span>', html, re.S).group(1)
        position = position.replace('<e class="address">', '').replace('</e>', '')\
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
        print('-----'*30)


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

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"')
    # chrome --remote-debugging-port=9222
    chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 100)

    with open('./全球免费代理.csv', 'r', encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        proxies_list = []
        for i in csvreader:
            proxies_list.append(i)
        f.close()
    # print(proxies_list)

    # with open('./89代理.txt', 'r', encoding='utf-8') as f:
    #     proxies_list = [eval(i.strip(',\n')) for i in f.readlines()]
        # print(proxies_list)

    with open('获取映射关系/address.txt', 'r', encoding='utf-8') as address_txt:
        address_dict = eval(address_txt.readline())
    with open('获取映射关系/num.txt', 'r', encoding='utf-8') as num_txt:
        num_dict = eval(num_txt.readline())
    with open('获取映射关系/tagName.txt', 'r', encoding='utf-8') as tagName_txt:
        tagName_dict = eval(tagName_txt.readline())

    # book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # sheet = book.add_sheet('全国宠物店信息', cell_overwrite_ok=True)
    f = open('./全国宠物店信息.csv', 'w+', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    header = ('宠物店名称', '宠物店类型',
              '评分',
              '评价数量', '费用', '地址', '电话号码')

    writer.writerow(header)

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    for page in range(1, 3):
        # if page == 1:
        #     page_url = 'https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97'
        # else:
        page_url = f'https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97/p{page}'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(2):
        t1 = DZProducer(page_queue, info_queue, proxies_list, wait)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    c_lst = []
    # 创建五个消费者
    for j in range(15):
        t2 = DZConsumer(info_queue, header, writer)
        t2.start()
        c_lst.append(t2)

    for c in c_lst:
        c.join()

    f.close()
    # book.save('./全国宠物店信息.xls')
    print('关闭文件')
    ti2 = time.time()
    print(f'用时：{ti2-ti1}')




