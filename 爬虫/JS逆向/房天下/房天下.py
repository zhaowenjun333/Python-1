# 网站：https://cs.fang.com/
# 登录
# 加密方式：RSA

import execjs
import requests
from requests import utils

class FangLogin:

    def __init__(self, ur1, ur2):
        self.headers1 = {
            'Cookie': 'global_cookie=ak21wjrdvh1b47d164o1f0n7k17l5nwi15r; __jsluid_s=e2fdeeefe6e7a13c64a73e035754e88f; __utmz=147393320.1657976679.1.1.utmcsr=cq.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; city=cs; fang_hao123_layed=1; g_sourcepage=txz_dl%5Egg_pc; __utma=147393320.1270394924.1657976679.1657976679.1658152894.2; __utmc=147393320; token=eb7945739f9c43f3a5df31315a294a96; unique_cookie=U_xb9fpjy14msy2ugqr3cz3mnzk11l5qt4sgv*9; __utmt_t0=1; __utmt_t1=1; __utmb=147393320.4.10.1658152894',
            'Host': 'passport.fang.com',
            'Origin': 'https://passport.fang.com',
            'Referer': 'https://passport.fang.com/?backurl=http%3A%2F%2Fmy.fang.com%2F',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        self.data = {
            'uid': '{0}',
            'pwd': '{0}',
            'Service': 'soufun-passport-web',
            'AutoLogin': '1',
        }
        self.ur1 = ur1
        self.ur2 = ur2

    def LoginUser(self):
        username = input('请输入用户名：')   # geanlry
        pwd = input('请输入密码：')         # lry1730225
        return username, pwd

    def RSA(self, pwd):
        with open('fang.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        # 编译js代码
        compile_result = execjs.compile(js_code)
        # print(compile_result)
        # 调用js代码，调用wx()函数，并传参
        return compile_result.call('encryptedString', pwd)

    def first_parse(self, username, pwd):
        data = {
            'uid': username,
            'pwd': pwd,
            'Service': 'soufun-passport-web',
            'AutoLogin': '1'
        }
        resp = requests.post(self.ur1, headers=self.headers1, data=data)
        print(resp.json())
        new_loginid = resp.json()['UserID']
        resp.close()
        return new_loginid

    def second_parse(self, username, pwd, new_loginid):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'cookie': 'global_cookie=ak21wjrdvh1b47d164o1f0n7k17l5nwi15r; '
                      '__utmz=147393320.1657976679.1.1.utmcsr=cq.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
                      'city=cs; g_sourcepage=undefined; g_sourcepage=txz_dl%5Egg_pc; '
                      '__utma=147393320.1270394924.1657976679.1658510497.1658544728.5; __utmc=147393320; '
                      'token=41772f053c4747bc8b95b4f4e0abba87; __utmb=147393320.22.10.1658544728; '
                      f'sfut={pwd}; new_loginid={new_loginid}; login_username={username}; '
                      'unique_cookie=U_0so4nrquow8pohxpx8qocq7jk24l5xanus5*37'
        }
        session = requests.Session()
        session_resp = session.get(self.ur2, headers=headers)
        session_resp.encoding = 'gb2312'
        print(session_resp.text)
        # 如何通过session把cookie提取出来
        # 第一种转换方式
        cookies_dict = session.cookies.get_dict()
        print(cookies_dict)
        # 第二种转换方式
        cookies_dict = utils.dict_from_cookiejar(session.cookies)
        print(cookies_dict)

    def run(self):
        username, pwd = self.LoginUser()
        pwd = self.RSA(pwd)
        print(pwd)
        new_loginid = self.first_parse(username, pwd)
        self.second_parse(username, pwd, new_loginid)


if __name__ == '__main__':
    url1 = 'https://passport.fang.com/login.api'
    url2 = 'https://cs.fang.com/'
    souhu = FangLogin(url1, url2)
    souhu.run()

