# 7.(必做题1)目标网站：https://www.zhipin.com/job_detail/?query=&city=101250100&industry=&position=
# 需求：
# 1、点击全部城市
# 2、地区选择 广州
# 3、输入关键字 python
# 4、抓取到前10页所有的岗位标题，地区，薪资，公司名称
# 5、保存到csv
# 提示，适当的页面等待

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
import csv
import asyncio


class ZPSpider:
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
        self.driver.get('https://www.zhipin.com/job_detail/?query=&city=101250100&industry=&position=')
        time.sleep(3)

    def Login(self):
        # 登录
        self.driver.find_element(By.CLASS_NAME, 'btn-outline').click()
        time.sleep(3)
        print(self.driver.current_url)  # 当前页面的url
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
        # 手机号
        self.driver.find_elements(By.XPATH, '//span[@class="ipt-wrap"]/input[@class="ipt ipt-phone required"]')[1].send_keys('17302254866')
        # 同意
        self.driver.find_elements(By.CLASS_NAME, 'agree-policy')[1].click()
        # 验证按钮
        # self.driver.find_element(By.XPATH, '//div[@id="regVerrifyCode"]').click()
        time.sleep(2)
        # self.driver.find_element(By.CLASS_NAME, 'yidun_intelli-control').click()
        # 发送验证码
        self.driver.find_elements(By.XPATH, '//span[@class="ipt-wrap"]/button[@class="btn btn-sms"]')[1].click()

    def City(self):
        all_city = self.driver.find_element(By.CLASS_NAME, 'btn-allcity')
        all_city.click()
        # print(self.driver.current_url)  # 当前页面的url
        time.sleep(2)
        # 点击广州
        self.driver.find_element(By.XPATH, '//ul[@class="section-city"]/li[4]').click()
        time.sleep(1)

    def Search(self):
        self.driver.find_element(By.CLASS_NAME, 'ipt-search').send_keys('python')
        self.driver.find_element(By.CLASS_NAME, 'ipt-search').send_keys(Keys.ENTER)

    def parseData(self):
        height = 1200
        self.driver.execute_script(
            f'window.scrollTo(0, document.body.scrollHeight-{height})'
        )
        lis = self.driver.find_elements(By.CLASS_NAME, 'info-primary')
        lst = []
        for info in lis:
            try:
                item = {}
                item['岗位标题'] = info.find_element(By.XPATH, './/div[@class="job-title"]/span[@class="job-name"]').text
                item['地区'] = info.find_element(By.XPATH, './/div[@class="job-title"]//span[@class="job-area"]').text
                item['薪资'] = info.find_element(By.XPATH, './/div[@class="job-limit clearfix"]/span[@class="red"]').text
                item['公司名称'] = info.find_element(By.XPATH, '//div[@class="info-company"]//h3/a').text
                lst.append(item)
            except Exception as e:
                print(e)
            time.sleep(2)
        return lst

    async def saveData(self, page, lst):
        header = ('岗位标题', '地区', '薪资', '公司名称')
        with open(f'./Data/Boss直聘/{page}.csv', 'w', encoding='utf-8', newline='') as f:
            csvwriter = csv.DictWriter(f, header)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            print(f'第{page}页下载完毕')
            f.close()

    async def main(self):
        # 登录
        # self.Login()
        # 选择城市
        self.City()
        # 搜索Python
        self.Search()
        # 异步下载
        tasks = []
        for i in range(0, 2):
            lst = self.parseData()
            if self.driver.page_source.find('next disabled') == -1:

                # self.driver.find_element(By.CLASS_NAME, 'next').click()

                # js点击
                div_tag = self.driver.find_element(By.CLASS_NAME, 'next')
                self.driver.execute_script('arguments[0].click();', div_tag)

                print(lst)
                tasks.append(asyncio.create_task(self.saveData(i+1, lst)))
            else:
                self.driver.quit()
                break
        await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    spider = ZPSpider()
    asyncio.run(spider.main())
    t2 = time.time()
    print(t2 - t1)
