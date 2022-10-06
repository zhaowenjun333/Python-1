import csv
import random
import re
from lxml import etree

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Host': 'www.dianping.com'
}
Cookie = {
    'Cookie': '_lxsdk_cuid=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _lxsdk=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _hc.v=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198; s_ViewType=10; ctu=f038cc6e62074d02d2dccf4f1fee2914ce130122d343e9146f7edebe2a902766; fspop=test; WEBDFPID=vw0z7286x72v5yy8048ywvw1705486u1816789uwzz097958z1v0u6u7-1978067029903-1662707029572YGMKOUSfd79fef3d01d5e9aadc18ccd4d0c95073605; cy=1; cye=shanghai; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1662913957,1662914153,1662951906,1662958958; dplet=7915105ca766b8b548b0e5b382c6daf8; dper=d337bc7d6fb74b0bba231d0f6194495b20f0b2cd353b4eb24a6e4c5d8225d625c77f38869048fa45971e3002641a81ade2c39b49bdd7aa8e881baf3802f9d0642eb4f001ecea3d8d440c467bfef8dbf263306bfd6ccbfcc928b23cd7f24e7411; ll=7fd06e815b796be3df069dec7836c3df; ua=Gean; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1662966557; _lxsdk_s=1833047b23e-e29-dd9-9fc%7C%7C1091'
}

url = 'https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97'
s = requests.session()

while True:
    resp = s.get(url, headers=headers, cookies=Cookie)
    html = resp.text
    html_element = etree.HTML(html)
    title = html_element.xpath('//html/head/title/text()')[0]
    if title == '403 Forbidden':
        print('403')
        continue
    else:
        print(title)
        # print(resp.cookies)
        s.cookies.update(resp.cookies)
        print(s.cookies)
        # print(resp.text)
        print('---------'*10)
    break

# with open('./宠物店信息/89代理.txt', 'r', encoding='utf-8') as f:
#     proxies_list = [eval(i.strip(',\n')) for i in f.readlines()]
#     print(proxies_list)
# resp = requests.get(url, headers=headers)
# html = resp.text
# print(html)
# resp.close()

# with open('./宠物店信息/全球免费代理.csv', 'r', encoding='utf-8') as f:
#     csvreader = csv.DictReader(f)
#     proxies_list = []
#     for i in csvreader:
#         proxies_list.append(i)
#     f.close()
    # print(proxies_list)
#
# headers['User_Agent'] = random.choice(User_Agent)
# headers['Cookie'] = random.choice(Cookie)
# print(headers)


# html_element = etree.HTML(html)
# shops = html_element.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
# for info in range(len(shops)):
#     url = shops[info].xpath('.//div[@class="tit"]/a/@href')[0]
#     print(url)



