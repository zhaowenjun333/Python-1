# Define your item.txt pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item.txt types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from urllib import request
import re

class DoutuPipeline:
    # 方法一: images
    # def get_media_requests(self, item.txt, info):
    #     img_url = item.txt['img_url']
    #     yield scrapy.Request(img_url)
    #
    # def file_path(self, request, response=None, info=None, *, item.txt=None):
    #     name = item.txt['img_name']
    #     return f'{name}.gif'

    # 方法二: 斗图
    def process_item(self, item, spider):
        url = item['img_url']
        name = item['img_name'] + '.' + url.split('.')[-1]
        filename = './斗图/{}'.format(name)
        print(filename, '下载完成')

        # 保存图片
        request.urlretrieve(url, filename)
        return item

# 方法三：img,可保存gif
# from scrapy.utils.misc import md5sum
# import os
#
#
# class DouTuGifPipline(ImagesPipeline):
#     def get_media_requests(self, item.txt, info):
#         url = item.txt['img_url']
#         yield scrapy.Request(url)
#
#     def file_path(self, request, response=None, info=None, *, item.txt=None):
#         name = item.txt['img_name'] + '.' + request.url.split('.')[-1]
#         path = u'{}'.format(name)
#         return path
#
#     def check_gif(self, image):
#         if image.format is None:
#             return True
#
#     def persist_gif(self, key, data, info):
#         root, ext = os.path.split(key)
#         absolute_path = self.store._get_filesystem_path(key)
#         self.store._mkdir(os.path.dirname(absolute_path), info)
#         f = open(absolute_path, 'wb')  # use 'b' to write binary data.
#         f.write(data)
#
#     def image_downloaded(self, response, request, info, *, item.txt=None):
#         try:
#             checksum = None
#             for path, image, buf in self.get_images(response, request, info, item.txt=item.txt):
#                 if checksum is None:
#                     buf.seek(0)
#                     checksum = md5sum(buf)
#                 width, height = image.size
#                 if self.check_gif(image):
#                     self.persist_gif(path, response.body, info)
#                 else:
#                     self.store.persist_file(
#                         path, buf, info,
#                         meta={'width': width, 'height': height},
#                         headers={'Content-Type': 'image/jpeg'})
#                 return checksum
#         except:
#             pass
