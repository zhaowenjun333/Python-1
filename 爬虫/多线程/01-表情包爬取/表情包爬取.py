# https://www.fabiaoqing.com/biaoqing/lists/page/1.html

import time
import requests
from lxml import etree
from queue import Queue
import threading


class BiaoQingBaoSpider:
    def __init__(self):
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
        lst = []
        for div in divs:
            img = []
            title = div.xpath('.//a/@title')[0]
            data_original = div.xpath('.//a/img/@data-original')[0]
            img.append(title)
            img.append(data_original)
            lst.append(img)
        return lst

    # 传入img
    def set_Gif(self, q, lst):
        for i in lst:
            q.put(i)

    # 得到img
    def get_Gif(self, q):
        while True:
            img = q.get()
            # print(img)
            th3 = threading.Thread(target=self.downloadGif, args=(img, ))
            th3.start()
            if q.empty():
                break

    # 下载表情包
    def downloadGif(self, img):
        resp = requests.get(img[1], headers=self.headers)
        time.sleep(0.01)
        with open(f'./Gif/{img[1].split("/")[-1]}', 'wb') as f:
            f.write(resp.content)     # 将图片写入文件
            f.close()
            print(f'{img[0]}下载完毕')

    def main(self):
        q = Queue(45)
        for i in range(1, 11):
            url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{i}.html'
            html = self.readHtml(url)
            time.sleep(0.02)
            lst = self.parseHtml(html)
            # print(len(lst))
            th1 = threading.Thread(target=self.set_Gif, args=(q, lst))
            th2 = threading.Thread(target=self.get_Gif, args=(q, ))
            th1.start()
            th2.start()
            # print(lst)
        t2 = time.time()
        print(f'结束时间：{t2-t1}')


if __name__ == '__main__':
    t1 = time.time()
    bqb = BiaoQingBaoSpider()
    bqb.main()
