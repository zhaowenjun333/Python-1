import requests
import re
# import os

url = 'https://music.163.com/discover/toplist?id=3778678'

# headers请求头 就是用伪装python代码 吧python伪装成浏览器对于服务器发送请求
# 服务器接收到请求之后，会给我们返回相应数据（response）
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
}

resp = requests.get(url, headers=headers)

# print(resp.text)


# res = re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a>', resp.text)
# print(res)

obj = re.compile(r'<li><a href="/song\?id=(?P<id>\d+)">(?P<music>.*?)</a>', re.S)
result = obj.finditer(resp.text)
dic = {}
for it in result:
    # ls.append((it.group("id"), it.group("music")))
    music_url = f'https://music.163.com//song/media/outer/url?id={it.group("id")}.mp3'
    dic[it.group('music')] = music_url
# print(dic)

for i in range(10, 0, -1):
    print(f"你还有{i}次机会")
    music = input("请输入你想听得歌曲：")
    if music in dic:
        print(dic[music])
    else:
        continue

resp.close()
