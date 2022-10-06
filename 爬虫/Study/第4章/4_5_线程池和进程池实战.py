# 1.如何提取单个页面的数据
# 2.上线程池，多个页面同时抓取

import requests
import csv
# 导入线程池
from concurrent.futures import ThreadPoolExecutor


url = 'http://www.xinfadi.com.cn/getPriceData.html'
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
}


def download_one_page(url, dat):
    resp = requests.post(url, data=dat)
    # print(resp.json())
    ls = resp.json()['list']
    l = []
    dic = {}
    for i in ls:
        for j in i.keys():
            l.append(j)
        break
    head = tuple(l)
    csvwriter = csv.DictWriter(f, head)
    csvwriter.writerows(ls)
    print("over!")
    f.close()
    resp.close()


if __name__ == '__main__':
    # 抓取单个页面
    # download_one_page(url, data)
    # 创建10的线程池
    with ThreadPoolExecutor(10) as t:
        # 获取50页数据
        for i in range(1, 50):
            # 把下载任务提交给线程池
            data = {
                'limit': '20',
                'current': f'{i}'
            }
            f = open(f'./csv/data/data{i}页', 'w', encoding='utf-8', newline='')
            t.submit(download_one_page(url, data))
    print('全部下载完毕!')


