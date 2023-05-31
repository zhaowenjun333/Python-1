import requests
# 导入线程池
from concurrent.futures import ProcessPoolExecutor
import execjs
import urllib3
import timeit
urllib3.disable_warnings()

class MoneySpider:
    def __init__(self):
        self.num = 6
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
        self.cookies = 'Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1684192866,1684317806,1684472524,1684551635; Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1684551656; no-alert3=true; tk=-5804823927319330515; sessionid=eu89incbiot05ej8trr5oin9tykbt9zt; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1684192871,1684317862,1684472531,1684553246; Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3=1684561359; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1684567286; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1684570823'

        self.session = requests.session()
        self.session.headers.update(self.headers)
        for i in self.cookies.split(';'):
            item = i.split('=')
            self.session.cookies.set(item[0], item[1])
        self.chart_set = 'utf-8'

        self.js_filename = f'JS/m{self.num}.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_compile = execjs.compile(self.js_f.read())
        self.js_f.close()
        self.lst = []

    def deal_sum(self, params):
        js_result = self.js_compile.call('get_params')
        params['m'] = js_result[0]
        params['q'] = js_result[1]
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
        total = sum(self.lst) * 24
        print(total)


if __name__ == '__main__':
    money = MoneySpider()
    # money.run()
    t = timeit.timeit(stmt=money.run, number=1)
    print(t)
