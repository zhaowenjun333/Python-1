from fontTools.ttLib import TTFont
import requests

# 加载字体文件
sz = TTFont('szec.ttf')
# sz.saveXML('sz.xml')

# 得到映射关系
# print(sz.getBestCmap())

# 替换后的字典
replace_dict = {}

for k, v in sz.getBestCmap().items():
    # 转换16进制
    # 把0x替换成&#x, 并加;结尾
    # print(k, v)
    key = hex(k).replace('0x', '&#x') + ';'
    # print(key, v)
    value = int(v[-2:]) - 1
    # print(f'{key}{value}')
    replace_dict[key] = value

# print(replace_dict)

url = 'http://shanzhi.spbeen.com/index/'

resp = requests.get(url)
# print(resp.text)
html = resp.text

for k, v in replace_dict.items():
    html = html.replace(k, f'{v}')

# print(html)
