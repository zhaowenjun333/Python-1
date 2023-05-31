# 目标网站：贝壳找房
# 需求：
# 采集杭州市新房楼盘数据
# 数据要求：
# 要贝壳网的楼盘数据，字段只需要楼盘名称，开发商名称，是否售罄再加上销售单价，楼盘性质。
# 预算：100

import csv
import random
import time

import requests
from lxml import etree
import asyncio
import aiohttp
import aiofiles

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


class BeiKe:
    def __init__(self, w):
        self.writer = w

    async def parse_page(self, buildings, page):
        page = eval(page)
        num = 20 * (page-1)
        for building in buildings['data']['body']['_resblock_list']:
            num += 1
            if building['show_price_info'] == '价格待定':
                price = building['show_price_info']
            else:
                if building['reference_total_price_range']['price'] != '0':
                    price = f"{building['reference_total_price_range']['price']}万/套"
                else:
                    price = f"{building['reference_avg_price']}元/㎡"
            developer_company = building['developer_company'][0]
            if developer_company == '':
                developer_company = '未知开发商'
            item = {
                '楼盘编号': num,
                '楼盘名称': building['title'],
                '开发商名称': developer_company,
                '是否售空': building['sale_status'],
                '销售单价': price,
                '楼盘性质': building['house_type'],
            }
            await self.process_item(item)

    async def process_item(self, item):
        rows = []
        for header in headers:
            rows.append(item[header])
        rows = tuple(rows)
        writer.writerow(rows)
        print("Over！")

    async def aio_task(self, url, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    buildings = await resp.json()
                    # print(buildings)
                    page = url.split('/')[-2].strip('pg')
                    # print(page)
                    await self.parse_page(buildings, page)

    async def main(self):
        semaphore = asyncio.Semaphore(11)  # 限制并发量为12
        tasks = []
        for page in range(1, 97):
            page_url = f'https://m.ke.com/hz/loupan/pg{page}/?_t=1&source=list'
            tasks.append(asyncio.create_task(self.aio_task(page_url, semaphore)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    f = open('./CSV/贝壳找房_杭州.csv', 'w+', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    headers = ('楼盘名称', '开发商名称', '是否售空', '销售单价', '楼盘性质')
    writer.writerow(headers)
    bk = BeiKe(writer)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bk.main())
    # asyncio.run(bk.main())
    f.close()
    t2 = time.time()
    print(t2 - t1)
