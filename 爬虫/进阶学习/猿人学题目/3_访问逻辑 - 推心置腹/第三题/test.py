import requests
from collections import defaultdict

# proxies = {
#     'http': 'http://localhost:8889',
#     'https': 'http://localhost:8889'
#
# }

headers = {
    'content-length': '0',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile':	'?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'accept': '*/*',
    'origin': 'https://match.yuanrenxue.cn',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://match.yuanrenxue.cn/match/3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
}
cookies = {
    "sessionid": "0yonn8wa4w6zhlqrrigenikxg594pxk8",
    "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1684145810,1684192605,1684192866,1684317806",
    "qpfccr": "true",
    "no-alert3": "true",
    "tk": "7117510294618647776",
    "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1684145827,1684192630,1684192871,1684317862",
    "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1684411583",
    "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1684411586"
}
session = requests.session()
session.headers = headers
res = defaultdict(int)
for i in range(1, 6):
    url = "https://match.yuanrenxue.cn/jssm"
    response = session.post(url, cookies=cookies)

    url_p = 'https://match.yuanrenxue.cn/api/match/3?page={}'.format(i)
    resp = session.get(url=url_p, cookies=cookies)
    for data in resp.json()['data']:
        value = data['value']
        res[value] += 1
print(res)
print(dict(res))
print(max(res, key=lambda x: res[x]))
