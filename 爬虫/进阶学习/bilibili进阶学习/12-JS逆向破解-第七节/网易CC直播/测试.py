import json

import execjs
import js2py

chart_set = 'utf-8'
get_d_js_filename = './JS/get_d.js'
get_d_js_f = open(get_d_js_filename, 'r', encoding='utf-8')

get_d_js_compile = execjs.compile(get_d_js_f.read(), cwd=r'D:\AppData\npm_global\node_modules')
get_d_js_f.close()
coo = "__snaker__id=SQHgxqQjE4WwiYRq; utid=nF8KQIg9J3yjE0obcEVd9uIka1HmwDhC; NTES_WEB_FP=3c53467e6df4e8d143202cd100a7fa22; l_yd_s_ccPFClpTB=8F7AD574C145A0CBC2259FC8358E677E00D460E4BA2001887E0EFCBD73625837557F2EEEA783BA0D7696E29A5E46B33730A231D93D0AEE5916562FC36C0209C0F394207860EBF35137D2CDF2A43E79D83D7F7886163F4B69FCB728E0887ABD0F; l_s_ccPFClpTB=8F7AD574C145A0CBC2259FC8358E677E00D460E4BA2001887E0EFCBD73625837A2AD729DCD4E362A9C9BDB6EB9907B9BF11593FE1C056225F4AD412300C6F3714AE2957F24CE8730DB6630AA218418E70AD468D19C6DB96FF6160E99DD456147; gdxidpyhxdE=5xGvMY0LI2pIAt6PTEdeKlA3nb+eOMKzl6C7Hjyc1\HYkI8XUvcLjINJ\hWiuWlH1h/VejZqt4vKWMkSnxEWoALV2iBs6cRlC\PzCKAblXCujwsCgVpCBVS3j0W1NjPWlwecomTTneB8CO687SiqovVtLKunohwctou2h+1f\cOv7HUP:1680503072034; _9755xjdesxxd_=32"
get_d_js_compile.call('get_d', coo)
#
d_txt = open('get_d.txt', 'r', encoding=chart_set)
d = d_txt.read()
d_txt.close()
print(f'd: {d}')
# result = get_d_js_obj.d(coo)
# print(result)

