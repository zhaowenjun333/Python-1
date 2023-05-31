import json
import re
import urllib.parse
import requests
import execjs


class WeiBoSpider:

    def __init__(self, username, password):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)

        self.user = username
        self.pwd = password

        self.js_filename = './JS/login.js'
        self.f = open(self.js_filename, 'r', encoding='utf-8')
        self.js_compile = execjs.compile(self.f.read())
        self.su = self.js_compile.call('result_name', self.user)
        self._ = self.js_compile.call('result_time')
        self.params = {
            'client': 'ssologin.js(v1.4.15)',
            '_': self._,
        }
        self.f.close()

        self.prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php'
        self.login_url = 'https://login.sina.com.cn/sso/login.php'

    def get_prelogin_result(self, url):
        self.headers['referer'] = 'https://login.sina.com.cn/signup/signin.php'
        self.session.headers.update(self.headers)
        params = self.params
        params['entry'] = 'account'
        params['callback'] = 'sinaSSOController.preloginCallBack'
        params['su'] = self.su
        params['rsakt'] = 'mod'
        resp = self.session.get(url, params=params)
        prelogin_result = json.loads(re.split(r'[()]', resp.text)[1])

        return prelogin_result

    def post_login(self, url, result):
        nonce = result['nonce']
        servertime = result['servertime']
        sp = self.js_compile.call('get_sp', result['pubkey'], servertime, nonce, self.pwd)
        datas = {
            'entry': 'account',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'pagerefer': '',
            'vsnf': '1',
            'su': self.su,
            'service': 'account',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': result['rsakv'],
            'sp': sp,
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': '580',
            'returntype': 'TEXT',
        }
        params = self.params
        resp = self.session.post(url, data=datas, params=params)
        login_result = json.loads(re.split(r'[()]', resp.text)[1])
        return login_result

    def get_protection_url(self, login_result):
        protection_url = urllib.parse.unquote(login_result['protection_url'])
        resp = self.session.get(protection_url)
        resp.encoding = resp.apparent_encoding
        result = resp.text
        return result

    def run(self):
        prelogin_result = self.get_prelogin_result(self.prelogin_url)
        print(prelogin_result)
        login_result = self.post_login(self.login_url, prelogin_result)
        print(login_result)
        protection_result = self.get_protection_url(login_result)
        print(protection_result)


if __name__ == '__main__':
    user = '15314656636'
    pwd = 'lry1730225'
    weibo = WeiBoSpider(user, pwd)
    weibo.run()
