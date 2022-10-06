import execjs
import requests
import json
import re
import collections

url = 'https://www.bilibili.com/video/BV1N94y1R7K5/'
resp = requests.get(url)


def gen_ids():
    with open('bilibili.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        f.close()
    # 编译JS代码
    compile_result = execjs.compile(js_code)
    # b_lsid
    b_lsid = compile_result.call('b_lsid')
    # _uuid
    _uuid = compile_result.call('r')
    return b_lsid, _uuid


if __name__ == '__main__':
    session = requests.Session()
    session.headers.update({
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })

    video_url = 'https://www.bilibili.com/video/BV1N94y1R7K5/'

    bvid = video_url.split('/')[-1]

    # 自动保存cookie: buvid3, buvid4
    resp1 = session.get(video_url)
    # print(session.cookies.get_dict())

    # 获取aid,cid
    data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', resp1.text)
    # 转为字典
    data_dict = json.loads(data_list[0])
    data = {
        'aid': data_dict['aid'],
        'cid': data_dict['videoData']['cid']
    }
    print(data)

    b_lsid, _uuid = gen_ids()
    session.cookies.set('b_lsid', b_lsid)
    session.cookies.set('_uuid', _uuid)
    session.cookies.set('CURRENT_FNVAL', '4048')
    # session.cookies.set('buvid_fp', "bf8242df3c64fb172aa7a9e7786f85f8")

    spi_url = 'https://api.bilibili.com/x/frontend/finger/spi'
    resp2 = session.get(spi_url)
    buvid4 = resp2.json()['data']['b_4']
    session.cookies.set('buvid4', buvid4)

    url = f'https://api.bilibili.com/x/player/v2?aid={data["aid"]}&cid={data["cid"]}'
    resp3 = session.get(
        url=url,
        params={
            'aid': data["aid"],
            'cid': data["cid"],
            'bvid': bvid
        })
    sid = resp3.cookies.get_dict()['sid']
    print(sid)

