import _thread
import time

import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.19 NetType/4G Language/zh_TW",
}

mainUrl = 'https://api.myip.la/en?json'


def testUrl():
    # 账密
    entry = 'http://{}:{}@ip:port'.format("账户", "密码")

    proxy = {
        'http': entry,
        'https': entry,
    }
    try:
        res = requests.get(mainUrl, headers=headers, proxies=proxy, timeout=10)
        print(res.status_code, res.text)
    except Exception as e:
        print("访问失败", e)
        pass


for port in range(0, 10):
    _thread.start_new_thread(testUrl, ())
    time.sleep(0.1)

time.sleep(10)
