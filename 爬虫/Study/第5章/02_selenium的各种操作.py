import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
web = webdriver.Chrome(chrome_options=options)
web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

web.get('http://lagou.com')

# 找到某个元素，点击它
# 点击全国
web.find_element(By.XPATH, '//p[@class="checkTips"]/a').click()

time.sleep(1)

# 搜索Python
web.find_element(By.ID, 'search_input').send_keys('python')
web.find_element(By.ID, 'search_input').send_keys(Keys.ENTER)
time.sleep(0.1)
jobList = web.find_elements(By.CLASS_NAME, 'item__10RTO')
for job in jobList:
    job_name = job.find_element(By.XPATH, './/div[@class="item.txt-top__1Z3Zo"]//div[@class="p-top__1F7CL"]/a').text
    company_name = job.find_element(By.XPATH, './/div[@class="item.txt-top__1Z3Zo"]//div[@class="company-name__2-SjF"]/a').text
    job_salary = job.find_element(By.XPATH, './/div[@class="item.txt-top__1Z3Zo"]//span[@class="money__3Lkgq"]').text
    print(job_name, company_name, job_salary)
