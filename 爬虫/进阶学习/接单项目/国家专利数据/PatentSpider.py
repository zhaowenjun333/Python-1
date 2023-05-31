import re

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver import ActionChains, Keys
import urllib.request
from lxml import etree
import cv2

import random
import os
import sys

import time
import timeit
import urllib3
urllib3.disable_warnings()


class PatentSpider:
    def __init__(self, username, password):
        self.search_url = 'https://pss-system.cponline.cnipa.gov.cn/conventionalSearch'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.username = username
        self.password = password

        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
        self.image_dir = 'image'
        self.image_dir_path = self.base_dir + '/' + self.image_dir
        if not os.path.exists(self.image_dir_path):
            os.mkdir(self.image_dir_path)

        # 有缺口的背景图片
        self.back_file = './image/back.png'
        # 缺口图片
        self.tp_file = './image/tp.png'

    def chrome_driver(self):
        # s = input('请先在cmd中打开, 然后输入yes:')
        s = 'y'
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

    # 进行识别
    # 获取缺口偏移量
    # 识别缺口位置
    def identify_gap(self, bg_image, tp_image, out="./image/new_image.png"):
        """
        通过cv2计算缺口位置
        :param bg_image: 有缺口的背景图片文件
        :param tp_image: 缺口小图文件图片文件
        :param out: 绘制缺口边框之后的图片
        :return: 返回缺口位置
        """
        # 读取背景图片和缺口图片
        bg_img = cv2.imread(bg_image)  # 背景图片
        tp_img = cv2.imread(tp_image)  # 缺口图片

        # 识别图片边缘
        # 因为验证码图片里面的目标缺口通常是有比较明显的边缘 所以可以借助边缘检测算法结合调整阈值来识别缺口
        # 目前应用比较广泛的边缘检测算法是Canny John F.Canny在1986年所开发的一个多级边缘检测算法 效果挺好的
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)

        # 转换图片格式
        # 得到了图片边缘的灰度图，进一步将其图片格式转为RGB格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        # 缺口匹配
        # 一幅图像中找与另一幅图像最匹配(相似)部分 算法：cv2.TM_CCOEFF_NORMED
        # 在背景图片中搜索对应的缺口
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        # res为每个位置的匹配结果，代表了匹配的概率，选出其中「概率最高」的点，即为缺口匹配的位置
        # 从中获取min_val，max_val，min_loc，max_loc分别为匹配的最小值、匹配的最大值、最小值的位置、最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        # 绘制方框
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite(out, bg_img)  # 保存在本地

        # 返回缺口的X坐标
        return tl[0]

    # 生成移动轨迹
    def get_track(self, distance):
        # 移动轨迹
        track = []
        # 当前位置
        current = 0
        """
        如果是匀速运动 极验很有可能会识别出它是程序的操作 因为人是没有办法做到完全匀速拖动的
        需要用到物理学里面的两个公式
        通过这两个公式可以构造轨迹移动算法 计算出先加速后减速的运动轨迹
        """
        # 减速阈值(大概到3/4的位置 开始减速)
        mid = distance * 3 / 4
        # 计算间隔
        t = 0.5
        # 初速度
        v = 0
        while current < distance:
            if current < mid:
                a = random.randint(4, 5)
            else:
                a = -random.randint(9, 10)
            # 初速度
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 0.5 * a * t * t
            # round：https://www.runoob.com/python/func-number-round.html
            track.append(round(move))  # 把计算得到的新的移动距离放入移动轨迹列表中
            current += move  # 更新当前位置

        return track

    def move_slide(self, chrome_driver, left):
        # 定位滑块坐标
        icon = chrome_driver.find_element(By.XPATH, '//div[@class="verify-move-block"]')
        # 实例化对象
        action = ActionChains(chrome_driver)
        # 鼠标动作链
        # 移动到滑块按钮位置  按住准备滑动
        # 鼠标左键按下不放
        action.move_to_element(icon).click_and_hold(icon).perform()
        track = self.get_track(left)
        for x in track:
            ActionChains(chrome_driver).move_by_offset(xoffset=x, yoffset=0).perform()  # 提交才生效
        time.sleep(0.5)
        # 释放
        ActionChains(chrome_driver).release().perform()
        chrome_driver.implicitly_wait(3)
        if chrome_driver.current_url == self.search_url:
            print('登陆成功')

    def login(self, chrome_driver, chrome_wait):
        chrome_driver.implicitly_wait(2)

        login_button = chrome_driver.find_element(By.XPATH, '//div[@class="loginul" and contains(text(), "登录")]')
        login_button[0].click()

        chrome_driver.implicitly_wait(1)
        # 实例化对象
        action = ActionChains(chrome_driver)
        uname_input_xpath = '//div[@class="login-input-template el-input el-input--medium el-input--prefix el-input--suffix"]/input[@type="text"]'
        uname_input = chrome_driver.find_element(By.XPATH, uname_input_xpath)
        chrome_driver.implicitly_wait(1)
        action.move_to_element(uname_input).double_click(uname_input).send_keys_to_element(uname_input, self.username).perform()
        print('输入账号')
        password_input_xpath = '//div[@class="login-input-template el-input el-input--medium el-input--prefix el-input--suffix"]/input[@type="password"]'
        password_input = chrome_driver.find_element(By.XPATH, password_input_xpath)
        action.move_to_element(password_input).double_click(password_input).send_keys_to_element(password_input, self.password).perform()
        print('输入密码')

        # 登录按钮
        do_login = chrome_driver.find_element(By.XPATH, '//button[@class="el-button login-btn el-button--default el-button--medium"]')
        action.move_to_element(do_login).click(do_login).perform()
        print('点击登录')

        # 某个页面后判定元素中是否存在指定的文本
        chrome_wait.until(ec.text_to_be_present_in_element(
            (By.XPATH, '//div[@class="verify-bar-area"]/span[@class="verify-msg"]'), '向右滑动完成验证')
        )

        time.sleep(1)

        # 获取滑块图片和背景图片
        html = chrome_driver.page_source
        html_element = etree.HTML(html)

        back_img_xpath = '//div[@class="verify-img-panel"]/img/@src'
        back_img = html_element.xpath(back_img_xpath)[0]
        urllib.request.urlretrieve(back_img, self.back_file)

        tp_img_xpath = '//div[@class="verify-sub-block"]/img/@src'
        tp_img = html_element.xpath(tp_img_xpath)[0]
        urllib.request.urlretrieve(tp_img, self.tp_file)

    def get_cookies(self, chrome_driver):
        cookies = chrome_driver.get_cookies()
        li = []
        for cookie in cookies:
            # print(cookie)
            name = cookie['name']
            value = cookie['value']
            li.append(f'{name}={value}')
        cookie = '; '.join(li)
        print(cookie)

    def run(self):
        driver = self.chrome_driver()
        # 显示等待
        wait = WebDriverWait(driver, 10)

        # 打开网址
        driver.get(self.search_url)
        print(driver.get_cookies())

        driver.delete_all_cookies()
        print(driver.get_cookies())
        # driver.delete_cookie('dX1xbeyMT58WP')
        # driver.delete_cookie('dX1xbeyMT58WO')

        driver.implicitly_wait(2)
        driver.refresh()
        driver.implicitly_wait(2)
        # driver.maximize_window()
        self.login(driver, wait)

        left = self.identify_gap(self.back_file, self.tp_file) * 1.25
        print(left)
        left += 3
        self.move_slide(driver, left)
        self.get_cookies(driver)


if __name__ == '__main__':
    uname = '17302254866'
    pwd = 'Lry1730225@'
    patent = PatentSpider(uname, pwd)
    t = timeit.timeit(stmt=patent.run, number=1)
    print(t)
