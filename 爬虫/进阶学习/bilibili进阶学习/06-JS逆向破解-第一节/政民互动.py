import csv
import time
from queue import Queue
import requests
import threading
import collections


class SHProducer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q

    def get_headers(self):
        t = f'{time.time()}'.split('.')[0]
        new_headers = {}
        cookie = '_pk_testcookie.55.542e=1; ' \
                 f'_pk_id.52.542e=69503bc83678fcf1.1668010601.0.{t}..; ' \
                 '_pk_ref.55.542e=%5B%22%22%2C%22%22%2C1668099951%2C%22https%3A%2F%2Fwww.shanghai.gov.cn%2F%22%5D; ' \
                 '_pk_id.55.542e=1c68aec97eb2a354.1668010601.3.1668099951.1668099951.; ' \
                 '_pk_ses.55.542e=1'
        new_headers['User-Agent'] = self.headers['User-Agent']
        new_headers['Cookie'] = cookie
        return new_headers

    def parse_json(self, data1):
        url = 'https://hd.sh.gov.cn/front/collect/collectOnline/findPage'
        headers = self.get_headers()
        resp = requests.post(url, headers=headers, data=data1)
        records = resp.json()['data']['records']
        for record in records:
            item = collections.OrderedDict()
            item['id'] = record['id']
            item['title'] = record['title']
            item['ongoingStatus'] = record['ongoingStatus']
            item['createDate'] = record['createDate']
            item['endDate'] = record['endDate']
            # print(item)
            self.info_q.put(item)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            data1 = self.page_q.get()
            # print(data1)
            self.parse_json(data1)


class SHConsumer(threading.Thread):
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
            print(info)
            self.saveData(info)


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    data_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    for i in range(1, 9):
        data = {
            'pageNo': f'{i}',
            'pageSize': '10',
            'activityType': 'COLLECT',
            'ongoingStatus': 'FINISHED',
            'displayInShangHai': '1'
        }
        data_queue.put(data)

    p_lst = []
    for i in range(5):
        t1 = SHProducer(data_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    f = open('./data/activities.csv', 'w+', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    header = ('id', 'title', 'ongoingStatus', 'createDate', 'createDate', 'endDate')
    writer.writerow(header)

    c_lst = []
    # 创建五个消费者
    for j in range(15):
        t2 = SHConsumer(info_queue, header, writer)
        t2.start()
        c_lst.append(t2)

    for c in c_lst:
        c.join()

    f.close()
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')

