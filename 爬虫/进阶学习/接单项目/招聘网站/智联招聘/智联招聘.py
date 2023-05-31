# 1、网站名称：BOSS直聘；网址：https://www.zhaopin.com/；
# 2、爬取数据示例：上海-徐汇区 数据分析助理
# 上海思勃商务咨询有限公司  20-99人  民营  6千-8千 本科  数据分析 不限
# 3、展示内容：
# （1）city（2）position（3）company_name（4）company_size（5）company_type（6）salary

import re
import threading
import time
import random
from lxml import etree

import requests
from urllib import parse

from queue import Queue
import csv
import xlwt


class BossProducer(threading.Thread):
    header1 = {
        'cookie': 'souJDJobLevel=%5B%7B%22name%22%3A%22IT%E6%8A%80%E6%9C%AF%22%2C%22code%22%3A%229000000000000%3B20000000000000%22%7D%2C%7B%22name%22%3A%22%E8%A1%8C%E6%94%BF%E8%B4%A2%E5%8A%A1%22%2C%22code%22%3A%2214000000000000%22%7D%2C%7B%22name%22%3A%22%E4%BA%A7%E5%93%81%2F%E9%A1%B9%E7%9B%AE%22%2C%22code%22%3A%223000000000000%22%7D%2C%7B%22name%22%3A%22%E6%88%BF%E5%9C%B0%E4%BA%A7%22%2C%22code%22%3A%227000000000000%22%7D%2C%7B%22name%22%3A%22%E7%AE%A1%E5%9F%B9%E7%94%9F%22%2C%22code%22%3A%228000000000000%22%7D%2C%7B%22name%22%3A%22%E6%9C%BA%E6%A2%B0%2F%E5%88%B6%E9%80%A0%22%2C%22code%22%3A%2215000000000000%22%7D%2C%7B%22name%22%3A%22%E5%B8%82%E5%9C%BA%2F%E8%BF%90%E8%90%A5%22%2C%22code%22%3A%225000000000000%3B16000000000000%22%7D%2C%7B%22name%22%3A%22%E9%94%80%E5%94%AE%22%2C%22code%22%3A%2219000000000000%22%7D%2C%7B%22name%22%3A%22%E9%87%91%E8%9E%8D%E4%BF%9D%E9%99%A9%22%2C%22code%22%3A%2212000000000000%22%7D%2C%7B%22name%22%3A%22%E5%85%B6%E4%BB%96%22%2C%22code%22%3A%2217000000000000%3B2000000000000%3B21000000000000%3B18000000000000%3B11000000000000%3B1000000000000%3B4000000000000%3B6000000000000%22%7D%5D; souJDIndustryLevel=%5B%7B%22name%22%3A%22%E4%BA%92%E8%81%94%E7%BD%91%2FIT%2F%E7%94%B5%E5%AD%90%2F%E9%80%9A%E4%BF%A1%22%2C%22code%22%3A%22100000000%22%7D%2C%7B%22name%22%3A%22%E6%88%BF%E5%9C%B0%E4%BA%A7%2F%E5%BB%BA%E7%AD%91%22%2C%22code%22%3A%22400000000%22%7D%2C%7B%22name%22%3A%22%E9%87%91%E8%9E%8D%E4%B8%9A%22%2C%22code%22%3A%22300000000%22%7D%2C%7B%22name%22%3A%22%E6%95%99%E8%82%B2%E5%9F%B9%E8%AE%AD%2F%E7%A7%91%E7%A0%94%22%2C%22code%22%3A%221200000000%22%7D%2C%7B%22name%22%3A%22%E5%B9%BF%E5%91%8A%2F%E4%BC%A0%E5%AA%92%2F%E6%96%87%E5%8C%96%2F%E4%BD%93%E8%82%B2%22%2C%22code%22%3A%22900000000%22%7D%2C%7B%22name%22%3A%22%E7%94%9F%E7%89%A9%E5%8C%BB%E8%8D%AF%2F%E5%8C%BB%E7%96%97%22%2C%22code%22%3A%221300000000%22%7D%2C%7B%22name%22%3A%22%E6%89%B9%E5%8F%91%2F%E9%9B%B6%E5%94%AE%2F%E8%B4%B8%E6%98%93%22%2C%22code%22%3A%22700000000%22%7D%2C%7B%22name%22%3A%22%E5%88%B6%E9%80%A0%E4%B8%9A%22%2C%22code%22%3A%22500000000%22%7D%2C%7B%22name%22%3A%22%E6%B1%BD%E8%BD%A6%22%2C%22code%22%3A%221600000000%22%7D%2C%7B%22name%22%3A%22%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2F%E4%BB%93%E5%82%A8%2F%E7%89%A9%E6%B5%81%22%2C%22code%22%3A%221000000000%22%7D%2C%7B%22name%22%3A%22%E4%B8%93%E4%B8%9A%E6%9C%8D%E5%8A%A1%22%2C%22code%22%3A%22800000000%22%7D%2C%7B%22name%22%3A%22%E7%94%9F%E6%B4%BB%E6%9C%8D%E5%8A%A1%22%2C%22code%22%3A%221500000000%22%7D%2C%7B%22name%22%3A%22%E8%83%BD%E6%BA%90%2F%E7%8E%AF%E4%BF%9D%2F%E7%9F%BF%E4%BA%A7%22%2C%22code%22%3A%221100000000%22%7D%2C%7B%22name%22%3A%22%E6%94%BF%E5%BA%9C%2F%E9%9D%9E%E7%9B%88%E5%88%A9%E6%9C%BA%E6%9E%84%22%2C%22code%22%3A%221400000000%22%7D%2C%7B%22name%22%3A%22%E5%86%9C%2F%E6%9E%97%2F%E7%89%A7%2F%E6%B8%94%22%2C%22code%22%3A%22600000000%22%7D%5D; souJDCompanyLevel=%5B%7B%22name%22%3A%22%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%22%2C%22code%22%3A%229%22%7D%2C%7B%22name%22%3A%22%E5%9B%BD%E4%BC%81%22%2C%22code%22%3A%221%22%7D%2C%7B%22name%22%3A%22%E5%A4%96%E4%BC%81%22%2C%22code%22%3A%222%3B4%22%7D%2C%7B%22name%22%3A%22%E6%B0%91%E4%BC%81%22%2C%22code%22%3A%225%22%7D%2C%7B%22name%22%3A%22%E8%82%A1%E4%BB%BD%E5%88%B6%E4%BC%81%E4%B8%9A%22%2C%22code%22%3A%228%22%7D%2C%7B%22name%22%3A%22%E6%9C%BA%E5%85%B3%2F%E4%BA%8B%E4%B8%9A%E5%8D%95%E4%BD%8D%22%2C%22code%22%3A%226%3B10%22%7D%2C%7B%22name%22%3A%22%E5%85%B6%E4%BB%96%22%2C%22code%22%3A%223%3B7%3B11%3B12%3B13%3B14%3B15%22%7D%5D; x-zp-client-id=c3db95ca-6291-4645-e4bc-027f04f01c91; urlfrom2=121114583; adfcid2=www.baidu.com; adfbid2=0; sts_deviceid=181c3a9a99f3c4-06f4b3ec73fca1-26021b51-1327104-181c3a9a9a053e; locationInfo_search={%22code%22:%22531%22%2C%22name%22:%22%E5%A4%A9%E6%B4%A5%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; selectCity_search=538; campusOperateJobUserInfo=5246cc93-d498-44a0-9ab5-604313897264; Hm_lvt_d7ede48beea78a2945672aed33b15da7=1663089187; ssxmod_itna2=QqRx2iG=DQoYqD50=DXDn7AIW8BCDcD41BjiO4nFfrxDsqddDLl7QybBbTqO6NqidtIx8hdd4TGMAhmqo8Dmdqn4SjKQLqF80GLeGe3rjxoUmjQYoCoikPbnuwW3E=Rx4xoyaehqGDvuCBIGKAQyQgN4ejN+4R4K=w3Lmf6WD7QvtuLO+hKk024tEgu8YCKYKDGcDijPeD==; BEST_EMPLOYER_SHOW_TIME=[1663556029262]; ssxmod_itna=YqUx0DnDBAoewqBPbSD97xuACOQY5d5G8+fDBwQ4iNDnD8x7YDv+zHQ+KQKK=WYCRHKTwlCbhPev/l20o4itZQq4eI+DB3DEx06Qq+AY4GGIxBYDQxAYDGDDPDocPD1D3qDkD7EZlMBsqDEDYp9DA3Di4D+8MQDmqG0DDUF94G2D7U9j7v9WCd56ubSRirY8qDM0eGXKOaq8TbF1cD/WjWYKlmuDB=zxBQljLXUjeDHGuXlKWvpKBfCK7jrboq5WBqeQ0wLK7vNK0xq/Yq+WAGiCY3jRE1xD; LastCity=%E4%B8%8A%E6%B5%B7; LastCity%5Fid=538; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1663086918,1663225498,1663556214,1663813686; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221131967883%22%2C%22first_id%22%3A%22181c3a859df22c-02b168b7bae3fa2-26021b51-1327104-181c3a859e06ee%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxYzNhODU5ZGYyMmMtMDJiMTY4YjdiYWUzZmEyLTI2MDIxYjUxLTEzMjcxMDQtMTgxYzNhODU5ZTA2ZWUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTMxOTY3ODgzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221131967883%22%7D%2C%22%24device_id%22%3A%22181c3a859df22c-02b168b7bae3fa2-26021b51-1327104-181c3a859e06ee%22%7D; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1663814090; ZL_REPORT_GLOBAL={%22//www%22:{%22seid%22:%22%22%2C%22actionid%22:%22accdbd3a-18f8-4c51-a381-7b5e4f159ef2-cityPage%22}%2C%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%22f1f03fa9-a164-43cc-b9b9-a7a6e9868dda-job%22}}; zp_passport_deepknow_sessionId=5b2878das1fe9d41e18198a11865e76d5eaf; at=c26f7a1209024a2a90937a11b366242b; rt=6a5483e0b17f46ae9fa197581ca2008a; acw_tc=276077ca16638142237181799eff952a1db894a13bcf270f5d6f51897c52e6; acw_sc__v2=632bcafa5322821e0ec41412f8e105199c32e63b',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    header2 = {
        'cookie': 'x-zp-client-id=c3db95ca-6291-4645-e4bc-027f04f01c91; urlfrom2=121114583; adfcid2=www.baidu.com; adfbid2=0; sts_deviceid=181c3a9a99f3c4-06f4b3ec73fca1-26021b51-1327104-181c3a9a9a053e; locationInfo_search={%22code%22:%22531%22%2C%22name%22:%22%E5%A4%A9%E6%B4%A5%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; selectCity_search=538; campusOperateJobUserInfo=5246cc93-d498-44a0-9ab5-604313897264; Hm_lvt_d7ede48beea78a2945672aed33b15da7=1663089187; ssxmod_itna2=QqRx2iG=DQoYqD50=DXDn7AIW8BCDcD41BjiO4nFfrxDsqddDLl7QybBbTqO6NqidtIx8hdd4TGMAhmqo8Dmdqn4SjKQLqF80GLeGe3rjxoUmjQYoCoikPbnuwW3E=Rx4xoyaehqGDvuCBIGKAQyQgN4ejN+4R4K=w3Lmf6WD7QvtuLO+hKk024tEgu8YCKYKDGcDijPeD==; BEST_EMPLOYER_SHOW_TIME=[1663556029262]; ssxmod_itna=YqUx0DnDBAoewqBPbSD97xuACOQY5d5G8+fDBwQ4iNDnD8x7YDv+zHQ+KQKK=WYCRHKTwlCbhPev/l20o4itZQq4eI+DB3DEx06Qq+AY4GGIxBYDQxAYDGDDPDocPD1D3qDkD7EZlMBsqDEDYp9DA3Di4D+8MQDmqG0DDUF94G2D7U9j7v9WCd56ubSRirY8qDM0eGXKOaq8TbF1cD/WjWYKlmuDB=zxBQljLXUjeDHGuXlKWvpKBfCK7jrboq5WBqeQ0wLK7vNK0xq/Yq+WAGiCY3jRE1xD; LastCity=%E4%B8%8A%E6%B5%B7; LastCity%5Fid=538; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1663086918,1663225498,1663556214,1663813686; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221131967883%22%2C%22first_id%22%3A%22181c3a859df22c-02b168b7bae3fa2-26021b51-1327104-181c3a859e06ee%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxYzNhODU5ZGYyMmMtMDJiMTY4YjdiYWUzZmEyLTI2MDIxYjUxLTEzMjcxMDQtMTgxYzNhODU5ZTA2ZWUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTMxOTY3ODgzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221131967883%22%7D%2C%22%24device_id%22%3A%22181c3a859df22c-02b168b7bae3fa2-26021b51-1327104-181c3a859e06ee%22%7D; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1663814090; ZL_REPORT_GLOBAL={%22//www%22:{%22seid%22:%22%22%2C%22actionid%22:%22accdbd3a-18f8-4c51-a381-7b5e4f159ef2-cityPage%22}%2C%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%22f1f03fa9-a164-43cc-b9b9-a7a6e9868dda-job%22}}; zp_passport_deepknow_sessionId=5b2878das1fe9d41e18198a11865e76d5eaf; at=c26f7a1209024a2a90937a11b366242b; rt=6a5483e0b17f46ae9fa197581ca2008a; acw_tc=276077e016638162584993589e543630fd398fa4f9223abd7716bb9907f549; acw_sc__v2=632bd242c4c2a0b4dc78e766ea8ab9bb407b33e6',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    def __init__(self, page_q, info_q, proxies_dicts):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        self.proxies_dicts = proxies_dicts

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            # print(url)
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, random.choice(self.proxies_dicts), headers=self.header1)
        resp.encoding = 'utf-8'
        job_list = resp.json()['data']['data']['list']
        # print(job_list)
        resp.close()
        for job in job_list:
            item = {
                # 职位名称
                'job_name': job['name'],
                # 公司地点
                'position': job['workCity'],
                # 文凭
                'diploma': job['education'],
                # 公司名称
                'company_name': job['companyName'],
                # 公司规模
                'company_size': job['companySize'],
                # 公司类型
                'company_type': job['property'],
                # 薪资
                'salary': job['salary60'],
            }
            print(item)
            self.info_q.put(item)
            print(self.info_q.qsize())


class BossConsumer(threading.Thread):
    def __init__(self, info_q):
        super().__init__()
        self.info_q = info_q

    def saveData1(self, item):
        # book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # sheet = book.add_sheet('数据分析助理', cell_overwrite_ok=True)
        print(item)

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            self.saveData1(info)
            # lst.append(info)
        # print(lst)
        # self.saveData1(lst)


if __name__ == '__main__':
    ti1 = time.time()
    kw = input('请输入你要查询的岗位：')
    city_id = input('请输入城市id：')
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    with open('./全球免费代理.csv', 'r', encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        proxies_list = []
        for i in csvreader:
            proxies_list.append(i)
        f.close()
    # print(proxies_list)

    col = ('job_name', 'position',
           'diploma', 'company_name', 'company_size',
           'company_type', 'salary')
    with open('智联校招new.csv', 'w', encoding='utf-8-sig', newline='') as f1:
        csvwriter = csv.DictWriter(f1, col)  # 标题
        csvwriter.writeheader()  # 写入标题

    for i in range(1, 35):
        page_url = f'https://xiaoyuan.zhaopin.com/api/sou?S_SOU_FULL_INDEX={parse.quote(kw)}&' \
                   f'S_SOU_POSITION_SOURCE_TYPE=&pageIndex={i}&' \
                   f'S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY={city_id}&' \
                   f'S_SOU_JD_INDUSTRY_LEVEL=&S_SOU_COMPANY_TYPE=&' \
                   f'S_SOU_REFRESH_DATE=&order=12&pageSize=30&_v=0.36212744&' \
                   f'at=d065c80aa7c84d28a89f2a5a2bb70b37&rt=9a9999d4f70543928178d7c879968984&' \
                   f'x-zp-page-request-id=5c537cd731424e02875891a1aa46d643-1665672564904-479503' \
                   f'&x-zp-client-id=19c1f885-8e1e-459c-b827-8d17ffa99bb0'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = BossProducer(page_queue, info_queue, proxies_list)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(1):
        t2 = BossConsumer(info_queue)
        t2.start()
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')


