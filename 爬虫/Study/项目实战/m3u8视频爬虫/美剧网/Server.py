import requests
import re
import os
# pip install pycryptodome
from Crypto.Cipher import AES
import asyncio
import aiohttp

# copy /b *.ts movie_new.ts
# https://www.meijuw.com/vodplay/90223-1-1/

# 创建文件夹
dirName1 = 'tsLib'
dirName2 = 'm3u8'
if not os.path.exists(dirName1):
    os.mkdir(dirName1)

if not os.path.exists(dirName2):
    os.mkdir(dirName2)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# 一级m3u8
m1_url = 'https://v4.cdtlas.com/20220612/LlEuhEYD/index.m3u8'
# m1_page_text = requests.get(m1_url, headers=headers).text.strip()
# print(m1_page_text)
# m1_page_text = requests.get(m1_url, headers=headers).text
f1 = open('./m3u8/1_m3u8.m3u8', 'r+', encoding='utf-8')
# f1.write(m1_page_text)
m1_page_text = f1.read().strip()
f1.close()

# 从一级m3u8文件解析出二级m3u8地址
# 二级m3u8地址
m2_url = m1_page_text.split('\n')[-1]
print(m2_url)
m2_url = f"{m1_url.split('//')[0]}//{m1_url.split('//')[1].split('/')[0]}{m2_url}"
# print(m2_url)
# 请求二级文件地址内容
# m2_page_text = requests.get(m2_url, headers=headers).text.strip()
f2 = open('./m3u8/2_m3u8.m3u8', 'r+', encoding='utf-8')
# f2.write(m2_page_text)
f2.seek(0, 0)
m2_page_text = f2.read()
f2.close()
# print(m2_page_text)

# 解析出解密密钥key的地址
key_url = re.findall('URI="(.*?)"', m2_page_text, re.S)[0]
print(key_url)

# 请求key的地址，获取密钥
'''
    注意：key和IV需要为bytes类型
'''
key = requests.get(key_url, headers=headers).content
iv = b"0000000000000000"
# print(key)

# 解析出每一个ts切片的地址
ts_url_list = []
for line in m2_page_text.split('\n'):
    if not line.startswith('#'):
        ts_url = line
        ts_url_list.append(ts_url)


# print(ts_url_list)

# 异步请求每一个ts片段的数据
async def get_ts(ur):
    async with aiohttp.ClientSession() as session:
        async with await session.get(ur, headers=headers) as resp:
            ts_data = await resp.read()  # 获取byte形式的数据
            await asyncio.sleep(2)
            # 解密ts数据
            # 需要对ts片段数据进行解密 （需要用到key和iv）
            # 实例化对象
            aes = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
            desc_data = aes.decrypt(ts_data)  # 获取解密后的数据
            return desc_data, ur


def download(t):
    data, tsUrl = t.result()
    ts_name = tsUrl.split('/')[-1]
    ts_path = f'./{dirName1}/{ts_name}'
    with open(ts_path, 'wb') as fp:
        fp.write(data)
        print(f'保存{ts_name}')


tasks = []
for url in ts_url_list:
    c = get_ts(url)
    task = asyncio.ensure_future(c)
    task.add_done_callback(download)
    tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
