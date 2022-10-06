# coding=utf-8
# ！/usr/bin/env python
import json
import threading
import time
import requests as rq

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br"
}
testUrl = 'https://api.myip.la/en?json'


# 核心业务
def testPost(host, port):
    proxies = {
        'http': 'http://{}:{}'.format(host, port),
        'https': 'http://{}:{}'.format(host, port),
    }
    res = ""

    while True:
        try:
            res = rq.get(testUrl, proxies=proxies, timeout=5)
            # print(res.status_code)
            print(res.status_code, "***", res.text)
            break
        except Exception as e:
            print(e)
            break

    return


class ThreadFactory(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        testPost(self.host, self.port)


# 提取代理的链接  json类型的返回值
tiqu = '提取链接'

while 1 == 1:
    # 每次提取10个，放入线程中
    resp = rq.get(url=tiqu, timeout=5)
    try:
        if resp.status_code == 200:
            dataBean = json.loads(resp.text)
        else:
            print("获取失败")
            time.sleep(1)
            continue
    except ValueError:
        print("获取失败")
        time.sleep(1)
        continue
    else:
        # 解析json数组
        print("code=", dataBean["code"])
        code = dataBean["code"]
        if code == 0:
            threads = []
            for proxy in dataBean["data"]:
                threads.append(ThreadFactory(proxy["ip"], proxy["port"]))
            for t in threads:  # 开启线程
                t.start()
                time.sleep(0.01)
            for t in threads:  # 阻塞线程
                t.join()
    # break
    time.sleep(1)
