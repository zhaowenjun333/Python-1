# 网址：https://www.89ip.cn/
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

    def __init__(self, page_q, proxies_q):
        super().__init__()
        self.page_q = page_q
        self.proxies_q = proxies_q

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            print(url)
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, headers=random.choice(self.headers))
        resp.encoding = 'utf-8'
        # print(resp.text)
        selector = parsel.Selector(resp.text)
        # 获取tr标签  --- 列表
        trs = selector.css('.layui-table > tbody > tr')
        proxies_list = []
        for tr in trs:
            ip_num = tr.css('td:nth-child(1)::text').get().replace('\n', '').replace('\t', '')
            ip_port = tr.css('td:nth-child(2)::text').get().replace('\n', '').replace('\t', '')
            '''
            IP代理的结构：
            proxies_dict = {
                'http': f'http://{ip}:{端口}',
                'https': f'https://{ip}:{端口}'
            }
            '''
            proxies_dict = {
                'http': f'http://{ip_num}:{ip_port}',
                'https': f'https://{ip_num}:{ip_port}'
            }
            # print(proxies_dict)
            # 检测IP代理是否可用
            try:
                url1 = 'https://www.baidu.com/'
                resp1 = requests.get(url1, proxies_dict, headers=random.choice(self.headers), timeout=1)
                if resp1.status_code == 200:
                    proxies_list.append(proxies_dict)
                    print('代理可用', proxies_dict)
                    self.proxies_q.put(proxies_dict)

            except Exception as e:
                # print(f'不可用，要报错了：{e}')
                print('当前代理', proxies_dict, f'请求超时{e}')

        print(f'获取到可用代理数量{len(proxies_list)}')
        print(proxies_list)


class IpsConsumer(threading.Thread):
    def __init__(self, proxies_q):
        super().__init__()
        self.proxies_q = proxies_q

    def saveData(self, proxies_dict):
        with open('89代理.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(proxies_dict))
            # f.write(proxies_dict)
            f.write(',\n')
            f.close()

    def run(self):
        while True:
            if self.proxies_q.empty():
                break
            proxies = self.proxies_q.get()
            self.saveData(proxies)
        print('over!')


if __name__ == '__main__':
    ti1 = time.time()

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    proxies_queue = Queue()
    for i in range(1, 7):
        page_url = f'https://www.89ip.cn/index_{i}.html'
        page_queue.put(page_url)

    p_lst = []
    # 创建5个生产者
    for i in range(5):
        t1 = IpsProducer(page_queue, proxies_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(5):
        t2 = IpsConsumer(proxies_queue)
        t2.start()

    ti2 = time.time()
    print(round(ti2 - ti1))
