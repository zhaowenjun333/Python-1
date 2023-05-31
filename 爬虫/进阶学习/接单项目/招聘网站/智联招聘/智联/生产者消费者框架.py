# 1、网站名称：BOSS直聘；网址：https://www.zhaopin.com/；
# 2、爬取数据示例：上海-徐汇区 数据分析助理
# 上海思勃商务咨询有限公司  20-99人  民营  6千-8千 本科  数据分析 不限
# 3、展示内容：
# （1）city（2）position（3）company_name（4）company_size（5）company_type（6）salary

import re
from lxml import etree
import threading
import time
import random
from urllib import parse

from lxml import etree

import requests
import urllib.request

from queue import Queue
import csv
import xlwt


class BossProducer(threading.Thread):

    def __init__(self, page_q, info_q, proxies_dicts, se):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        self.proxies_dicts = proxies_dicts
        self.session = se

    def run(self):
        while True:
            if self.page_q.empty():
                break
            ur = self.page_q.get()
            # print(url)
            self.parse_page(ur)

    def parse_page(self, ur):
        # self.session.proxies = random.choice(proxies_list)
        session.headers.update(random.choice(headers))
        resp1 = self.session.get(ur)
        # print(resp1.json())
        try:
            job_list = resp1.json()['data']['data']['list']
            # print(job_list)

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
        except Exception as e:
            re_url = re.match(
                f'https://xiaoyuan.zhaopin.com/api/sou\?S_SOU_FULL_INDEX=.*?&S_SOU_POSITION_SOURCE_TYPE=&pageIndex=(.*?)&S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY=(.*?)&.*?',
                ur, re.S)
            re_url_page = re_url.group(1)
            re_url_city = re_url.group(2)
            print(f'当前是报错的城市id:{re_url_city} ，是第{re_url_page}页')
            print(f'{ur}有问题：{e}')
            self.parse_page(ur)

        resp1.close()


class BossConsumer(threading.Thread):
    def __init__(self, info_q, writer):
        super().__init__()
        self.info_q = info_q
        self.writer = writer

    def saveData1(self, item):
        row = []
        for header in col:
            row.append(item[header])
        row = tuple(row)
        self.writer.writerow(row)

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            self.saveData1(info)


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}
    ]

    kw = input('请输入你要查询的岗位：')

    session = requests.Session()
    session.headers.update({
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    })
    url = f'https://xiaoyuan.zhaopin.com/search/jn=2&kw={kw}&pg=1'
    resp = session.get(url)

    at = '3c6c870340644ac4a4f7e55af7849b40'
    rt = '8d98e0a290e048d4acaa7f9b48d51768'
    sensorsdata2015jssdkcross = '%7B%22distinct_id%22%3A%221131967883%22%2C%22first_id%22%3A%22183d1cc11ed3f5-0795e0ad0df9f5c-26021f51-1327104-183d1cc11ef923%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZDFjYzExZWQzZjUtMDc5NWUwYWQwZGY5ZjVjLTI2MDIxZjUxLTEzMjcxMDQtMTgzZDFjYzExZWY5MjMiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTMxOTY3ODgzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221131967883%22%7D%2C%22%24device_id%22%3A%22183d1cc11ed3f5-0795e0ad0df9f5c-26021f51-1327104-183d1cc11ef923%22%7D'
    ZL_REPORT_GLOBAL = '{%22//www%22:{%22seid%22:%22ea3a641301bf421aafa28acaed0c1660%22%2C%22actionid%22:%2232c970de-5c93-42e2-beb4-cfb9c314bfd0-cityPage%22}}'
    Hm_lvt_38ba284938d5eddca645bb5e02a02006 = '1665933160'
    sajssdk_2015_cross_new_user = '1'

    session.cookies.set('at', at)
    session.cookies.set('rt', rt)
    session.cookies.set('sajssdk_2015_cross_new_user', sajssdk_2015_cross_new_user)
    session.cookies.set('sensorsdata2015jssdkcross', sensorsdata2015jssdkcross)
    # session.cookies.set('ZL_REPORT_GLOBAL', ZL_REPORT_GLOBAL)
    # session.cookies.set('Hm_lvt_38ba284938d5eddca645bb5e02a02006', Hm_lvt_38ba284938d5eddca645bb5e02a02006)

    x_zp_client_id = session.cookies.get_dict()['x-zp-client-id']

    with open('./代理.txt', 'r', encoding='utf-8') as f:
        proxies_list = [eval(i.strip(',\n')) for i in f.readlines()]
    #     print(proxies_list)

    # 531,533,543
    city_ids = {'北京': [530, 34], '天津': [531, 23], '河北': [532, 34], '山西': [533, 29], '内蒙古': [534, 9],
                '辽宁': [535, 30], '吉林': [536, 12], '黑龙江': [537, 10], '上海': [538, 34], '江苏': [539, 34],
                '浙江': [540, 34], '安徽': [541, 34], '福建': [542, 34], '江西': [543, 16], '山东': [544, 34],
                '河南': [545, 34], '湖北': [546, 34], '湖南': [547, 34], '广东': [548, 34], '广西': [549, 10],
                '海南': [550, 5], '重庆': [551, 18], '四川': [552, 34], '贵州': [553, 9], '云南': [554, 10],
                '西藏': [555, 2], '陕西': [556, 34], '甘肃': [557, 5], '青海': [558, 2], '宁夏': [559, 3],
                '新疆': [560, 4], '香港': [561, 1], '澳门': [562, 1], '台湾省': [563, 1]}

    for city in city_ids.values():
        for i in range(city[1] + 1):
            # page_url = f'https://xiaoyuan.zhaopin.com/api/sou?S_SOU_FULL_INDEX={parse.quote(kw)}&' \
            #            f'S_SOU_POSITION_SOURCE_TYPE=&pageIndex={i}&' \
            #            f'S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY={city[0]}&' \
            #            f'S_SOU_JD_INDUSTRY_LEVEL=&S_SOU_COMPANY_TYPE=&' \
            #            f'S_SOU_REFRESH_DATE=&order=12&pageSize=30&_v=0.45604219&' \
            #            f'at={at}&rt={rt}&' \
            #            f'x-zp-page-request-id=0786b3b5068b4b9e836df31b97289a3e-1665935479157-877476&' \
            #            f'x-zp-client-id={x_zp_client_id}'
            page_url = f'https://xiaoyuan.zhaopin.com/api/sou?S_SOU_FULL_INDEX={parse.quote(kw)}&' \
                       f'S_SOU_POSITION_SOURCE_TYPE=&pageIndex={i}&' \
                       f'S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY={city[0]}&' \
                       f'S_SOU_JD_INDUSTRY_LEVEL=&S_SOU_COMPANY_TYPE=&' \
                       f'S_SOU_REFRESH_DATE=&order=12&pageSize=30&_v=0.76037054&' \
                       f'at={at}&rt={rt}&' \
                       f'x-zp-page-request-id=54e2a817d018480ea132e27fdc01ae13-1665939414580-295611&' \
                       f'x-zp-client-id={x_zp_client_id}'
            page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = BossProducer(page_queue, info_queue, proxies_list, session)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    col = ('job_name', 'position',
           'diploma', 'company_name', 'company_size',
           'company_type', 'salary')

    f1 = open('智联校招.csv', 'w+', encoding='utf-8-sig', newline='')
    csvwriter = csv.writer(f1)  # 标题
    csvwriter.writerow(col)  # 写入标题
    session.close()

    # 创建五个消费者
    j_lst = []
    for j in range(1):
        t2 = BossConsumer(info_queue, csvwriter)
        t2.start()
        j_lst.append(t2)

    for j in j_lst:
        j.join()

    # f1.close()
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
