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
import logging

logging.captureWarnings(True)

class BeiKeProducer(threading.Thread):
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}
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
        resp = requests.get(url, random.choice(self.proxies_dicts), headers=random.choice(self.headers))
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()


class BeiKeConsumer(threading.Thread):
    def __init__(self, info_q):
        super().__init__()
        self.info_q = info_q

    def saveData(self, lst):
        headers = ('楼盘名称', '开发商名称', '是否售空', '销售单价', '楼盘性质')
        with open('./CSV/贝壳找房_杭州.csv', 'w', encoding='utf-8-sig', newline='') as f:
            csvwriter = csv.DictWriter(f, headers)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            f.close()
            print('保存完毕')

    def run(self):
        lst = []
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            lst.append(info)
        self.saveData(lst)


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
    print(proxies_list)
    for i in range(1, 21):
        # page_url = f'https://hz.fang.ke.com/loupan/pg{i}/'
        page_url = 'https://www.baidu.com/'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(5):
        t1 = BeiKeProducer(page_queue, info_queue, proxies_list)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    ti2 = time.time()
    print(f'用时：{ti2-ti1}')
