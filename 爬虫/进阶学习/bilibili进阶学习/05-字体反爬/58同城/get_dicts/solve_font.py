import requests
import re
import base64
from fontTools.ttLib import TTFont
from lxml import etree
from io import BytesIO

header1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'cookie': 'id58=CocGRmNhSUWvQzXzL4SMAg==; 58tj_uuid=99f4b17b-a446-4330-98bf-831ca8085f9c; new_uv=1; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DhsDsM1O7IdbtvjXMZqnDlMGQ05E2MHuiDIbDIGJv5ybT7PwgTHVhRCV8KqSqqJaw%2526wd%253D%2526eqid%253De25bdcf700000cdb000000046361493e; Hm_lvt_b4a22b2e0b326c2da73c447b956d6746=1667320135; ipcity=sh%7C%u4E0A%u6D77; als=0; myfeet_tooltip=end; new_session=0; Hm_lpvt_b4a22b2e0b326c2da73c447b956d6746=1667320245; city=sh; wmda_uuid=181f2e7d2e3c1d7f18e3954a4c0f0ddd; wmda_new_uuid=1; 58home=sh; sessionid=4534af3c-ed92-4039-8d57-91d839a87ab0; param8616=1; param8716kop=1; www58com="UserID=90297463171610&UserName=ddr9ymc1b"; 58cooper="userid=90297463171610&username=ddr9ymc1b"; 58uname=ddr9ymc1b; passportAccount="atype=0&bstate=0"; xxzl_smartid=cf0b87f75f8e04c8dce7489d12bf5c3f; ljrzfc=1; wmda_visited_projects=%3B1731916484865%3B11187958619315%3B10104579731767%3B1731918550401; xxzl_cid=c404c49b95e94fa38cd0252713aec404; xxzl_deviceid=PE38n1EmimQAjbBdwayAf0vLeSrikC0+3yS7r14xTxjn2RAklRU8OSfol4RVXhkW; JSESSIONID=5A50BAF1D26E7893B77B791904C73F63; PPU="UID=90297463171610&UN=ddr9ymc1b&TT=29af4d351f779da04719b19c2e9ddb83&PBODY=Z1y81T76WPgdobUZOUsKs62Sx8bo8gPMfTO2DLgZO_srovzgkaK-vmzBSUpsdJwV3DB1Rfy9nDWtq7yBcdYbDQiQdd_gI-G3i6J48_aem4gNfbtE_AeSYDvWFQPhSlXbN--JOmNeDBuLZus5ORC6GW8gDcrFSw4WI4Q6ryFrkQA&VER=1&CUID=SCqHayrOQUQJ6On4s0WvDA"'
}

# url1 = 'https://jllist.58.com/resume/searchpage'
# # session = requests.Session()
# # session.headers.update(header1)
# # resp1 = session.get(url1)
# # print(resp1.text)
#
# resp2 = requests.get(url1, headers=header1).text
# # print(resp2)
#
# # 匹配加密字符串
# result = re.search(r'base64,(.*?)\)', resp2, re.S).group(1)
# # print(result)
# b = base64.b64decode(result)
# # print(b)
# tf = TTFont(BytesIO(b))
# # print(tf)
# file_path = '../字体文件/zitiku1.woff'
# with open(file_path, 'wb') as f:
#     f.write(b)
# fonts = TTFont(file_path)
# file_xml = file_path.replace('woff', 'xml')
# fonts.saveXML(file_xml)
# str_list = fonts.getGlyphOrder()
# print(str_list)

url2 = 'https://jllist.58.com/resume/search?pageNumb=1&resumeSort=intelligent&update24Hours=1&cityId=2&cityType=guishu&fontKey=d36b7ea8b34e4ddbbda1600b69e380bc&fontkey=d36b7ea8b34e4ddbbda1600b69e380bc&_=1667626841525&callback=axiosJsonpCallback2'

header2 = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'id58=CocGRmNhSUWvQzXzL4SMAg==; 58tj_uuid=99f4b17b-a446-4330-98bf-831ca8085f9c; Hm_lvt_b4a22b2e0b326c2da73c447b956d6746=1667320135; als=0; myfeet_tooltip=end; city=sh; wmda_uuid=181f2e7d2e3c1d7f18e3954a4c0f0ddd; wmda_new_uuid=1; 58home=sh; param8616=1; param8716kop=1; 58uname=ddr9ymc1b; passportAccount="atype=0&bstate=0"; xxzl_smartid=cf0b87f75f8e04c8dce7489d12bf5c3f; wmda_visited_projects=%3B1731916484865%3B11187958619315%3B10104579731767%3B1731918550401; xxzl_deviceid=PE38n1EmimQAjbBdwayAf0vLeSrikC0+3yS7r14xTxjn2RAklRU8OSfol4RVXhkW; ljrzfc=1; xxzl_cid=c404c49b95e94fa38cd0252713aec404; new_session=1; new_uv=4; utm_source=; spm=; init_refer=; JSESSIONID=3E38BB737A17AF9E16500FC8B2D55402; PPU="UID=90297463171610&UN=ddr9ymc1b&TT=29af4d351f779da04719b19c2e9ddb83&PBODY=D76MyNt37ShSNJCRPElaG4PES-c_y0CdBUWvJL5wtTH-mITR_ipRFGjQ0RB4duCALAf2Dn6gZXNlCc2oY9HYO6NptBGYXUd_gtM21LPPTuyjcDO-UdVzhDumg9b1d22lGobW9LARAw0uSx5o5aoCjiqFFR1hzesiRiQDEgHTxjc&VER=1&CUID=SCqHayrOQUQJ6On4s0WvDA"',
    'referer': 'https://jllist.58.com/resume/searchpage',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

resp3 = requests.get(url2, headers=header2)
obj = re.compile(r'"nowPosition":"(?P<nowPosition>.*?)","targetPosition":"(?P<targetPosition>.*?)",'
                 r'"education":"(?P<education>.*?)","workYear":"(?P<workYear>.*?)".*?'
                 r'"sexText":"(?P<sexText>.*?)".*?"ageText":"(?P<ageText>.*?)".*?'
                 r'"targetArea":"(?P<targetArea>.*?)","targetSalary":"(?P<targetSalary>.*?)".*?'
                 r'"lspot":(?P<lspot>.*?)],"letter":"(?P<letter>.*?)".*?'
                 r'"experYears":"(?P<experYears>.*?)".*?"resumeTp":"(?P<resumeTp>.*?)".*?'
                 r'"url":"(?P<url>.*?)".*?'
                 r'"activeTime":"(?P<activeTime>.*?)"', re.S)
content = resp3.text
# print(content)

resumeList = obj.finditer(content)
items = []
first = True
for resume in resumeList:
    if first:
        url = f'https:{resume.group("url")}'
        # print(url)
        resp = requests.get(url, headers=header1).text
        # print(resp)
        # 匹配加密字符串
        result = re.search(r'base64,(.*?)\)', resp, re.S).group(1)
        # print(result)
        b = base64.b64decode(result)
        # print(b)
        # tf = TTFont(BytesIO(b))
        # print(tf)
        file_path = '../字体文件/zitiku1.woff'
        with open(file_path, 'wb') as f:
            f.write(b)
            f.close()
        fonts = TTFont(file_path)
        file_xml = file_path.replace('woff', 'xml')
        fonts.saveXML(file_xml)
        str_list = fonts.getGlyphOrder()
        print(str_list)
        first = False
with open('../字体文件/zitiku1.xml', 'rb') as f:
    xml = f.read()
xml_element = etree.XML(xml)
TTGlyph_lst = xml_element.xpath('//TTGlyph')[1:-1]
for TTGlyph in TTGlyph_lst:
    name = TTGlyph.xpath('.//@name')[0]
    xMin = TTGlyph.xpath('.//@xMin')[0]
    yMin = TTGlyph.xpath('.//@yMin')[0]
    xMax = TTGlyph.xpath('.//@xMax')[0]
    yMax = TTGlyph.xpath('.//@yMax')[0]
    print(name, (xMin, yMin, xMax, yMax))
    # item = {
    #     'nowPosition': resume.group('nowPosition'),
    #     'targetPosition': resume.group('targetPosition'),
    #     'education': resume.group('education'),
    #     'workYear': resume.group('workYear'),
    #     'sexText': resume.group('sexText'),
    #     'ageText': resume.group('ageText'),
    #     'targetArea': resume.group('targetArea'),
    #     'targetSalary': resume.group('targetSalary'),
    #     'lspot': resume.group('lspot'),
    #     'letter': resume.group('letter'),
    #     'experYears': resume.group('experYears'),
    #     'resumeTp': resume.group('resumeTp'),
    #     'activeTime': resume.group('activeTime')
    # }
    # print(item)
    # break
    # items.append(item)
# print(items)
