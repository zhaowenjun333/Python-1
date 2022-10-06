# 异步协程
import asyncio
import aiohttp

urls = [
    'http://kr.shanghai-jiuxin.com/file/2022/0414/smallba34fff6a58897cc5362b79e477c06d8.jpg',
    'http://kr.shanghai-jiuxin.com/file/2022/0414/small33f06e321d65146414aefd830013dfe7.jpg',
    'http://kr.shanghai-jiuxin.com/file/2020/1031/small191468637cab2f0206f7d1d9b175ac81.jpg'
]


async def aiodownload(url):
    # s = aiohttp.ClientSession()  <===> 等价于requests
    # 发送请求
    # 得到图片内容
    # 保存文件
    async with aiohttp.ClientSession() as session:
        # async with  不需要close
        async with session.get(url) as resp:
            # resp.json()     # <===> resp.json
            # 读取文本
            # resp.text()         # <===> 等价于resp.text
            # 读取字节流
            # resp.content.read()       # <====> 等价于resp.content
            name = url.rsplit('/', 1)[1]    # 从右边切割，用url的最后一个作为文件名
            with open(f'./img/{name}', 'wb') as f:
                f.write(await resp.content.read())    # 读取内容是异步的，需要挂取
    print(name, 'over!')


async def main():
    tasks = []
    for url in urls:
        tasks.append(aiodownload(url))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())


