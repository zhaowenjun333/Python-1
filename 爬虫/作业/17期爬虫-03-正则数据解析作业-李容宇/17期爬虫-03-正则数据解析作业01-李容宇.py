# 9.（必选题1）目标网站：https://music.163.com/#/discover/toplist
# 需求：
# 1、爬取页面源代码
# 2、用正则解析数据，获取到整个页面的歌手和歌手名
# 3、把数据保存到csv
import json

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
    contents = re.search('<textarea id="song-list-pre-data" style="display:none;">(.*?)</textarea>', html, re.S)

    content = contents.group(1)
    # 转成列表
    # data_lst = json.load(content)
    # print(type(data_lst))

    # print(content)
    # print(type(content))

    ls = re.findall('\"album\".*?\"alias\"\:\[]}]', content, re.S)
    pattern = re.compile('"album":\{"id":.*?,"name":"(.*?)".*?"artists":(.*)', re.S)
    lst = []
    for i in ls:
        r = pattern.match(i)
        singname = r.group(1)
        artists = eval(r.group(2))
        singernames = []
        for artist in artists:
            singernames.append(artist['name'])
        singername = '/'.join(singernames)
        sing = [singname, singername]
        lst.append(sing)
    return lst


def saveDate(sing_list):
    with open('./Data/飙升榜Top音乐.csv', 'w', encoding="utf-8", newline='') as f:
        header = ('歌曲', '歌手')
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        csvwriter.writerows(sing_list)
        f.close()


if __name__ == '__main__':
    url = 'https://music.163.com/discover/toplist'
    html1 = readHtml(url)
    # 解析数据
    ls = parseHtml(html1)
    # 保存数据
    saveDate(ls)
    print("over!")
