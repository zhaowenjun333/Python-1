import re

import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import timeit
urllib3.disable_warnings()

class NumberSpider:
    def __init__(self):
        self.num = 9
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
            'sessionid': 'zbvtcqso3elgrmt3kceycm1l9iuwns64'
        }

        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.js_filename = f'./JS/m{self.num}.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_code = self.js_f.read()
        self.js_f.close()
        self.lst = []

    def get_cookie(self):
        resp = self.session.get(self.url)
        js_text = resp.text
        # print(js_text)
        m9 = re.search(r'for\(var m=0x1;.*?\(m,(.*?)\);', js_text, re.S).group(1)
        tm = re.search(r"res=.*?decrypt.*?'(\d*?)'.*?'\\x72'", js_text, re.S).group(1)
        cookie_m = execjs.compile(self.js_code).call('get_cookie', m9, tm)
        self.session.cookies.set('m', cookie_m)

    def deal_sum(self, params):
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
        self.get_cookie()
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
