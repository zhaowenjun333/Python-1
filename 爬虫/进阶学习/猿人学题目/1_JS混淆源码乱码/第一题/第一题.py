# 题目1：抓取所有（5页）机票的价格，并计算所有机票价格的平均值，填入答案。
import requests
import execjs
import urllib.parse
import time


class JiPiaoSpider:
    def __init__(self):

        self.headers = {
            'referer': 'https://match.yuanrenxue.cn/match/1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.m_js_filename = './JS/m1.js'
        self.m_js_f = open(self.m_js_filename, 'r', encoding=self.chart_set)
        self.m_js_compile = execjs.compile(self.m_js_f.read())
        self.m_js_f.close()

    def get_content(self, url, params=None):
        if params:
            resp = self.session.get(url, params=params)
        else:
            resp = self.session.get(url)

        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        # print(resp.headers)
        # print(resp.url)
        return resp

    def get_json(self, url):
        resp = requests.get(url, headers=self.headers)
        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        # print(resp.status_code)
        # print(resp.headers)
        # print(resp.url)
        return resp

    def run(self):
        ticket = 0
        num = 0
        for page in range(1, 6):
            m = self.m_js_compile.call('get_m')
            m = urllib.parse.quote(urllib.parse.unquote(m).replace('|', '丨'))
            # print(m)
            url = f'https://match.yuanrenxue.cn/api/match/1?page={page}&m={m}'
            print(url)
            if page > 4:
                self.headers['User-Agent'] = 'yuanrenxue.project'
                self.session.cookies.set('sessionid', 'ma396onyax2qvrzwothnhocnhnaw0dyp')
            resp = self.get_content(url)
            content = resp.json()
            print(content)
            datas = content['data']
            num += len(datas)
            for i in datas:
                ticket += i['value']
        print(num, ticket)


if __name__ == '__main__':
    jipiao = JiPiaoSpider()
    jipiao.run()
