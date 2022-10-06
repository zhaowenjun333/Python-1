import re
from lxml import etree
import threading
import time
import random
import collections

import requests
import urllib.request
# url编码
from urllib import parse
from queue import Queue
import csv


class PDDProducer(threading.Thread):

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
        resp = requests.get(url, random.choice(self.proxies_dicts))
        goods_list = resp.json()['result']
        # print(goods_list)
        # ('goods_id', 'goods_name', 'sales_tip', 'group_price')
        for goods in goods_list:
            item = collections.OrderedDict()
            item['goods_id'] = goods['goods_id']
            item['goods_name'] = goods['goods_name']
            item['sales_tip'] = goods['sales_tip']
            item['group_price'] = f'¥{goods["group_price"]/100}'
            # print(item)
            self.info_q.put(item)


class PDDConsumer(threading.Thread):
    def __init__(self, info_q, cols):
        super().__init__()
        self.info_q = info_q
        self.cols = cols

    def save_csv(self, info):
        # print(f'{info[self.cols[0]]},{info[self.cols[1]]},{info[self.cols[2]]},{info[self.cols[3]]}\n')
        with open('./美食.csv', 'a+', encoding='utf-8', newline='') as f:
            f.write(f'{info[self.cols[0]]},{info[self.cols[1]]},{info[self.cols[2]]},{info[self.cols[3]]}\n')
            f.close()
        print('over!')

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            # if len(info) == len(self.cols):
            self.save_csv(info)


if __name__ == '__main__':
    ti1 = time.time()
    header = {
        'Accept': 'application/json, text/javascript',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'apiv2.pinduoduo.com',
        'Origin': 'https://www.pinduoduo.net',
        'Referer': 'https://www.pinduoduo.net/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    with open('./开放代理.csv', 'r', encoding='utf-8') as f1:
        csvreader = csv.DictReader(f1)
        proxies_list = []
        for i in csvreader:
            proxies_list.append(i)
        f1.close()

    col = ('goods_id', 'goods_name', 'sales_tip', 'group_price')
    with open('./美食.csv', 'w+', encoding='utf-8-sig', newline='') as f2:
        csvwriter = csv.DictWriter(f2, col)
        csvwriter.writeheader()
        f2.close()

    for i in range(1, 11):
        page_url = 'https://apiv2.pinduoduo.com/api/gindex/tf/query_tf_goods_info?' \
                   f'tf_id=TFRQ0v00000Y_13397&page={i}&size=100&' \
                   'anti_content=0aqWfxUkM_VenabEuGKaU4dvdtwbwqUDxL0z2QYi_IMuVhzUftpVMPHCCJqNStiVOqN-lfNPlXXpqJ_YNUTdAzTqNiTy7Casl7D3c09ObTlwiHPxnU4ylYPxn04an0P8lxPji0nYnduqnXny05Vaps4HclQlHgqOrtwHpXClrNInquSvAivYy22PxxKAS33OefC5PtZVkL2cwfwanYg7I64Yg_damBVP4ujT0EfQrlgJideEnGedg608qTgjyA6PpuYQjE2Tdv3QjidadMU4QwMwanYTwnwz9ZQdgOOqK_IDA4Pt60lqUTPHuVxpgSnnaJf5H4nlbxt0oQfibJqlarXt9FO0ONqqLcyr52D3w_z9hsdSfBC7IqGFSgmeGTnoFlZsxV96M2qa4i9t5FG'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(5):
        t1 = PDDProducer(page_queue, info_queue, proxies_list)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    for i in range(5):
        t2 = PDDConsumer(info_queue, col)
        t2.start()

    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
