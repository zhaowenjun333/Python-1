# 目标网站：贝壳找房
# 需求：
# 采集杭州市新房楼盘数据
# 数据要求：
# 要贝壳网的楼盘数据，字段只需要楼盘名称，开发商名称，是否售罄再加上销售单价，楼盘性质。
# 预算：100
import re
import threading
import time
import random

import requests
from lxml import etree
from queue import Queue
import urllib.request
import csv

class BeiKeProducer(threading.Thread):

    header = [
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'},
            {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'},
            {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
        ]

    def __init__(self, page_q, info_q, proxies_dicts):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        self.proxies_dicts = proxies_dicts

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            # print(url)
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, random.choice(self.proxies_dicts), headers=random.choice(self.header))
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()
        html_element = etree.HTML(html)
        buildings = html_element.xpath('//ul[@class="resblock-list-wrapper"]/li')
        if buildings:
            page = url.split('/')[-2].strip('pg')
            print(f'{url}\n第{page}页获取{len(buildings)}条\n')

            for li in range(len(buildings)):
                # 楼盘名
                building_name = buildings[li].xpath('.//div[@class="resblock-name"]/a/text()')[0]

                # 是否在售
                sale_situation = buildings[li].xpath('.//div[@class="resblock-name"]/span[1]/text()')[0]

                # 楼盘性质
                building_property = buildings[li].xpath('.//div[@class="resblock-name"]/span[2]/text()')[0]

                # 销售单价
                number = buildings[li].xpath('.//div[@class="main-price"]/span[@class="number"]/text()')[0]
                if number != '价格待定':
                    if buildings[li].xpath('.//div[@class="second"]/text()'):
                        unit_selling_price = buildings[li].xpath('.//div[@class="second"]/text()')[0]
                    else:
                        price = buildings[li].xpath('.//div[@class="main-price"]//span/text()')
                        unit_selling_price = ''.join(price).replace('\xa0', '')
                else:
                    unit_selling_price = '价格待定'

                # 开发商名称
                url = f'''https://hz.fang.ke.com{buildings[li].xpath('.//div[@class="resblock-name"]/a/@href')[0]}'''
                developer = self.parse_second(url)
                if eval(page) <= 19:
                    num = li + (eval(page)-1) * 10 + 1
                else:
                    num = li + (eval(page) + (eval(page)-20)) * 10 + 1
                item = {
                    '楼盘编号': num,
                    '楼盘名称': building_name,
                    '开发商名称': developer,
                    '是否售空': sale_situation,
                    '销售单价': unit_selling_price,
                    '楼盘性质': building_property,
                }
                self.info_q.put(item)
                print(f'管道：{self.info_q.qsize()}')
                # print(item.txt)

    def parse_second(self, url):
        resp = requests.get(url, headers=random.choice(self.header))
        resp.encoding = 'utf-8'
        html = resp.text
        resp.close()
        developer = re.match('.*?vendor_corp: "(.*?)",', html, re.S).group(1)
        return developer

class BeiKeConsumer(threading.Thread):
    def __init__(self, info_q, w):
        super().__init__()
        self.info_q = info_q
        self.writer = w

    def saveData(self, item):
        rows = []
        for header in headers:
            rows.append(item[header])
        rows = tuple(rows)
        writer.writerow(rows)
        print("Over！")

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            self.saveData(info)


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    with open('./全球免费代理.csv', 'r', encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        proxies_list = []
        for i in csvreader:
            proxies_list.append(i)
        f.close()
    # print(proxies_list)

    f = open('./CSV/贝壳找房_杭州1.csv', 'w+', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    headers = ('楼盘编号', '楼盘名称', '开发商名称', '是否售空', '销售单价', '楼盘性质')
    writer.writerow(headers)

    for i in range(1, 97):
        page_url = f'https://hz.fang.ke.com/loupan/pg{i}/'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = BeiKeProducer(page_queue, info_queue, proxies_list)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(20):
        t2 = BeiKeConsumer(info_queue, writer)
        t2.start()
    ti2 = time.time()
    print(f'用时：{ti2-ti1}')
