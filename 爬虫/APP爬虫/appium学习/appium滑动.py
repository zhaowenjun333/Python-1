import time

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey

t1 = time.time()
caps = dict()
# 配置连接参数
# 测试系统
caps['platformName'] = 'Android'
# 手机安卓版本
caps['platformVersion'] = '5.1.1'
# 设备名称
caps['deviceName'] = 'Android'
# 包名
caps['appPackage'] = 'com.android.settings'
# 界面名称
caps['appActivity'] = '.Settings'
# 输入中文 设置为True
caps['unicodeKeyboard'] = True
# 恢复原来的输入法
caps['resetKeyboard'] = True
# 一般来说 不需要重置app状态
caps['noReset'] = True

# caps['newCommandTimeout'] = 6000
# caps['automationName'] = 'UiAutomator2'

# 加载驱动，连接设备
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)

# 定位WLAN
WLAN = driver.find_element(By.XPATH, '//*[@text="WLAN"]')
YY = driver.find_element(By.XPATH, '//*[@text="应用"]')

# 滑动
# 从一个元素滑动到另一个元素
# 注意滑动方向  速度慢  精准 没有惯性
driver.drag_and_drop(YY, WLAN)

# 速度快 不是很精准
driver.scroll(YY, WLAN)

