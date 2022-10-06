# 7.(必做题1)目标网站：汽车之家
# 示例网址：https://www.autohome.com.cn/65/#levelsource=000000000_0&pvareaid=101594
# 需求：
# 1. 使用scrapy框架爬取该汽车的实拍图片
# 2. 保存图片到car文件夹
# 3. 图片数量不得少于500张

import random

import scrapy

from BaoMa.items import BaomaItem


class SpiderSpider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/photolist/series/65/p{}/'.format(i) for i in range(1, 8)]

    headers = [
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'},
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'},
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Safari/537.36'}
    ]

    # def start_requests(self):
    #     # 构造请求(随机)
    #     yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers=random.choice(self.headerds))

    def parse(self, response):
        lis = response.xpath('//ul[@id="imgList"]/li')
        num = 1
        for li in lis:
            item = BaomaItem()
            item['car_name'] = str(num) + '_' + li.xpath('./a/img/@alt').get()
            url = 'https:' + li.xpath('./a/img/@src').get()
            if url.endswith('.gif'):
                item['url'] = 'https:' + li.xpath('./a/img/@src2').get()
            else:
                item['url'] = url
            num += 1
            print(item)
            yield item

