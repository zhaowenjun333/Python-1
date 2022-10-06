import requests
import json
import re

# 视频链接：https://www.bilibili.com/video/BV1N94y1R7K5

# h5是自动播放的
# https://api.bilibili.com/x/click-interface/click/web/h5

url = 'https://www.bilibili.com/video/BV1N94y1R7K5/'

# data = {
#     'aid': '342971613',
#     'cid': '758255562',
#     'part': '1',
#     'lv': '0',
#     'ftime': '1664431462',
#     'stime': '1664431462',
#     'type': '3',
#     'sub_type': '0',
#     'refer_url': '',
#     'spmid': '333.788.0.0',
#     'from_spmid': '',
#     'csrf': '',
# }

resp = requests.get(url)

# 读取cookie
print(resp.cookies.get_dict())
'''
    .: 出换行符以外的所有字符
    +: 一个或多个
'''
data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', resp.text)
# 转为字典
data_dict = json.loads(data_list[0])

aid = data_dict['aid']
cid = data_dict['videoData']['cid']

print(aid)
print(cid)

resp.close()
