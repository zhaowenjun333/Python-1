import os
import re
import sys
import shutil

pic_dir = '/tupian'
base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
print(base_dir)

filename = os.listdir(base_dir + pic_dir)
print(filename)
# print(len(filename))

# 关键字
keywords = ['绝缘子污秽', '塔顶破损', '导线断股']
# print(keywords)

# 关键字文件夹
img_dir_lst = []
for keyword in keywords:
    keyword_dirname = base_dir + '\\' + keyword
    img_dir_lst.append(keyword_dirname)
    if not os.path.exists(keyword_dirname):
        os.mkdir(keyword_dirname)
for img in filename:
    for j in keywords:
        print(j)
        if j in img:
            shutil.move(f'{base_dir}{pic_dir}/{img}', base_dir + '\\' + j)

