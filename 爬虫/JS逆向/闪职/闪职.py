# 网站：https://cs.fang.com/
# 登录
# 加密方式：RSA

from lxml import etree
import requests
from requests import utils

from rsa_python import encrypt

class ShanZhi:
    def __init__(self, url1, url2):
        self.headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        self.headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            # 'Cookie': f'csrftoken={csrfmiddlewaretoken}'
        }
        self.data = {
            # 'username': '{}',
            # 'password': '{}',
            # 'csrfmiddlewaretoken': '{}'
        }
        self.url1 = url1
        self.url2 = url2

    # 发送第一次请求
    def first_parse(self):
        resp = requests.get(self.url1, headers=self.headers1)
        resp.encoding = "utf-8"
        html = etree.HTML(resp.text)
        csrfmiddlewaretoken = html.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
        pk = html.xpath('//input[@id="pk"]/@value')[0]
        resp.close()
        return csrfmiddlewaretoken, pk

    def RSA(self, pk, password):
        # 通过pk对密码做加密处理
        new_password = encrypt(pk, password)
        return new_password

    def second_parse(self):
        # 一、 post请求
        # resp = requests.post(self.url1, headers=self.headers2, data=self.data)
        # resp.encoding = "utf-8"
        # print(resp.text)
        # 二、 维持会话 在跨请求的时候保持某一些参数
        session = requests.Session()
        session_resp = session.post(self.url2, headers=self.headers2, data=self.data)
        print(session_resp.text)
        # 如何通过session把cookie提取出来
        # 第一种转换方式
        cookies_dict = session.cookies.get_dict()
        print(cookies_dict)
        # 第二种转换方式
        cookies_dict = utils.dict_from_cookiejar(session.cookies)
        print(cookies_dict)

    def run(self):
        username = input('请输入用户名：')
        password = input('请输入密码：')
        csrfmiddlewaretoken, pk = self.first_parse()
        new_password = self.RSA(pk, password)
        self.headers2['Cookie'] = f'csrftoken={csrfmiddlewaretoken}'
        self.data['username'] = username
        self.data['password'] = new_password
        self.data['csrfmiddlewaretoken'] = csrfmiddlewaretoken
        self.second_parse()


if __name__ == '__main__':
    ur1 = 'http://shanzhi.spbeen.com/login/'
    ur2 = 'http://shanzhi.spbeen.com/detail/?id=2425'
    souhu = ShanZhi(ur1, ur2)
    souhu.run()

