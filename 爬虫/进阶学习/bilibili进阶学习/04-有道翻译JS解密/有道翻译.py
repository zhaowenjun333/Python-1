import time
import random
from hashlib import md5
import execjs
import requests


def js_youdao(s, appversion):
    with open('有道翻译.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    # 编译js代码
    compile_result = execjs.compile(js_code)
    result = compile_result.call('form_data', s, appversion)
    return result


def py_md5(s):
    h = md5()
    h.update(s.encode())
    return h.hexdigest()


def data(w, result):
    form_data = {
        'i': w,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }
    # print(f'result{result}')
    form_data.update(result)
    return form_data


def run(s):
    url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '243',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=434593894@222.69.215.156; OUTFOX_SEARCH_USER_ID_NCOO=1906929335.062909; ___rl__test__cookies=1667127191389',
        'Host': 'fanyi.youdao.com',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    appVersion = headers['User-Agent'].strip('Mozilla/')
    lts = f'{time.time() * 1000}'.split('.')[0]
    salt = f'{lts}{random.randint(0, 10)}'
    result1 = {
        'salt': salt,
        'sign': py_md5(f'fanyideskweb{s}{salt}Ygy_4c=r#e#4EX^NUGUc5'),
        'lts': lts,
        'bv': py_md5(appVersion)
    }
    form_data1 = data(s, result1)
    # print(form_data1)

    result2 = js_youdao(s, appVersion)
    form_data2 = data(s, result2)
    print(form_data2)

    resp1 = requests.post(url, headers=headers, data=form_data1).json()
    print(resp1)

    resp2 = requests.post(url, headers=headers, data=form_data2).json()
    print(resp2)


if __name__ == '__main__':
    word = input('请输入你要翻译的单词：')
    run(word)




