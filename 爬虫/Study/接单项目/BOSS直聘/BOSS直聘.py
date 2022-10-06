# 1、网站名称：BOSS直聘；网址：https://m.zhipin.com/shanghai/；
# 2、爬取数据示例：上海-徐汇区 数据分析助理
# 上海思勃商务咨询有限公司  20-99人  民营  6千-8千 本科  数据分析 不限
# 3、展示内容：
# （1）city（2）position（3）company_name（4）company_size（5）company_type（6）salary

import re

import xlwt
from lxml import etree
import threading
import time
import random
import collections

import requests
import urllib.request

from queue import Queue
import csv


class BossProducer(threading.Thread):
    header1 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Host': 'm.zhipin.com',
        'X-Requested-With': 'XMLHttpRequest',
        'zp_token': 'V1RNsjFef_3VhoVtRvyRkaLiOy7z3TzSk~',
        'Cookie': 'lastCity=101020100; wt2=D2fuRTdOG9iJjRRRI2QLfs4hovbi46diR6wQTSVI8SnjUVHnnzJYF0Fdz7XNkGdPT2AH4eQuYZuT1OLEIz_ttrA~~; wbg=0; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1662643216,1663086807,1663684580,1664276149; __zp_seo_uuid__=0e95bc86-bc60-4bc0-95b6-7d92582c1a4c; __l=r=https%3A%2F%2Fwww.bosszhipin.com%2F&l=%2Fm.zhipin.com%2Fjob_detail%2F%3Fcity%3D101020100%26source%3D10%26query%3DPython&s=3&friend_source=0&s=3&friend_source=0; geek_zp_token=V1RNsjFef_3VhoVtRvyRkaLiOy7z3TzSk~; __c=1664276149; __a=85089430.1656838200.1663684580.1664276149.70.10.18.70; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1664277697; __zp_stoken__=e468eGmEnPFhxFCVvXHcFbm4Xd3cjB3MSN1YxOwQmKhU5OllQej46SXt7VXoZDB4rQR9SdDA6N15WE14NDXYuSU1OdU4jU3J4JhBmQjJ1KH9ieBtWPDATJSEmZ1kQXVx8AyZgfT88XTxpVkU%3D'
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
        # https://m.zhipin.com/wapi/zpgeek/mobile/search/joblist.json?query=Python&page={i}&city=101020100&query=Python
        page = url.split('&')[-3].strip('page=')
        resp = requests.get(url, random.choice(self.proxies_dicts), headers=self.header1)
        job_list = resp.json()['zpData']['html']
        # print(job_list)
        resp.close()
        obj = re.compile(r'<li class="item">.*?<a href="(?P<href>.*?)" ka="(?P<ka>.*?)".*?data-lid="(?P<lid>.*?)".*?'
                         r'<span class="title-text">(?P<jobName>.*?)</span>.*?'
                         r'<span class="salary">(?P<salary>.*?)</span>.*?'
                         r'<span class="company">(?P<company_name>.*?)</span>.*?'
                         r'<span class="workplace">(?P<city>.*?)</span>.*?'
                         r'<div class="labels">(?P<labels>.*?)</div>.*?'
                         # r'<span>(?P<work_time>.*?)</span>.*?<span>(?P<diploma>.*?)</span>.*?'
                         # r'<span>(?P<skills>.*?)</div>.*?'
                         r'<div class="name">(?P<HR>.*?)</div>', re.S)

        lis = obj.finditer(job_list)
        for li in lis:
            href = li.group('href')
            ka = li.group('ka')
            lid = li.group('lid')
            url = f'https://m.zhipin.com{href}?ka={ka}_blank&lid={lid}'
            # location = self.location(url)
            item = collections.OrderedDict()
            # ('岗位名称', '薪资', '城市', '工作地址', '公司名称', '工作时间', '实习期', '学历', '技能', 'HR')
            item['岗位名称'] = li.group('jobName')
            item['薪资'] = li.group('salary')
            item['城市'] = li.group('city')
            # item['工作地址'] = location
            item['公司名称'] = li.group('company_name')
            labels = li.group('labels')
            element = etree.HTML(labels)
            spans = element.xpath('//span/text()')
            # print(len(spans))
            # print(spans)

            if '天' in spans[0]:
                item['工作时间'] = spans[0]
            else:
                item['工作时间'] = '面议'

            if '年' in spans[0] or '在校/应届' in spans[0] or '应届生' in spans[0] or '经验不限' in spans[0]:
                item['工作经验'] = spans[0]
            else:
                item['工作经验'] = '经验不限'

            if '个月' in spans[1]:
                item['实习期'] = spans[1]
            else:
                item['实习期'] = '面议'

            if '大专' in spans[1] or '本科' in spans[1] or '硕士' in spans[1]:
                item['学历'] = spans[1]
                index = 1
            elif '大专' in spans[2] or '本科' in spans[2] or '硕士' in spans[2]:
                item['学历'] = spans[2]
                index = 2
            else:
                item['学历'] = '学历不限'
                index = spans.index('学历不限')

            item['技能'] = ' '.join(spans[index + 1:])
            item['HR'] = li.group('HR')
            # print(item, page)
            self.info_q.put((item, page))

    def location(self, url):
        header2 = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Host': 'm.zhipin.com',
            'Referer': 'https://m.zhipin.com/job_detail/?city=101020100&source=10&query=Python',
            'Cookie': 'lastCity=101020100; wt2=D2fuRTdOG9iJjRRRI2QLfs4hovbi46diR6wQTSVI8SnjUVHnnzJYF0Fdz7XNkGdPT2AH4eQuYZuT1OLEIz_ttrA~~; wbg=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1662643216,1663086807,1663684580,1664276149; __zp_seo_uuid__=5a205884-b932-40a8-b30c-b10e600671f7; __g=-; JSESSIONID=222EAF6CFB51DA30EB2BBCC31C510358; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DfMnW-dsiYeHJKEFF1HKCHLP5HMaJ8fa6MTYjr-ga5li%26wd%3D%26eqid%3Db66d73ea0002249c000000036332e0cc&l=%2Fm.zhipin.com%2Fjob_detail%2Ff3012f6e780a730e1XZ53dy1EVtU.html%3Fka%3Djob_list_11_blank%26lid%3D1vbvrK4dMeN.search.11&s=3&g=&friend_source=0&s=3&friend_source=0; __c=1664276149; __a=85089430.1656838200.1663684580.1664276149.84.10.32.84; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1664288084; __zp_stoken__=e468eGmEnPFhxGyEiTHhubm4Xd3dhAzYQIVYxOwQmKhUFSDxcVT46SXt7GC9cGQ10QR9SdDA6LURVFxcNFloJK2kxNUwEXHV%2BGBZhQjJ1KH9ieERFKXVGaCEmZ1kQclx8AyZgfT88XTxpVkU%3D; geek_zp_token=V1RNsjFef_3VhoVtRvyRkaISO25Dzewyg~'
        }
        resp = requests.get(url, random.choice(self.proxies_dicts), headers=header2)
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)
        resp.close()
        html_element = etree.HTML(html)
        location = html_element.xpath('//div[@class="location-address"]/text()')[0]
        return location


class BossConsumer(threading.Thread):
    def __init__(self, info_q, s, cols):
        super().__init__()
        self.info_q = info_q
        self.cols = cols
        self.sheet = s

    def saveData1(self, lst):
        # print(len(lst))
        for m in range(len(lst)):
            page = eval(lst[m][0])
            data = lst[m][1]
            for n in range(len(data.values())):
                self.sheet.write(m + 1, n, data[self.cols[n]])

    def run(self):
        lst = []
        while True:
            if self.info_q.empty():
                break
            info, page = self.info_q.get()
            lst.append((page, info))
            # print(lst)
        self.saveData1(lst)


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    # with open('./全球免费代理.csv', 'r', encoding='utf-8') as f:
    #     csvreader = csv.DictReader(f)
    #     proxies_list = []
    #     for i in csvreader:
    #         proxies_list.append(i)
    #     f.close()
    # print(proxies_list)

    with open('./代理1.txt', 'r', encoding='utf-8') as f:
        proxies_list = []
        lines = f.readlines()
        for line in lines:
            proxies_list.append(eval(line))
        f.close()
    # print(proxies_list)

    header = {
        'Cache-Control': 'no - cache',
        'Content-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Date': 'Tue, 27 Sep 2022 15:57:06 GMT'
    }

    city_url = 'https://m.zhipin.com/wapi/zpCommon/data/city.json'
    resp = requests.get(city_url, headers=header)
    city_list = resp.json()['zpData']['cityList']
    city_lst = {}
    for city in city_list:
        city_lst[city['name']] = city['subLevelModelList'][0]['code']
    print(city_lst)

    query = input('请输入你要查询的岗位：')
    city = input('请输入城市：')

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('Python岗位信息', cell_overwrite_ok=True)
    col = ('岗位名称', '薪资', '城市', '公司名称', '工作时间', '工作经验', '实习期', '学历', '技能', 'HR')
    for c in range(len(col)):
        sheet.write(0, c, col[c])

    for i in range(1, 11):
        page_url = f'https://m.zhipin.com/wapi/zpgeek/mobile/search/joblist.json?' \
                   f'query={query}&page={i}&city={city_lst[city]}&query={query}'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(5):
        t1 = BossProducer(page_queue, info_queue, proxies_list)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(4):
        t2 = BossConsumer(info_queue, sheet, col)
        t2.start()
    book.save('./Boss直聘Python岗位信息.xls')
    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
