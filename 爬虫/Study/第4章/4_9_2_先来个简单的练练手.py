"""
流程：
    1. 拿到 23691-4-1.html的页面源代码
    2. 从源代码中提取到m3u8的url
    3. 下载m3u8
    4. 读取m3u8文件，下载视频
    5. 合并视频
"""
# https://m3api.awenhao.com/index.php?note=kkRqcy2386tjeamxdbfh1&raw=1&n.m3u8
# https://m3api.awenhao.com/index.php?note=kkR8m17rwbh2zscng5kt3&raw=1&n.m3u8
import requests
import re
import asyncio
import aiohttp
import aiofiles
import time

url = 'http://www.91kanju2.com/vod-play/23691-4-1.html'

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
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
    obj = re.compile(r"url: '(?P<url>.*?)',", re.S)  # 用来提取m3u8的地址
    m3u8_url = obj.search(html).group("url")  # 拿到m3u8的地址
    return m3u8_url


# 下载m3u8文件
def saveData(m3u8url):
    resp = requests.get(m3u8url, headers=headers)
    m3u8 = resp.content
    resp.close()
    with open("./mp4/超体.m3u8", 'wb') as f:
        f.write(m3u8)
        print('下载完毕')


async def aiodownMp4(src, n, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(src) as resp:
                content = await resp.content.read()
                async with aiofiles.open(f'./mp4/{n}.ts', 'wb') as f:
                    await f.write(content)
                    await f.close()


async def parseM3u8():
    semaphore = asyncio.Semaphore(500)  # 限制并发量为500
    # 解析m3u8文件
    n = 1
    tasks = []
    with open("./mp4/超体.m3u8", 'r', encoding='utf-8') as f:
        txt = f.readlines()
        for line in txt:
            line = line.strip()  # 先去掉空格，空白，换行符
            if line.startswith('#'):  # 如果 # 开头，跳过
                continue
            tasks.append(asyncio.create_task(aiodownMp4(line, n, semaphore)))
            n += 1
        await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    url = 'http://www.91kanju2.com/vod-play/23691-4-1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
    }
    # 读取网页原码
    htm = readHtml(url)
    # 解析数据
    m3u8Url = parseHtml(htm)
    # 下载m3u8文件
    saveData(m3u8Url)
    # 解析m3u8文件
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parseM3u8())
    loop.close()
    # asyncio.run(parseM3u8())
    print('over!')
    t2 = time.time()
    print(t2-t1)
