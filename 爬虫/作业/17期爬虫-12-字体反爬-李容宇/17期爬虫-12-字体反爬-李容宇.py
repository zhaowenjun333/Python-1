import requests
from urllib import request
from lxml import etree
from xml.etree import ElementTree
from fontTools.ttLib import TTFont
from aip import AipOcr
import re


class DaZhongDianPing:
    def __init__(self):
        self.url = 'https://www.dianping.com/ajax/json/shopDynamic/allReview?shopId=lagiq1A50rFGpeOG&cityId=344&shopType=10&tcv=2udm55o5oc&_token=eJxVj11vgjAUhv9LrxtosS3KnYvDgaCTgtlcvCjolChSKYof2X9fmW7Jrt6nT99z0t5A5S2BgxFCBENwWlXAAdhABgMQ1ErfMNrD1GbMJoRBkP13PZtCkFazAXA%2BMO0waFls0ZpIi7vpMrKAD7Q0WgS2AVJPV8CmrqVyTLNpGmOZi73M92sjKwtTbUpp7sQ6P%2BA%2BRZU7lKvJUL8J6NEibkcpIRAzrN2d0A%2FZEHfsP2JtfdvWdYpH1r%2FnUP9VV1W%2B3mta%2BeeYK6IOn1Go4sQKZy9BgKQfpF59TWo%2Fzk4hRzgadW0vaJ5GlPNifn4XE1kKNyioy2J2JK%2Fu9FIGSYHGgyUf8c74%2BqxXmpF%2FTaiLdjl%2Fs6LDTB65KI4ipXlW9ad9vr1M5uDrG1n1bsg%3D&uuid=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198&platform=1&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fwww.dianping.com%2Fshop%2Flagiq1A50rFGpeOG'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Cookie': 'fspop=test; cy=160; cye=zhengzhou; _lxsdk_cuid=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _lxsdk=1822b24a0f6c8-09faabfa662e34-26021a51-144000-1822b24a0f65c; _hc.v=fd094450-0739-5a0c-659e-1f6517c498fa.1658581198; s_ViewType=10; dplet=7e9a16bc9a035410b74ce750116e1c17; dper=e7b1f5a48f7115e49fd94aa510b74f4d48dc8f79ab470841c9ce28f328425e3a19574afc34fe6658cfbfc30376c9e0d7f520e5a2fa3285d5b1768f8a486e1caadc27cfdb907129eba197957cb878ca07a90c79ecf8004c5e5aaa2c8559de1460; ua=Gean; ctu=f038cc6e62074d02d2dccf4f1fee2914ce130122d343e9146f7edebe2a902766; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1658581197,1658584004,1659155804; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1659155804; _lxsdk_s=1824d646d39-218-449-e7%7C%7C25'
        }
        self.img = 'tp.png'
        self.APP_ID = '26844959'
        self.APP_KEY = 'Rc6CIKDayLjW9fzY6upd4ear'
        self.SECRET_KEY = 'cytVQ2FOuzdnaHRqqbvGSG2Vak02nGvv'

    def get_review(self):
        # 发送请求
        resp = requests.get(self.url, headers=self.headers)
        # 获取响应原码
        all_review = resp.json()['reviewAllDOList']
        resp.close()
        return all_review

    def woff(self):
        # 加载字体文件
        wo = TTFont('b4b44a82.woff')
        # wo.saveXML('b4b44a82.xml')
        str1_list = wo.getGlyphOrder()[2:]
        return str1_list

    def parse_img(self):
        # 初始化对象
        client = AipOcr(self.APP_ID, self.APP_KEY, self.SECRET_KEY)
        with open('img.png', 'rb') as fp:
            image = fp.read()
            words = client.basicAccurate(image)['words_result']
            text = ''
            for word in words:
                text += word['words']
            fp.close()
        return text

    def parse_review(self, review_list, review_dict):
        for review in review_list:
            user_name = review['user']['userNickName']
            review_body = review['reviewDataVO']['reviewBody'].replace('<br />', '\n').replace('&nbsp;', ' ')
            review_body = review_body.replace('<svgmtsi class=\"review\">', '').replace('</svgmtsi>', '')
            img_tag = etree.HTML(review_body)
            img = img_tag.xpath('//img[@class="emoji-img"]')
            # img = ElementTree.to
            if img:
                for i in img:
                    src = i.xpath('./@src')[0]
                    review_body = review_body.replace(f'<img class="emoji-img" src="{src}" alt=""/>', f' {src}', 1)
            # 开始替换
            for k, v in review_dict.items():
                review_body = review_body.replace(k, v)
            print(user_name)
            print(review_body)
            print('------------------------')

    def main(self):
        all_review = self.get_review()
        str1_list = self.woff()
        text = list(self.parse_img())
        text.insert(text.index('下')+1, '嗅')
        review_dict = {}
        for k, v in zip(str1_list, text):
            review_dict[k.replace('uni', '&#x') + ';'] = v
        # print(review_dict)
        self.parse_review(all_review, review_dict)


if __name__ == '__main__':
    dz = DaZhongDianPing()
    dz.main()
