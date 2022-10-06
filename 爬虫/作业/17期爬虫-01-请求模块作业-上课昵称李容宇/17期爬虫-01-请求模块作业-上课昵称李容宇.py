import requests

key = input("请输入：")
fanyi = input("英文翻译成中文请输入1，中文翻译成英文请输入0：")
url = f'https://fanyi.so.com/index/search?eng={fanyi}&validate=&ignore_trans=0&query={key}'

headers = {
    'pro': 'fanyi',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
}
data = {
    'eng': fanyi,
    'validate': '',
    'ignore_trans': '0',
    'query': key,
}


resp = requests.post(url, headers=headers, data=data)
data_json = resp.json()
print(data_json['data']['fanyi'])
