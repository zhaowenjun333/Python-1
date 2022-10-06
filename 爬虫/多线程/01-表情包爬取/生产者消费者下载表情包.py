import random
import time
import requests
from lxml import etree
from queue import Queue
import threading
import urllib.request
import re


class GifProducer(threading.Thread):
    def __init__(self, pq, iq):
        super().__init__()
        self.pq = pq
        self.iq = iq
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }

    def run(self):
        while True:
            if self.pq.empty():
                break
            url = self.pq.get()
            # 解析数据
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, headers=self.headers)
        time.sleep(1)
        resp.encoding = 'utf-8'
        html = resp.text
        resp.close()
        html_element = etree.HTML(html)
        divs = html_element.xpath('//div[@class="ui segment imghover"]/div[@class="tagbqppdiv"]')
        for div in divs:
            img = []
            title = div.xpath('.//a/@title')[0]
            title = re.sub(r'[，。？?/\\<>:]', '', title)
            data_original = div.xpath('.//a/img/@data-original')[0]
            title = title + '.' + data_original.split('.')[-1]
            img.append(title)
            img.append(data_original)
            self.iq.put(img)
            print(img)
            # print(self.iq.qsize())


class GifConsumer(threading.Thread):
    def __init__(self, iq):
        super().__init__()
        self.iq = iq

    def run(self):
        while True:
            if self.iq.empty():
                break
            img_data = self.iq.get()
            # print(img_data)
            url = img_data[1]
            filename = img_data[0]
            # print(f'{filename}')
            urllib.request.urlretrieve(url, f'./Img/{filename}')
            print(f'{filename} ---- 下载完毕')


if __name__ == '__main__':
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    img_queue = Queue()
    for i in range(1, 11):
        page_url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{i}.html'
        page_queue.put(page_url)

    p_lst = []
    # 创建三个生产者
    for i in range(3):
        t1 = GifProducer(page_queue, img_queue)
        t1.start()   # 会执行run方法
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建三个消费者
    for j in range(3):
        t2 = GifConsumer(img_queue)
        t2.start()
