import re
import requests
from urllib import request
import pytesseract
from PIL import Image
from lxml import etree


class ZiRoom:
    def __init__(self):
        # 目标url
        self.url = 'https://www.ziroom.com/z/'
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        # 数字图片
        self.back_num = 'back_num.png'

    # 获取网页源码和图片
    def get_html(self):
        # 发送请求
        resp = requests.get(self.url, headers=self.headers)
        resp.encoding = 'utf-8'
        # 获取响应原码
        html_str = resp.text

        # 从网页源码获取图片url
        result = re.search(r'background-image: url\((.*?)\)', html_str)
        # 构造完整图片url
        num_url = 'https:' + result.group(1)
        print(num_url)

        # 保存图片
        request.urlretrieve(num_url, self.back_num)
        return html_str

    # 解析数据
    def parse_html(self, html_str, replace_dict):
        html = etree.HTML(html_str)
        div_list = html.xpath('//div[@class="Z_list-box"]/div[@class="item.txt"]')

        for div in div_list:
            title = div.xpath('.//h5/a/text()')[0]
            # print(title)

            # 获取符号
            span_rmb = div.xpath('.//span[@class="rmb"]/text()')[0]

            # 获取单位
            span_unit = div.xpath('.//span[@class="unit"]/text()')[0]

            # 获取偏移量
            span_list = div.xpath('.//span[@class="num"]')

            price = ''
            for span in span_list:
                # 获取每个span标签对应的数字
                style = span.xpath('./@style')[0]
                position = style.split(': ')[-1]

                number = replace_dict[position]
                price = price + number
            price = span_rmb + price + span_unit
            print(title, price)

    # 主函数
    def main(self):
        html_str = self.get_html()

        # 识别数字图片
        im = Image.open(self.back_num)
        res = pytesseract.image_to_string(im)
        # print(res)

        num_lst = re.findall(r'\d', res)
        # 偏移量列表
        print(num_lst)
        x_list = ['-0px', '-21.4px', '-42.8px', '-64.2px', '-85.6px',
                  '-107px', '-128.4px', '-149.8px', '-171.2px', '-192.6px']

        replace_dict = dict(zip(x_list, num_lst))
        print(replace_dict)

        # 解析方法
        self.parse_html(html_str, replace_dict)


if __name__ == '__main__':
    zr = ZiRoom()
    zr.main()




