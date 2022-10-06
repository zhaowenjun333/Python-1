# Python实现IP代理批量采集，并检测代理是否可用
# 快代理：https://free.kuaidaili.com/free

import requests
import parsel
from lxml import etree
import threading
from queue import Queue
import random
import time


class IpsProducer(threading.Thread):
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

    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            # print(url)
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, headers=random.choice(self.headers))
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()
        html_element = etree.HTML(html)
        trs = html_element.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for tr in trs:
            ip = tr.xpath('.//td[@data-title="IP"]/text()')[0]
            port = tr.xpath('.//td[@data-title="PORT"]/text()')[0]
            print(f'代理ip: {ip}:{port}')


class IpsConsumer(threading.Thread):
    def __init__(self, info_q):
        super().__init__()
        self.info_q = info_q

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    for i in range(1, 2):
        page_url = f'https://free.kuaidaili.com/free/inha/{i}/'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = IpsProducer(page_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    ti2 = time.time()
    print(round(ti2 - ti1))
