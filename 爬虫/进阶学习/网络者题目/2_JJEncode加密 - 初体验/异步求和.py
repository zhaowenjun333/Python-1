import asyncio
import random
import requests
import aiohttp
import execjs
import urllib3
import time

class JJEncodeSpider:
    def __init__(self):
        self.url = 'https://www.wangluozhe.com/challenge/2'
        self.api_url = 'https://www.wangluozhe.com/challenge/api/2'
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        ]
        self.headers = {
            'origin': 'https://www.wangluozhe.com',
            'referer': self.url,
            'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        self.cookies = {
            'session': 'c094ae59-d1ad-4dc7-9262-0b0dcdfd24a3.o3KaxQr4I-e2gVXLO8nalqkXZLU'
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        for k, v in self.cookies.items():
            self.session.cookies.set(k, v)
        self.chart_set = 'utf-8'

        self.js_filename = 'JS/w2.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_compile = execjs.compile(self.js_f.read())
        self.js_f.close()
        self .num = []

    async def aiosum(self, datas, semaphore):
        with open(self.js_filename, 'r', encoding=self.chart_set) as f:
            js_code = f.read()
            f.close()
            datas['_signature'] = execjs.compile(js_code).call('_signature')
        async with semaphore:
            async with aiohttp.ClientSession(headers=self.headers, cookies=self.cookies) as session:
                async with session.post(self.api_url, data=datas, ssl=False) as resp:
                    content = await resp.json()
                    print(content)
                    if content:
                        self.num.append(sum([i['value'] for i in content['data']]))
                    else:
                        print(f'{datas["page"]}重新请求')
                        # datas['_signature'] = self.js_compile.call('_signature')
                        # resp = self.session.post(self.api_url, data=datas, verify=False)
                        # content = resp.json()
                        # if content:
                        #     self.num.append(sum([i['value'] for i in content['data']]))
                        # else:
                        await self.aiosum(datas, semaphore)

    async def main(self):
        semaphore = asyncio.Semaphore(61)  # 限制并发量为12
        tasks = []
        for page in range(1, 101):
            datas = {
                'page': page,
                'count': '10',
                # '_signature': self.js_compile.call('_signature')
            }
            tasks.append(asyncio.create_task(self.aiosum(datas, semaphore)))
        await asyncio.wait(tasks)
        print(sum(self.num))


if __name__ == '__main__':
    t1 = time.time()
    jj = JJEncodeSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(jj.main())
    # asyncio.run(jj.main())
    # jj.deal_num()
    t2 = time.time()
    print(t2 - t1)
