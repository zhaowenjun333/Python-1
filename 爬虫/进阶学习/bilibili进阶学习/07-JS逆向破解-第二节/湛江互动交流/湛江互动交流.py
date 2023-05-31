import re
import time
from queue import Queue
import requests
import csv
import threading
import collections


class ZJProducer(threading.Thread):
    headers = {
        'Host': 'www.zjmazhang.gov.cn',
        'Origin': 'http://www.zjmazhang.gov.cn',
        'Referer': 'http://www.zjmazhang.gov.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q

    def get_url_ck(self):
        cookie_url = 'http://www.zjmazhang.gov.cn/hdjlpt/published?via=pc'
        resp = requests.get(cookie_url, self.headers)

        # 动态获取 szxx_session
        cookies = resp.cookies
        szxx_session = cookies['szxx_session']
        # print(szxx_session)

        # 网页原码获取 szxx_session
        html = resp.text
        X_CSRF_TOKEN = re.match(r".*?var _CSRF = '(?P<X_CSRF_TOKEN>.*?)';", html, re.S).group('X_CSRF_TOKEN')
        # print(X_CSRF_TOKEN)
        return szxx_session, X_CSRF_TOKEN

    def get_js_ck(self):
        pass

    def get_headers(self):
        new_headers = self.headers
        szxx_session, X_CSRF_TOKEN = self.get_url_ck()
        new_headers['Cookie'] = f'szxx_session={szxx_session};'
        new_headers['X-CSRF-TOKEN'] = X_CSRF_TOKEN
        return new_headers

    def parse_json(self, data1):
        url = 'http://www.zjmazhang.gov.cn/hdjlpt/letter/pubList'
        headers = self.get_headers()
        resp = requests.post(url, headers=headers, data=data1)
        # print(resp.json())
        data_list = resp.json()['data']['list']
        for li in data_list:
            item = collections.OrderedDict()
            for head in header:
                item[head] = li[head]
            # print(item)
            self.info_q.put(item)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            data1 = self.page_q.get()
            # print(data1)
            self.parse_json(data1)


class ZJConsumer(threading.Thread):
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


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    data_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    header = ('handle_code', 'id', 'nickname', 'title', 'org_name', 'summary', 'time')
    for i in range(1, 3):
        data = {
            'offset': f'{(i - 1) * 20}',
            'limit': '20',
            'site_id': '759010',
        }
        data_queue.put(data)

    p_lst = []
    for i in range(2):
        t1 = ZJProducer(data_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    f = open('./data/留言选登.csv', 'w+', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    writer.writerow(header)

    c_lst = []
    # 创建五个消费者
    for j in range(2):
        t2 = ZJConsumer(info_queue, header, writer)
        t2.start()
        c_lst.append(t2)

    for c in c_lst:
        c.join()

    f.close()
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
