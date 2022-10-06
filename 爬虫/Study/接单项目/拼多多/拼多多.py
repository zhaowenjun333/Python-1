import re
from lxml import etree
import threading
import time
import random
import collections

import requests
import urllib.request
# url编码
from urllib import parse
from queue import Queue
import csv


class PDDProducer(threading.Thread):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'cookie': 'api_uid=CkoXwWM2j1HCqwBoWsuXAg==; _nano_fp=XpEjn0dxX09al0TbnT_FKEnPfISpfiiOdVg9VOkh; webp=1; dilx=kG12w5lMteFO~ha3txPVw; jrpl=RsdMDZOjYEMv4yvEoxDfUiWD9VXyG0oX; njrpl=RsdMDZOjYEMv4yvEoxDfUiWD9VXyG0oX; PDDAccessToken=M5NKENMJFEITZ4BSSHDKWOPO7IWCUNUX7GVLKIJCMAAWQ3JRA4OQ1122d90; pdd_user_id=4544664441389; pdd_user_uin=ZIQELYOS4MGDVI5W4T5K6K5TNY_GEXDA; rec_list_personal=rec_list_personal_lsncvy; pdd_vds=gaFLkOktZLcGviYiqQYbqEMirnFtkIYQWECIvbWaZbZmHtqtFyzIqECIvLCI'
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
        resp = requests.get(url, random.choice(self.proxies_dicts))
        goods_list = resp.json()
        print(goods_list)


class PDDConsumer(threading.Thread):
    def __init__(self, info_q, cols, csvw):
        super().__init__()
        self.info_q = info_q
        self.cols = cols
        self.csvwriter = csvw


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    with open('./全球免费代理.csv', 'r', encoding='utf-8') as f1:
        csvreader = csv.DictReader(f1)
        proxies_list = []
        for i in csvreader:
            proxies_list.append(i)
        f1.close()

    col = ('goods_name', 'sales_tip', 'price_info', 'tag_list')
    with open('./零食信息.csv', 'w+', encoding='utf-8-sig', newline='') as f2:
        csvwriter = csv.DictWriter(f2, col)
        csvwriter.writeheader()

    keyword = '零食'
    keyword = parse.quote(keyword)

    for i in range(1, 2):
        page_url = 'https://mobile.yangkeduo.com/proxy/api/search?pdduid=4544664441389&item_ver=lzqq&source=index&' \
                   'search_met=history&' \
                   'track_data=refer_page_id,10015_1664520729458_fbsnebmnsq%3Brefer_search_met_pos,0&' \
                   f'list_id=h3e7wrs9i4&sort=default&filter=&q={keyword}&page={i}&' \
                   f'is_new_query=1&size=50&flip=0%3B0%3B0%3B0%3B3f1bc108-6caf-b42d-0cd8-47b8e33e7a2e%3B%2F20%3B18%3B2%3B4ff9d1db9b4c6fd82c27bb53ea344217&' \
                   f'anti_content=0aqAfa5e-wCEBErPWAl3_DpeBkBnxaJ-eEaXra-Am4Y-eMVfmHpKSQX04iE75suE-ebqhtBLp-PAHuYFCvPhzALqT1UQ52uECX1RmqYgUwiEjIn25pFsyXhlNnDF5iX4iUeJI6NepIgqh42KE63lEV1e6r04kwk-lua9kFz3ShmT47OqGn3CWIk-uA410D-dra9wrToJRwFAX7_qQxE08VYXjXhQ12iqmaujg41VWUxQy4oV7-7Pn4ZsckpCCoWCWKc45fN2KIxdK22ASQ_9SUKxVHFWZCWUI2SEXoSt_USOOG7qNyQxHafykOXqghQpUYKquuGqHjvGY3nGgIlZ4itG_rntu6GtXMnHEmtekuz811Lz1Kkl1UL-EgE5Hk1F-31dnMmyfGbU1Gg3BqD5XqZUhxZ_KVg_zv21-yLWM3tHvKaW-Fwm1SOC3jiM8L62KbuD23xaZk-wHk-wCDBVck-VcEzFI1Be-e9PTnGPxnpPbc92SAPGbcjWdxHqtoHbMBhxQWnINIXxdMdnidqdn9PqNaGx_Nhvh9Gdp9YY0lovC9t-fFEty_E-zC1l2Ed3t_BKxe3e3DS-a1DLa-DtzVbAbpbRcCS3Bw-Kx1bKxeM38H1lBmd3AA-LVHk-lUeCt24mBfkEFg-vgc0wU_2kykATdKsVPsFES32_sfA_GxDO8OATfKMmgske1ej_FZLeeVjuUE6Y_SMBl9njLGdMX__qGGdA64TC_nC21Rf1EUfXsaXp9xnG_o7_0VM3YAdVjHkewFLl2AzlRz6s3uBltDD813UJXDEJtcrp6_6p71Z-YR8WJefFgRxAyF-eBeVEBw_SkOheFBAzY-8e8wCctcqeyF_ABfddF_cwYFVZvOFFzmV_Xq68WX49o2O8oU6pFMzYoj'
        page_queue.put(page_url)

    p_lst = []
    # 创建五个生产者
    for i in range(5):
        t1 = PDDProducer(page_queue, info_queue, proxies_list)
        t1.start()
        p_lst.append(t1)

    # 让生产者线程运行完
    for p in p_lst:
        p.join()


    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
