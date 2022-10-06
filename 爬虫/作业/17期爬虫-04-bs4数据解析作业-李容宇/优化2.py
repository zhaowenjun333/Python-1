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


# 保存csv
async def saveData(lst, page):
    with open(f'./Data/save2/audio{page}.csv', 'w', encoding="utf-8", newline='') as f:
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


async def aiodownAudio(src, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(src) as resp:
            content = await resp.content.read()
            async with aiofiles.open(f'./Data/mp3/{name}.mp3', 'wb') as f:
                await f.write(content)
                await f.close()


async def main():
    tasks1 = []
    tasks2 = []
    urls = ['https://sc.chinaz.com/yinxiao/index.html']
    for i in range(1, 51):
        if i == 1:
            continue
        url = f'https://sc.chinaz.com/yinxiao/index_{i}.html'
        urls.append(url)
    for i in range(0, 50):
        # tasks.append(aiodownload(urls[i], i+1))
        tasks1.append(asyncio.create_task(aiodownload(urls[i], i+1)))
    await asyncio.wait(tasks1)
    for audio in audios:
        tasks2.append(asyncio.create_task(aiodownAudio(audio[0], audio[1])))
        break
    await asyncio.wait(tasks2)


if __name__ == '__main__':
    t1 = time.time()
    audios = []
    asyncio.run(main())
    t2 = time.time()
    print("mp3 over!")
    print(t2-t1)
