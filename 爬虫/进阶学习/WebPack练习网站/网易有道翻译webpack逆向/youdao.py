import requests
import execjs
import json
import timeit
import os
import sys


class YouDaoSpider:
    def __init__(self):
        self.url = 'https://dict.youdao.com/webtranslate'
        self.headers = {
            "Cookie": "OUTFOX_SEARCH_USER_ID=1295984880@10.110.96.153; OUTFOX_SEARCH_USER_ID_NCOO=202206778.42412636",
            "Host": "dict.youdao.com",
            "Origin": "https://fanyi.youdao.com",
            "Referer": "https://fanyi.youdao.com/",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
        self.JS_dir_path = f'{self.base_dir}/JS'
        if not os.path.exists(self.JS_dir_path):
            os.mkdir(self.JS_dir_path)
        self.JS_file = open(f'{self.JS_dir_path}/sign.js', 'r', encoding=self.chart_set)
        self.js_compile = execjs.compile(self.JS_file.read())
        self.JS_file.close()

        self.data = {
            "from": "AUTO",
            "to": "",
            "domain": 0,
            "dictResult": "true",
            "keyid": "webfanyi"
        }

    def get_params(self):
        params = self.js_compile.call('get_params')
        return params

    def get_codes(self):
        resp = self.session.post(self.url, data=self.data)
        return resp.text

    def get_result(self, codes):
        result = self.js_compile.call('get_result', codes)
        return result

    def run(self):
        keyword = input(f'请输入你要翻译的单词：')
        self.data['i'] = keyword
        params = self.get_params()
        self.data.update(params)
        # print(self.data)
        codes = self.get_codes()
        result = self.get_result(codes)
        print(result)


if __name__ == '__main__':
    youdao = YouDaoSpider()
    t = timeit.timeit(stmt=youdao.run, number=1)
    print(t)

