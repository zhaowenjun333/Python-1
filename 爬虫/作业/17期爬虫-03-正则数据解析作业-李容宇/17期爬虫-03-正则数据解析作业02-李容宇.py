# 10.（必选题1）目标网站：https://top.baidu.com/board?tab=movie
# 需求：
# 1、爬取页面源代码
# 2、用正则解析数据，获取到整个榜单的电影名，电影类型和演员
# 3、把数据保存到csv

import requests
import re
import csv

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
    contents = re.findall('<div class="hot-index_1Bl1a">.*?</div>.*?查看更多', html, re.S)
    # lst = re.math('.*?<!--s-data:.*?,"content":(.*?),"more":0,', content, re.S)

    pattern = re.compile('<div class="hot-index_1Bl1a">(.*?)</div>.*?'  # 热搜指数
                         '<div class="c-single-text-ellipsis">(.*?)</div>.*?'  # 电影名
                         '<div class="intro_1l0wp"> 类型：(.*?)</div>'  # 类型
                         '<div class="intro_1l0wp"> 演员：(.*?)</div>', re.S)  # 演员
    lst = []
    for content in contents:
        r = pattern.match(content)
        lis = [r.group(1), r.group(2), r.group(3), r.group(4)]
        lst.append(lis)
    return lst


def saveDate(movie_list):
    with open('./Data/百度热搜电影.csv', 'w', encoding="utf-8", newline='') as f:
        header = ('热搜指数', '电影名', '类型', '演员')
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        csvwriter.writerows(movie_list)
        f.close()


if __name__ == '__main__':
    url = 'https://top.baidu.com/board?tab=movie'
    html1 = readHtml(url)
    # 解析数据
    ls = parseHtml(html1)
    # 保存数据
    saveDate(ls)
    print("over!")
