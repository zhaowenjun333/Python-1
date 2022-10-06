import random
import time
import cv2
import pyautogui
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import request
from selenium.webdriver.chrome.options import Options
import subprocess


class ZhiHu:
    def __init__(self, username, password):
        # self.cmd = r'"D:\Programs\Python\Python39\chromedriver.exe" ' \
        #            r'--remote-debugging-port=9222'
        # subprocess.run(self.cmd)
        self.url = 'https://www.zhihu.com/signin'
        self.username = username
        self.password = password
        # 加载驱动
        # 反爬
        self.chrome_options = Options()
        # 等效在cmd中：chrome --remote-debugging-port=9222
        self.chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')

        # 加载驱动
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # self.driver = webdriver.Chrome()
        try:
            # 窗口最大化
            self.driver.maximize_window()
        except:
            pass
        # 显示等待
        self.wait = WebDriverWait(self.driver, 100)
        # 有缺口的背景图片
        self.back_file = 'back.jpg'
        # 缺口图片
        self.tp_file = 'tp.png'

    # 获取验证码
    def get_captcha(self):
        # 打开目标网页
        self.driver.get(self.url)
        # 切换登录模式：密码登录
        # self.driver.find_element(By.XPATH,'//div[@class="SignFlow-tabs"]/div[@class="SignFlow-tab"][1]').click()
        model = self.wait.until(
            # 可以点击的元素,从0开始
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="SignFlow-tabs"]/div[@class="SignFlow-tab"][1]')
            )
        )
        model.click()

        username = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@name="username"]')
            )
        )
        username.send_keys(self.username)
        password = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@name="password"]')
            )
        )
        password.send_keys(self.password)
        time.sleep(0.5)
        # 登录按钮
        bnt = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="submit"]'))
        )
        bnt.click()
        # 保存验证码图片
        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.yidun_tips__text.yidun-fallback__tip'), "向右拖动滑块填充拼图")
        )

        time.sleep(1)
        """
        selenium中的xpath语法和lxml中的xpath语法有点区别
        //img[@class="yidun_bgimg"]/@src
        selenium中需要通过get_attribute()标签内的属性
        """
        back_url = self.driver.find_element(By.CLASS_NAME, "yidun_bg-img").get_attribute('src')
        tp_url = self.driver.find_element(By.CLASS_NAME, "yidun_jigsaw").get_attribute('src')
        print(back_url)
        print(tp_url)
        request.urlretrieve(back_url, self.back_file)
        request.urlretrieve(tp_url, self.tp_file)

    # 识别缺口位置
    def identify_gap(self, bg_image, tp_image, out="new_image.png"):
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
        self.get_captcha()
        left = self.identify_gap(self.back_file, self.tp_file)
        print(left)
        left += 10
        # 定位滑块坐标
        icon = self.driver.find_element(By.XPATH, '//div[@class="yidun_slider"]/span')
        location = icon.location

        # 从location获取坐标
        x_offset = location.get('x') * 1.25
        y_offset = location.get('y') * 1.25
        print(x_offset, y_offset)
        self.move_slide(x_offset, y_offset, left * 1.25)
        # self.move_slide(778, 515, left)


if __name__ == '__main__':
    z = ZhiHu('17302254866', 'lry1730225')
    z.main()
