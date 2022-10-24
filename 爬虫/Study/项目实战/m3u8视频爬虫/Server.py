import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# 一级m3u8
m1_url = 'https://v4.cdtlas.com/20220612/LlEuhEYD/index.m3u8'
m1_page_text = requests.get(m1_url, headers=headers).text.strip()
# print(m1_page_text.split('\n'))

# 从一级m3u8文件解析出二级m3u8地址
# 二级m3u8地址
m2_url = m1_page_text.split('\n')[-1]
# print(m2_url)
m2_url = f"{m1_url.split('//')[0]}//{m1_url.split('//')[1].split('/')[0]}{m2_url}"
# print(m2_url)
# 请求二级文件地址内容
m2_page_text = requests.get(m2_url, headers=headers).text.strip()
# print(m2_page_text)

# 解析出解密密钥key的地址
key_url = re.findall('URI="(.*?)"', m2_page_text, re.S)[0]
print(key_url)

# 请求key的地址，获取密钥
'''
    注意：key和IV需要为bytes类型
'''
key = requests.get(key_url, headers=headers).content
iv = b'0000000000000000'
print(key)

# 解析出每一个ts切片的地址


# 请求到每一个ts切片的数据
# 使用秘钥key和IV向量对ts片段进行解密
# 拼接每一个ts片段合并成完整的视频文件


