from aip import AipOcr
from fontTools.ttLib import TTFont
import json

APP_ID = '27411961'
APP_KEY = 'jUbsK7TsBPTTqd4ZNHMiaZyM'
SECRET_KEY = 'YiTkxM9LHZVI6GwsI2LMwIfoDGZTIjeC'

# 初始化对象
client = AipOcr(APP_ID, APP_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


def woff(file):
    # 加载字体文件
    wo = TTFont(file)
    file_xml = file.replace('woff', 'xml')
    wo.saveXML(file_xml)
    str_list = wo.getGlyphOrder()[2:]
    return str_list


# 高精度版本
def high_ocr(image):
    # 通用文字识别
    # client.basicGeneral(image)
    result = client.basicAccurate(image)['words_result']
    text = ''.join([i['words'] for i in result])
    return text


def dict_zip(words_list, text):
    words_dict = {}
    for k, v in zip(words_list, text):
        words_dict[k.replace('uni', '&#x') + ';'] = v
    return words_dict


if __name__ == '__main__':
    image1 = get_file_content('address.png')
    image2 = get_file_content('num.png')

    address_list = woff('5e8c7271.woff')
    num_list = woff('fdfa8a0f.woff')

    address_text = high_ocr(image1)
    address_text = list(address_text)
    address_text.insert(address_text.index('下') + 1, '県')
    num_text = high_ocr(image2).replace('果', '県')

    address_dict = dict_zip(address_list, address_text)
    num_dict = dict_zip(num_list, num_text)

    print(address_dict)
    print(num_dict)

    with open('address.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(address_dict))
        print('address_dict:over!')

    with open('num.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(num_dict))
        print('num_dict:over!')
