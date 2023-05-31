# https://match.yuanrenxue.cn/match/13
import re

import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import timeit
urllib3.disable_warnings()

class MoneySpider:
    def __init__(self):
        self.num = 13
        self.url = f'https://match.yuanrenxue.cn/match/{self.num}'
        self.api_url = f'https://match.yuanrenxue.cn/api/match/{self.num}'
        self.headers = {
            'User-Agent': 'yuanrenxue.project',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.cookies = {
            'sessionid': 'bqbq8yk2qsmvhuh8d0jawu5skrvr0cz0'
        }

        self.session = requests.session()
        self.session.headers = self.headers
        self.session.cookies.update(self.cookies)
        self.chart_set = 'utf-8'

        # self.js_filename = f'JS/m{self.num}.js'
        # self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        # self.js_compile = execjs.compile(self.js_f.read())
        # self.js_f.close()
        self.lst = []

    def deal_sum(self, page):
        if page > 3:
            self.headers['User-Agent'] = 'yuanrenxue.project'
            self.session.headers.update(self.headers)
            self.cookies['sessionid'] = 'bqbq8yk2qsmvhuh8d0jawu5skrvr0cz0'
            self.session.cookies.update(self.cookies)
        resp = self.session.get(f'{self.api_url}?page={page}')
        content = resp.json()
        print(content)
        if content:
            datas = content['data']
            self.lst.append(sum([data['value'] for data in datas]))
        else:
            self.deal_sum(page)

    def run(self):
        first_resp = self.session.get(self.url)
        js_text = first_resp.text
        # print(js_text)
        js_code = 'function get_cookie() {return' + re.search(r"<script>document\.cookie=(.*?)\+';path=/'", js_text,
                                                              re.S).group(1) + '}'
        yuanrenxue_cookie, value = execjs.compile(js_code).call('get_cookie').split('=')

        self.session.cookies.update({yuanrenxue_cookie: value})
        print(self.session.cookies.get_dict())
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
    print(t)
