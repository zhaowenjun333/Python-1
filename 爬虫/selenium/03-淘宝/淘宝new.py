import asyncio

import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

import collections
import csv
import time


class TBSpider:
    # 1. 初始化方法
    def __init__(self, username, password, cols, s):
        # 用户名
        self.username = username
        # 密码
        self.password = password

        self.chrome_options = Options()
        # 反爬
        # 等效在cmd中：chrome --remote-debugging-port=9222
        self.chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
        # 加载驱动
        self.driver = webdriver.Chrome(options=self.chrome_options)

        # 显示等待
        self.wait = WebDriverWait(self.driver, 100)

        self.url = 'https://www.taobao.com/'

        self.cols = cols
        self.sheet = s

    def login(self):
        # 打开目标网页
        self.driver.get(self.url)
        # 点击登录
        pLogin = self.wait.until(
            ec.element_to_be_clickable(
                (By.XPATH, '//div[@class="site-nav-sign"]/a[@class="h"]')
            )
        )
        pLogin.click()

        # 输入用户名
        username = self.wait.until(
            ec.element_to_be_clickable(
                (By.ID, 'fm-login-id')
            )
        )
        ActionChains(self.driver).double_click(username).perform()
        time.sleep(0.5)
        username.send_keys(self.username)

        # 输入密码
        password = self.wait.until(
            ec.element_to_be_clickable(
                (By.ID, 'fm-login-password')
            )
        )
        ActionChains(self.driver).double_click(password).perform()
        password.send_keys(self.password)
        # 点击登录
        self.wait.until(
            ec.element_to_be_clickable(
                (By.CLASS_NAME, 'password-login')
            )
        ).click()

    def parse_html(self):
        height = 800
        self.driver.execute_script(
            f'window.scrollTo(0, document.body.scrollHeight-{height})'
        )
        time.sleep(1)
        goods = self.driver.find_elements(By.CLASS_NAME, 'ctx-box')
        num = len(goods)
        print(f'本页获取{len(goods)}个数据')
        lst = []
        for good in goods:
            try:
                item = collections.OrderedDict()
                item['商品名'] = good.find_element(By.XPATH, './/div[@class="row row-2 title"]/a').text
                item['价格'] = good.find_element(By.CLASS_NAME, 'price').text
                item['付款人数'] = good.find_element(By.CLASS_NAME, 'deal-cnt').text
                item['店铺'] = good.find_element(By.XPATH, './/div[@class="shop"]/a/span[last()]').text
                item['地点'] = good.find_element(By.XPATH,
                                               './/div[@class="row row-3 g-clearfix"]/div[@class="location"]').text
                print(item)
                lst.append(item)
            except Exception as e:
                print(f'异常信息{e}')
            time.sleep(0.2)
        return lst, num

    # 存储数据
    async def saveData(self, page, lst, num):
        print(page+1)
        print('---'*10)
        for m in range(len(lst)):
            data = lst[m]
            for n in range(len(data.values())):
                self.sheet.write(m+1+page*num, n, data[self.cols[n]])

    async def run(self):
        self.login()
        time.sleep(0.5)
        self.driver.find_element(By.ID, 'q').send_keys('realmegt大师探索版手机壳')
        time.sleep(2)
        self.driver.find_element(By.ID, 'q').send_keys(Keys.ENTER)
        time.sleep(2)
        tasks = []
        for i in range(0, 6):
            lst, num = self.parse_html()
            if self.driver.page_source.find('icon icon-btn-next-2-disable') == -1:
                self.driver.find_element(By.XPATH, '//li[@class="item.txt next"]/a').click()
                # print(lst)
                tasks.append(asyncio.create_task(self.saveData(i, lst, num)))
            else:
                self.driver.quit()
                break
        await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('realmegt大师探索版手机壳', cell_overwrite_ok=True)
    col = ('商品名', '价格', '付款人数', '店铺', '地点')
    for c in range(len(col)):
        sheet.write(0, c, col[c])
    spider = TBSpider('17302254866', 'lry1730225', col, sheet)
    asyncio.run(spider.run())
    book.save('./realmegt大师探索版手机壳.xls')
    t2 = time.time()
    print(f'用时{round(t2 - t1)}s')
