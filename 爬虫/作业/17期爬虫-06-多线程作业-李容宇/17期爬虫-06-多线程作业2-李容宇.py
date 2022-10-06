# 7.(必做题2)目标网站：https://sc.chinaz.com/tupian/
# 需求：
# 1、用多线程爬取前10页图片链接和图片名
# 2、把图片名称和链接保存到图片.csv文件里面
import threading
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
from queue import Queue
import urllib.request
import csv


class ImgProducer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    def __init__(self, page_q, img_q):
        super().__init__()
        self.page_q = page_q
        self.img_q = img_q

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            # print(url)

            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, headers=self.headers)
        time.sleep(1)
        resp.encoding = 'utf-8'
        html = resp.text
        resp.close()
        html_element = etree.HTML(html)
        img_divs = html_element.xpath('//div[@id="container"]/div[@class="box picblock col3"]')
        # print(f'获取{len(img_divs)}')
        for img_div in img_divs:
            img = []
            img_name = img_div.xpath('.//div/a/img/@alt')[0]
            img_url = f"https:{img_div.xpath('.//div/a/img/@src')[0]}"
            img.append(img_name)
            img.append(img_url)
            self.img_q.put(img)
            # print(img)
            print(self.img_q.qsize())


class ImgConsumer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    def __init__(self, img_q):
        super().__init__()
        self.img_q = img_q

    def saveData(self, lst):
        header = ('图片名称', '链接')
        with open(f'./csv/图片.csv', 'w', encoding='utf-8', newline='') as f:
            csvwriter = csv.DictWriter(f, header)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            f.close()
            print('保存完毕')

    def download(self, img):
        resp = requests.get(img[1], headers=self.headers)
        time.sleep(0.1)
        with open(f'./Data/img/{img[0]}.jpg', 'wb') as f:
            f.write(resp.content)
            f.close()
            print(f'{img[0]} ---- 下载完毕')

    def run(self):
        lst = []
        while True:
            if self.img_q.empty():
                break
            item = {}
            img = self.img_q.get()
            img_name = img[0]
            url = img[1]
            item['图片名称'] = img_name
            item['链接'] = url
            lst.append(item)
            # urllib.request.urlretrieve(url, f'./Data/img/{img_name}.jpg')
            self.download(img)
        print(lst)
        self.saveData(lst)


if __name__ == '__main__':
    ti1 = time.time()

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    img_queue = Queue()
    for i in range(1, 11):
        if i == 1:
            page_url = 'https://sc.chinaz.com/tupian/index.html'
        else:
            page_url = f'https://sc.chinaz.com/tupian/index_{i}.html'
        page_queue.put(page_url)

    p1_lst = []
    for i in range(3):
        t1 = ImgProducer(page_queue, img_queue)
        t1.start()
        p1_lst.append(t1)

    # 让生产者线程运行完
    for p in p1_lst:
        p.join()

    p2_lst = []
    # 创建五个消费者
    for j in range(5):
        t2 = ImgConsumer(img_queue)
        t2.start()
        p2_lst.append(t2)

    # 让生产者线程运行完
    for p in p2_lst:
        p.join()
    ti2 = time.time()
    print(ti2-ti1)
