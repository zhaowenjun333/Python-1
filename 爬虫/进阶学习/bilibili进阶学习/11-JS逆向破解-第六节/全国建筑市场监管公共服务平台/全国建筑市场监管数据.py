import json
import time
import xlwt

import requests
import execjs

from queue import Queue
import threading


class BuildingCompany(threading.Thread):
    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q

        self.session = requests.session()
        self.headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,el;q=0.7,pl;q=0.6',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c=1678183535,1678423282; Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c=1678428261',
            'Host': 'jzsc.mohurd.gov.cn',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'timeout': '30000',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.node = execjs.get()
        self.js_filename = './JS/app.js'
        self.f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.node_compile = self.node.compile(self.f.read(), cwd=r'D:\应用缓存\npm_global\node_modules')
        self.f.close()

    def get_content(self, url):
        resp = self.session.get(url)
        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        content = resp.text
        resp.close()
        return content

    def parse_page(self, url, page):
        data = self.get_content(url)
        parse_data = json.loads(self.node_compile.call('h', data))
        # print(parse_data)
        for co in parse_data['data']['list']:
            try:
                item = {
                    '序号': co['RN'],
                    'ID': co['QY_ID'],
                    '统一社会信用代码': co['QY_ORG_CODE'],
                    '企业名称': co['QY_NAME'],
                    '企业法定代表人': co['QY_FR_NAME'],
                    '企业注册属地': co['QY_NAME'],
                    '企业注册属地编号': co['QY_REGION']
                }
                self.info_q.put(item)
            except Exception as e:
                # print(f'第{page}页编号{co["RN"]}数据有问题：{e}')
                # print(parse_data)
                item = {
                    '序号': co['RN'],
                    'ID': co['QY_ID'],
                    '统一社会信用代码': co['QY_ORG_CODE'],
                    '企业名称': co['QY_NAME'],
                    '企业法定代表人': '',
                    '企业注册属地': co['QY_NAME'],
                    '企业注册属地编号': co['QY_REGION']
                }
                self.info_q.put(item)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url, page = self.page_q.get()
            self.parse_page(url, page)


class BuildingCompanyConsumer(threading.Thread):
    def __init__(self, info_q, s, cols):
        super().__init__()
        self.info_q = info_q
        self.cols = cols
        self.sheet = s

    def saveData1(self, info):
        for n in range(len(self.cols)):
            self.sheet.write(info['序号'], n, info[self.cols[n]])

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            # print(info)
            self.saveData1(info)


if __name__ == '__main__':
    ti1 = time.time()

    # 写表头
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('全国建筑市场公司信息', cell_overwrite_ok=True)
    col = ('ID', '统一社会信用代码', '企业名称', '企业法定代表人', '企业注册属地', '企业注册属地编号')
    for c in range(len(col)):
        sheet.write(0, c, col[c])

    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    # https://jzsc.mohurd.gov.cn/Api/webApi/dataservice/query/comp/list?pg=0&pgsz=15&total=0
    for pg in range(30):
        page_url = f'https://jzsc.mohurd.gov.cn/Api/webApi/dataservice/query/comp/list?pg={pg}&pgsz=15&total=0'
        page_queue.put((page_url, pg))

    p_lst = []
    # 创建五个生产者
    for i in range(10):
        t1 = BuildingCompany(page_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(10):
        t2 = BuildingCompanyConsumer(info_queue, sheet, col)
        t2.start()
    book.save('./全国建筑市场信息.xlsx')

    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')

