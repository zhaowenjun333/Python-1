import random
import cv2
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib import request
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import ActionChains
import threading
import time
import random
from chaojiying import Chaojiying_Client

chrome_options = Options()
# chrome --remote-debugging-port=9222
chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
driver = webdriver.Chrome(options=chrome_options)
first_img = './img/one.png'
second_img = './img/two.png'
# try:
#     # 窗口最大化
#     driver.maximize_window()
# except Exception as e:
#     print(e)

wait = WebDriverWait(driver, 100)
url = 'https://hz.fang.ke.com/loupan'
driver.get(url)

ros_but = wait.until(
    # 可以点击的元素,从0开始
    ec.element_to_be_clickable(
        (By.XPATH, '//div[@class="geetest_radar_btn"]')
    )
)
ros_but.click()

time.sleep(1)

# 保存验证码图片
# 截图
first_tag = driver.find_element(By.CLASS_NAME, 'geetest_tip_img')
first_tag.screenshot(first_img)
second_tag = driver.find_element(By.CLASS_NAME, 'geetest_item_wrap')
second_tag.screenshot(second_img)

chaojiying = Chaojiying_Client('17302254866', 'lry1730225', '937055')  # 用户中心>>软件ID 生成一个替换 96001
# img = open('back_num.png', 'rb').read()                                       # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
img1 = open('./img/one.png', 'rb').read()
words1 = list(chaojiying.PostPic(img1, 2004)['pic_str'])
print(words1)
img2 = open('./img/two.png', 'rb').read()
words2_info = chaojiying.PostPic(img2, 9501)['pic_str'].split('|')
item = {}
for i in words2_info:
    words = i.split(',')
    item[words[0]] = [eval(words[1])*1.25-30, eval(words[2])*1.25-30]
print(item)

# 1. 实例化对象
actions = ActionChains(driver)
for word in words1:
    actions.move_to_element_with_offset(second_tag, item[word][0], item[word][1]).click()
    time.sleep(1)
    print(item[word])
    # 3. 执行提交
actions.perform()

driver.find_element(By.CLASS_NAME, 'geetest_commit_tip').click()
