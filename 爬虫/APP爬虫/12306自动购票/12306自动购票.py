import time
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class APP12306:
    def __init__(self, from_station, to_station):
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
        self.from_station = from_station
        self.to_station = to_station

        # 保存数据  去重
        self.targ_list = []
        self.num = 1

    def station(self):
        # 发车站
        from_p = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'com.MobileTicket.launcher:id/home_page_train_dep1'))
        )
        from_p.click()
        time.sleep(0.5)
        # 搜索发车站位置
        from_search = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.EditText'))
        )
        from_search.click()
        from_search.send_keys(self.from_station)
        time.sleep(2)

        # 取消更新软件
        no_update = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'com.android.packageinstaller:id/cancel_button'))
        )
        print('取消更新')
        no_update.click()
        time.sleep(0.5)

        from_sta = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.widget.ListView/android.view.View[3]/android.view.View'))
        )
        from_sta.click()
        time.sleep(0.5)

        to_p = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'com.MobileTicket.launcher:id/home_page_train_arr1'))
        )
        to_p.click()
        time.sleep(0.5)
        to_search = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.EditText'))
        )
        to_search.click()
        time.sleep(0.5)
        to_search.send_keys(self.to_station)
        to_sta = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.widget.ListView/android.view.View[2]/android.view.View'))
        )
        to_sta.click()
        time.sleep(0.5)

    def choice_date(self):
        # 选择时间
        date = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'com.MobileTicket.launcher:id/home_page_depart_date_view_container'))
        )
        date.click()
        time.sleep(0.5)
        next_date = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.widget.ListView[5]/android.view.View[3]'))
        )
        next_date.click()
        time.sleep(0.5)

    # 查询票
    def search(self):
        # 学生票
        student_ticket = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'com.MobileTicket.launcher:id/home_page_student'))
        )
        student_ticket.click()
        # 查询
        search_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'com.MobileTicket.launcher:id/ticket_home_btn_search'))
        )
        search_btn.click()
        time.sleep(0.5)

    # 解析数据
    def parse_ticket(self):
        # first = self.wait.until(
        #     EC.presence_of_element_located((By.ID, 'com.MobileTicket.launcher:id/h5_rl_title_bar'))
        # ).size
        # first_height = first['height']
        # second = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.widget.ListView[1]'))
        # ).size
        # second_height = second['height']
        # print(first_height+second_height)
        # third = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.widget.ListView[2]'))
        # ).size
        # print(f'third:{third["height"]}')
        # height = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH, '	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[1]'))
        # ).size
        # print(f'滑动距离{height["height"]}')
        ticket_lst = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/'
                                                           'android.widget.LinearLayout/android.widget.FrameLayout/'
                                                           'android.widget.RelativeLayout/'
                                                           'android.widget.RelativeLayout/'
                                                           'android.widget.RelativeLayout/'
                                                           'android.widget.RelativeLayout/'
                                                           'android.widget.FrameLayout/android.webkit.WebView/'
                                                           'android.webkit.WebView/android.view.View/'
                                                           'android.view.View[2]/android.view.View[1]/'
                                                           'android.view.View'))
        )
        # 前六个数据
        if self.num == 1:
            # 过滤掉刷新标签
            ticket_lst = ticket_lst[1:-1]
            for i in ticket_lst:
                self.targ_list.append(i)
        else:
            for i in ticket_lst:
                if i in self.targ_list:
                    ticket_lst.remove(i)
                else:
                    self.targ_list.append(i)
        print(f'共有：{len(ticket_lst)}')

        for i in range(0, len(ticket_lst), 3):
            ticket = (ticket_lst[i], ticket_lst[i + 2])
            # if ticket not in self.tickets_set:
            #     self.tickets_set.add(ticket)
            item = {}
            for ticket_info in ticket:
                try:
                    if ticket_info == ticket_lst[i]:
                        # 车次
                        train_num = ticket_info.find_element(By.XPATH, './/android.widget.TextView[1]')
                        item['train_num'] = train_num.text
                        # print(f'下标：{train_num.get_attribute("index")}')

                        # 起始时间
                        start = ticket_info.find_element(By.XPATH, './/android.view.View[2]')
                        end = ticket_info.find_element(By.XPATH, './/android.widget.TextView[2]')
                        train_time = start.text + '-' + end.text.replace("\xa0", "")
                        item['train_time'] = f'{train_time}'

                        # 车程时长
                        pass_time = ticket_info.find_element(By.XPATH, './/android.view.View[3]')
                        item['pass_time'] = pass_time.text
                    else:
                        if ticket_info.find_elements(By.XPATH, './/android.widget.Button') == 4:
                            # 软卧
                            soft_sleeper = ticket_info.find_element(By.XPATH, './/android.widget.Button[1]')
                            item['soft_sleeper'] = soft_sleeper.text.replace('\xa0', '')

                            # 硬卧
                            hard_sleeper = ticket_info.find_element(By.XPATH, './/android.widget.Button[1]')
                            item['hard_sleeper'] = hard_sleeper.text.replace('\xa0', '')

                            # 硬座
                            hard_seat = ticket_info.find_element(By.XPATH, './/android.widget.Button[3]')
                            item['hard_seat'] = hard_seat.text.replace('\xa0', '')

                            # 无座
                            no_seat = ticket_info.find_element(By.XPATH, './/android.widget.Button[4]')
                            item['no_seat'] = no_seat.text.replace('\xa0', '')
                        else:
                            # 商务
                            business = ticket_info.find_element(By.XPATH, './/android.widget.Button[1]')
                            item['business'] = business.text.replace('\xa0', '')

                            # 一等座
                            first_class = ticket_info.find_element(By.XPATH, './/android.widget.Button[2]')
                            item['first_class'] = first_class.text.replace('\xa0', '')

                            # 二等座
                            second_class = ticket_info.find_element(By.XPATH, './/android.widget.Button[3]')
                            item['second_class'] = second_class.text.replace('\xa0', '')
                except Exception as e:
                    print(e)
            print(item)
            # if len(item.txt.keys()) == 7:
            #     self.tickets_set.add(json.dumps(item.txt, ensure_ascii=False))
        self.num += 1
        # print(self.targ_list)
        if len(self.targ_list) <= 117:
            self.driver.swipe(self.width * 0.5, self.height * 0.7, self.width * 0.5, self.height * 0.14, 500)
            print('滑动成功')
            self.buy_ticket()
        #     # 滑动完之后 继续解析
        #     self.parse_ticket()

    def buy_ticket(self):
        # 购买票
        train_ticket = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View[5]'))
        )
        train_ticket.click()
        username = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[1]'))
        )
        username.click()
        username.send_keys('17302254866')
        password = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, ''))
        )
        password.click()
        password.send_keys('lry1730225')

    def main(self):
        # 关闭已经打开的铁路12306软件
        try:
            self.driver.terminate_app('com.MobileTicket')
        except Exception as e:
            print(e)
        # 打开12306app
        self.driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="铁路12306"]').click()
        time.sleep(0.5)
        self.station()
        self.choice_date()
        self.search()
        # 开始解析
        print('开始解析')
        self.parse_ticket()
        print(f'一共滑了{self.num}次')


if __name__ == '__main__':
    t1 = time.time()
    s = APP12306('郑州', '天津')
    s.main()
    t2 = time.time()
    print(round(t2 - t1))
