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
from queue import Queue
import csv


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
        buildings = resp.json()['data']['body']['_resblock_list']
        resp.close()
        # print(buildings)
        for building in buildings:
            #
            if building['show_price_info'] == '价格待定':
                price = building['show_price_info']
            else:
                if building['reference_total_price_range']['price'] != '0':
                    price = f"{building['reference_total_price_range']['price']}万/套"
                else:
                    price = f"{building['reference_avg_price']}元/㎡"
            developer_company = building['developer_company'][0]
            if developer_company == '':
                developer_company = '未知开发商'
            item = {
                '楼盘名称': building['title'],
                '开发商名称': developer_company,
                '是否售空': building['sale_status'],
                '销售单价': price,
                '楼盘性质': building['house_type'],
            }
            # print(item.txt)
            self.info_q.put(item)

class BeiKeConsumer(threading.Thread):
    def __init__(self, info_q):
        super().__init__()
        self.info_q = info_q
        # self.f = open('./CSV/贝壳找房_杭州.csv', 'w+', encoding='utf-8-sig', newline='')
        # self.writer = csv.writer(self.f)
        # self.headers = ('楼盘名称', '开发商名称', '是否售空', '销售单价', '楼盘性质')
        # self.writer.writerow(self.headers)

    def saveData1(self, lst):
        headers = ('楼盘名称', '开发商名称', '是否售空', '销售单价', '楼盘性质')
        with open('./CSV/贝壳找房_杭州.csv', 'w', encoding='utf-8-sig', newline='') as f:
            csvwriter = csv.DictWriter(f, headers)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            f.close()
            print('保存完毕')
        # f.close()

    def run(self):
        lst = []
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            lst.append(info)
        # print(lst)
        self.saveData1(lst)


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    for i in range(1, 97):
        page_url = f'https://m.ke.com/hz/loupan/pg{i}/?_t=1&source=list'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = BeiKeProducer(page_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(1):
        t2 = BeiKeConsumer(info_queue)
        t2.start()
    ti2 = time.time()
    print(f'用时：{ti2-ti1}')
