import scrapy
import random
from copy import deepcopy
from animalshop_scrapy.items import AnimalshopScrapyItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['dianping.com']
    base_url = 'https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97/p{}'
    start_urls = ['https://www.dianping.com/search/keyword/1/0_%E5%AE%A0%E7%89%A9%E5%BA%97']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Cookie': 'navCtgScroll=100; _lxsdk_cuid=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _lxsdk=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _hc.v=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198; s_ViewType=10; ctu=f038cc6e62074d02d2dccf4f1fee2914ce130122d343e9146f7edebe2a902766; fspop=test; WEBDFPID=vw0z7286x72v5yy8048ywvw1705486u1816789uwzz097958z1v0u6u7-1978067029903-1662707029572YGMKOUSfd79fef3d01d5e9aadc18ccd4d0c95073605; cy=1; cye=shanghai; dplet=0eb2a067614adcdcfe4da740bf6207b3; dper=d337bc7d6fb74b0bba231d0f6194495b7bc835b59ee410badd854bc934878b300eec12856d13be3ab7a6891f46b2303d5a96dbdc61fcea824a7ae6619f95bc16a2426ff6b160d4b121122aa5af605a1024ebedf13271115385828e6a08365096; ua=Gean; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1662706988,1662745147,1662791256; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1662822410; _lxsdk_s=18327a80d5f-81a-9b5-7b7%7C%7C906',
        'Host': 'www.dianping.com',
        'Referer': 'https://www.dianping.com/',
    }

    # 重写请求
    def start_requests(self):
        for page in range(1, 2):
            if page == 1:
                url = self.start_urls[0]
            else:
                url = self.base_url.format(page)
            # 构造请求(随机)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.text)
        # shops = response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
        # for info in shops:
        #     url = info.xpath('.//div[@class="tit"]/a/@href').get()
        #     print(url)
        #     # yield scrapy.Request(url, callback=self.parse_second, headers=self.headers)
        #     break

    def parse_second(self, response):
        print(response.text)
        shop = response.xpath('//div[@id="basic-info"]')
        # # item.txt = AnimalshopScrapyItem()
        # # item.txt['shop_name'] = shop.xpath('.//h1[@class="shop-name"]/text()').get()
        with open('address.txt', 'r', encoding='utf-8') as address_file:
            address_dict = address_file.read()
            print(type(address_dict))
        # 宠物店名称
        if shop.xpath('.//h1[@class="shop-name"]/e/@href').get() == 'address':
            shop_name = shop.xpath('.//h1[@class="shop-name"]//text()').get()
            shop_name = ''.join(shop_name)
            print(shop_name)

        # 评分
        grade = shop.xpath('.//div[@class="mid-score score-50"]/text()').get()
        print(grade)

        # 评价数量
        # comment_num = shop.xpath('.//span[@id="reviewCount"]')
