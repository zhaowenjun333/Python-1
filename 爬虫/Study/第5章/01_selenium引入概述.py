# 能不能让我的程序连接到浏览器，让浏览器来完成各种复杂的操作，我们只接受最终的结果

# selenium： 自动化测试
# 可以打开浏览器，然后操作浏览器

from selenium.webdriver import Chrome

# 1. 创建浏览器对象
web = Chrome()
# 2. 打开一个网址
web.get('https://www.baidu.com/')

print(web.title)
