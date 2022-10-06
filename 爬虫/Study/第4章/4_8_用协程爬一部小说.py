# https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306063500"}    =>   所有章节的内容(名称, cid)  不需要异步
# https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":1}

import requests
import asyncio
import aiohttp
import aiofiles
import json
import time

# 1.同步操作：访问getCatalog  拿到所有章节的名称和cid
# 2.异步操作：访问getChapterContent  下载所有的文章内容


async def aiodownload(cid, b_id, title):
    data = {
        "book_id": b_id,
        "cid": f"{b_id}|{cid}",
        "need_bookinfo": 1
    }
    data = json.dumps(data)     # 转成json字符串
    # 准备url
    url = f'https://dushu.baidu.com/api/pc/getChapterContent?data={data}'
    # 发送请求
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic = await resp.json()
            content = dic['data']['novel']['content']
            async with aiofiles.open(f'./novels/西游记/{title}', 'w', encoding='utf-8') as f:
                # 异步需要加await
                await f.write(content)


async def getCatalog(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    dic = resp.json()
    tasks = []
    for item in dic['data']['novel']['items']:
        title = item['title']
        cid = item['cid']
        # 准备异步任务
        tasks.append(aiodownload(cid, book_id, title))
    # asyncio.run(await asyncio.wait(tasks))   函数不使用async定义
    await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    book_id = "4306063500"
    ur = 'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + book_id + '"}'
    asyncio.run(getCatalog(ur))
    t2 = time.time()
    print("over!")
    print(t2-t1)

