import json

import requests
import execjs


class WangYiCC:
    def __init__(self):
        self.start_url = 'https://cc.163.com/category/'
        self.ini_url = 'https://dl.reg.163.com/dl/dlzc/yd/ini'
        self.session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.datas_js_filename = 'JS/getId.js'
        self.datas_file = open(self.datas_js_filename, 'r', encoding='utf-8')
        self.datas_js_compile = execjs.compile(self.datas_file.read())
        self.datas_file.close()

        self.enc_js_filename = './JS/encParams.js'
        self.enc_file = open(self.enc_js_filename, 'r', encoding='utf-8')
        self.enc_js_compile = execjs.compile(self.enc_file.read())
        self.enc_file.close()

    def get_content(self, url, data=None):
        if not data:
            resp = self.session.get(url)
        else:
            resp = self.session.post(url, data=data)

        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        return resp

    def start_request(self):
        resp = self.get_content(self.start_url)
        print(self.get_cookies())
        resp.close()

    def get_cookies(self):
        return self.session.cookies.get_dict()

    def get_ini(self):
        # l_yd_s_ccPFClpTB: 8F7AD574C145A0CBC2259FC8358E677E9AB96A6AC1FE9A2B2ACCCE8A0A2B29ED71F1886064EA233F6147BB556663D881312BBC2FE9E070BF04590D7560A4A3C9D531D3BCB7C4723CB12FAB631327D44AA05922DD876B7E0E3089A83AC4E171A4
        # NTES_WEB_FP=16ce384d8478f26482e28557203afe1c
        utid = self.datas_js_compile.call('utid')
        self.session.cookies.set('utid', utid)
        self.session.cookies.set('NTES_WEB_FP', '16ce384d8478f26482e28557203afe1c')

        print(self.get_cookies())
        self.headers['Content-Type'] = 'application/json'
        self.headers['Referer'] = 'https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html?cd=https%3A%2F%2Fcc.res.netease.com%2F_next%2F_static%2Fstatic%2Fstyles%2F&cf=urs_component-v2.css%3Fversion%3D202208080951&MGID=1679926767132.66&wdaId=&pkid=PFClpTB&product=cc'
        print(self.headers)
        self.session.headers.update(self.headers)

        data = {
            "pd": "cc",
            "pkid": "PFClpTB",
            "pkht": "cc.163.com",
            "channel": 14,
            "topURL": "https://cc.163.com/category/",
            "rtid": self.datas_js_compile.call('rtid')
        }
        data = self.enc_js_compile.call('encParams', data)
        data = json.dumps({"encParams": f"{data}"})
        resp = self.get_content(self.ini_url, data)
        content = resp.text
        print(content)
        print(self.get_cookies())
        return content

    def run(self):
        self.start_request()
        self.get_ini()
        # utid = self.datas_js_compile.call('utid')
        # self.session.cookies.set('utid', utid)
        # ini_content = self.get_ini()
        # print(ini_content)
        # cookies = self.get_cookies()
        # print(cookies)


if __name__ == '__main__':
    cc = WangYiCC()
    cc.run()
# https://webzjac.reg.163.com/v2/config/js?pn=YD00000710348764&cvk=&cb=__wmjsonp_06a06810&t=1680498993958
# 9ca170a1abeedba16ba1f2ac96ed26f3eafdcfe265aff1bad3ae70e2f4ee83e27fe2e6ee82e226a8aba2cfb43ef1f2ad90f025b6eee183a128e2bca4c3b92ae2f4ee8ee867e2e6fbd1af2aafbba7c3b939f4f0e4c3e26faffef6d3b328e2bdab8aa132f1f000cda161a7b3eedbb43cf0fea586ec2afaed00d1af2aa6bba3c3b93af4f4ee87e863e2e6fdd1b328e2adab8ea132f2f0e4c3f26fabfef6d4b33cf0feab8be270e2e6aa82ef79a7f4ee86e579e2e6aa82ef79a7f4ee86f679e2e6aa82ef79a7f4ee93e880e2e6ffcda169afb2eedbb128e2bda7c3b93bf4f0e4c3ee80a7b3eedbb83cf0fea195e863e2e6fdd1b328e2b3bc86f02afaeb00cda167b8bba7c3b939f4f0e4c3f366e2e6eebac73cf4f000d1b63bf4edfcd9b63ef8fee4c3e870a1fef695f17fa7f4ee83ef2afafeeecda163b6b0eedbb23cf4f000d1af2aa8acba91a132fceafcd1b33cf4f0e4c3f780adfef6d3b33cf4f4ee86e47fe2e6aa82ef79a7f4ee82e780e2e6fbd1af2aa7acadc3b96ea3b4bd86af2ab8bdbcc3b93cbf
