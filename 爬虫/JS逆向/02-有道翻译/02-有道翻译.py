import requests
import execjs

url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
header = {
    "Cookie": "OUTFOX_SEARCH_USER_ID=-1017129654@2408:8220:146:3e80:4c11:c61f:b0aa:336; OUTFOX_SEARCH_USER_ID_NCOO=132012882.40254839; fanyi-ad-id=307888; fanyi-ad-closed=1; ___rl__test__cookies=1657816731719",
    "Host": "fanyi.youdao.com",
    "Origin": "https://fanyi.youdao.com",
    "Referer": "https://fanyi.youdao.com/",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    # 判断异步程序
    'X-Requested-With': 'XMLHttpRequest'
}
word = input('请输入要翻译的内容：')

with open('youdao.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 编译js代码
compile_result = execjs.compile(js_code)
print(compile_result)
# 调用js代码，调用youdao()函数，并传参
result = compile_result.call('youdao', word)
print(result)

data = {
    "i": f"{word}",
    "from": "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    # "salt": "16578058369652",
    # "sign": "625eaab2fadeee6a520f4a3382f0be70",
    # "lts": "1657805836965",
    # "bv": "f0819a82107e6150005e75ef5fddcc3b",
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_REALTlME",
}
# 添加数据
data.update(result)

resp = requests.post(url, headers=header, data=data)
print(resp.json())
