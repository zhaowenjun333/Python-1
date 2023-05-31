import requests
import time

session = requests.session()


def get_content(url, referer):
    headers = {
        'Referer': referer,
        'Cookie': 'wzws_sessionid=gmZjNWVlMYEyY2UxZmSgZAlRnoAyMjIuNjcuMjM2LjE0Ng==; u=6; JSESSIONID=Eu_FLT0AO_U-3sySwBFGjXeUqvYi7vCmYxAhr2vcRg7BUeusAQ-5!1171792879',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    session.headers.update(headers)
    resp = session.get(url, verify=False)
    content = resp.json()
    resp.close()
    return content


def parse_page(url, referer, y):
    content = get_content(url, referer)
    print(content)
    items = content['returndata']['datanodes']
    num = len(items)
    if num == 6:
        item = {
            '林业用地面积(万公顷)': items[0]['data']['data'],
            '森林面积(万公顷)': items[1]['data']['data'],
            '人工林面积(万公顷)': items[2]['data']['data'],
            '森林覆盖率(%)': items[3]['data']['data'],
            '活立木总蓄积量(亿立方米)': items[4]['data']['data'],
            '森林蓄积量(亿立方米)': items[5]['data']['data'],
        }
        print(f'{y}年：{item}')


# url_list = []
cid = '110000'
for year in range(2011, 2022):
    page_url = f'https://data.stats.gov.cn/easyquery.htm'
    referer_url = f'https://data.stats.gov.cn/easyquery.htm?cn=E0103&zb=A0C0A&reg={cid}&sj={year}'
    parse_page(page_url, referer_url, year)
