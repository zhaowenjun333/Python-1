import time
import random
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

import pyautogui

class Slide:
    def __init__(self):
        # 反爬
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 加载驱动
        self.driver = webdriver.Chrome(chrome_options=self.options)
        try:
            # 窗口最大化
            self.driver.maximize_window()
        except:
            pass
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
        })
        # 显示等待
        self.wait = WebDriverWait(self.driver, 100)
        # 加载网站
        self.url = 'https://www.geetest.com/demo/slide-float.html'
        # self.driver.get('https://www.geetest.com/demo/slide-float.html')
        # self.driver.implicitly_wait(1)

        # 有缺口的图片名称
        self.gap_img = 'tp.png'
        # 没有缺口的图片名称
        self.intact_img = 'back.png'

    def get_captcha(self):
        # 获取验证码图片，保存本地
        self.driver.get(self.url)
        # 点击按钮
        self.wait.until(
            ec.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_radar_tip_content'), '点击按钮进行验证')
        )
        self.driver.find_element(By.CLASS_NAME, 'geetest_radar_tip_content').click()

        time.sleep(1)

        # 滑块加载完毕  截图 （100%）
        # 索引 从0开始
        self.driver.execute_script('document.querySelectorAll("canvas")[1].style="opacity: 1; display: none;"')

        # 截图
        captcha_tag = self.driver.find_element(By.CLASS_NAME, 'geetest_window')
        # 有缺口的验证码图片
        captcha_tag.screenshot(self.gap_img)
        self.driver.execute_script('document.querySelectorAll("canvas")[2].style=""')

        # 没有缺口的验证码图片
        captcha_tag.screenshot(self.intact_img)

        # 恢复样式
        self.driver.execute_script('document.querySelectorAll("canvas")[1].style="opacity: 1; display: block;"')
        self.driver.execute_script('document.querySelectorAll("canvas")[2].style="display: none; opacity: 0;"')

    # 进行识别
    # 获取缺口偏移量
    def get_gap(self, image1, image2):
        """
        :param image1:
        :param image2:
        :return: 返回偏移量
        """
        # 打开图片
        image1_img = Image.open(image1)
        image2_img = Image.open(image2)
        # print(image1_img.size)      # (260, 160)
        # exit()
        # 遍历图片的每个坐标点
        # image1_img和image2_img的长宽是一样的 所以在遍历的时候用其中一张就行
        for i in range(image1_img.size[0]):      # 宽度
            for j in range(image1_img.size[1]):  # 高度
                # 判断像素点出现偏差的位置
                if not self.is_pixel_equal(image1_img, image2_img, i, j):
                    return i

    # 判断这个坐标点像素是否相同
    def is_pixel_equal(self, image1, image2, x, y):
        """
        :param image1:图片一
        :param image2:图片二
        :param x:需要对比的坐标(x)
        :param y:需要对比的坐标(y)
        :return: 像素是否相同 相同返回True 不同返回False
        """
        # 获取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 阈值 （范围）
        threshold = 60
        # 获取到两张图片对应像素点的RGB数据
        # 如果差距在一定范围之类 就代表两个像素相同 继续对比下一个像素点
        # 如果差距超过一定范围 则表示像素点不同 即为缺口位置
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        return False

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
                a = random.randint(2, 3)
            else:
                a = -random.randint(7, 8)
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

    # 移动函数
    def move_slide(self, offset_x, offset_y, left):
        """
        :param offset_x: 滑块的x轴坐标
        :param offset_y: 滑块的y轴坐标
        :param left: 需要移动的距离
        :return:
        """
        # pyautogui库操作鼠标指针
        # 移动到滑块的位置
        # duration为持续时间
        # random.uniform(参数1，参数2) 返回参数1和参数2之间的任意值
        pyautogui.moveTo(offset_x, offset_y,
                         duration=0.1 + random.uniform(0, 0.1 + random.randint(1, 100) / 100))

        # 按下鼠标 准备开始滑动
        pyautogui.mouseDown()
        # random.randint(参数1, 参数2) 函数返回参数1和参数2之间的任意整数
        offset_y += random.randint(9, 19)
        pyautogui.moveTo(offset_x + int(left * random.randint(15, 25) / 20), offset_y, duration=0.28)
        offset_y += random.randint(-9, 0)
        pyautogui.moveTo(offset_x + int(left * random.randint(18, 22) / 20), offset_y,
                         duration=random.randint(19, 31) / 100)
        offset_y += random.randint(0, 8)
        pyautogui.moveTo(offset_x + int(left * random.randint(19, 21) / 20), offset_y,
                         duration=random.randint(20, 40) / 100)
        offset_y += random.randint(-3, 3)
        pyautogui.moveTo(left + offset_x + random.randint(-3, 3), offset_y,
                         duration=0.5 + random.randint(-10, 10) / 100)
        offset_y += random.randint(-2, 2)
        pyautogui.moveTo(left + offset_x + random.randint(-2, 2), offset_y,
                         duration=0.5 + random.randint(-3, 3) / 100)
        pyautogui.mouseUp()
        time.sleep(3)

    def main(self):
        # 1. 获取两张图片
        self.get_captcha()

        # 2. 识别缺口
        left = self.get_gap(self.gap_img, self.intact_img)
        print(left)
        # if left == 1:
        #     self.driver.close()
        # 实际滑动距离 细微调整
        left -= 5
        # 3. 滑动
        track = self.get_track(left)

        # 定位滑动按钮
        btn = self.driver.find_element(By.CLASS_NAME, "geetest_slider_button")
        # 鼠标动作链
        # 移动到滑块按钮位置  按住准备滑动
        ActionChains(self.driver).click_and_hold(btn).perform()

        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()  # 提交才生效

        time.sleep(0.5)
        # 释放
        ActionChains(self.driver).release().perform()


if __name__ == '__main__':
    s = Slide()
    s.main()
