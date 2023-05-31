# https://dl.reg.163.com/dl/zj/mail/vftcp

import json
import time

import execjs
import urllib.parse
import requests

if __name__ == '__main__':
    start_url = 'https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html?cd=https%3A%2F%2Fcc.res.netease.com%2F_next%2F_static%2Fstatic%2Fstyles%2F&cf=urs_component-v2.css%3Fversion%3D202208080951&MGID=1679988650664.507&wdaId=&pkid=PFClpTB&product=cc'
    session = requests.session()
    # data = {
    #     'encParams': '7e3ba6f5eea9ee4fe8c8bf6a367329fa8ae97d92bf431367362db28508e37e245abf73b2d20c6ecce7998087abae2050567ccec30ee4300d780cb67a9088f2efd649ececf1d215d52be81c7e374efd335c7b9aa48944dfd3c1b94e512b9bb86cf6b727e36631fac49bef843625a4544ffb9d78af74c7760ec70562cb42a5bb044435c1a32dd8e0924943492d262493ecf9f9ddb048709e8028c6f6bae428c2e580407eba91961d92348874279985a28618b307936eb1d7d8dcf528323e04683e94fb6cd9d957847b1c30c61873dd81df77086f9e3e6aad32efc04f88e67cd7915231a4c15349297b8b20c29d7ef04808120b29632d4a60e0a26870baeb982dd339091493841c8e08017fb704d400a2978c9fba7d79fe0528fccb0513c7c71e579e73776afad5333b6101e60da6dbb9259c73b4af27e774207e72c0d1d96428a41998443b34f586d9d7f6dbb497dd1cdb6cc82790df24ca687458c1872fe47b955c1c42a1e49e4b0f4189949d8b0b994dd9649bea9a38e3c096843307d69e3dca184d7d9d6cf4cb41fcbaff4e89248c1dba7cfdf987e8cca99359211a4e5cde12aa08aeece645647ff95b3e281dc367491c2056b883f7f2e9f181e5246d4747258356463280560c2947504c81954aac7ac5afd694be2b835c92c6a85f1ea0ece7d0929a2dec6e35310a51d6310ad58c85741d0345a065a723499c4fd188204c35123db667b4bcd8eb1826c9158a58cab40e44e6bb5aa478022683562e04cbf9270d1750e8f00c1b60059de913bffec5b24ef612e68c66a6d6bfcae837f71926ee130ada444feca260e5afee397bb9373ab089e48f9d69fee57c6cca6da1d147f60adb65e93cc6c92c102a67092fce9bdd8ad7de2de8a2551610f9bada422a057b62947cee704006bc1f2a504280942814b5cece1d879e9f550d2e1d1cdc926890e735f427741d96023dfa01d1a85be49cd52c8dc6b4d47e1f1ef9ec4140a0ec7298913e32def169c16459229706bea702'
    # }
    # data = json.dumps(data)
    headers = {
        'Host': 'dl.reg.163.com',
        'Referer': 'https://cc.163.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    # session.cookies.set('gdxidpyhxdE', r'KpZSwPJky8\ugsUN8tUJlts6rPArAo8me162eN599755pmDs/UZdniAyktL9o9Urxt8JEsL4jhVmBOqz9x59+c7B\08BJ49wvLUYn66OhNGyNbx6TsTWeJqPfYlAHUxP\YHTlB1JUKTjwdhVAc7O3Cy1EAT/K/KMqhxB4tw9q1lBLdja:1679977057726')
    # session.cookies.set('_9755xjdesxxd_', '32')
    session.headers.update(headers)
    resp = session.get(start_url)
    print(resp.status_code)
    print(resp.text)
    print(session.cookies.get_dict())

print(time.time())
