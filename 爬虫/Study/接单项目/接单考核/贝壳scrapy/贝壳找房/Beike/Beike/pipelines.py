# Define your item.txt pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item.txt types with a single interface
import csv

from itemadapter import ItemAdapter


class BeikePipeline:
    def __init__(self):
        self.f = open('./CSV/贝壳找房_杭州.csv', 'w+', encoding='utf-8-sig', newline='')
        self.writer = csv.writer(self.f)
        self.headers = ('building_name', 'developer_company', 'sale_status', 'unit_selling_price', 'house_type')
        self.writer.writerow(self.headers)

    def process_item(self, item, spider):
        rows = []
        for header in self.headers:
            rows.append(item[header])
        rows = tuple(rows)
        self.writer.writerow(rows)
        print("Over！")
        return item

    def close_spider(self, spider):
        print('关闭文件')
        self.f.close()

