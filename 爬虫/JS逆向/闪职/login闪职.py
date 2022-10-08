import requests
from lxml import etree
from rsa_python import encrypt

class ShanZhi:
    def __init__(self, url):
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
        self.url = url

    # 发送第一次请求
    def first_parse(self):
        resp = requests.get(self.url, headers=self.headers1)
        resp.encoding = "utf-8"
        html = etree.HTML(resp.text)
        csrfmiddlewaretoken = html.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
        pk = html.xpath('//input[@id="pk"]/@value')[0]
        resp.close()
        return csrfmiddlewaretoken, pk

    def RSA(self, pk, password):
        new_password = encrypt(pk, password)
        return new_password

    def second_parse(self):
        # resp = requests.post(self.url, headers=self.headers2, data=self.data)
        # resp.encoding = "utf-8"
        # print(resp.text)
        # 维持会话 在跨请求的时候保持某一些参数
        session = requests.Session()
        session_resp = session.post(self.url, headers=self.headers2, data=self.data)
        cookies_dict = session.cookies.get_dict()
        print(session_resp.text)
        # print(cookies_dict)

    def run(self):
        username = input('请输入用户名：')
        password = input('请输入密码：')
        csrfmiddlewaretoken, pk = self.first_parse()
        # print(csrfmiddlewaretoken, '\n', pk)
        new_password = self.RSA(pk, password)
        self.headers2['Cookie'] = f'csrftoken={csrfmiddlewaretoken}'
        self.data['username'] = username
        self.data['password'] = new_password
        self.data['csrfmiddlewaretoken'] = csrfmiddlewaretoken
        # print(self.headers2, '\n', self.data)
        self.second_parse()


if __name__ == '__main__':
    ur = 'http://shanzhi.spbeen.com/login/'
    souhu = ShanZhi(ur)
    souhu.run()

