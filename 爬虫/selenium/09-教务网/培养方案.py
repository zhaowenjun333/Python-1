import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import Select
import time
import csv


class PlanSpider:
    def __init__(self):
        # 反爬
        self.options = webdriver.ChromeOptions()

        # self.proxy_ip = ""
        # proxy = "--proxy-server=http://" + self.proxy_ip
        # self.options.add_argument(proxy)

        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 加载驱动
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
        })
        # 加载网站
        self.driver.get('http://61.181.145.1:89/jsxsd/')
        time.sleep(3)

    def Login(self):
        self.driver.find_element(By.ID, 'userAccount').send_keys('195150118')
        self.driver.find_element(By.ID, 'userPassword').send_keys('lry981222')
        self.driver.find_element(By.ID, 'RANDOMCODE').click()
        time.sleep(5)
        # 等待输入验证码
        self.driver.find_element(By.ID, 'RANDOMCODE').send_keys(Keys.ENTER)
        # self.driver.find_element(By.CLASS_NAME, 'login_btn').click()

    def plane(self):
        # 培养管理
        self.driver.find_element(By.XPATH, '//ul[@class="first-menu"]/li[3]').click()
        self.driver.find_element(By.XPATH, '//ul[@class="sidebar-menu"]/li[5]/a').click()
        time.sleep(1)
        # 执行计划
        self.driver.find_element(By.XPATH, '//ul[@class="treeview-menu menu-open"]/li[2]').click()

    def info(self):
        # 切入iframe标签
        iframe = self.driver.find_element(By.ID, 'Frame1')
        self.driver.switch_to.frame(iframe)
        time.sleep(1)
        trs = self.driver.find_elements(By.XPATH, '//table[@id="dataList"]//tr')
        print(f'获取{len(trs)}条tr')
        # ths = self.driver.find_elements(By.CLASS_NAME, 'Nsb_r_list_thb')
        header = []
        lst = []
        for i in range(len(trs)):
            if i == 0:
                ths = trs[1].find_elements(By.XPATH, '//th[@class="Nsb_r_list_thb"]')
                print(f'获取{len(ths)}条th')
                for th in ths:
                    header.append(th.text)
            else:
                tds = trs[i].find_elements(By.XPATH, './/td')
                print(f'获取{len(tds)}条td')
                item = {}
                for j in range(len(tds)):
                    item[header[j]] = tds[j].text
                lst.append(item)
        print(header)
        print(lst)
        return header, lst

    async def save_info(self, header, lst):
        with open('./Info/培养方案.csv', 'w', encoding='utf-8', newline='') as f:
            csvwriter = csv.DictWriter(f, header)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            print('下载完毕')
            f.close()

    def main(self):
        # 登录
        self.Login()
        # 培养管理
        self.plane()
        header, lst = self.info()
        asyncio.run(self.save_info(header, lst))


if __name__ == '__main__':
    t1 = time.time()
    spider = PlanSpider()
    # asyncio.run(spider.main())
    spider.main()
    t2 = time.time()
    print(t2 - t1)
