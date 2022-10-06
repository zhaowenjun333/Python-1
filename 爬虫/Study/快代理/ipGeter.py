import csv

import requests
import time

# Python实现IP代理批量采集，并检测代理是否可用
# 快代理：https://free.kuaidaili.com/free

import requests
import parsel
from lxml import etree
import json
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

    def __init__(self, ips_q, proxies_q):
        super().__init__()
        self.ips_q = ips_q
        self.proxies_q = proxies_q

    def run(self):
        while True:
            if self.ips_q.empty():
                break
            IP = self.ips_q.get()
            # print(IP)
            self.parse_page(IP)

    def parse_page(self, n_ip):
        test_url = 'https://www.baidu.com/'
        proxies_dict = {
            'http': f'http://{n_ip}',
            'https': f'https://{n_ip}'
        }
        try:
            resp = requests.get(test_url, proxies_dict, headers=random.choice(self.headers), timeout=1)
            if resp.status_code == 200:
                # print(resp.text)
                self.proxies_q.put(proxies_dict)

        except Exception as ex:
            # print(f'不可用，要报错了：{e}')
            print('当前代理', proxies_dict, f'请求超时{ex}')


class IpsConsumer(threading.Thread):
    def __init__(self, proxies_q):
        super().__init__()
        self.proxies_q = proxies_q

    def saveData(self, proxies_lst):
        with open('./开放代理.csv', 'w+', encoding='utf-8', newline='') as f:
            header = ('http', 'https')
            csvwriter = csv.DictWriter(f, header)
            csvwriter.writeheader()
            csvwriter.writerows(proxies_lst)
            f.close()

    def run(self):
        proxies_list = []
        while True:
            if self.proxies_q.empty():
                break
            proxies = self.proxies_q.get()
            proxies_list.append(proxies)
            # print('代理可用', proxies)
            # self.saveData(proxies)
        self.saveData(proxies_list)
        # print('over!')


if __name__ == '__main__':
    ti1 = time.time()

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

    url = 'https://dev.kdlapi.com/api/getproxy/?secret_id=o3va9ta16o5bvtt5pwsp&num=10&protocol=1&method=1&an_ha=1&quality=0&signature=ocbh9onmhnc3umqs48qex91di5&sep=2'
    # 1. url存放到队列中
    ips_queue = Queue()
    # 2. 存放数据的队列
    proxies_queue = Queue()



    while True:
        try:
            res = requests.get(url)
            ips = res.text.split('\n')
            print(ips)
            if ips_queue.qsize() <= 50:
                # print(ips_queue.qsize())
                for ip in ips:
                    if '"msg"' not in ip:
                        ips_queue.put(ip)
                    else:
                        break
            else:
                break

        except Exception as e:
            print(f'获取IP失败{e}')

        finally:
            time.sleep(1)

    p_lst = []
    # 创建5个生产者
    for i in range(5):
        t1 = IpsProducer(ips_queue, proxies_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    j_lst = []
    # 创建五个消费者
    for j in range(1):
        t2 = IpsConsumer(proxies_queue)
        t2.start()
        j_lst.append(t2)
    for j in j_lst:
        j.join()

    ti2 = time.time()
    print(round(ti2 - ti1))
