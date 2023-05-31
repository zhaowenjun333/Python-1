import os

import requests
import re
import base64

import xlwt
from fontTools.ttLib import TTFont
from lxml import etree
import threading
import time
from queue import Queue


class TCProducer(threading.Thread):
    def __init__(self, page_q, info_q):
        super().__init__()
        self.page_q = page_q
        self.info_q = info_q
        self.words_dict = {
            ('0', '-147', '1982', '1521'): '王', ('0', '-261', '1864', '1603'): '届',
            ('0', '-26', '1113', '1575'): '0', ('0', '-285', '2012', '1701'): '专',
            ('0', '-269', '2016', '1699'): '博', ('0', '0', '1101', '1549'): '7',
            ('0', '-26', '1098', '1575'): '8', ('0', '-277', '1888', '1707'): '中',
            ('0', '0', '1128', '1549'): '4', ('0', '-271', '1940', '1673'): '杨',
            ('0', '-273', '1990', '1705'): '女', ('0', '-26', '1115', '1575'): '6',
            ('0', '-251', '2008', '1729'): '高', ('0', '0', '1178', '1549'): 'B',
            ('0', '-285', '2020', '1709'): '校', ('0', '-279', '2032', '1701'): '以',
            ('0', '-171', '2022', '1711'): '经', ('0', '-263', '2028', '1691'): '大',
            ('0', '-247', '2024', '1707'): '陈', ('0', '-285', '2008', '1605'): '吴',
            ('0', '0', '1077', '1582'): '1', ('0', '-117', '2000', '1699'): '士',
            ('0', '-26', '1094', '1575'): '9', ('0', '-255', '1916', '1703'): '刘',
            ('0', '0', '1800', '1549'): 'M', ('0', '-273', '1996', '1721'): '应',
            ('0', '-259', '2020', '1691'): '张', ('0', '-283', '2016', '1541'): '无',
            ('0', '-269', '2010', '1709'): '本', ('0', '-231', '2036', '1689'): '验',
            ('0', '-255', '2022', '1697'): '李', ('0', '-275', '1908', '1607'): '男',
            ('0', '-285', '2022', '1697'): '技', ('0', '-26', '1057', '1549'): '5',
            ('0', '-303', '2022', '1581'): '硕', ('0', '0', '1033', '1549'): 'E',
            ('0', '-291', '2000', '1709'): '黄', ('0', '-26', '1049', '1575'): '3',
            ('0', '-255', '1996', '1537'): '下', ('0', '0', '1062', '1575'): '2',
            ('0', '-263', '1914', '1619'): '周', ('0', '-283', '2022', '1685'): '赵',
            ('0', '-145', '2012', '1709'): '生', ('0', '-271', '2012', '1691'): '科',
            ('0', '0', '1417', '1549'): 'A'}

    def run(self):
        while True:
            if self.page_q.empty():
                break
            (htm, info, n, page_num) = self.page_q.get()
            # print(info)
            self.parse_page(htm, info, n, page_num)

    def parse_page(self, htm, info, n, page_num):
        obj2 = re.compile(r'<span id="name" class="name stonefont">(?P<name>.*?)</span>.*?'
                          r'<span class="sex stonefont">(?P<sex>.*?)</span>.*?'
                          r'<span class="age stonefont">(?P<age>.*?)</span>.*?'
                          r'<span class="edu stonefont">(?P<education>.*?)</span>.*?'
                          r'<span class="stonefont">(?P<workYear>.*?)</span>.*?'
                          r'''<p class="stonefont">.*?<span class='title'>期望薪资：</span>(?P<salary>.*?)</p>.*?''', re.S)
        font_dict = self.get_woff(htm, info['userID'])
        # print(font_dict)

        # 删除文件
        woff_path = f'./字体文件/{info["userID"]}.woff'
        xml_path = f'./字体文件/{info["userID"]}.xml'
        self.del_file(woff_path)
        self.del_file(xml_path)

        htm = obj2.finditer(htm)
        for message in htm:
            info['name'] = message.group('name').strip('\r\n\t\t\t\t')

            info['sex'] = message.group('sex')
            for k, v in font_dict.items():
                if k in info['sex']:
                    info['sex'] = info['sex'].replace(k, self.words_dict[v])

            info['age'] = message.group('age')
            for k, v in font_dict.items():
                if k in info['age']:
                    info['age'] = info['age'].replace(k, self.words_dict[v])

            info['education'] = message.group('education')
            for k, v in font_dict.items():
                if k in info['education']:
                    info['education'] = info['education'].replace(k, self.words_dict[v])

            info['workYear'] = message.group('workYear')
            for k, v in font_dict.items():
                if k in info['workYear']:
                    info['workYear'] = info['workYear'].replace(k, self.words_dict[v])

            info['salary'] = message.group('salary').strip('\r\n\t\t\t')
            if info['salary'] != '':
                for k, v in font_dict.items():
                    if k in info['salary']:
                        info['salary'] = info['salary'].replace(k, self.words_dict[v])
        print(n)
        print(info)
        self.info_q.put((info, n, page_num))
        print('----'*10)

    def get_woff(self, htm, userid):
        result = re.search(r'base64,(.*?)\)', htm, re.S).group(1)
        # print(result)
        b = base64.b64decode(result)
        file_path = f'./字体文件/{userid}'
        with open(f'{file_path}.woff', 'wb') as f:
            f.write(b)
            f.close()
        fonts = TTFont(f'{file_path}.woff')
        file_xml = f'{file_path}.xml'
        fonts.saveXML(file_xml)

        with open(file_xml, 'rb') as f:
            xml = f.read()
            f.close()
        xml_element = etree.XML(xml)
        TTGlyph_lst = xml_element.xpath('//TTGlyph')[1:-1]
        font_dict = {}
        for TTGlyph in TTGlyph_lst:
            name = TTGlyph.xpath('.//@name')[0].replace('uni', '&#x') + ';'
            xMin = TTGlyph.xpath('.//@xMin')[0]
            yMin = TTGlyph.xpath('.//@yMin')[0]
            xMax = TTGlyph.xpath('.//@xMax')[0]
            yMax = TTGlyph.xpath('.//@yMax')[0]
            font_dict[name] = (xMin, yMin, xMax, yMax)
        return font_dict

    def del_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'{file_path}删除')


class TCConsumer(threading.Thread):
    def __init__(self, info_q, s, co):
        super().__init__()
        self.info_q = info_q
        self.sheet = s
        self.col = co

    def saveData(self, info, n, page_num):
        for column in range(len(self.col)):
            row = (page_num-1)*50 + n + 1
            data = self.col[column]
            self.sheet.write(row, column, info[data])

    def run(self):
        while True:
            if self.info_q.empty():
                break
            info, n, page_num = self.info_q.get()
            self.saveData(info, n, page_num)


if __name__ == '__main__':
    ti1 = time.time()
    # 1. url存放到队列中
    page_queue = Queue()
    # 2. 存放数据的队列
    info_queue = Queue()
    obj1 = re.compile(r'","userID":(?P<userID>.*?),.*?"nowPosition":"(?P<nowPosition>.*?)",'
                      r'"targetPosition":"(?P<targetPosition>.*?)","education":"(?P<education>.*?)",'
                      r'"workYear":"(?P<workYear>.*?)".*?"sexText":"(?P<sexText>.*?)".*?'
                      r'"ageText":"(?P<ageText>.*?)".*?"targetArea":"(?P<targetArea>.*?)",'
                      r'"targetSalary":"(?P<targetSalary>.*?)".*?"lspot":(?P<lspot>.*?)],'
                      r'"letter":"(?P<letter>.*?)".*?"experYears":"(?P<experYears>.*?)".*?'
                      r'"resumeTp":"(?P<resumeTp>.*?)".*?"url":"(?P<url>.*?)".*?'
                      r'"activeTime":"(?P<activeTime>.*?)"', re.S)
    header1 = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'id58=CocGRmNhSUWvQzXzL4SMAg==; 58tj_uuid=99f4b17b-a446-4330-98bf-831ca8085f9c; Hm_lvt_b4a22b2e0b326c2da73c447b956d6746=1667320135; als=0; myfeet_tooltip=end; city=sh; wmda_uuid=181f2e7d2e3c1d7f18e3954a4c0f0ddd; wmda_new_uuid=1; 58home=sh; param8616=1; param8716kop=1; xxzl_smartid=cf0b87f75f8e04c8dce7489d12bf5c3f; ljrzfc=1; new_uv=10; utm_source=; spm=; init_refer=; new_session=0; JSESSIONID=D1C798A110B3F4EFCA38820314D2524F; wmda_session_id_10104579731767=1667753859747-5ac99e4a-3ea4-d1d2; www58com="UserID=91725898555940&UserName=psundqg0b"; 58cooper="userid=91725898555940&username=psundqg0b"; 58uname=psundqg0b; passportAccount="atype=0&bstate=0"; vip=vipusertype%3D11%26vipuserpline%3D0%26v%3D1%26vipkey%3D406574dcfdc1aa1649f777970cbccea3%26masteruserid%3D91725898555940; wmda_session_id_2286118353409=1667753891797-2053ca87-6aa7-9636; wmda_visited_projects=%3B1731916484865%3B11187958619315%3B10104579731767%3B1731918550401%3B2286118353409; wmda_session_id_11187958619315=1667753893390-5125e3d5-7ac1-1a8d; showStatus=headClick; xxzl_cid=c404c49b95e94fa38cd0252713aec404; xxzl_deviceid=0vVFgGPqNnufBh0cpyBxSW4oDG3k%2FLvOv8tPF2flNSsauEYPZQJf2jEGx%2FhQ50ae; PPU="UID=91725898555940&UN=psundqg0b&TT=5c6f15581fc3c6e87f66e8e15adb2b32&PBODY=ixKyo2d4Exy1yJhvkYpslGDW_hcvqXOgCw08xdiGGx3DdzBdBs2MZW3vZixQF8cHIbh_SO2lCHDSb0dh5jMU9zldkvk0SjpCcRUTUDQiMEnHmy4D3uG0iNENZTOaXrDLGnV8UYhocXAPG5zQ1SD61rmtJdhEcu7Ig190-CKD124&VER=1&CUID=7oGK8_reTtXpdRYoDahZRw"',
        'referer': 'https://jllist.58.com/resume/searchpage',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    for page in range(1, 6):
        url1 = f'https://jllist.58.com/resume/search?pageNumb={page}&resumeSort=intelligent&update24Hours=1&cityId=2&cityType=guishu&fontKey=d36b7ea8b34e4ddbbda1600b69e380bc&fontkey=d36b7ea8b34e4ddbbda1600b69e380bc&_=1667626841525&callback=axiosJsonpCallback2'
        resp1 = requests.get(url1, headers=header1)
        content = resp1.text
        # print(content)
        first = True
        resumeList = obj1.finditer(content)
        url_list = []
        num = 0
        for resume in resumeList:
            url = f'https:{resume.group("url")}'
            resp = requests.get(url, headers=header1)
            # resp.encoding = 'utf-8'
            html = resp.text
            resp.close()
            item = {
                'userID': resume.group('userID'),
                'nowPosition': resume.group('nowPosition'),
                'targetPosition': resume.group('targetPosition'),
                'targetArea': resume.group('targetArea'),
                'lspot': resume.group('lspot').replace('[', ''),
                'letter': resume.group('letter'),
                'experYears': resume.group('experYears'),
                'resumeTp': resume.group('resumeTp'),
                'activeTime': resume.group('activeTime')
            }
            page_queue.put((html, item, num, page))
            num += 1

    p_lst = []
    # 创建五个生产者
    for i in range(10):
        t1 = TCProducer(page_queue, info_queue)
        t1.start()
        p_lst.append(t1)
    # 让生产者线程运行完
    for p in p_lst:
        p.join()

    col = ('userID', 'name', 'sex', 'age', 'education', 'workYear', 'salary',
           'nowPosition', 'targetPosition', 'targetArea', 'lspot', 'letter',
           'experYears', 'resumeTp', 'activeTime')

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('58同城简历信息', cell_overwrite_ok=True)
    for c in range(len(col)):
        sheet.write(0, c, col[c])

    c_lst = []
    # 创建五个消费者
    for j in range(10):
        t2 = TCConsumer(info_queue, sheet, col)
        t2.start()
        c_lst.append(t2)
    # 让消费者线程运行完
    for c in c_lst:
        c.join()

    book.save('./data/58同城简历信息.xls')
    print('关闭文件')

    ti2 = time.time()
    print(f'用时：{ti2 - ti1}')
