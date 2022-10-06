# 8.(必做题2)目标网站：https://music.163.com/#/song?id=399354373
# 需求：
# 1、爬取前10页此音乐对应的名字以及评论信息
# 2、保存到csv(名字和评论要对应)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
import csv
import asyncio


class WYunSpider:
    def __init__(self):
        # 反爬
        self.options = webdriver.ChromeOptions()
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
        self.driver.get('https://music.163.com/#/song?id=399354373')
        time.sleep(3)

    def BgMusic(self):
        self.driver.switch_to.frame('g_iframe')
        self.driver.find_element(By.XPATH, '//div[@id="content-operation"]/a[@class="u-btn2 u-btn2-2 u-btni-addply f-fl"]').click()

    def parseData(self):
        self.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)'
        )
        comments = self.driver.find_elements(By.CLASS_NAME, 'cntwrap')
        print(f"本页获取{len(comments)}条数据")
        lst = []
        for comment in comments:
            try:
                item = {}
                item['评论人'] = comment.find_element(By.XPATH, './/div[@class="cnt f-brk"]/a[@class="s-fc7"]').text
                item['评论信息'] = comment.find_element(By.XPATH, './/div[@class="cnt f-brk"]').text.replace(item['评论人'], '').replace('：', '')
                item['评论时间'] = comment.find_element(By.CLASS_NAME, 'time').text
                item['点赞量'] = comment.find_element(By.XPATH, './/i[@class="zan u-icn2 u-icn2-12"]/..').text.strip(" (").strip(")")
                # print(item.txt)
                lst.append(item)
            except Exception as e:
                print(e)
            time.sleep(2)
        return lst

    async def saveData(self, page, lst):
        header = ('评论人', '评论信息', '评论时间', '点赞量')
        # 解决乱码问题
        with open(f'./Data/可惜没有如果/{page}.csv', 'w', encoding='utf-8-sig', newline='') as f:
            csvwriter = csv.DictWriter(f, header)  # 标题
            csvwriter.writeheader()  # 写入标题
            csvwriter.writerows(lst)  # 写入数据
            print(f'第{page}页下载完毕')
            f.close()

    async def main(self):
        self.BgMusic()
        # 异步下载
        tasks = []
        for i in range(0, 10):
            lst = self.parseData()
            if self.driver.page_source.find('zbtn znxt js-n-1654093570790 js-disabled') == -1:
                u_page = self.driver.find_element(By.CLASS_NAME, 'u-page')
                u_page.find_element(By.XPATH, './/a[last()]').click()
                print(lst)
                tasks.append(asyncio.create_task(self.saveData(i+1, lst)))
                time.sleep(2)
            else:
                self.driver.quit()
                break
        await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    spider = WYunSpider()
    # spider.main()
    asyncio.run(spider.main())
    t2 = time.time()
    print(t2 - t1)

