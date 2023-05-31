import asyncio
from httpx import AsyncClient
'''

httpx不仅支持http代理，还支持https代理。
proxies = {
    "http://": "http://localhost:8030",
    "https://": "http://localhost:8031",
}

with httpx.Client(proxies=proxies) as client:
...

'''
ur = 'http://www.baidu.com'


async def request(url):
    async with AsyncClient() as client:
        response = await client.get(url=url)
        print(response.status_code)

asyncio.run(request(ur))
