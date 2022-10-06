# 网站登录 ：https://tv.sohu.com/

# 1、找到加密字段

# 2、定位到加密代码 进行js调试(vscode) 没有报错且有你想要的数据
# 得到一个js文件：17期爬虫-11-JS逆向-上课昵称(真实姓名).js

# 3、同python执行调试好的js代码 得到一个加密之后的字符串
# 得到一个py文件：17期爬虫-11-JS逆向-上课昵称(真实姓名).py

import execjs
import requests

class SouHuLogin:

    def __init__(self, ur):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'content-length': '169',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'reqtype=pc; gidinf=x099980109ee157d828a25c120005e7317ef0777224a; IPLOC=CN4101; SUV=2207171317357XU7; _sgid=_SSA.077c2ddd743684ae0998ecb66914536c; beans_dmp_done=1; beans_dmp=%7B%2210191%22%3A1658036310%2C%22admaster%22%3A1658036310%2C%22shunfei%22%3A1658036310%2C%22reachmax%22%3A1658036310%2C%22lingji%22%3A1658036310%2C%22yoyi%22%3A1658036310%2C%22ipinyou%22%3A1658036310%2C%22ipinyou_admaster%22%3A1658036310%2C%22miaozhen%22%3A1658036310%2C%22diantong%22%3A1658036310%2C%22huayang%22%3A1658036310%2C%22precisionS%22%3A1658036310%7D; beans_dmp_busi_done=1; lastpassport=17302254866; beans_freq=1; t=1658042596135; jv=8495bda92ad3350df1d1379f87a80f63-PmrUA31X1658042937038',
            'origin': 'https://tv.sohu.com',
            'referer': 'https://tv.sohu.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        self.ur = ur

    def LoginUser(self):
        username = input('请输入用户名：')
        pwd = input('请输入密码：')
        return username, pwd

    def MD5(self, pwd):
        with open('17期爬虫-11-JS逆向-李容宇.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        # 编译js代码
        compile_result = execjs.compile(js_code)
        # print(compile_result)
        # 调用js代码，调用wx()函数，并传参
        return compile_result.call('md5', pwd)

    def run(self):
        username, pwd = self.LoginUser()
        result = self.MD5(pwd)
        print(result)
        data = {
            'userid': f'86-{username}',
            'password': result,
            'persistentCookie': '1',
            'appid': '107405',
            'callback': 'passport408_cb1658054303008',
        }
        resp = requests.post(self.ur, headers=self.headers, data=data)
        print(resp.text)


if __name__ == '__main__':
    url = 'https://v4.passport.sohu.com/i/login/107405'
    souhu = SouHuLogin(url)
    souhu.run()

