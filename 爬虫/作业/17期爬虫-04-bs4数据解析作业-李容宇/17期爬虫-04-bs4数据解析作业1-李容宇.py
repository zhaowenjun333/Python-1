# 7.(必做题1)目标网站：https://sc.chinaz.com/tupian/
# 需求：
# 1、翻页爬网页上的图片名字，图片链接
# 2、保存到csv

import requests
from bs4 import BeautifulSoup
import csv
import time


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}


# 获取网页源代码
def readHtml(ur):
    resp = requests.get(ur, headers=headers)
    resp.encoding = "utf-8"
    html = resp.text
    resp.close()
    return html


# 解析数据
def parseHtml(html):
    soup = BeautifulSoup(html, 'lxml')
    boxs = soup.find_all('div', class_='box')
    lst = []
    for box in boxs:
        img = []
        img_src = f'https:{box.find("img").get("src2")}'
        img_name = box.find_all('a')[1].string
        imgs.append([img_src, img_name])
        img.append(img_name)
        img.append(img_src)
        lst.append(img)
    return lst


# 保存csv
def saveData(lst, page):
    with open(f'./Data/csv/img/img{page}.csv', 'w', encoding="utf-8", newline='') as f:
        header = ('图片名称', '图片链接')
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        csvwriter.writerows(lst)
        f.close()


# 保存img
def saveImg(sr, title):
    img_src = requests.get(sr)
    with open(f'./Data/img/{title}.jpg', 'wb') as f:
        f.write(img_src.content)
        f.close()
    img_src.close()


if __name__ == '__main__':
    imgs = []
    urls = ['https://sc.chinaz.com/tupian/index.html']
    for i in range(1, 51):
        if i == 1:
            continue
        url = f'https://sc.chinaz.com/tupian/index_{i}.html'
        urls.append(url)
    for i in range(0, 50):
        # 读取数据
        htm = readHtml(urls[i])
        # 解析数据
        ls = parseHtml(htm)
        # 保存数据
        saveData(ls, i+1)
        print("over!")
    for img in imgs:
        saveImg(img[0], img[1])
    print("img over!")




