import re

import requests

def start_requests():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    start_url = 'http://cfx.health.xywy.com/question/1/index.htm'
    resp = requests.get(start_url, headers=headers)
    resp.encoding = 'utf-8'
    return resp

def html_cookie():
    start_resp = start_requests()
    html = start_resp.text
    # 源码获取cookie
    _csrf_obj = re.compile(r'.*?<input type="hidden" name="_csrf" value="(?P<_csrf>.*?)"', re.S)
    _csrf = _csrf_obj.match(html).group('_csrf')
    return _csrf

def resp_cookie():
    start_resp = start_requests()
    cookies = start_resp.cookies
    php_id = cookies['PHPCFXSESSID']
    csrf = cookies['_csrf']
    return php_id, csrf

def parse_html(ur, php_id, csrf):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Host': 'cfx.health.xywy.com',
        'Referer': 'http://cfx.health.xywy.com/question/1/index.htm',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': f'PHPCFXSESSID={php_id}; _csrf={csrf}'
    }

    data = {
        '_csrf': csrf,
        'params[age]': '21',
        'params[gender]': '1',
        'params[hbp_his]': '2',
        'params[diab_his]': '2',
        'params[diab_family]': '1',
        'params[smoke_status]': '1',
        'params[vegetable]': '2',
        'params[fru]': '2',
        'params[is_act]': '1',
        'params[act_freq]': '2',
        'params[act_time]': '2',
        'params[act_intensity]': '2',
        'params[waist]': '60.0',
        'params[tg]': '12.00',
        'params[hdl]': '12.00',
        'params[height]': '163.0',
        'params[weight]': '53.00',
        'params[fbg]': '25.00',
    }
    resp = requests.get(ur, headers=headers)
    resp.encoding = 'utf-8'
    return resp.text


if __name__ == '__main__':
    url = 'http://cfx.health.xywy.com/report/19530/show.htm'
    # result1 = parse_html(url, html_cookie(), html_cookie())
    PHPCFXSESSID, _csrf = resp_cookie()
    result2 = parse_html(url, PHPCFXSESSID, _csrf)

    print(result2)
