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
        self.api_url = f'https://spa2.scrape.center/api/movie/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
        self.JS_dir = 'JS'
        self.JS_dir_path = self.base_dir + '/' + self.JS_dir
        if not os.path.exists(self.JS_dir_path):
            os.mkdir(self.JS_dir_path)
        self.js_filename = f'{self.JS_dir_path}/test.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_code = self.js_f.read()
        self.js_code_compile = execjs.compile(self.js_code)
        self.js_f.close()
        self.lst = []

    def get_token(self):
        token = self.js_code_compile.call('get_token')
        return token

    def deal_sum(self, page):
        n = (page-1)*10
        token = self.get_token()
        params = {
            'limit': '10',
            'offset': n,
            'token': token
        }
        print(params)

        resp = self.session.get(self.api_url, params=params, verify=False)
        content = resp.text
        print(content)
        # if content:
        #     datas = content['data']
        #     self.lst.append(sum([data['value'] for data in datas]))
        # else:
        #     self.deal_sum(params)

    def run(self):
        # 创建10的线程池
        with ProcessPoolExecutor(6) as p:
            for page in range(1, 2):
                # 把下载任务提交给线程池
                p.submit(self.deal_sum(page))


if __name__ == '__main__':
    number = NumberSpider()
    # money.run()
    t = timeit.timeit(stmt=number.run, number=1)
    print(t)


