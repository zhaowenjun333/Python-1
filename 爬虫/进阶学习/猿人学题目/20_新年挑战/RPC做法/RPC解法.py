import hashlib
import json
import re

import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import pywasm
import timeit
import time
import os
import sys
from hashlib import md5
urllib3.disable_warnings()

class NumberSpider:
    def __init__(self):
        self.num = 20
        self.url = f'https://match.yuanrenxue.cn/match/{self.num}'
        self.api_url = f'https://match.yuanrenxue.cn/api/match/{self.num}'
        self.rpc_url = 'http://127.0.0.1:5620/business-demo/invoke?group=ws-group&action=y20'
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
            'tk': '-3381690536614391216',
            'sessionid': 'wxlhpg9zv44lji9p2drmxdnyujpmn367',
            'm': '982382b08ce0711a406445f406fc6199',
            'RM4hZBv0dDon443M': '+ADF4136Dfa5KSX8SwsV+SHf9KdYIlWlZD3xkpOhZMvQyRhiXJZiwlZnT3EyjrrwJxMqdANUVpZvZ3W1V7zJw6I2okeW9zRKTqsqzPQ9/w8niNKJsRuIhhcHd4FGAhqCpzfukrBe222fCodoYuqdhXdlu/UV8YBwZuuLPFWSjlY8AvySEzW5575sILTTCmqsrJLGgsxrEDpseesJBKhu0vpgUMYMD1DZgtshPjQAxqI='
        }

        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)
        self.chart_set = 'utf-8'

        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
        self.lst = []

    def get_params(self, page):
        resp = self.session.get(f'{self.rpc_url}&page={page}')
        result = resp.text
        result = json.loads(result)
        resp.close()
        return result

    def deal_sum(self, page):
        result = self.get_params(page)
        params = {
            'page': page,
            'sign': result['sign'],
            't': result['t']
        }
        if page > 3:
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
    number = NumberSpider()
    # money.run()
    t = timeit.timeit(stmt=number.run, number=1)
    print(t)


