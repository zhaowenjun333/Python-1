from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(chrome_options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

driver.get('https://signup.zhipin.com/?ka=header-register')
driver.find_elements(By.XPATH, '//span[@class="ipt-wrap"]/input[@class="ipt ipt-phone required"]')[1].send_keys('17302254866')
driver.find_elements(By.CLASS_NAME, 'agree-policy')[1].click()
driver.find_element(By.XPATH, '//div[@id="regVerrifyCode"]').click()
time.sleep(10)
driver.find_elements(By.XPATH, '//span[@class="ipt-wrap"]/button[@class="btn btn-sms"]')[1].click()


