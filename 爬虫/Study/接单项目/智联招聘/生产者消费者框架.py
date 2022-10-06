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
import urllib.request

from queue import Queue
import csv
import xlwt


class BossProducer(threading.Thread):
    header1 = {
        'cookie': 'x-zp-client-id=c3db95ca-6291-4645-e4bc-027f04f01c91; urlfrom2=121114583; adfcid2=www.baidu.com; adfbid2=0; sts_deviceid=181c3a9a99f3c4-06f4b3ec73fca1-26021b51-1327104-181c3a9a9a053e; FSSBBIl1UgzbN7NO=5ZNa4TMOATlXipMIJ2d52UN.0__pL0JgCrl3xvg4TsOsjEJr4VHmBXKwXVOqjWNLIAoEcXdugYeY9qhbxXqsNoq; locationInfo_search={%22code%22:%22531%22%2C%22name%22:%22%E5%A4%A9%E6%B4%A5%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; selectCity_search=538; at=fedab1d719fc4f5abf73e35fbd5ec163; rt=8ffa90faf577403f8d8cdcada192d883; ZP_OLD_FLAG=false; campusOperateJobUserInfo=5246cc93-d498-44a0-9ab5-604313897264; LastCity=%E4%B8%8A%E6%B5%B7; LastCity%5Fid=538; acw_tc=2760829d16632254949578893e29fd0b77029c67674ef9df461168b878682c; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1662522328,1662561617,1663086918,1663225498; ssxmod_itna=QqRx2iG=DQoYqD50=DXDn7AIW8BCDcD41BjiOfx0vxYPGzDAxn40iDtr=kx18KU7+3idKAxnGefGm04dm3pGic4f8ADB3DEx0=NWGixiiyDCeDIDWeDiDG4GmB4GtDpxG=Djjtz1M6xYPDEjKDaxDbDin8pxGCDeKD0PwFDQKDu69qdjK+82Y1W3yDY8GxLxG1F40HGASIiU8LdA5+wF8GfWKDXEdDvO51M2PpDB+kl1HGABmqFi2okixYjQGxm7rr=h+oeBGxdi0DKxhqbAGxb1PnNqDWAw+K4D; ssxmod_itna2=QqRx2iG=DQoYqD50=DXDn7AIW8BCDcD41BjiO4nFfrxDsqddDLl7QybBbTqO6NqidtIx8hdd4TGMAhmqo8Dmdqn4SjKQLqF80GLeGe3rjxoUmjQYoCoikPbnuwW3E=Rx4xoyaehqGDvuCBIGKAQyQgN4ejN+4R4K=w3Lmf6WD7QvtuLO+hKk024tEgu8YCKYKDGcDijPeD==; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221131967883%22%2C%22first_id%22%3A%22181c3a859df22c-02b168b7bae3fa2-26021b51-1327104-181c3a859e06ee%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxYzNhODU5ZGYyMmMtMDJiMTY4YjdiYWUzZmEyLTI2MDIxYjUxLTEzMjcxMDQtMTgxYzNhODU5ZTA2ZWUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTMxOTY3ODgzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221131967883%22%7D%2C%22%24device_id%22%3A%22181c3a859df22c-02b168b7bae3fa2-26021b51-1327104-181c3a859e06ee%22%7D; ZL_REPORT_GLOBAL={%22//www%22:{%22seid%22:%22fedab1d719fc4f5abf73e35fbd5ec163%22%2C%22actionid%22:%22db25ade6-5daa-487d-8be9-8288aebbccb3-cityPage%22}%2C%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%2248968eb5-b0c0-4b8c-bf3d-3623ea158407-job%22}}; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1663226049; FSSBBIl1UgzbN7NP=53nhABCWP0hZqqqDkAq7vzqGxV0KQSP_5UROZWjwoVEaOpKvXDrMRResBhRiH4l6sammzXZDeDDzFC5wnBlmxpCmAPUEWHRxGrLzcvqtC8fHc534VSKafov7FdTrL3lAG3q4MQa9MB1DMGHW2l2maDXkMIGGXnZYhMtAyxdDdSmvY.upznoKJb23G_wMd6YY5iKUF8GhbuXCFqJzpAWmW_.ir7maztfMzVMEMA2rLd.oHP1kQSK.py3u2Ua5Iqzgkr2dEuliGjXovac25ctsPRbYfynUCXNwknGlKdnsoswAREQmF02t1Ob6QHiTPfwKy6hLDp4J.ZmWngeygvvUNZJ',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'referer': 'https://www.zhaopin.com/'
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
        html = resp.text
        # print(html)
        resp.close()
        html_element = etree.HTML(html)
        # print(html)
        # with open('./html.txt', 'w', encoding='utf-8') as f:
        #     f.write(html)
        job_list = html_element.xpath('//div[@class="positionlist"]/div[@class="joblist-box__item clearfix"]')
        # print(len(job_list))
        for job in job_list:
            # item.txt = {
            #     'jobName': ''.join(job.xpath('.//span[@class="iteminfo__line1__jobname__name"]//text()')),
            #     'position': job.xpath('.//div[@class="iteminfo__line2__jobdesc"]/ul/li[1]/text()')[0],
            #     'company_name': job.xpath('.//span[@class="iteminfo__line1__compname__name"]/text()')[0],
            #     'company_size': job.xpath('.//div[@class="iteminfo__line2__compdesc"]//text()')[-1],
            #     'company_type': job.xpath('.//div[@class="iteminfo__line2__compdesc"]//text()')[0],
            #     'salary': job.xpath('.//p[@class="iteminfo__line2__jobdesc__salary"]/text()')[0].replace('\n', '').strip(' ')
            # }
            # print(item.txt)
            # self.info_q.put(item.txt)

            job_info = []
            # 职位名称
            job_name = ''.join(job.xpath('.//span[@class="iteminfo__line1__jobname__name"]//text()'))
            job_info.append(job_name)
            # 公司地点
            position = job.xpath('.//div[@class="iteminfo__line2__jobdesc"]/ul/li[1]/text()')[0]
            job_info.append(position)
            # 工作时间
            work_time = job.xpath('.//div[@class="iteminfo__line2__jobdesc"]/ul/li[2]/text()')[0]
            job_info.append(work_time)
            # 文凭
            diploma = job.xpath('.//div[@class="iteminfo__line2__jobdesc"]/ul/li[3]/text()')[0]
            job_info.append(diploma)
            # 公司名称
            company_name = job.xpath('.//span[@class="iteminfo__line1__compname__name"]/text()')[0]
            job_info.append(company_name)
            # 公司规模
            company_size = job.xpath('.//div[@class="iteminfo__line2__compdesc"]//text()')[-1]
            job_info.append(company_size)
            # 公司类型
            company_type = job.xpath('.//div[@class="iteminfo__line2__compdesc"]//text()')[0]
            job_info.append(company_type)
            # 薪资
            salary = job.xpath('.//p[@class="iteminfo__line2__jobdesc__salary"]/text()')[0].replace('\n', '').strip(' ')
            job_info.append(salary)
            # 职业需求
            job_requirement = job.xpath('.//div[@class="iteminfo__line iteminfo__line3"]//div/text()')
            job_requirement = ' '.join(job_requirement).strip(' ')
            job_info.append(job_requirement)
            print(job_info)
            self.info_q.put(job_info)


class BossConsumer(threading.Thread):
    def __init__(self, info_q):
        super().__init__()
        self.info_q = info_q

    def saveData1(self, lst):
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('数据分析助理', cell_overwrite_ok=True)
        col = ('job_name', 'position', 'work_time', 'diploma', 'company_name', 'company_size', 'company_type', 'salary', 'job_requirement')
        for c in range(len(col)):
            sheet.write(0, c, col[c])
        for m in range(len(lst)):
            data = lst[m]
            for n in range(len(col)):
                sheet.write(m+1, n, data[n])
        book.save('./智联招聘.xls')
        # with open('./智联招聘.csv', 'w', encoding='utf-8-sig', newline='') as f1:
        #     csvwriter = csv.DictWriter(f1, col)  # 标题
        #     csvwriter.writeheader()  # 写入标题
        #     csvwriter.writerows(lst)  # 写入数据
        #     f1.close()
        #     print('保存完毕')
        # f1.close()

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

    with open('../BOSS直聘/全球免费代理.csv', 'r', encoding='utf-8') as f:
        csvreader = csv.DictReader(f)
        proxies_list = []
        for i in csvreader:
            proxies_list.append(i)
        f.close()
    print(proxies_list)

    for i in range(1, 12):
        page_url = f'https://sou.zhaopin.com/?jl=538&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%8A%A9%E7%90%86&p={i}'
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
    print(f'用时：{ti2-ti1}')


