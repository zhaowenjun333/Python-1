# https://cc.163.com/category/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver import ActionChains, Keys
from PIL import Image
import random
import time
import urllib.request
import cv2
import pyautogui


class WangYiCC:
    def __init__(self, username, password):
        self.start_url = 'https://cc.163.com/category/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        self.username = username
        self.password = password

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

    def login(self, chrome_driver, chrome_wait):
        chrome_driver.implicitly_wait(1)
        # try:
        #     no_reminder = chrome_driver.find_elements(By.XPATH, '//div[@class="btn-close-forever"]')
        #     if no_reminder:
        #         no_reminder[0].click()
        # except Exception as e:
        #     print(f'没有广告：{e}')
        chrome_driver.implicitly_wait(1)
        login_button = chrome_driver.find_element(By.XPATH, '//button[@class="login-btn js-need-log-now"]')
        login_button.click()
        chrome_driver.implicitly_wait(1)

        # checkbox
        agree_checkbox = chrome_driver.find_element(By.XPATH, '//em[@id="agreecheck_login"]')
        if agree_checkbox.get_attribute('class') == 'checkbox ':
            chrome_driver.execute_script('arguments[0].value="checkbox checked"', agree_checkbox)
        print('勾选同意复选框')

        # 切入iframe
        login_iframe = chrome_driver.find_element(By.XPATH, '//div[@class="login_frame"]/iframe[@name]')
        try:
            chrome_driver.switch_to.frame(login_iframe)
            # print('切入成功')
            chrome_driver.implicitly_wait(1)
        except Exception as e:
            print(e)

        # 实例化对象
        action = ActionChains(chrome_driver)

        # 选择网易通行证登录
        email_login = chrome_driver.find_element(By.XPATH, '//div[@class="u-head1 active j-head"]')
        action.move_to_element(email_login).click(email_login).perform()

        # 输入账号密码
        username_input = chrome_driver.find_element(By.XPATH, '//input[@class="j-inputtext dlemail j-nameforslide"]')
        if username_input.get_attribute('value'):
            username_input.clear()
        action.move_to_element(username_input).send_keys_to_element(username_input, self.username)
        print('输入账号')
        password_input = chrome_driver.find_element(By.XPATH, '//input[@class="j-inputtext dlpwd"]')
        if password_input.get_attribute('value'):
            password_input.clear()
        action.move_to_element(password_input).send_keys_to_element(password_input, self.password)
        print('输入密码')

        # 登录按钮
        do_login = chrome_driver.find_element(By.XPATH, '//a[@id="dologin"]')
        action.move_to_element(do_login).click(do_login).perform()
        print('点击登录')

        # 某个页面后判定元素中是否存在指定的文本
        chrome_wait.until(ec.text_to_be_present_in_element(
            (By.XPATH, '//span[@class="yidun_tips__text yidun-fallback__tip"]'), '向右拖动滑块填充拼图')
        )
        # 获取滑块图片和背景图片
        back_url = chrome_driver.find_element(By.XPATH, '//img[@class="yidun_bg-img"]')
        back_url_x = back_url.location.get('x')
        # print(back_url_x)
        tp_url = chrome_driver.find_element(By.XPATH, '//img[@class="yidun_jigsaw"]')
        # print(tp_url.size)
        urllib.request.urlretrieve(tp_url.get_attribute('src'), self.tp_file)

        chrome_driver.execute_script('arguments[0].style="left: 0px; display: none;"', tp_url)
        back_url.screenshot(self.back_file)
        chrome_driver.execute_script('arguments[0].style="left: 0px;"', tp_url)

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
        icon = chrome_driver.find_element(By.XPATH, '//div[@class="yidun_slider"]')
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
        if chrome_driver.page_source.find('登录'):
            print('登陆成功')

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
        driver.get(self.start_url)
        driver.maximize_window()
        driver.implicitly_wait(1)
        self.login(driver, wait)

        left = self.identify_gap(self.back_file, self.tp_file)
        # print(left)
        left += 3
        self.move_slide(driver, left)
        self.get_cookies(driver)


if __name__ == '__main__':
    t1 = time.time()
    uname = '17302254866@163.com'
    pwd = 'Lry1730225@'
    cc = WangYiCC(uname, pwd)
    cc.run()
    t2 = time.time()
    print(t2 - t1)
