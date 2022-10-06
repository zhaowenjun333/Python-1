# 8.(必做题2)目标网站：https://www.9ku.com/music/t_new.htm
# 需求：
# 1、爬取到榜单页面使有的歌曲名、歌曲地址
# 2、保存到csv

import requests
from lxml import etree
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}
music_url = 'https://www.9ku.com/'


# 获取网页源代码
def readHtml(ur):
    resp = requests.get(ur, headers=headers)
    html = resp.text
    return html


# 解析数据
def parseHtml(html):
    html_element = etree.HTML(html)
    music_divs = html_element.xpath('.//form/div[@class="bangMusic"]//div[@class="songList clearfix"]')
    # print(music_divs)

    music_list = []
    for music_div in music_divs:
        music_lis = music_div.xpath('.//ol//li')
        for music_li in music_lis:
            dic = {}
            music_num = music_li.xpath('./span/text()')[0]
            music_name = music_li.xpath('./a/text()')[0]
            music_name = music_num + music_name
            music_href = music_url + music_li.xpath('./a/@href')[0]
            dic['音乐名'] = music_name
            dic['链接'] = music_href
            music_list.append(dic)
            # print(music_list)
    return music_list


def saveDate(music_list):
    with open('./Data/九酷音乐.csv', 'w', encoding="utf-8", newline='') as f:
        th = ('音乐名', '链接')
        csvwriter = csv.DictWriter(f, th)
        csvwriter.writeheader()
        csvwriter.writerows(music_list)


if __name__ == '__main__':
    url = 'https://www.9ku.com/music/t_new.htm'
    html1 = readHtml(url)
    # 解析数据
    ls = parseHtml(html1)
    # 保存数据
    saveDate(ls)
    print("over!")
