import shutil

import csv

from lxml import etree
from queue import Queue
import os
import sys
import time
import threading

import xlwt


class CountKeywordsProducer(threading.Thread):
    def __init__(self, file_q, info_q):
        super().__init__()
        self.file_q = file_q
        self.info_q = info_q
        self.chart_set = 'utf-8'

    def get_content(self, fpath):
        f = open(rf'{fpath}', 'r', encoding=self.chart_set)
        content = f.read()
        f.close()
        return content.encode('utf-8')

    def parse_page(self, fpath):
        xml = self.get_content(fpath)
        xml_element = etree.XML(xml)
        img_name = xml_element.xpath('//annotation/filename/text()')[0].strip()
        object_element = xml_element.xpath('//annotation/object')
        if len(object_element) > 0:
            # obj_num = len(object_element)
            # obj_dict = {}
            for obj in object_element:
                component = obj.xpath('./Component/text()')[0].strip()
                name = obj.xpath('./name/text()')[0].strip()
                part = obj.xpath('./Part/text()')[0].strip()
                dedescription = obj.xpath('./DeDescription/text()')[0].strip()
                defectlevel = obj.xpath('./DefectLevel/text()')[0].strip()
                obj_name = f'{component}_{name}_{part}_{dedescription}_{defectlevel}'
                # obj_dict[obj_name] = obj_dict.get(obj_name, 0) + 1
                self.info_q.put((img_name, obj_name))
            # print(obj_dict)
        else:
            print('当前文件没有object')

    def run(self):
        while True:
            if self.file_q.empty():
                break
            fpath = self.file_q.get()
            # print(fpath)
            self.parse_page(fpath)


class CountKeywordsConsumer(threading.Thread):
    def __init__(self, info_q, b_dir, i_dir, image_lst):
        super().__init__()
        self.info_q = info_q
        self.base_dir = b_dir
        self.image_dir = i_dir
        self.csv_dir = '/csv'
        self.image_file_lst = image_lst

    def save_data(self, obj_dict):
        header = ('name', 'count')
        csv_path = f'{self.base_dir}/{self.csv_dir}'
        if not os.path.exists(csv_path):
            os.mkdir(csv_path)
        with open('./csv/统计.csv', 'w', encoding='utf-8-sig', newline='') as f1:
            csvwriter = csv.writer(f1)  # 标题
            csvwriter.writerow(header)  # 写入标题

            for k, v in obj_dict.items():
                csvwriter.writerow((k, v))

    def copy_img(self, obj_name, img_name):
        if img_name in self.image_file_lst:
            img_path = f'{self.base_dir}{self.image_dir}/{img_name}'
            if '/' in obj_name:
                obj_name = obj_name.replace('/', '÷')
            obj_dir = f'{self.base_dir}/{obj_name}'

            if not os.path.exists(obj_dir):
                os.mkdir(obj_dir)
            shutil.copy(img_path, obj_dir)
        else:
            print(f'没有找到图片：{img_name}')

    def run(self):
        obj_dict = {}
        while True:
            if self.info_q.empty():
                break
            img_name, obj_name = self.info_q.get()
            obj_dict[obj_name] = obj_dict.get(obj_name, 0) + 1
            # print((img_name, obj_name))
            self.copy_img(obj_name, img_name)
            print(f'正在分类图片：{img_name}')

        print(obj_dict)
        self.save_data(obj_dict)


if __name__ == '__main__':
    ti1 = time.time()
    xml_dir = '/XML文件'
    image_dir = '/image'
    base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
    # print(base_dir)

    xml_file_lst = os.listdir(base_dir + xml_dir)
    # # print(xml_file_lst)
    image_file_lst = os.listdir(base_dir + image_dir)
    # print(image_file_lst)

    # 1. url存放到队列中
    file_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()

    for file_name in xml_file_lst:
        file_path = base_dir + xml_dir + '/' + file_name
        file_queue.put(file_path)

    p_lst = []
    # 创建五个生产者
    for i in range(10):
        t1 = CountKeywordsProducer(file_queue, info_queue)
        t1.start()
        p_lst.append(t1)
    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(1):
        t2 = CountKeywordsConsumer(info_queue, base_dir, image_dir, image_file_lst)
        t2.start()

    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
