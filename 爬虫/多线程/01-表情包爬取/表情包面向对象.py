import time
import requests
from lxml import etree
from queue import Queue
import threading
import urllib.request


class GifProducer(threading.Thread):
    def __init__(self, page_q, img_q):
        super().__init__()
        self.page_q = page_q
        self.img_q = img_q
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }

    def readHtml(self, url):
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf-8'
        html = resp.text
        resp.close()
        return html

    def parseHtml(self, html):
        html_element = etree.HTML(html)
        divs = html_element.xpath('//div[@class="ui segment imghover"]/div[@class="tagbqppdiv"]')
        for div in divs:
            img = []
            title = div.xpath('.//a/@title')[0]
            data_original = div.xpath('.//a/img/@data-original')[0]
            img.append(title)
            img.append(data_original)
            print(img)
            self.img_q.put(img)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            html = self.readHtml(url)
            self.parseHtml(html)


class GifConsumer(threading.Thread):
    def __init__(self, img_q):
        super().__init__()
        self.img_q = img_q

    def run(self):
        while True:
            if self.img_q.empty():
                break
            img = self.img_q.get()
            img_url = img[1]
            img_title = img[0]
            urllib.request.urlretrieve(img_url, f'./Gif/{img_url.split("/")[-1]}')
            print(f'{img_title}---下载完毕')


if __name__ == '__main__':
    page_queue = Queue(11)
    img_queue = Queue()
    for i in range(1, 11):
        page_url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{i}.html'
        page_queue.put(page_url)
    pt = GifProducer(page_queue, img_queue)
    ct = GifConsumer(img_queue)
    pt.start()
    time.sleep(2.5)
    ct.start()
