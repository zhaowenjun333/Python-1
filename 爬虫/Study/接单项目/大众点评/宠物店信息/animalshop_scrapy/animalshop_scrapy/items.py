# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimalshopScrapyItem(scrapy.Item):
    # define the fields for your item.txt here like:
    # name = scrapy.Field()

    # 宠物店名称
    shop_name = scrapy.Field()

    # 评分
    grade = scrapy.Field()

    # 评价数
    comment_num = scrapy.Field()

    # 人均费用
    price = scrapy.Field()

    # 地址
    position = scrapy.Field()

    # 电话
    tel = scrapy.Field()

