import requests
import execjs
import timeit

import urllib3
urllib3.disable_warnings()

class JJEncodeSpider:
    def __init__(self):
        self.url = 'https://www.wangluozhe.com/challenge/2'
        self.api_url = 'https://www.wangluozhe.com/challenge/api/2'
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
            'session': 'c094ae59-d1ad-4dc7-9262-0b0dcdfd24a3.o3KaxQr4I-e2gVXLO8nalqkXZLU'
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        for k, v in self.cookies.items():
            self.session.cookies.set(k, v)
        self.chart_set = 'utf-8'

        self.js_filename = 'JS/w2.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_compile = execjs.compile(self.js_f.read())
        self.js_f.close()

    def run(self):
        num = 0
        for page in range(1, 101):
            _signature = self.js_compile.call('_signature')
            datas = {
                'page': page,
                'count': '10',
                '_signature': _signature,
            }
            resp = self.session.post(self.api_url, data=datas, verify=False)
            content = resp.json()
            num += sum([i['value'] for i in content['data']])
        # 5186861
        print(num)


if __name__ == '__main__':
    jjencode = JJEncodeSpider()
    # jjencode.run()
    t = timeit.timeit(stmt=jjencode.run, number=1)
    print(t)
