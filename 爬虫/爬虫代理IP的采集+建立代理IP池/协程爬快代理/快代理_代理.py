# Python实现IP代理批量采集，并检测代理是否可用
# 快代理：https://free.kuaidaili.com/free
import json
import random

import aiofiles
import requests
import parsel
from lxml import etree
import asyncio
import aiohttp
import time

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}
]


class IpSpider:
    def __init__(self):
        pass

    async def parse_page(self, html):
        html_element = etree.HTML(html)
        trs = html_element.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        tasks = []
        for tr in trs:
            ip = tr.xpath('.//td[@data-title="IP"]/text()')[0]
            port = tr.xpath('.//td[@data-title="PORT"]/text()')[0]
            print(f'代理ip: {ip}:{port}')
            proxies_dict = {
                'http': f'http://{ip}:{port}',
                'https': f'https://{ip}:{port}'
            }
            try:
                url1 = 'https://www.baidu.com/'
                resp1 = requests.get(url1, proxies_dict, headers=random.choice(self.headers), timeout=1)
                if resp1.status_code == 200:
                    # print(resp1.text)
                    print('代理可用', proxies_dict)
                    tasks.append(asyncio.create_task(self.aiosavedata(proxies_dict)))
            except Exception as e:
                # print(f'不可用，要报错了：{e}')
                print('当前代理', proxies_dict, f'请求超时{e}')
        await asyncio.wait(tasks)

    async def aiosavedata(self, proxies_dict):
        async with aiofiles.open('./快代理.txt', 'a', encoding='utf-8') as f:
            await f.write(json.dumps(proxies_dict) + '\n')

    async def aio_task(self, url, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession(headers=random.choice(headers)) as session:
                async with session.get(url) as resp:
                    html = await resp.text()
                    await self.parse_page(html)

    async def main(self):
        semaphore = asyncio.Semaphore(10)  # 限制并发量为12
        tasks = []
        for page in range(1, 10):
            page_url = f'https://free.kuaidaili.com/free/inha/{page}/'
            tasks.append(asyncio.create_task(self.aio_task(page_url, semaphore)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    spider = IpSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.main())
    t2 = time.time()
    print(round(t2-t1))
