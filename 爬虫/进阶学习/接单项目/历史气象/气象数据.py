# coding=utf-8
import json
import os
import sys
import re
import base64
import execjs
import xlwt
from lxml import etree
import threading
import time
import random
import collections

import requests
import urllib.request
from urllib.parse import urljoin
import urllib3

from queue import Queue
import csv

urllib3.disable_warnings()


class FindUrl:
    def __init__(self, url, s):
        self.citys_url = url
        self.session = s
        self.chart_set = 'utf-8'

    def get_content(self, url):
        resp = self.session.get(url, verify=False)
        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        html = resp.text
        resp.close()
        return html

    def parse_content(self, html):
        html_element = etree.HTML(html)
        city_lst_url = [urljoin(self.citys_url, u) for u in
                        html_element.xpath('//div[@class="all"]//ul[@class="unstyled"]/div/li/a/@href')]
        return city_lst_url

    def run(self):
        html = self.get_content(self.citys_url)
        city_lst_url = self.parse_content(html)
        return city_lst_url


class AQProducer(threading.Thread):
    def __init__(self, page_q, info_q, s, h, url):
        super().__init__()
        self.start_url = url
        self.page_q = page_q
        self.info_q = info_q
        self.session = s
        self.headers = h
        self.chart_set = 'utf-8'
        self.data_url = 'https://www.aqistudy.cn/historydata/api/historyapi.php'
        self.js_file = open('./JS/p1yD5oa6xy.js', 'r', encoding=self.chart_set)
        self.js_content = self.js_file.read()
        self.js_file.close()

        self.Hm_js_file = open('./JS/Hm.js', 'r', encoding=self.chart_set)
        self.Hm_js_compile = execjs.compile(self.Hm_js_file.read())
        self.Hm_js_file.close()

    def get_response(self, url, params=None, data=None):
        if data:
            if not params:
                resp = self.session.post(url, data=data)
            else:
                resp = self.session.post(url, params=params, data=data)
        else:
            if not params:
                resp = self.session.get(url, verify=False)
            else:
                resp = self.session.get(url, params=params)
        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        return resp

    def parse_data(self, js_code, city):
        key_name = re.search(r'data:.*?\{(.*?):.*?\}', js_code, re.S).group(1).strip()
        js_code = js_code + self.js_content
        # print(js_code)
        real_js_compile = execjs.compile(js_code)
        value_name = re.search(r'data:.*?\{.*?:(.*?)\}', js_code, re.S).group(1).strip()
        # print(value_name)
        re_compile = 'if.*?\(!.*?\).*?\{.*?var ' + value_name + '.*?=(.*?)\('
        # print(re_compile)
        # print(js_code)
        function_name = re.search(rf'{re_compile}', js_code, re.S).group(1).strip()
        # print(function_name)
        result = real_js_compile.call(function_name, 'GETMONTHDATA', {"city": city})
        data = {
            key_name: result
        }
        return data, real_js_compile, js_code, city

    def get_data(self, data):
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        # self.session.cookies.set('Hm_lvt_6088e7f72f5a363447d4bafe03026db8', "1680080490,1680157835,1680234802,1680236909")
        # self.session.cookies.set('Hm_lpvt_6088e7f72f5a363447d4bafe03026db8', self.Hm_js_compile.call('Hm_lpvt'))
        self.session.headers.update(self.headers)
        resp = self.get_response(self.data_url, None, data)
        data_code = resp.text
        resp.close()
        return data_code

    def second_parse_data(self, data_code, js_compile, js_code, city):
        function_name = re.search(r'success:.*?function.*?\(.*?\).*?\{.*?=(.*?)\(.*?\);', js_code, re.S).group(1)
        result = js_compile.call(function_name, data_code).encode('utf-8').decode('unicode_escape')
        # print(result)
        result = json.loads(result)
        # print(result)
        # ('Year', 'Month', 'AQI', 'Range', 'Air quality level', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3')
        for d in result['result']['data']['items']:
            d_time = d['time_point']
            item = {
                '城市名': city,
                'Year': d_time.split('-')[0],
                'Month': d_time.split('-')[1],
                'AQI': d['aqi'],
                'Range': f'{d["min_aqi"]}~{d["max_aqi"]}',
                'Air quality level': d['quality'],
                'PM2.5': d['pm2_5'],
                'PM10': d['pm10'],
                'SO2': d['so2'],
                'CO': d['co'],
                'NO2': d['no2'],
                'O3': d['o3']
            }
            # print(item)
            self.info_q.put(item)

    def parse_page(self, url):
        city = re.search(r'city=(\w+)', url, re.S).group(1)
        # print(city)
        resp1 = self.get_response(url, None, None)
        html1 = resp1.text
        resp1.close()
        html_element1 = etree.HTML(html1)
        real_script_url = html_element1.xpath('//script[contains(@src, "?t")]/@src')[0].strip()
        real_script_url = urljoin(self.start_url, real_script_url)
        # print(real_script_url)
        real_script_resp = self.get_response(real_script_url, None, None)
        html2 = real_script_resp.text
        real_script_resp.close()
        real_script_content = f'var func = {html2[4:]}'
        js_compile = execjs.compile(real_script_content)
        js_code = js_compile.eval('func')
        if 'const' not in js_code:
            js_code = re.search(r"eval\(.*?\('(.*?)'\)\)", js_code, re.S).group(1)
            while True:
                js_code = str(base64.b64decode(js_code), self.chart_set)
                if 'const' in js_code:
                    break
        data, real_js_compile, real_js_code, city = self.parse_data(js_code, city)
        data_code = self.get_data(data)
        self.second_parse_data(data_code, real_js_compile, real_js_code, city)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            self.parse_page(url)


class AQConsumer(threading.Thread):
    def __init__(self, info_q, writer):
        super().__init__()
        self.info_q = info_q
        self.csvwriter = writer

    def saveData1(self, lst):
        self.csvwriter.writerows(lst)

    def run(self):
        lst = []
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            print(info)
            lst.append(info)
        self.saveData1(lst)


if __name__ == '__main__':
    ti1 = time.time()
    start_url = 'https://www.aqistudy.cn/historydata/'
    col = ('城市名', 'Year', 'Month', 'AQI', 'Range', 'Air quality level', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3')

    data_filename = '全国气象数据.csv'
    base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
    data_dir = '/Data'
    data_dir_path = base_dir + data_dir
    if not os.path.exists(data_dir_path):
        os.mkdir(data_dir_path)
    data_file_path = f'{data_dir_path}/{data_filename}'
    f = open(data_file_path, 'w', encoding='utf-8', newline='')
    csvwriter = csv.DictWriter(f, col)
    csvwriter.writeheader()    # 写入标题

    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    session.headers.update(headers)
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    find_url = FindUrl(start_url, session)
    url_lst = find_url.run()
    # print(url_lst)

    for page_url in url_lst:
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(10):
        t1 = AQProducer(page_queue, info_queue, session, headers, start_url)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    c_lst = []
    for j in range(5):
        t2 = AQConsumer(info_queue, csvwriter)
        t2.start()
        c_lst.append(t2)
    for c in c_lst:
        c.join()

    f.close()
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
