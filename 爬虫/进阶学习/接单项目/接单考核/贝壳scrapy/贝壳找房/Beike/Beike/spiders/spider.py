import scrapy
import random
from copy import deepcopy
from Beike.items import BeikeItem
import json


class SpiderSpider(scrapy.Spider):
    # 爬虫名字
    name = 'spider'
    # 域名限制
    allowed_domains = ['hz.fang.ke.com']
    # 初始请求
    # start_urls = [f'https://hz.fang.ke.com/loupan/pg{i}/' for i in range(1, 6)]
    start_urls = ['https://m.ke.com/hz/loupan/pg{}/?_t=1&source=list']

    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',

        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
        {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'},
        {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}
    ]

    # 重写请求
    def start_requests(self):
        for page in range(1, 97):
            url = self.start_urls[0].format(page)
            # 构造请求(随机)
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=random.choice(self.headers))

    # 解析方法
    def parse(self, response):
        # print(response.text)
        buildings = json.loads(response.text)['data']['body']['_resblock_list']
        for building in buildings:
            item = BeikeItem()
            # 楼盘名称
            item['building_name'] = building['title']
            # 开发商名称
            developer_company = building['developer_company'][0]
            if developer_company == '':
                developer_company = '未知开发商'
            item['developer_company'] = developer_company
            # 是否售空
            item['sale_status'] = building['sale_status']
            # 销售单价
            if building['show_price_info'] == '价格待定':
                price = building['show_price_info']
            else:
                if building['reference_total_price_range']['price'] != '0':
                    price = f"{building['reference_total_price_range']['price']}万/套"
                else:
                    price = f"{building['reference_avg_price']}元/㎡"
            item['unit_selling_price'] = price
            # 楼盘性质
            item['house_type'] = building['house_type']
            yield item

