import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import timeit
urllib3.disable_warnings()

class JSFuckSpider:
    def __init__(self):
        self.num = 4
        self.url = f'https://www.wangluozhe.com/challenge/{self.num}'
        self.api_url = f'https://www.wangluozhe.com/challenge/api/{self.num}'
        self.headers = {
            'origin': 'https://www.wangluozhe.com',
            'referer': self.url,
            'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.cookies = {
            'session': 'b0deb7a1-5b26-40b1-9209-73168753bd57.9B1B1KAzxP6KwapAZvF8-9wZ86U'
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        for k, v in self.cookies.items():
            self.session.cookies.set(k, v)
        self.chart_set = 'utf-8'

        self.js_filename = f'JS/w{self.num}.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_compile = execjs.compile(self.js_f.read())
        self.js_f.close()
        self.lst = []

    def deal_sum(self, datas):
        datas['_signature'] = self.js_compile.call('_signature')
        resp = self.session.post(self.api_url, data=datas, verify=False)
        content = resp.json()
        print(content)
        if content:
            self.lst.append(sum([i['value'] for i in content['data']]))
        else:
            self.deal_sum(datas)

    def run(self):
        # 创建10的线程池
        with ProcessPoolExecutor(61) as p:
            for page in range(1, 101):
                # 把下载任务提交给线程池
                datas = {
                    'page': page,
                    'count': '10',
                }
                p.submit(self.deal_sum(datas))
        print(sum(self.lst))


if __name__ == '__main__':
    jsfuck = JSFuckSpider()
    # jjencode.run()
    t = timeit.timeit(stmt=jsfuck.run, number=1)
    print(t)
