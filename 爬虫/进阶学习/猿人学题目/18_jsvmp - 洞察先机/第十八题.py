import random
import re
import time

import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import timeit
urllib3.disable_warnings()

class MoneySpider:
    def __init__(self):
        self.num = 18
        self.url = f'https://match.yuanrenxue.cn/match/{self.num}'
        self.api_url = f'https://match.yuanrenxue.cn/match/{self.num}data'
        self.headers = {
            'Referer': self.url,
            'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.cookies = {
            'sessionid': 'unc3ie3yfizgfv9j8l1483kytviju3wh'
        }
        self.session.cookies.update(self.cookies)
        self.chart_set = 'utf-8'

        self.js_filename = f'JS/m{self.num}.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_code = self.js_f.read()
        self.js_compile = execjs.compile(self.js_code)
        self.js_f.close()
        self.lst = []

    def response_item(self, page):
        item = self.js_compile.call('get_v', page)
        return item

    def deal_sum(self, page):
        item = self.response_item(page)
        params = {
            'page': page,
            't': item[0],
            'v': item[1]
        }
        print(params)
        if page > 2:
            self.headers['User-Agent'] = 'yuanrenxue.project'
            self.session.headers.update(self.headers)
        resp = self.session.get(self.api_url, params=params)
        content = resp.json()
        print(content)
        if content:
            datas = content['data']
            self.lst.append(sum([data['value'] for data in datas]))
        else:
            self.deal_sum(page)

    def run(self):
        # 创建10的线程池
        with ProcessPoolExecutor(6) as p:
            for page in range(1, 6):
                # 把下载任务提交给线程池
                p.submit(self.deal_sum(page))
        total = sum(self.lst)
        print(total)


if __name__ == '__main__':
    money = MoneySpider()
    # money.run()
    t = timeit.timeit(stmt=money.run, number=1)
    # t = timeit.timeit(stmt=money.test, number=1)
    print(t)
