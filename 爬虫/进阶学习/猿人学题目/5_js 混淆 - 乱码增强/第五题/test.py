import requests
import execjs

api_url = 'https://match.yuanrenxue.cn/api/match/5'

js_f = open('./JS/m5.js', 'r', encoding='utf-8')
js_compile = execjs.compile(js_f.read())

session = requests.session()

headers = {
    'User-Agent': 'yuanrenxue.project',
    'X-Requested-With': 'XMLHttpRequest',
}
sessionid = '4wbumndboopt4d6l8zv1tro4yujs2si1'

for page in range(1, 6):
    values = js_compile.call('get_params')
    print(values)
    params = {
        'page': str(page),
        'm': values['url_m'],
        'f': values['url_f']
    }
    cookies = {"sessionid": sessionid, "m": values['m'], 'RM4hZBv0dDon443M': values['RM4hZBv0dDon443M']}
    resp = requests.get(api_url, headers=headers, cookies=cookies, params=params)
    print(resp.text)
