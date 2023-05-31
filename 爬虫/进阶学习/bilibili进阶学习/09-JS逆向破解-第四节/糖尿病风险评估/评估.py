import re

import requests
from lxml import etree
import time

class FengXianSpider:
    def __init__(self, form_data):
        self.data = form_data
        self.session = requests.Session()

    def session_csrf(self, url):
        resp = self.session.get(url)
        _csrf = self.session.cookies.get_dict()['_csrf']
        return _csrf

    def parse_html(self, url, form_data, _csrf):
        form_data.update({'_csrf': _csrf})
        resp = self.session.post(url, form_data)
        resp.encoding = 'utf-8'
        html = resp.text
        html_element = etree.HTML(html)
        trs = html_element.xpath('//table[@class="mytable"]/tbody/tr')
        items = {}
        for tr in trs:
            tds = tr.xpath('.//td/text()')
            items[tds[0]] = [tds[1], tds[2]]
        report_box = html_element.xpath('//table/following::div[@class="reportBox"]')[1]
        report_title = report_box.xpath('.//p[@class="reportTitle"]/text()')[0]
        report_txt = report_box.xpath('.//p[@class="txt2"]//text()')
        report_txt = ''.join(report_txt)
        report_txt = re.sub(r'[\n ]', '', report_txt)
        items.update({report_title: report_txt})
        print(items)
        return items

    def run(self):
        self.session.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        })
        url = 'http://cfx.health.xywy.com/question/1/index.htm'
        _csrf = self.session_csrf(url)
        items = self.parse_html(url, self.data, _csrf)
        print(items)


if __name__ == '__main__':
    data = {
        'params[age]': '21',
        'params[gender]': '1',
        'params[hbp_his]': '2',
        'params[diab_his]': '2',
        'params[diab_family]': '1',
        'params[smoke_status]': '1',
        'params[vegetable]': '2',
        'params[fru]': '2',
        'params[is_act]': '1',
        'params[act_freq]': '2',
        'params[act_time]': '2',
        'params[act_intensity]': '2',
        'params[waist]': '60.0',
        'params[tg]': '12.00',
        'params[hdl]': '12.00',
        'params[height]': '163.0',
        'params[weight]': '53.00',
        'params[fbg]': '25.00',
    }
    tnbfxpg = FengXianSpider(data)
    tnbfxpg.run()

