import requests
from fontTools.ttLib import TTFont

url = 'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId=G6b0BasC9aS47JRs&cityId=160&shopType=10&tcv=fg7sk9q5ku&_token=eJx1kFtPwjAYhv9Lk9017OuOLXfCmG4MItvwgDGmOwgIg7FOhhj%2Fux1Cohfe9H369ju86SeqvAx1CQAYBKN9XqEuIh3oWAijWsgXy6QmszWd6rqFUfrXo8TGKKnuHNR9IqYsIDY8t04ojR%2BHWsYzPqMmUTNwKyjxZAla1HUpuqraNE0nW%2FJNudzMO%2Bm2UMViW6rXVgI9LvqMR4bth0Jm%2Br8h51W6UFf5R7OtMpVYoMKLMrCUnqn0bGUgzyuFma1DHYUNkMxQxG0Gw6CYgiaH67aJCZATGZLgTIydQL%2BAdgGCGT0BYGa3YLFfYJ5AtmvtslW7TCo%2Fa325j%2BSXy0qxnG8k5f4hjoQhdq%2FhSMRTGBEnCKD0g8Srj9Paj9P9KAISDqntBU1v%2BD4T6%2Bt4vnbf6sSf86S4Ea77eOtOPrbBtICxk0XDSB8fB3KkGvrHqenCehk9aJyvi0O2uT9wPivT3dXEOXr9cY6%2BvgHOv5CQ&uuid=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2FG6b0BasC9aS47JRs'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Cookie': 'fspop=test; cy=160; cye=zhengzhou; _lxsdk_cuid=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _lxsdk=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _hc.v=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198; s_ViewType=10; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1658581197,1658584004; WEBDFPID=4x5466x1504353300199u4u401z0z1xy8177y4zx1y2979580v725w9w-1658671145470-1658584744839MUMKUCQfd79fef3d01d5e9aadc18ccd4d0c95073827; dplet=7e9a16bc9a035410b74ce750116e1c17; dper=e7b1f5a48f7115e49fd94aa510b74f4d48dc8f79ab470841c9ce28f328425e3a19574afc34fe6658cfbfc30376c9e0d7f520e5a2fa3285d5b1768f8a486e1caadc27cfdb907129eba197957cb878ca07a90c79ecf8004c5e5aaa2c8559de1460; ll=7fd06e815b796be3df069dec7836c3df; ua=Gean; ctu=f038cc6e62074d02d2dccf4f1fee2914ce130122d343e9146f7edebe2a902766; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1658597227; _lxsdk_s=1822c15619a-871-d-7e0%7C%7C67',
    'Host': 'www.dianping.com',
    'Referer': 'https://www.dianping.com/shop/G6b0BasC9aS47JRs'
}

resp = requests.get(url, headers=headers)
# print(resp.json())
resp.close()

# 加载字体文件
bw = TTFont('b493796a.woff')
# bw.saveXML('b493796a.xml')

# 得到映射关系
# print(bw.getBestCmap())

# 替换后的字典
replace_dict = {}

for k, v in bw.getBestCmap().items():
    # 转换16进制
    # 把0x替换成&#x, 并加;结尾
    key = hex(k).replace('0x', '&#x') + ';'
    print(key, v)
