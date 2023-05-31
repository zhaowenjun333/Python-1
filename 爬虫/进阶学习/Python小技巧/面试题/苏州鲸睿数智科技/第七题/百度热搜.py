import os
import sys
import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver import ActionChains, Keys
import collections

import timeit

class BaiDu:
    def __init__(self):
        self.baidu_url = 'https://www.baidu.com/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        self.keywords = '面试'
        self.chart_set = 'utf-8'

        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
        self.excel_path = f'{self.base_dir}/EXCEL'
        if not os.path.exists(self.excel_path):
            os.mkdir(self.excel_path)

        self.col = ('序号', 'title', 'url')
        self.book = xlwt.Workbook(encoding=self.chart_set, style_compression=0)
        self.sheet = self.book.add_sheet('百度热搜信息', cell_overwrite_ok=True)
        for c in range(len(self.col)):
            self.sheet.write(0, c, self.col[c])

    def chrome_driver(self):
        # s = input('请先在cmd中打开, 然后输入yes:')
        s = 's'
        options = webdriver.ChromeOptions()
        if s.lower() == 'y':
            # 方式一
            # 等效在cmd中执行：chrome --remote-debugging-port=9222
            options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
            # options.add_argument('--headless')
            chrome_driver = webdriver.Chrome(chrome_options=options)
        else:
            # 方式二
            # proxy = 'http://104.223.212.161:65432'
            # options.add_argument('--headless')
            # options.add_argument(f'--proxy-server={proxy}')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument(f'user-agent={self.headers["user-agent"]}')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('disable-infobars')
            options.add_argument("service_args = ['–ignore - ssl - errors = true', '–ssl - protocol = TLSv1']")
            chrome_driver = webdriver.Chrome(chrome_options=options)
            chrome_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
            })
        return chrome_driver

    def save_data(self, lst):
        for m in lst:
            for n in range(len(self.col)):
                self.sheet.write(m['序号']+1, n, m[self.col[n]])
        self.book.save(f'{self.excel_path}/百度热搜信息.xls')

    def run(self):
        driver = self.chrome_driver()
        # 显示等待
        wait = WebDriverWait(driver, 10)
        # 打开网址
        driver.get(self.baidu_url)
        driver.implicitly_wait(2)
        search_element = driver.find_element(By.XPATH, '//input[@class="s_ipt"]')
        # if search_element.get_attribute('value'):
        #     search_element.clear()

        search_element.send_keys(self.keywords)
        search_element.send_keys(Keys.ENTER)
        driver.implicitly_wait(2)
        lst = []
        top_list = driver.find_elements(By.XPATH, '//div[@class="opr-toplist1-table_3K7iH"]/div[not(@style)]/div[contains(@class, "toplist")]')
        for i in top_list:
            try:
                item = collections.OrderedDict()
                a = i.find_element(By.XPATH, './div/a')
                item = {
                    '序号': top_list.index(i),
                    'title': a.get_attribute('title'),
                    'url': a.get_attribute('href')
                }
                lst.append(item)
            except Exception as e:
                print(f'异常信息{e}')
            driver.implicitly_wait(2)

        self.save_data(lst)


if __name__ == '__main__':
    baidu = BaiDu()
    t = timeit.timeit(stmt=baidu.run, number=1)
    print(t)

