import random

# from selenium import webdriver
from seleniumwire import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import ProxyType


proxies_list = ['198.49.68.80:80', '3.221.105.1:80', '172.104.80.136:80',
                '118.238.12.55:80', '154.64.117.242:80', '154.64.118.39:80',
                '112.80.248.73:80', '47.112.167.85:80', '203.78.146.70:80']

chrome_options = Options()

# 添加请求头
header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
chrome_options.add_argument(f'User-Agent={header}')
proxy = random.choice(proxies_list)
# print(proxy)
# 添加代理
chrome_options.add_argument('--proxy-server=http://%s' % proxy)

chrome = webdriver.Chrome(options=chrome_options)
chrome.get('https://www.baidu.com/')
print(chrome.get("http://httpbin.org/ip"))
# print(chrome.proxy)

# for request in chrome.requests:
#     print(dict(request.headers))
#     print(request.response.status_code)
#     print(request)
#     break
# print(chrome.page_source)
# print(chrome.title)

chrome.close()


