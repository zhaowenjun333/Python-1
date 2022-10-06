import csv
import random

import execjs
import requests
import json
import re
import collections
import time
import math


def get_tunnel_proxies():
    # proxy_host = ''
    proxy_username = '47.106.105.236'
    proxy_pwd = '80'

    return {
        'http': f'http://{proxy_username}:{proxy_pwd}',
        'https': f'https://{proxy_username}:{proxy_pwd}'
    }
    # with open('./代理1.txt', 'r', encoding='utf-8') as f:
    #     proxies_list = []
    #     lines = f.readlines()
    #     for line in lines:
    #         proxies_list.append(eval(line))
    #     f.close()
    # return proxies_list


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


def session_cookie(video_url, proxies):
    session = requests.Session()
    session.headers.update({
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })
    bvid = video_url.split('/')[-1]

    # 自动保存cookie: buvid3, buvid4
    resp1 = session.get(video_url)
    # print(session.cookies.get_dict())
    session.cookies.set('CURRENT_FNVAL', '4048')

    b_lsid, _uuid = gen_ids()
    session.cookies.set('b_lsid', b_lsid)
    session.cookies.set('_uuid', _uuid)

    # 获取aid,cid
    data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', resp1.text)
    # 转为字典
    data_dict = json.loads(data_list[0])
    aid = data_dict['aid']
    cid = data_dict['videoData']['cid']

    spi_url = 'https://api.bilibili.com/x/frontend/finger/spi'
    resp2 = session.get(spi_url)
    buvid4 = resp2.json()['data']['b_4']
    session.cookies.set('buvid4', buvid4)

    api_url = f'https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}'
    resp3 = session.get(
        url=api_url,
        params={
            'aid': aid,
            'cid': cid,
            'bvid': bvid
        })
    sid = resp3.cookies.get_dict()['sid']
    session.cookies.set('sid', sid)
    session.cookies.set('rpdid', "|(u)YRR)mku~0J'uYYRllRu~~")
    session.cookies.set('buvid_fp', 'bf8242df3c64fb172aa7a9e7786f85f8')

    # session_dict = session.cookies.get_dict()
    # col = ('buvid3', 'b_nut', 'CURRENT_FNVAL', 'b_lsid', '_uuid', 'buvid4', 'rpdid', 'buvid_fp', 'sid')
    # cookies = ';'.join([f'{i}={session_dict[i]}' for i in col])
    # # print(cookies)
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    #     'cookie': cookies
    # }
    return aid, cid, bvid, buvid4, session


def play(aid, cid, bvid, buvid4, session, proxies):
    ctime = int(time.time())
    resp = session.post(
        url='https://api.bilibili.com/x/click-interface/click/web/h5',
        # proxies=proxies,
        data={
            'aid': aid,
            'cid': cid,
            'part': '1',
            'lv': '0',
            'ftime': ctime - random.randint(100, 500),  # 浏览器首次打开时间
            'stime': ctime,
            'type': '3',
            'sub_type': '0',
            'refer_url': '',
            'spmid': '333.788.0.0',
            'from_spmid': '',
            'csrf': ''
        }
    )
    # print(resp.status_code)


def get_video_id_info(cid, bvid, session, proxies):
    # print(session.cookies.get_dict())
    url = f'https://api.bilibili.com/x/web-interface/view?cid={cid}&bvid={bvid}'
    # print(url)
    resp = session.get(
        url=url,
        # proxies=proxies
    )
    res_json = resp.json()
    # print(res_json)
    # 播放量
    view_count = res_json['data']['stat']['view']
    # 播放时长
    duration = res_json['data']['duration']
    print(f'bilibili视频：{bvid}: 平台播放量：{view_count}')

    return duration, view_count


def run():
    proxies = get_tunnel_proxies()
    # print(proxies)
    video_url = 'https://www.bilibili.com/video/BV1N94y1R7K5'
    aid, cid, bvid, buvid4, session = session_cookie(video_url, proxies)
    duration, view_count = get_video_id_info(cid, bvid, session, proxies)
    real_count = view_count
    while True:
        try:
            view_count = get_video_id_info(cid, bvid, session, proxies)[1]
            play(aid, cid, bvid, buvid4, session, proxies)
            time.sleep(1)
            if view_count == real_count:
                print('刷视频失败')
                time.sleep(2)
            else:
                real_count += 1
                print('刷视频成功')
                time.sleep(1)
            print('理论刷的播放量：', view_count)
        except Exception as e:
            print(f'出错啦：{e}')


if __name__ == '__main__':
    run()
