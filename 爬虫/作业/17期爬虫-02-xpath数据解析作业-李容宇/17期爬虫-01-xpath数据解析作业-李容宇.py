# 7.(必做题1)目标网站：https://www.iyingku.cn/IMDB250
# 需求：
# 1、爬取页面所有电影名及评分
# 2、保持到csv

import requests
from lxml import etree
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}


# 获取网页源代码
def readHtml(ur):
    resp = requests.get(ur, headers=headers)
    html = resp.text
    return html


# 解析数据
def parseHtml(html):
    html_element = etree.HTML(html)
    # 获取电影列表
    movielist = html_element.xpath('//tbody[@class="rl_lister-list"]/tr')
    lst = []
    for movie in movielist:
        # print(movie)
        dic = {}
        title = movie.xpath('.//td[@class="rl_name"]/a/@title')[0]
        year = movie.xpath('.//td[@class="rl_name"]/a/span/text()')[0]
        title += year
        grade = movie.xpath('.//td[@class="rl_grade_IMDB"]/span/text()')[0]
        dic['电影名'] = title
        dic['评分'] = grade
        lst.append(dic)
    return lst


def saveDate(lst):
    with open('./Data/IMDB.csv', 'w', encoding="utf-8", newline='') as f:
        th = ('电影名', '评分')
        csvwriter = csv.DictWriter(f, th)
        csvwriter.writeheader()
        csvwriter.writerows(lst)


if __name__ == '__main__':
    url = 'https://www.iyingku.cn/IMDB250'
    html1 = readHtml(url)
    # 解析数据
    ls = parseHtml(html1)
    # 保存数据
    saveDate(ls)
    print("over!")


