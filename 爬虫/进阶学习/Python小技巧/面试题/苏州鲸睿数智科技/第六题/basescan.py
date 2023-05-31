import requests
import timeit
import os
import sys
import xlwt
from lxml import etree
import urllib3
urllib3.disable_warnings()

class BaseScanSpider:
    def __init__(self):
        self.url = 'https://goerli.basescan.org/address/0x2d2377c00676e97add9a4b9c1e7856fcb7d86a33'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)

        self.chart_set = 'utf-8'

        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
        self.excel_path = f'{self.base_dir}/EXCEL'
        if not os.path.exists(self.excel_path):
            os.mkdir(self.excel_path)

        self.col = ('Txn Hash', 'Method', 'Block', 'From', 'To', 'Value', 'Txn Fee')
        self.book = xlwt.Workbook(encoding=self.chart_set, style_compression=0)
        self.sheet = self.book.add_sheet('basescan', cell_overwrite_ok=True)
        for c in range(len(self.col)):
            self.sheet.write(0, c, self.col[c])

    def get_content(self, url):
        resp = self.session.get(url, verify=False)
        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        html = resp.text
        resp.close()
        return html

    def parse_content(self, html):
        html_element = etree.HTML(html)
        trs = html_element.xpath('//div[@id="transactions"]/div/table/tbody/tr')
        lst = []
        for tr in trs:
            item = {}
            txn_hash = tr.xpath('./td/a[@class="hash-tag text-truncate myFnExpandBox_searchVal"]/text()')
            if txn_hash:
                item['Txn Hash'] = txn_hash[0].strip()
            else:
                item['Txn Hash'] = ''

            method = tr.xpath('./td/span[@class="u-label u-label--xs u-label--info rounded text-dark text-center"]/text()')
            if method:
                item['Method'] = method[0].strip()
            else:
                item['Method'] = ''

            block = tr.xpath('./td[@class="d-none d-sm-table-cell"]/a/text()')
            if block:
                item['Block'] = block[0].strip()
            else:
                item['Block'] = ''

            _from = tr.xpath('./td/span[@class="hash-tag text-truncate"]/text()')
            if _from:
                item['From'] = _from[0].strip()
            else:
                item['From'] = ''

            to = tr.xpath('./td/a[@class="hash-tag text-truncate"]/text()')
            if _from:
                item['To'] = to[0].strip()
            else:
                item['To'] = ''

            value = tr.xpath('./td[last()-2]//text()')
            if _from:
                item['Value'] = ''.join(value).strip()
            else:
                item['Value'] = ''

            txn_fee = tr.xpath('./td[@class="showTxnFee"]/span[@class="small text-secondary"]//text()')
            if _from:
                item['Txn Fee'] = ''.join(txn_fee).strip()
            else:
                item['Txn Fee'] = ''
            lst.append(item)
        return lst

    def save_data(self, lst):
        for m in lst:
            for n in range(len(self.col)):
                self.sheet.write(lst.index(m) + 1, n, m[self.col[n]])
        self.book.save(f'{self.excel_path}/BaseScan.xls')

    def run(self):
        html = self.get_content(self.url)
        data_lst = self.parse_content(html)
        self.save_data(data_lst)


if __name__ == '__main__':
    basescan = BaseScanSpider()
    t = timeit.timeit(stmt=basescan.run, number=1)
    print(t)
