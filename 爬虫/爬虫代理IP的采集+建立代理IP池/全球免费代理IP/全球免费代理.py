
# 网址：https://ip.jiangxianli.com/?page=1
import csv

import requests
import parsel
import random
import time
import json


class Ips:

    def __init__(self, ur, headers):
        self.url = ur
        self.headers = headers

    def readHtml(self, ur):
        resp = requests.get(ur, headers=self.headers)
        resp.encoding = 'utf-8'
        html = resp.text
        resp.close()
        return html

    def parseHtml(self, html):
        selector = parsel.Selector(html)
        trs = selector.xpath('//table[@class="layui-table"]/tbody/tr')
        proxies_list = []
        for tr in trs:
            if tr.xpath('.//td[1][@colspan="11"]'):
                continue
            ip_num = tr.xpath('.//td[1]/text()').get()
            ip_port = tr.xpath('.//td[2]/text()').get()
            proxies_dict = {
                'http': f'http://{ip_num}:{ip_port}',
                'https': f'https://{ip_num}:{ip_port}'
            }
            try:
                url1 = 'https://hz.fang.ke.com/loupan/pg1/'
                resp1 = requests.get(url1, proxies_dict, headers=self.headers)
                if resp1.status_code == 200:
                    # print(resp1.text)
                    proxies_list.append(proxies_dict)
                    print('代理可用', proxies_dict)
            except Exception as e:
                print('当前代理', proxies_dict, f'请求超时\n{e}')
        return proxies_list

    def saveData(self, proxies_list):
        with open('./全球免费代理.csv', 'w', encoding="utf-8", newline='') as f:
            headers = ('http', 'https')
            csvwriter = csv.DictWriter(f, headers)
            csvwriter.writeheader()
            csvwriter.writerows(proxies_list)
            f.close()

    def main(self):
        html = self.readHtml(self.url)
        proxies_list = self.parseHtml(html)
        print(proxies_list)
        # self.saveData(proxies_list)


if __name__ == '__main__':
    url = 'https://ip.jiangxianli.com/?page=1'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    ips = Ips(url, header)
    ips.main()
