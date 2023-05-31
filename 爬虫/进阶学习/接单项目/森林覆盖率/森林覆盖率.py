import requests

import time
import random

import csv
import xlwt
from selenium import webdriver
from queue import Queue
import threading

import re
from lxml import etree


class GetCookies:
    def __init__(self):
        self.start_url = 'https://data.stats.gov.cn/easyquery.htm?cn=E0103&zb=A0C0A&reg=410000&sj=2011'
        self.headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,el;q=0.7,pl;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'data.stats.gov.cn',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        self.cookies = ''

    def chrome_driver(self):
        # s = input('请先在cmd中打开, 然后输入yes:')
        s = 'y'
        options = webdriver.ChromeOptions()
        if s.lower() == 'y':
            # 方式一
            # 等效在cmd中执行：chrome --remote-debugging-port=9222
            options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
            # options.add_argument('--headless')
            chrome_driver = webdriver.Chrome(chrome_options=options)
        else:
            # 方式二
            # proxy = 'http://104.223.212.161:65432'
            # options.add_argument('--headless')
            # options.add_argument(f'--proxy-server={proxy}')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument(f'user-agent={self.headers["User-Agent"]}')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('disable-infobars')
            options.add_argument("service_args = ['–ignore - ssl - errors = true', '–ssl - protocol = TLSv1']")
            chrome_driver = webdriver.Chrome(chrome_options=options)
            chrome_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
            })
        return chrome_driver

    def driver_get_cookies(self):
        driver = self.chrome_driver()
        driver.get(self.start_url)
        cookies = driver.get_cookies()
        # for cookie in cookies:
        #     self.session.cookies.set(cookie['name'], cookie['value'])
        driver.close()
        driver.quit()
        return cookies

    def run(self):
        self.cookies = self.driver_get_cookies()


class ForestCoverageProducer(threading.Thread):
    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        self.session = requests.session()
        self.headers = {
            'Cookie': 'wzws_sessionid=gDIyMi42Ny4yMzYuMTQ2gTJjZTFmZIJmYzVlZTGgZAm/dA==; wzws_cid=4bc10e4337eecc2678865d6dcbb9348cf515f1848bfe144b37fbe0d9ac06703583638ee6b486e1262c5fd91d1f01d56ac916739dcc9223e25e40c34b845fef8768d65deeae68dc39a95addae8f859bde; JSESSIONID=4A7GE4EyxAPcsJ9_9nQhXGm2ni39NyM9Zh_A4jYwjttGotmInwIt!-278686416; u=2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

    def get_content(self, url, referer, cook):
        self.headers['Referer'] = referer
        self.headers['Cookie'] = cook
        self.session.headers.update(self.headers)
        resp = self.session.get(url, verify=False)
        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        content = resp.json()
        resp.close()
        return content

    def parse_page(self, url, cname, y, referer, cook, pos):
        try:
            content = self.get_content(url, referer, cook)
            items = content['returndata']['datanodes']
            num = len(items)
            if num == 6:
                item = {
                    '城市': cname,
                    '年份': y,
                    '林业用地面积(万公顷)': items[0]['data']['data'],
                    '森林面积(万公顷)': items[1]['data']['data'],
                    '人工林面积(万公顷)': items[2]['data']['data'],
                    '森林覆盖率(%)': items[3]['data']['data'],
                    '活立木总蓄积量(亿立方米)': items[4]['data']['data'],
                    '森林蓄积量(亿立方米)': items[5]['data']['data'],
                }
                self.info_q.put((item, pos))
                print(cname, y, item)
                print('\n')
        except Exception as e:
            print(f'{cname}-{y}-没有数据', e)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            cname, y, url, referer, cook, pos = self.page_q.get()
            self.parse_page(url, cname, y, referer, cook, pos)


class ForestCoverageConsumer(threading.Thread):
    def __init__(self, info_q, s, cols):
        super().__init__()
        self.info_q = info_q
        self.cols = cols
        self.sheet = s

    def saveData1(self, info, pos):
        for n in range(len(info.values())):
            self.sheet.write(pos, n, info[self.cols[n]])

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info, pos = self.info_q.get()
            self.saveData1(info, pos)


if __name__ == '__main__':
    ti1 = time.time()

    # 写表头
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('2011-2021城市森林资源数据', cell_overwrite_ok=True)
    col = ('城市', '年份', '林业用地面积(万公顷)', '森林面积(万公顷)', '人工林面积(万公顷)', '森林覆盖率(%)', '活立木总蓄积量(亿立方米)', '森林蓄积量(亿立方米)')
    for c in range(len(col)):
        sheet.write(0, c, col[c])

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    get_cookies = GetCookies()
    get_cookies.run()
    cookies = get_cookies.cookies
    cookies = '; '.join(['='.join([cookie['name'], cookie['value']]) for cookie in cookies])
    print(cookies)
    # https://data.stats.gov.cn/easyquery.htm?cn=E0103&zb=A0C0A&reg=410000&sj=2011
    city_info = {'北京': {'reg': '110000'}, '天津': {'reg': '120000'}, '河北': {'reg': '130000'},
                 '山西': {'reg': '140000'}, '内蒙古': {'reg': '150000'}, '辽宁': {'reg': '210000'},
                 '吉林': {'reg': '220000'}, '黑龙江': {'reg': '230000'}, '上海': {'reg': '310000'},
                 '江苏': {'reg': '320000'}, '浙江': {'reg': '330000'}, '安徽': {'reg': '340000'},
                 '福建': {'reg': '350000'}, '江西': {'reg': '360000'}, '山东': {'reg': '370000'},
                 '河南': {'reg': '410000'}, '湖北': {'reg': '420000'}, '湖南': {'reg': '430000'},
                 '广东': {'reg': '440000'}, '广西': {'reg': '450000'}, '海南': {'reg': '460000'},
                 '重庆': {'reg': '500000'}, '四川': {'reg': '510000'}, '贵州': {'reg': '520000'},
                 '云南': {'reg': '530000'}, '西藏': {'reg': '540000'}, '陕西': {'reg': '610000'},
                 '甘肃': {'reg': '620000'}, '青海': {'reg': '630000'}, '宁夏': {'reg': '640000'},
                 '新疆': {'reg': '650000'}}

    # k1 = str(time.time()*1000)
    position = 1
    for city_name, city_reg in city_info.items():
        for year in range(2011, 2022):
            page_url = f'https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22reg%22%2C%22valuecode%22%3A%22{city_reg["reg"]}%22%7D%5D&dfwds=%5B%5D'
            referer_url = f'https://data.stats.gov.cn/easyquery.htm?cn=E0103&zb=A0C0A&reg={city_reg["reg"]}&sj={year}'
            page_queue.put((city_name, year, page_url, referer_url, cookies, position))
            position += 1

    p_lst = []
    # 创建五个生产者
    for i in range(5):
        t1 = ForestCoverageProducer(page_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(5):
        t2 = ForestCoverageConsumer(info_queue, sheet, col)
        t2.start()
    book.save('./2011-2021年城市森林资源数据.xlsx')

    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
