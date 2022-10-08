# import os
# import subprocess
#
#
# # npm -g bin
# os.environ['NODE_PATH'] = 'D:\\Program Files\\nodejs'
#
# signature = subprocess.getoutput('node test2.js')

# 方法二
# import js2py
#
# # 执行js代码
# # 获取时间戳的js代码
# js_text = '''
#       var r = new Date().getTime()
# '''
# r = js2py.eval_js(js_text)  # 执行js代码
# print(r)
#
# # 执行js函数法一：
# log = js2py.eval_js(open('./test2.js', 'r', encoding='utf-8').read())
# print(log(123))  # 直接将参数传给log就行


import execjs
import os

os.environ['NODE_PATH'] = 'D:\\' + u'应用缓存' + '\\npm_global\\node_modules/'


with open('./v1.js', 'r', encoding='utf-8') as f:
    js = f.read()

JS = execjs.compile(js)

sign = JS.call('func', '微信')
print(sign)   # 微信666

