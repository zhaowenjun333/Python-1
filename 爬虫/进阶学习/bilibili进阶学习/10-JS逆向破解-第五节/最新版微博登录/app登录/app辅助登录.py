from selenium import webdriver as s_webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver as chromedriver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from appium import webdriver as a_webdriver
from selenium.webdriver.common.by import By

class APPWeibo:
    def __init__(self):
        self.caps = dict()
        self.driver = self.app_driver()
        # 显示等待
        self.wait = WebDriverWait(self.driver, 100)

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

    def apply_login(self):
        # 点击消息
        self.wait.until(
            ec.element_to_be_clickable((By.XPATH,
                                        '//android.widget.FrameLayout[@content-desc="消息"]'))
        ).click()
        print('点击底部消息')
        self.wait.until(
            ec.element_to_be_clickable(
                (By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.TabHost/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.TextView'))
        ).click()
        print('点击顶部消息')
        # 点击微博安全中心
        self.wait.until(
            ec.element_to_be_clickable((By.XPATH,
                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.TabHost/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[5]/android.widget.LinearLayout/android.widget.RelativeLayout'))
        ).click()
        print('进入微博安全中心')
        apply_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout'
        # 点击最后一个申请
        self.wait.until(
            ec.element_to_be_clickable((By.XPATH, apply_xpath))
        ).click()
        print('点击最新的申请')
        allow_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]'
        self.wait.until(
            ec.element_to_be_clickable((By.XPATH, allow_xpath))
        ).click()
        print('允许登录')
        time.sleep(2)
        close_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]'
        self.wait.until(
            ec.element_to_be_clickable((By.XPATH, close_xpath))
        ).click()
        print('关闭')
        # self.driver.close()

    def run(self):
        try:
            self.driver.terminate_app('com.sina.weibo')
        except Exception as e:
            print(f'{e}')
            # 打开微博APP
        self.driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="微博"]').click()
        try:
            self.wait.until(
                ec.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView'))
            ).click()
            print(f'点击跳过')
        except Exception as e:
            print(f'没有找到跳过按钮：{e}')
        time.sleep(1)
        self.apply_login()


class WebWeibo:
    # 1. 初始化方法
    def __init__(self, username, password):
        # 用户名
        self.username = username
        # 密码
        self.password = password

    def get_chrome_driver(self):
        # s = input('请先在cmd中打开, 然后输入yes:')
        s = 'y'
        options = s_webdriver.ChromeOptions()
        if s.lower() == 'y':
            # 反爬
            # 方式一
            # 等效在cmd中：chrome --remote-debugging-port=9222
            options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
            # options.add_argument('--headless')
            chrome_driver = s_webdriver.Chrome(chrome_options=options)
        else:
            # 方式二
            # options.add_argument('--headless')
            # proxy = 'http://104.223.212.161:65432'
            # options.add_argument(f'--proxy-server={proxy}')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('disable-infobars')
            options.add_argument("service_args = ['–ignore - ssl - errors = true', '–ssl - protocol = TLSv1']")
            chrome_driver = s_webdriver.Chrome(chrome_options=options)
            chrome_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
            })
        return chrome_driver

    def login(self, driver, wait):
        url = 'https://login.sina.com.cn/signup/signin.php'
        driver.get(url)

        # 输入用户名
        username = driver.find_element(By.ID, 'username')
        if len(username.get_attribute('value')) > 0:
            username.clear()
        driver.execute_script(f'''arguments[0].value="{self.username}"''', username)

        # 输入密码
        password = driver.find_element(By.ID, 'password')
        if len(password.get_attribute('value')) > 0:
            password.clear()
        driver.execute_script(f'''arguments[0].value="{self.password}"''', password)
        # password.send_keys(self.password)

        # 点击登录
        login_xpath = '//input[@class="W_btn_a btn_34px"]'
        login = driver.find_element(By.XPATH, login_xpath)
        login.click()
        print('点击登录')
        # print(f'点击登录按钮：{login.get_attribute("outerHTML")}')

        time.sleep(2)
        # 选择私信验证
        driver.find_element(By.XPATH, '//a[@id="dmCheck"]').click()
        print(f'选择私信验证')
        # 点击私信发送
        driver.find_element(By.ID, 'send_dm_btn').click()
        print('点击发送')

    def get_cookies(self, driver):
        cookies = driver.get_cookies()
        li = []
        for cookie in cookies:
            # print(cookie)
            name = cookie['name']
            value = cookie['value']
            li.append(f'{name}={value}')
        cookie = '; '.join(li)
        print(cookie)

    def run(self, driver, wait):
        self.login(driver, wait)
        # time.sleep(3)


if __name__ == '__main__':
    t1 = time.time()
    # 15314656636
    # user = input('请输入用户名：')
    user = '15314656636'
    # lry1730225
    # key = input('请输入密码：')
    key = 'lry1730225'
    weibo_web = WebWeibo(user, key)
    chrome_driver = weibo_web.get_chrome_driver()
    chrome_wait = WebDriverWait(chrome_driver, 100)
    weibo_web.run(chrome_driver, chrome_wait)
    weibo_app = APPWeibo()
    weibo_app.run()
    weibo_web.get_cookies(chrome_driver)
    chrome_driver.close()
    chrome_driver.quit()

    t2 = time.time()
    print(round(t2 - t1))

