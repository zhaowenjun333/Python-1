from appium import webdriver as a_webdriver

class APPWeiBo:
    def __init__(self):
        self.caps = dict()

    def app_driver(self):
        self.caps = {
            # 测试的系统
            'platformName': 'Android',
            # 手机安卓版本
            'platformVersion': '9.0.0',
            # 设备名称
            'deviceName': 'Android',
            # 包名
            # 'appPackage': 'com.android.settings',
            # 界面名称
            # 'appActivity': '.Settings',
            # 输入中文  设置为True
            'unicodeKeyboard': True,
            # 恢复原来的输入法
            'resetKeyboard': True,
            # 一般来说  不需要重置app状态  设置True
            'noReset': True
        }
        app_driver = a_webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.caps)
        return app_driver

