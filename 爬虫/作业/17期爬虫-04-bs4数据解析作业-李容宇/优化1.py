from bs4 import BeautifulSoup
import asyncio
import aiohttp
import aiofiles
import time
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}


# 解析数据
async def parseHtml(html):
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
async def saveData(lst, page):
    with open(f'./Data/save1/img{page}.csv', 'w', encoding="utf-8", newline='') as f:
        header = ('图片名称', '图片链接')
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        csvwriter.writerows(lst)
        f.close()


async def aiodownload(url, page):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.encoding = "utf-8"
            html = await resp.text()
            lst = await parseHtml(html)
            # print(lst)
            await saveData(lst, page)


async def aiodownImg(src, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(src) as resp:
            content = await resp.content.read()
            async with aiofiles.open(f'./Data/img/{name}.jpg', 'wb') as f:
                await f.write(content)
                await f.close()


async def main():
    tasks1 = []
    tasks2 = []
    urls = ['https://sc.chinaz.com/tupian/index.html']
    for i in range(1, 51):
        if i == 1:
            continue
        url = f'https://sc.chinaz.com/tupian/index_{i}.html'
        urls.append(url)
    for i in range(0, 50):
        # tasks.append(aiodownload(urls[i], i+1))
        tasks1.append(asyncio.create_task(aiodownload(urls[i], i+1)))
    await asyncio.wait(tasks1)
    for img in imgs:
        tasks2.append(asyncio.create_task(aiodownImg(img[0], img[1])))
    await asyncio.wait(tasks2)


if __name__ == '__main__':
    t1 = time.time()
    imgs = []
    asyncio.run(main())
    t2 = time.time()
    print('over!')
    print(t2-t1)
