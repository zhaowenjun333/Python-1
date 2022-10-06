import requests
from fontTools.ttLib import TTFont
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
import ddddocr
from lxml import etree

url = 'https://club.autohome.com.cn/bbs/thread/665330b6c7146767/80787515-1.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

resp = requests.get(url, headers=headers)
text_str = resp.text
# print(resp.text)

# 解析数据
html = etree.HTML(text_str)
content_lst = html.xpath('//div[@class="tz-paragraph"]//text()')
resp.close()
# print(content_lst)

# 加载字体文件
car_font = TTFont('wKgHFVsUz1eAH_VRAABj9PS-ubk57..ttf')
# car_font.saveXML('car_font.xml')
# print(car_font.getGlyphOrder())

str1_list = car_font.getGlyphOrder()
str2_list = [eval(r'"\u' + i[3:] + '"') for i in str1_list[1:]]
# print(str2_list)
text = '很五多远大十更了的矮不少九三八一右坏近着呢左是长六上短七高二得好下和四地小低'
str3_list = list(text)
# print(str3_list)
car_dict = {}

for k, v in zip(str2_list, str3_list):
    car_dict[k] = v
print(car_dict)

content_str = ''.join(content_lst)

# 开始替换
for k, v in car_dict.items():
    content_str = content_str.replace(k, v)

print(content_str)
