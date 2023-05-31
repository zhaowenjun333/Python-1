import re

import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import timeit
import httpx

urllib3.disable_warnings()

class MoneySpider:
    def __init__(self):
        self.num = 17
        self.url = f'https://match.yuanrenxue.cn/match/{self.num}'
        self.m_url = 'https://match.yuanrenxue.cn/api/match/14/m'
        self.api_url = f'https://match.yuanrenxue.cn/api/match/{self.num}'
        self.headers = {
            'Referer': self.url,
            'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.cookies = {
            'sessionid': '9xg0l1sjbrls4cvcnepo6hq1pfo062qc'
        }
        self.client = httpx.Client(http2=True)

        self.chart_set = 'utf-8'

        self.lst = []

    def deal_sum(self, page):
        if page > 3:
            self.headers['User-Agent'] = 'yuanrenxue.project'
        resp = self.client.get(f'{self.api_url}?page={page}', headers=self.headers, cookies=self.cookies)
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
