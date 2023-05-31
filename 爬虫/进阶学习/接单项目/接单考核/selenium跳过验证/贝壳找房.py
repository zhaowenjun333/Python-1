# 目标网站：贝壳找房
# 需求：
# 采集杭州市新房楼盘数据
# 数据要求：
# 要贝壳网的楼盘数据，字段只需要楼盘名称，开发商名称，是否售罄再加上销售单价，楼盘性质。
# 预算：100
import re

import cv2
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib import request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium import webdriver
import threading
import time
import random

from chaojiying import Chaojiying_Client

import requests
from lxml import etree
from queue import Queue
import csv


class BeiKeProducer(threading.Thread):
    headers = [
        # Chrome
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'},
        # Microsoft Edge
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'},
        # 火狐
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/104.0'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/105.0'},
        # 360
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    ]

    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        # # 加载驱动
        # # 反爬
        # self.chrome_options = Options()
        # # 等效在cmd中：chrome --remote-debugging-port=9222
        # self.chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
        #
        # # 加载驱动
        # self.driver = webdriver.Chrome(options=self.chrome_options)
        #
        # # 显示等待
        # self.wait = WebDriverWait(self.driver, 100)
        # self.first_img = './img/one.png'
        # self.second_img = './img/two.png'

        # try:
        #     # 窗口最大化
        #     self.driver.maximize_window()
        # except Exception as e:
        #     print(e)

    def run(self):
        while True:
            if self.page_q.empty():
                break
            url = self.page_q.get()
            # print(url)
            self.parse_page(url)

    # def man_machine(self, url):
    #     # 打开目标网页
    #     self.driver.get(url)
    #     ros_but = self.wait.until(
    #         # 可以点击的元素,从0开始
    #         ec.element_to_be_clickable(
    #             (By.XPATH, '//div[@class="geetest_radar_btn"]')
    #         )
    #     )
    #     ros_but.click()
    #     time.sleep(1)
    #
    #     # 保存验证码图片
    #     # 截图
    #     first_tag = self.driver.find_element(By.CLASS_NAME, 'geetest_tip_img')
    #     first_tag.screenshot(self.first_img)
    #     second_tag = self.driver.find_element(By.CLASS_NAME, 'geetest_item_wrap')
    #     second_tag.screenshot(self.second_img)
    #
    #     chaojiying = Chaojiying_Client('17302254866', 'lry1730225', '937055')  # 用户中心>>软件ID 生成一个替换 96001
    #     # img = open('back_num.png', 'rb').read()                                       # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    #     img1 = open('./img/one.png', 'rb').read()
    #     words1 = list(chaojiying.PostPic(img1, 2004)['pic_str'])
    #     print(words1)
    #     img2 = open('./img/two.png', 'rb').read()
    #     words2_info = chaojiying.PostPic(img2, 9501)['pic_str'].split('|')
    #     item.txt = {}
    #     for word in words2_info:
    #         words = word.split(',')
    #         item.txt[words[0]] = [eval(words[1]) * 1.25 - 30, eval(words[2]) * 1.25 - 30]
    #     print(item.txt)
    #
    #     # 1. 实例化对象
    #     actions = ActionChains(self.driver)
    #     for word in words1:
    #         actions.move_to_element_with_offset(second_tag, item.txt[word][0], item.txt[word][1]).click()
    #         time.sleep(1)
    #         print(item.txt[word])
    #         # 3. 执行提交
    #     actions.perform()
    #
    #     self.driver.find_element(By.CLASS_NAME, 'geetest_commit_tip').click()

    def parse_page(self, url):
        resp = requests.get(url, headers=random.choice(self.headers))
        resp.encoding = 'utf-8'
        html = resp.text
        resp.close()
        html_element = etree.HTML(html)

        buildings = html_element.xpath('//ul[@class="resblock-list-wrapper"]/li')
        print(buildings)
        # if buildings:
        #     page = url.split('/')[-2].strip('pg')
        #     print(f'{url}\n第{page}页获取{len(buildings)}条\n')
        #
        #     for li in range(len(buildings)):
        #         # 楼盘名
        #         building_name = buildings[li].xpath('.//div[@class="resblock-name"]/a/text()')[0]
        #
        #         # 是否在售
        #         sale_situation = buildings[li].xpath('.//div[@class="resblock-name"]/span[1]/text()')[0]
        #
        #         # 楼盘性质
        #         building_property = buildings[li].xpath('.//div[@class="resblock-name"]/span[2]/text()')[0]
        #
        #         # 销售单价
        #         number = buildings[li].xpath('.//div[@class="main-price"]/span[@class="number"]/text()')[0]
        #         if number != '价格待定':
        #             if buildings[li].xpath('.//div[@class="second"]/text()'):
        #                 unit_selling_price = buildings[li].xpath('.//div[@class="second"]/text()')[0]
        #             else:
        #                 price = buildings[li].xpath('.//div[@class="main-price"]//span/text()')
        #                 unit_selling_price = ''.join(price).replace('\xa0', '')
        #         else:
        #             unit_selling_price = '价格待定'
        #
        #         # 开发商名称
        #         url = f'''https://hz.fang.ke.com{buildings[li].xpath('.//div[@class="resblock-name"]/a/@href')[0]}'''
        #         developer = self.parse_second(url)
        #         if eval(page) <= 19:
        #             num = li + (eval(page) - 1) * 10
        #         else:
        #             num = li + (eval(page) + (eval(page) - 20)) * 10
        #         item.txt = {
        #             '楼盘编号': num,
        #             '楼盘名称': building_name,
        #             '开发商名称': developer,
        #             '是否售空': sale_situation,
        #             '销售单价': unit_selling_price,
        #             '楼盘性质': building_property,
        #         }
        #         self.info_q.put(item.txt)
        #         print(f'管道：{self.info_q.qsize()}')
        #         print(item.txt)

    def parse_second(self, url):
        resp = requests.get(url, headers=random.choice(self.headers))
        resp.encoding = 'utf-8'
        html = resp.text
        resp.close()
        developer = re.match('vendor_corp: ".*?",', html).group()
        return developer

class BeiKeConsumer(threading.Thread):
    def __init__(self, info_q):
        super().__init__()
        self.info_q = info_q
        # self.f = open('./CSV/贝壳找房_杭州.csv', 'w+', encoding='utf-8-sig', newline='')
        # self.writer = csv.writer(self.f)
        # self.headers = ('楼盘名称', '开发商名称', '是否售空', '销售单价', '楼盘性质')
        # self.writer.writerow(self.headers)

    def saveData(self, lst):
        headers = ('楼盘编号', '楼盘名称', '开发商名称', '是否售空', '销售单价', '楼盘性质')
        with open('./CSV/贝壳找房_杭州.csv', 'w', encoding='utf-8-sig', newline='') as f:
            csvwriter = csv.DictWriter(f, headers)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            f.close()
            print('保存完毕')

    def run(self):
        lst = []
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            lst.append(info)
        self.saveData(lst)


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    for i in range(1, 2):
        page_url = f'https://hz.fang.ke.com/loupan/pg{i}/'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(20):
        t1 = BeiKeProducer(page_queue, info_queue)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    # for j in range(20):
    #     t2 = BeiKeConsumer(info_queue)
    #     t2.start()
    ti2 = time.time()
    print(f'用时：{ti2-ti1}')



