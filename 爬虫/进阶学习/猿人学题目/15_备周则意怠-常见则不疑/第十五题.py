import re

import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import pywasm
import timeit
import os
import sys
urllib3.disable_warnings()

class NumberSpider:
    def __init__(self):
        self.num = 15
        self.url = f'https://match.yuanrenxue.cn/match/{self.num}'
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
            'sessionid': '6hwfdyy99f2nv1o7s9wulaok1cvuuca2',
        }

        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)
        self.chart_set = 'utf-8'

        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
        self.JS_dir = 'JS'
        self.JS_dir_path = self.base_dir + '/' + self.JS_dir
        if not os.path.exists(self.JS_dir_path):
            os.mkdir(self.JS_dir_path)
        self.js_filename = f'{self.JS_dir_path}/m{self.num}.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_code = self.js_f.read()
        self.js_f.close()
        self.lst = []

    def get_m(self):
        t1, t2 = execjs.compile(self.js_code).call('t')
        func = pywasm.load(f'{self.JS_dir_path}/main.wasm')
        m = f'{func.exec("encode", [t1, t2])}|{t1}|{t2}'
        return m

    def deal_sum(self, params):
        m = self.get_m()
        params['m'] = m
        if params['page'] > 3:
            self.headers['User-Agent'] = 'yuanrenxue.project'
            self.session.headers.update(self.headers)

        resp = self.session.get(self.api_url, params=params)
        content = resp.json()
        print(content)
        if content:
            datas = content['data']
            self.lst.append(sum([data['value'] for data in datas]))
        else:
            self.deal_sum(params)

    def run(self):
        # 创建10的线程池
        with ProcessPoolExecutor(6) as p:
            for page in range(1, 6):
                # 把下载任务提交给线程池
                params = {
                    'page': page,
                }
                p.submit(self.deal_sum(params))
        total = sum(self.lst)
        print(total)


if __name__ == '__main__':
    number = NumberSpider()
    # money.run()
    t = timeit.timeit(stmt=number.run, number=1)
    print(t)


