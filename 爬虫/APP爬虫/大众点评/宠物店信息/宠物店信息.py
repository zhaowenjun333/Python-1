import time
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class APPDZ:
    def __init__(self):
        # 配置链接参数
        caps = dict()
        # 测试的系统
        caps['platformName'] = 'Android'
        # 手机安卓版本
        caps['platformVersion'] = '7.1.2'
        # 设备名称
        caps['deviceName'] = 'Android'
        # 包名
        # caps['appPackage'] = 'com.android.settings'
        # 界面名称
        # caps['appActivity'] = '.Settings'
        # 输入中文  设置为True
        caps['unicodeKeyboard'] = True
        # 恢复原来的输入法
        caps['resetKeyboard'] = True
        # 一般来说  不需要重置app状态  设置True
        caps['noReset'] = True

        # 加载驱动
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)

        # 显示等待
        self.wait = WebDriverWait(self.driver, 100)
        # 获取屏幕高度
        window_size = self.driver.get_window_size()
        self.height, self.width = window_size.get('height'), window_size.get('width')
        print(self.height, self.width)

    def main(self):
        try:
            self.driver.terminate_app('com.MobileTicket')
        except Exception as e:
            print(e)
        # 打开12306app
        self.driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="大众点评"]').click()
        time.sleep(0.5)


if __name__ == '__main__':
    t1 = time.time()
    dz = APPDZ()
    dz.main()
    t2 = time.time()
    print(round(t2 - t1))
