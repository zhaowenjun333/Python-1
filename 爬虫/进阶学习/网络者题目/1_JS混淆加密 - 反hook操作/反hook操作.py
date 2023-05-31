import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import timeit
urllib3.disable_warnings()

class FanHookSpider:
    def __init__(self):
        self.num = 1
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
        self.cookies = 'session=dde1ca0a-8fa7-41bb-a9be-a2863f9b5ff0.DxPeKOXydIfziqsHq7w8QjLOALg; __51cke__=; __tins__21539413=%7B%22sid%22%3A%201684602617414%2C%20%22vd%22%3A%208%2C%20%22expires%22%3A%201684604983743%7D; __51laig__=8'

        self.session = requests.session()
        self.session.headers.update(self.headers)
        for i in self.cookies.split(';'):
            item = i.split('=')
            self.session.cookies.set(item[0], item[1])
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
        # print(content)
        if content:
            print(content['data'])
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
    fan_hook = FanHookSpider()
    # fan_hook.run()
    t = timeit.timeit(stmt=fan_hook.run, number=1)
    print(t)
