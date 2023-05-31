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

from selenium import webdriver
import string
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
import requests
import urllib.request
import re
from queue import Queue
import csv
import xlwt


class ZhiLianProducer(threading.Thread):
    headers = {
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,el;q=0.7,pl;q=0.6',
        'cache-control': 'max-age=0',
        'referer': 'https://sou.zhaopin.com/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        self.start_url = 'https://sou.zhaopin.com/'
        self.session = requests.session()
        self.session.headers.update(self.headers)

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
            proxy = 'http://104.223.212.161:65432'
            # options.add_argument('--headless')
            # options.add_argument(f'--proxy-server={proxy}')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument(f'user-agent={self.headers["user-agent"]}')
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
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        driver.close()
        driver.quit()

    def run(self):
        self.driver_get_cookies()
        while True:
            if self.page_q.empty():
                break
            url, c_name, p_num = self.page_q.get()
            # print(url)
            self.parse_page(url, c_name, p_num)

    def parse_page(self, url, c_name, p_num):
        resp = self.session.get(url)
        resp.encoding = resp.apparent_encoding
        html = resp.text
        resp.close()
        html_element = etree.HTML(html)
        job_list = html_element.xpath('//div[@class="positionlist"]/div[@class="joblist-box__item clearfix"]')
        # print(len(job_list))
        if job_list:
            for job in job_list:
                item = {
                    'jobName': job.xpath('.//div[@class="iteminfo__line1__jobname"]/span/@title')[0].strip(),
                    'position': job.xpath('.//ul/li[1]/text()')[0].strip(),
                    'company_name': job.xpath('.//span[@class="iteminfo__line1__compname__name"]/@title')[0].strip(),
                    'company_size': job.xpath('.//div[@class="iteminfo__line2__compdesc"]/span[last()]/text()')[0].strip(),
                    'company_type': job.xpath('.//div[@class="iteminfo__line2__compdesc"]//text()')[0].strip(),
                    'salary': ''.join([m.replace('\n', '').strip() for m in job.xpath('.//p[@class="iteminfo__line2__jobdesc__salary"]//text()')])
                }
                print(item)
                self.info_q.put(item)
        else:
            print(f'{c_name}的第{p_num}页没有符合你要查找的岗位信息！！！')


class BossConsumer(threading.Thread):
    def __init__(self, info_q):
        super().__init__()
        self.info_q = info_q

    def saveData1(self, lst):
        # book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # sheet = book.add_sheet('数据分析助理', cell_overwrite_ok=True)
        col = ('jobName', 'position', 'company_name', 'company_size', 'company_type', 'salary')
        with open('智联招聘.csv', 'w', encoding='utf-8-sig', newline='') as f1:
            csvwriter = csv.DictWriter(f1, col)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            f1.close()
            print('保存完毕')
        f1.close()

    def run(self):
        lst = []
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            lst.append(info)
        print(lst)
        self.saveData1(lst)


if __name__ == '__main__':
    ti1 = time.time()

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    city_ids = {'北京': [530, 34], '天津': [531, 23], '河北': [532, 34], '山西': [533, 29], '内蒙古': [534, 9],
                '辽宁': [535, 30], '吉林': [536, 12], '黑龙江': [537, 10], '上海': [538, 34], '江苏': [539, 34],
                '浙江': [540, 34], '安徽': [541, 34], '福建': [542, 34], '江西': [543, 16], '山东': [544, 34],
                '河南': [545, 34], '湖北': [546, 34], '湖南': [547, 34], '广东': [548, 34], '广西': [549, 10],
                '海南': [550, 5], '重庆': [551, 18], '四川': [552, 34], '贵州': [553, 9], '云南': [554, 10],
                '西藏': [555, 2], '陕西': [556, 34], '甘肃': [557, 5], '青海': [558, 2], '宁夏': [559, 3],
                '新疆': [560, 4], '香港': [561, 1], '澳门': [562, 1], '台湾省': [563, 1]}

    # print(proxies_list)
    for city_name, city_id in city_ids.items():
        for page in range(1, 2):
            page_url = f'https://sou.zhaopin.com/?jl={city_id[0]}&kw=数据分析助理&p={page}'
            page_queue.put((page_url, city_name, page))

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = ZhiLianProducer(page_queue, info_queue)
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
    print(f'用时：{ti2-ti1}')


