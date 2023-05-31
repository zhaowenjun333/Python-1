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
        self.num = 14
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
        # self.cookies = 'Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1684551635,1684663154,1684666176,1684728847; qpfccr=true; no-alert3=true; tk=-4343004847358857667; sessionid=zp5povkg0nb7gggcpzy4glykojwj1ar1; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1684553246,1684663161,1684666182,1684728857; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1684728993; mz=TW96aWxsYSxOZXRzY2FwZSw1LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMy4wLjAuMCBTYWZhcmkvNTM3LjM2LFtvYmplY3QgTmV0d29ya0luZm9ybWF0aW9uXSx0cnVlLCxbb2JqZWN0IEdlb2xvY2F0aW9uXSw4LHpoLUNOLHpoLUNOLHpoLDAsW29iamVjdCBNZWRpYUNhcGFiaWxpdGllc10sW29iamVjdCBNZWRpYVNlc3Npb25dLFtvYmplY3QgTWltZVR5cGVBcnJheV0sdHJ1ZSxbb2JqZWN0IFBlcm1pc3Npb25zXSxXaW4zMixbb2JqZWN0IFBsdWdpbkFycmF5XSxHZWNrbywyMDAzMDEwNyxbb2JqZWN0IFVzZXJBY3RpdmF0aW9uXSxNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTEzLjAuMC4wIFNhZmFyaS81MzcuMzYsR29vZ2xlIEluYy4sLFtvYmplY3QgRGVwcmVjYXRlZFN0b3JhZ2VRdW90YV0sW29iamVjdCBEZXByZWNhdGVkU3RvcmFnZVF1b3RhXSw4MjQsMCwwLDE1MzYsMjQsODY0LFtvYmplY3QgU2NyZWVuT3JpZW50YXRpb25dLDI0LDE1MzYsW29iamVjdCBET01TdHJpbmdMaXN0XSxmdW5jdGlvbiBhc3NpZ24oKSB7IFtuYXRpdmUgY29kZV0gfSwsbWF0Y2gueXVhbnJlbnh1ZS5jbixtYXRjaC55dWFucmVueHVlLmNuLGh0dHBzOi8vbWF0Y2gueXVhbnJlbnh1ZS5jbi9tYXRjaC8xNCxodHRwczovL21hdGNoLnl1YW5yZW54dWUuY24sL21hdGNoLzE0LCxodHRwczosZnVuY3Rpb24gcmVsb2FkKCkgeyBbbmF0aXZlIGNvZGVdIH0sZnVuY3Rpb24gcmVwbGFjZSgpIHsgW25hdGl2ZSBjb2RlXSB9LCxmdW5jdGlvbiB0b1N0cmluZygpIHsgW25hdGl2ZSBjb2RlXSB9LGZ1bmN0aW9uIHZhbHVlT2YoKSB7IFtuYXRpdmUgY29kZV0gfQ==; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1684736708; m=40806d2bfca80822b57acfb0afae62a7|1684736712000|13477893696000|2'

        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.cookies = {
            'sessionid': 'zp5povkg0nb7gggcpzy4glykojwj1ar1',
            'mz': 'TW96aWxsYSxOZXRzY2FwZSw1LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMy4wLjAuMCBTYWZhcmkvNTM3LjM2LFtvYmplY3QgTmV0d29ya0luZm9ybWF0aW9uXSx0cnVlLCxbb2JqZWN0IEdlb2xvY2F0aW9uXSw4LHpoLUNOLHpoLUNOLHpoLDAsW29iamVjdCBNZWRpYUNhcGFiaWxpdGllc10sW29iamVjdCBNZWRpYVNlc3Npb25dLFtvYmplY3QgTWltZVR5cGVBcnJheV0sdHJ1ZSxbb2JqZWN0IFBlcm1pc3Npb25zXSxXaW4zMixbb2JqZWN0IFBsdWdpbkFycmF5XSxHZWNrbywyMDAzMDEwNyxbb2JqZWN0IFVzZXJBY3RpdmF0aW9uXSxNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTEzLjAuMC4wIFNhZmFyaS81MzcuMzYsR29vZ2xlIEluYy4sLFtvYmplY3QgRGVwcmVjYXRlZFN0b3JhZ2VRdW90YV0sW29iamVjdCBEZXByZWNhdGVkU3RvcmFnZVF1b3RhXSw4MjQsMCwwLDE1MzYsMjQsODY0LFtvYmplY3QgU2NyZWVuT3JpZW50YXRpb25dLDI0LDE1MzYsW29iamVjdCBET01TdHJpbmdMaXN0XSxmdW5jdGlvbiBhc3NpZ24oKSB7IFtuYXRpdmUgY29kZV0gfSwsbWF0Y2gueXVhbnJlbnh1ZS5jbixtYXRjaC55dWFucmVueHVlLmNuLGh0dHBzOi8vbWF0Y2gueXVhbnJlbnh1ZS5jbi9tYXRjaC8xNCxodHRwczovL21hdGNoLnl1YW5yZW54dWUuY24sL21hdGNoLzE0LCxodHRwczosZnVuY3Rpb24gcmVsb2FkKCkgeyBbbmF0aXZlIGNvZGVdIH0sZnVuY3Rpb24gcmVwbGFjZSgpIHsgW25hdGl2ZSBjb2RlXSB9LCxmdW5jdGlvbiB0b1N0cmluZygpIHsgW25hdGl2ZSBjb2RlXSB9LGZ1bmN0aW9uIHZhbHVlT2YoKSB7IFtuYXRpdmUgY29kZV0gfQ=='
        }
        self.session.cookies.update(self.cookies)
        self.chart_set = 'utf-8'

        self.js_filename = f'JS/m{self.num}.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_code = self.js_f.read()
        self.js_f.close()
        self.lst = []

    def response_m(self):
        resp = self.session.get(self.m_url)
        js_text = resp.text
        set_interval = re.search('(setInterval\(function.*?,0xfa0\);)', js_text).group(1)
        new_js = js_text.replace(set_interval, '')
        x_func = re.findall(r';(\$_.*?\(\);)', js_text)
        x_func_lst = [i for i in x_func if len(i) == 13]
        for x in x_func_lst:
            new_js = new_js.replace(x, '')

        new_js = 'window={};' + new_js + ';function get_v(){return window}'

        window = execjs.compile(new_js).call('get_v')
        return window['v14'], window['v142']

    def deal_sum(self, page):
        v14, v142 = self.response_m()
        new_js = f'window=global;window.v14="{v14}";window.v142="{v142}"' + self.js_code
        m = execjs.compile(new_js).call('get_m', page)
        self.session.cookies.update({'m': m})
        if page > 3:
            self.headers['User-Agent'] = 'yuanrenxue.project'
            self.session.headers.update(self.headers)
        resp = self.session.get(f'{self.api_url}?page={page}')
        content = resp.json()
        print(content)
        if content:
            datas = content['data']
            self.lst.append(sum([data['value'] for data in datas]))
        else:
            self.deal_sum(page)

    def test(self):
        for page in range(1, 3):

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
