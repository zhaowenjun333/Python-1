# 6.(必做题1)目标网站：https://www.1ppt.com/moban/
# 需求：
# 1、用多线程爬取前10页模板名字和模板下载链接
# 2、把模板名字和模板下载链接保存到模板.csv文件里面
import threading
import time
import requests
from lxml import etree
from queue import Queue
import urllib.request
import csv


class PPTProducer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    def __init__(self, page_q, ppt_q):
        super().__init__()
        self.page_q = page_q
        self.ppt_q = ppt_q

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            # print(url)
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'gb2312'
        html = resp.text
        resp.close()
        html_element = etree.HTML(html)
        lis = html_element.xpath('//ul[@class="tplist"]/li')
        for li in lis:
            ppt = []
            title = f"{li.xpath('.//h2/a/text()')[0]}.zip"
            href = f"https://www.1ppt.com/{li.xpath('.//h2/a/@href')[0]}"
            download_url = self.DownLoadUrl(href)
            ppt.append(title)
            ppt.append(download_url)
            self.ppt_q.put(ppt)
            # print(ppt)
            print(self.ppt_q.qsize())

    def DownLoadUrl(self, url):
        resp1 = requests.get(url, headers=self.headers)
        resp1.encoding = 'gb2312'
        html1 = resp1.text
        resp1.close()
        html1_element = etree.HTML(html1)
        open_url = f'''https://www.1ppt.com/{html1_element.xpath('//ul[@class="downurllist"]/li/a/@href')[0]}'''
        # print(open_url)
        resp2 = requests.get(open_url, headers=self.headers)
        resp2.encoding = 'gb2312'
        html2 = resp2.text
        resp2.close()
        html2_element = etree.HTML(html2)
        download_url = html2_element.xpath('//ul[@class="downloadlist"]/li[1]/a/@href')[0]
        return download_url


class PPTConsumer(threading.Thread):
    def __init__(self, ppt_q):
        super().__init__()
        self.ppt_q = ppt_q

    def saveData(self, lst):
        header = ('模板名字', '模板链接')
        with open(f'./csv/PPT模板.csv', 'w', encoding='utf-8', newline='') as f:
            csvwriter = csv.DictWriter(f, header)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            f.close()
            print('保存完毕')

    def run(self):
        lst = []
        while True:
            if self.ppt_q.empty():
                break
            item = {}
            ppt = self.ppt_q.get()
            url = ppt[1]
            filename = ppt[0]
            item['模板名字'] = filename.strip('.zip')
            item['模板链接'] = url
            lst.append(item)
            urllib.request.urlretrieve(url, f'./Data/ppt/{filename}')
            print(f'{filename} ------- 下载完毕')
        print(lst)
        self.saveData(lst)


if __name__ == '__main__':
    t1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    ppt_queue = Queue()
    for i in range(1, 11):
        if i == 1:
            page_url = 'https://www.1ppt.com/moban/'
        else:
            page_url = f'https://www.1ppt.com/moban/ppt_moban_{i}.html'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(5):
        t1 = PPTProducer(page_queue, ppt_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(5):
        t2 = PPTConsumer(ppt_queue)
        t2.start()
