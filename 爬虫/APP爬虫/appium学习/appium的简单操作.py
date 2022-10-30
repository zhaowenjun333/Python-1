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
caps['appPackage'] = 'com.android.browser'
# 界面名称
caps['appActivity'] = '.BrowserActivity'
# 输入中文 设置为True
caps['unicodeKeyboard'] = True
# 恢复原来的输入法
caps['resetKeyboard'] = True
# 一般来说 不需要重置app状态
caps['noReset'] = True

caps['newCommandTimeout'] = 6000
caps['automationName'] = 'UiAutomator2'

# 加载驱动，连接设备
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)

# 定位地址栏
url_tag = driver.find_element(By.ID, 'com.android.browser:id/url')
# 点击出现光标
url_tag.click()
time.sleep(0.2)
# 输入内容 www.douban.com
url_tag.send_keys('www.douban.com')
time.sleep(0.2)
# 回车
driver.press_keycode(AndroidKey.ENTER)
t2 = time.time()
print(round(t2-t1))

