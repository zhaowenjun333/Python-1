import time
from lxml import etree
import asyncio
import aiohttp
import aiofiles


class BiaoQingBaoSpider:
    def __init__(self):
        pass

    async def aioParseHtml(self, html):
        html_element = etree.HTML(html)
        divs = html_element.xpath('//div[@class="ui segment imghover"]/div[@class="tagbqppdiv"]')
        lst = []
        for div in divs:
            img = []
            title = div.xpath('.//a/@title')[0]
            data_original = div.xpath('.//a/img/@data-original')[0]
            img.append(title)
            img.append(data_original)
            lst.append(img)
        return lst

    async def aiodownload(self, img, session):
        async with session.get(img[1]) as resp:
            async with aiofiles.open(f'./Img/{img[1].split("/")[-1]}', 'wb') as f:
                content = await resp.content.read()
                await f.write(content)
                await f.close()

    async def aioTask(self, url):
        tasks = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
                lst = await self.aioParseHtml(html)
                print(lst)
                for img in lst:
                    task = asyncio.create_task(self.aiodownload(img, session))
                    tasks.append(task)
                    print(img)
                await asyncio.wait(tasks)

    async def main(self):
        tasks = []
        for i in range(1, 11):
            url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{i+1}.html'
            tasks.append(asyncio.create_task(self.aioTask(url)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    bq = BiaoQingBaoSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bq.main())
    # asyncio.run(bq.main())
    t2 = time.time()
    print(t2-t1)
