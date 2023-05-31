import re
import shutil

import csv

from lxml import etree
from parsel import Selector
from queue import Queue
import os
import sys
import time
import threading

import xlwt


class ReplaceKeywordsProducer(threading.Thread):
    def __init__(self, file_q, info_q):
        super().__init__()
        self.file_q = file_q
        self.info_q = info_q
        self.chart_set = 'utf-8'

    def get_content(self, fpath):
        f = open(rf'{fpath}', 'r', encoding=self.chart_set)
        content = f.read()
        f.close()
        return content.encode(self.chart_set)

    def parse_page(self, fpath):
        xml = self.get_content(fpath)
        xml_element = etree.XML(xml)
        object_element = xml_element.xpath('//annotation/object')
        if len(object_element) > 0:
            for obj in object_element:
                item = {
                    'file_path': fpath,
                    'name': obj.xpath('./name/text()')[0].strip(),
                    'dedescription': obj.xpath('./DeDescription/text()')[0].strip(),
                    'Serial': obj.xpath('./Serial/text()')[0].strip(),
                }
                self.info_q.put(item)
        else:
            print('当前文件没有object')

    def run(self):
        while True:
            if self.file_q.empty():
                break
            fpath = self.file_q.get()
            # print(fpath)
            self.parse_page(fpath)


class ReplaceKeywordsConsumer(threading.Thread):
    def __init__(self, info_q, b_dir, n_xml_dir):
        super().__init__()
        self.info_q = info_q
        self.base_dir = b_dir
        self.new_xml_dir = n_xml_dir
        self.chart_set = 'utf-8'

    def writer(self, info):
        if not os.path.exists(self.new_xml_dir):
            os.mkdir(self.new_xml_dir)
        xml_file_name = info['file_path']
        new_xml_file_path = self.new_xml_dir + '/' + xml_file_name.split('/')[-1]
        if not os.path.exists(new_xml_file_path):
            f1 = open(xml_file_name, 'r', encoding=self.chart_set)
        else:
            f1 = open(new_xml_file_path, 'r', encoding=self.chart_set)
        content = f1.read()
        # print(f'原来的文件: \n {content}')
        f1.close()
        obj1 = re.search(rf'(<Serial>{info["Serial"]}</Serial>.*?<name>.*?</name>)', content, re.S).group(1)
        obj2 = obj1.replace(f'<name>{info["name"]}</name>', f'<name>{info["dedescription"]}</name>')
        new_content = content.replace(obj1, obj2)
        # print(new_content)
        f2 = open(new_xml_file_path, 'w', encoding=self.chart_set)
        f2.write(new_content)
        f2.close()
        print(f'{new_xml_file_path}替换成功')

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info = self.info_q.get()
            self.writer(info)


if __name__ == '__main__':
    ti1 = time.time()
    xml_dir = '/XML文件'
    new_xml_dir = '/New_XML文件'
    base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
    # print(base_dir)

    xml_file_lst = os.listdir(base_dir + xml_dir)
    # # print(xml_file_lst)
    new_xml_dir_path = base_dir + new_xml_dir

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
        t1 = ReplaceKeywordsProducer(file_queue, info_queue)
        t1.start()
        p_lst.append(t1)
    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    # 创建五个消费者
    for j in range(1):
        t2 = ReplaceKeywordsConsumer(info_queue, base_dir, new_xml_dir_path)
        t2.start()

    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
