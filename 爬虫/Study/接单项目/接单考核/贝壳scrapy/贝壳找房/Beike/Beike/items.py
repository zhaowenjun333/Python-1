# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# 楼盘名称，开发商名称，是否售罄再加上销售单价，楼盘性质。


import scrapy


class BeikeItem(scrapy.Item):
    # define the fields for your item.txt here like:
    # name = scrapy.Field()
    # 楼盘名称
    building_name = scrapy.Field()
    # 开发商名称
    developer_company = scrapy.Field()
    # 是否售空
    sale_status = scrapy.Field()
    # 销售单价
    unit_selling_price = scrapy.Field()
    # 楼盘性质
    house_type = scrapy.Field()


