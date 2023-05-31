import csv
import json
import time
from queue import Queue
import threading
import requests
import execjs
import os

# start_url = 'https://www.qimingpian.com/finosda/project/pinvestment'


class QMProducer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Host': 'vipapi.qimingpian.cn',
        'Origin': 'https://www.qimingpian.com'
    }

    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q

    def encrypt_parse(self, encrypt_data):
        with open('./JS文件/企名科技.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
            # 编译js代码
            compile_result = execjs.compile(js_code)
            decrypt_data = compile_result.call('my_encrypt', encrypt_data)
            # print(decrypt_data)
            json_list = json.loads(decrypt_data)
            return json_list['list']

    def handle_data(self, li):
        item = {
            '项目': li['product'],
            '行业领域': li['hangye1'],
            '业务': li['yewu'],
            '地区': li['province'],
            '投资轮次': li['lunci'],
            '投资金额': li['money'],
            '投资时间': li['time']
        }
        return item

    def parse_json(self, data1):
        url = 'https://vipapi.qimingpian.cn/DataList/productListVip'
        resp = requests.post(url, headers=self.headers, data=data1)
        encrypt_data = resp.json()['encrypt_data']
        json_list = self.encrypt_parse(encrypt_data)
        for li in json_list:
            content = self.handle_data(li)
            print(content)
            self.info_q.put(content)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            data1 = self.page_q.get()
            # print(data1)
            self.parse_json(data1)


class QMConsumer(threading.Thread):
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

    for i in range(1, 3):
        data = {
            'page': f'{i}',
            'num': '20',
            'unionid': '4AW0kxXbQcAcyzkmezd+PHBUkcaNFDj9hZ2cHSVcpxyuUMCUwSVj5cnoQAFInc7aeJWqqIs6kiQsM8IbOYgM5A=='
        }
        data_queue.put(data)

    p_lst = []
    for i in range(15):
        t1 = QMProducer(data_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    dirName = 'Data'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    f = open(f'./{dirName}/productListVIP.csv', 'w+', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    header = ('项目', '行业领域', '业务', '地区', '投资轮次', '投资金额', '投资时间')
    writer.writerow(header)

    c_lst = []
    # 创建五个消费者
    for j in range(15):
        t2 = QMConsumer(info_queue, header, writer)
        t2.start()
        c_lst.append(t2)

    for c in c_lst:
        c.join()

    f.close()
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
