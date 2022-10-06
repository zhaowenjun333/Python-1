# 8.(必做题2)目标网站：https://sc.chinaz.com/yinxiao/
# 需求：
# 1、翻页爬网页上的音乐名字，音乐链接
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
    audio_items = soup.find_all('div', class_='audio-item.txt')
    lst = []
    for audio_item in audio_items:
        audio = []
        name = audio_item.find('p', class_='name').string.strip("\r\n ")
        src = f'https:{audio_item.find("audio").get("src")}'
        audios.append([src, name])
        audio.append(name)
        audio.append(src)
        lst.append(audio)
    return lst


def saveData(lst, page):
    with open(f'./Data/csv/audio/audio{page}.csv', 'w', encoding="utf-8", newline='') as f:
        header = ('图片名称', '图片链接')
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        csvwriter.writerows(lst)
        f.close()


def saveAudio(sr, name):
    audio_src = requests.get(sr)
    with open(f'./Data/mp3/{name}.mp3', 'wb') as f:
        f.write(audio_src.content)
        f.close()
    audio_src.close()


if __name__ == '__main__':
    audios = []
    urls = ['https://sc.chinaz.com/yinxiao/index.html']
    for i in range(1, 51):
        if i == 1:
            continue
        url = f'https://sc.chinaz.com/yinxiao/index_{i}.html'
        urls.append(url)
    for i in range(0, 50):
        # 读取数据
        htm = readHtml(urls[i])
        # 解析数据
        ls = parseHtml(htm)
        # 保存数据
        saveData(ls, i+1)
        print('over!')
    for audio in audios:
        saveAudio(audio[0], audio[1])
    print("mp3 over!")
