import re

import requests
import execjs


class ReDuSpider:
    def __init__(self):
        self.url = 'https://match.yuanrenxue.cn/api/match/2'
        self.headers = {
            'referer': 'https://match.yuanrenxue.cn/match/2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.m_js_filename = './JS/m.js'
        self.m_js_f = open(self.m_js_filename, 'r', encoding=self.chart_set)
        self.m_js_compile = execjs.compile(self.m_js_f.read())
        self.m_js_f.close()

    def get_content(self, url, params=None):
        m = re.match(r'm=(.*?);', self.m_js_compile.call('get_cookie'), re.S).group(1)
        self.session.cookies.set('m', m)
        if params:
            resp = self.session.get(url, params=params)
        else:
            resp = self.session.get(url)

        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set

        return resp

    def run(self):
        num = 0
        for page in range(1, 6):
            # https://match.yuanrenxue.cn/api/match/2?page=2
            params = {
                'page': page
            }
            if page > 4:
                self.headers['User-Agent'] = 'yuanrenxue.project'
                self.session.cookies.set('sessionid', 'r4s6p72q8jauwlvlk5kq806e0062bs9e')
            resp = self.get_content(self.url, params)
            content = resp.json()
            datas = content['data']
            num += sum([i['value'] for i in datas])
        print(num)


if __name__ == '__main__':
    redu = ReDuSpider()
    redu.run()

