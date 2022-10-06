from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': '198.49.68.80:80',
    'sslProxy': '198.49.68.80:80',
    'ftpProxy': '198.49.68.80:80'
})

driver = webdriver.Remote(
    command_executor="http://10.168.99.197:4444/wd/hub",
    desired_capabilities=DesiredCapabilities.CHROME,
    proxy=proxy
)

driver.get("https://www.baidu.com")
driver.maximize_window()
# driver.save_screenshot('bd.png')
print(driver.title)
print(driver.proxy)

