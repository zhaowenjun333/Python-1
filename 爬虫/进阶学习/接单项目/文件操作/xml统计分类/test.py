import shutil

import csv

from parsel import Selector
from queue import Queue
import os
import sys
import time
import threading

import xlwt


filename_path = 'D:\\pythonProject\\xml统计分类/XML文件/10kV _ 白店线 _ 6号杆塔 _ 塔顶破损 _ 一般-20211021135152533.xml'
f1 = open(filename_path, 'r', encoding='utf-8')
content = f1.read()
xml_content = content.encode('utf-8')
f1.close()

xml = Selector(content)
first_obj_element = xml.xpath('//annotation/*[name()="object"][1]').get()
print(first_obj_element)
