"""
思路:
    1. 拿到主页面的页面源代码, 找到iframe
    2. 从iframe的页面源代码中拿到m3u8文件的地址
    3. 下载第一层m3u8文件 -> 下载第二层m3u8文件(视频存放路径)
    4. 下载视频
    5. 下载秘钥, 进行解密操作
    6. 合并所有ts文件为一个mp4文件
"""
import time
import requests
from bs4 import BeautifulSoup
import re
import asyncio
import aiohttp
import aiofiles
from Crypto.Cipher import AES  # windows系统导入不成功请参考csdn
import os


def get_iframe_src(ur):
    resp = requests.get(ur)
    main_page = BeautifulSoup(resp.text, "html.parser")  # 设置文本为html文本
    src = main_page.find("iframe").get("src")
    return src


def get_first_m3u8_url(ur):
    resp = requests.get(ur)
    obj = re.compile(r'var main = "(?P<m3u8_url>.*?)"', re.S)  # 正则表达式re解析
    m3u8_url = obj.search(resp.text).group("m3u8_url")
    return m3u8_url


# 只用定义一次m3u8文件下载程序，第二次直接调用
def download_m3u8_file(ur, name):
    resp = requests.get(ur)
    with open(name, mode="wb") as f:
        f.write(resp.content)


# 之所以在现在出现了异步协程，主要是之前的都是同步操作，还没有出现多任务的情况。从这里开始了多ts文件下载，所以创造异步协程程序加快下载速度。
# 异步协程的代码都是分为两个步骤，首先定义我们的主要任务，其次定义异步协程的代码。在异步协程里面调用主要任务。
async def download_ts(ur, name, session):
    async with session.get(ur) as resp:
        async with aiofiles.open(f"./越狱第一季/video/{name}", mode="wb") as f:
            await f.write(await resp.content.read())  # 把下载到的内容写入到文件中
    print(f"{name}下载完毕")


async def aio_download(up_url):  # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/
    tasks = []
    async with aiohttp.ClientSession() as session:  # 提前准备好session
        async with aiofiles.open("./越狱第一季/m3u8/越狱第一季第一集_second_m3u8.txt", mode="r", encoding='utf-8') as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                # line就是xxxxx.ts
                line = line.strip()  # 去掉没用的空格和换行
                # 拼接真正的ts路径
                ts_url = up_url + line
                task = asyncio.create_task(download_ts(ts_url, line, session))  # 创建任务
                tasks.append(task)

            await asyncio.wait(tasks)  # 等待任务结束


# 下载秘钥
def get_key(ur):
    resp = requests.get(ur)
    return resp.text


# AES解密，解密涉及到多ts文件解密，设计aiofiles，所以设计异步协程程序来加速揭秘过程
async def dec_ts(name, key):
    # IV为偏移量，如果没有说明就直接是16位的0， 看key的长度，
    aes = AES.new(key=key, IV=b"0000000000000000", mode=AES.MODE_CBC)
    # 同时创建两个异步程序，一个读一个写
    async with aiofiles.open(f"./越狱第一季/video/{name}", mode="rb") as f1, \
            aiofiles.open(f"./越狱第一季/video/temp_{name}", mode="wb") as f2:
        bs = await f1.read()  # 从源文件读取内容
        await f2.write(aes.decrypt(bs))  # 把解密好的内容写入文件
    print(f"{name}处理完毕")


async def aio_dec(key):
    # 解密
    tasks = []
    async with aiofiles.open("./越狱第一季/m3u8/越狱第一季第一集_second_m3u8.txt", mode="r", encoding="utf-8") as f:
        async for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            # 开始创建异步任务
            # line: 文件名， key: 密钥
            task = asyncio.create_task(dec_ts(line, key))
            tasks.append(task)
        await asyncio.wait(tasks)


# 用python代码把多ts文件合并成一个mp4文件
def merge_ts():
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    lst = []
    with open("./越狱第一季/m3u8/越狱第一季第一集_second_m3u8.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            lst.append(f"./越狱第一季/video/temp_{line}")

    s = "+".join(lst)  # 1.ts+2.ts+3.ts
    os.system(f"copy /b {s}  movie.mp4")
    print("搞定!")


# 主程序调用各个子程序
def main(ur):
    # 1. 拿到主页面的页面源代码, 找到iframe对应的url
    iframe_src = get_iframe_src(ur)
    # 2. 拿到第一层的m3u8文件的下载地址
    first_m3u8_url = get_first_m3u8_url(iframe_src)
    # 拿到iframe的域名
    # "https://boba.52kuyun.com/share/xfPs9NPHvYGhNzFp"
    iframe_domain = iframe_src.split("/share")[0]
    # 拼接出真正的m3u8的下载路径
    first_m3u8_url = iframe_domain + first_m3u8_url
    # https://boba.52kuyun.com/20170906/Moh2l9zV/index.m3u8?sign=548ae366a075f0f9e7c76af215aa18e1
    # print(first_m3u8_url)
    # 3.1 下载第一层m3u8文件
    download_m3u8_file(first_m3u8_url, "越狱第一季第一集_first_m3u8.txt")
    # 3.2 下载第二层m3u8文件
    with open("./越狱第一季/m3u8/越狱第一季第一集_first_m3u8.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            else:
                line = line.strip()  # 去掉空白或者换行符  hls/index.m3u8
                # 准备拼接第二层m3u8的下载路径
                # https://boba.52kuyun.com/20170906/Moh2l9zV/ + hls/index.m3u8
                # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/index.m3u8
                # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/cFN8o3436000.ts
                second_m3u8_url = first_m3u8_url.split("index.m3u8")[0] + line
                download_m3u8_file(second_m3u8_url, "越狱第一季第一集_second_m3u8.txt")
                print("m3u8文件下载完毕")

    # 4. 下载视频
    second_m3u8_url_up = second_m3u8_url.replace("index.m3u8", "")
    # 异步协程
    asyncio.run(aio_download(second_m3u8_url_up))  # 测试的使用可以注释掉

    # 5.1 拿到秘钥
    key_url = second_m3u8_url_up + "key.key"  # 偷懒写法, 正常应该去m3u8文件里去找
    key = get_key(key_url)
    # 5.2 解密
    asyncio.run(aio_dec(key))

    # 6. 合并ts文件为mp4文件
    merge_ts()


if __name__ == '__main__':
    t1 = time.time()
    url = "https://www.91kanju.com/vod-play/541-2-1.html"
    main(url)
    # 简单的问题复杂化, 复杂的问题简单化
    t2 = time.time()
    print(t2-t1)
