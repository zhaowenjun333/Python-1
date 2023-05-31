# coding=UTF-8
import base64
import random
import re
import string
import time
import datetime

import time
import urllib.parse
from hashlib import md5

import requests
from lxml import etree
from hashlib import md5

num = '1|1685019152000D#uqGdcw41pWeNXm'
# 884793822378fb15bafbb8cca151edf9
# 884793822378fb15bafbb8cca151edf9
parse_num = md5(num.encode()).hexdigest()
print(parse_num)

url1 = "https://s.wordpress.com/mshots/v1/http%3A%2F%2Fwww.allsummer2016.com%2F?w=200"

print(urllib.parse.unquote(url1))

# # ##########################  b64decode处理方法  ##########################
code = str(base64.b64decode('eXVhbnJlbnh1ZTE='), 'utf-8')
#
# code = str(base64.b64decode('L2NvZGUtcHJvbW8tYXZpcmEuaHRtbCMxOTMwMjUy'), 'utf-8')

print(f'code: {code}')
# ##########################################################################


# ##########################  \u处理方法  ##########################
str1 = '\u003cp\u003eSome exclusions apply. See site for complete details.\u003c/p\u003e'

str1 = str1.encode('utf-8').decode('unicode_escape')
print(str1)
# #################################################################


# ##########################  \x处理方法  ##########################
# str2 = '\x80'
# str2 = bytes(str2, encoding='utf-8').decode()
# str2 = str2.encode('raw_unicode_escape')
# print(str2)
# #################################################################


# ################################### 跨时区格式化时间 ###############################
from dateutil import parser
import calendar


# def iosdate_to_localdate(datetime='2023-08-04 23:59:59+01:00'):
#     # 字符串时间转化为datetime对象
#     dt = parser.isoparse(datetime)
#     # 转化为本地时区的datetime对象
#     localdt = dt.astimezone(tz=None)
#     # 产生本地格式 字符串
#     return localdt.strftime('%Y-%m-%d %H:%M:%S')
#
#
# print(f'跨时区: {iosdate_to_localdate("2023-01-31 23:59:59+01:00")}')
# #################################################################################


# ################################### 时间推移 ###############################
from dateutil.relativedelta import relativedelta
import pandas as pd
now_time = datetime.datetime.now()
now_time1 = now_time.strftime('%Y-%m-%d')
now_time2 = time.mktime(time.strptime(now_time1, "%Y-%m-%d"))
now_year = now_time.year
# 日推移
day = 3
after_day = str(now_time + datetime.timedelta(days=+day))
print(f'推移{day}天后的时间：{after_day}')

# 星期推移
week = 3
after_week = str(now_time + datetime.timedelta(days=+week*7))
print(f'推移{week}周后的时间：{after_week}')

# 月推移
month = 3
after_month = pd.to_datetime(now_time) + relativedelta(months=+month)
after_month = after_month.strftime("%Y-%m-%d %H:%M:%S.%f")
print(f'推移{month}月后的时间：{after_month}')

# 年推移
year = 3
after_year = now_time.replace(year=now_year + year)
print(f'推移{year}年后的时间：{after_year}')

# 过期日期判断
date = '2023-05-04'
end_date = time.mktime(time.strptime(date, "%Y-%m-%d"))
if now_time2 > end_date:
    print(f"{date}已过期")

# ########################################################################


# if date:
#     date = date[0].strip()
#     date = parser.isoparse(date)
#     date = date.astimezone(tz=None)
#     end_date = time.mktime(time.strptime(date.strftime('%Y-%m-%d'), "%Y-%m-%d"))
#     if now_time2 > end_date:
#         continue
#     data['EndDate'] = date.strftime('%Y-%m-%d %H:%M:%S')
# else:
#     data['EndDate'] = '0000-00-00 00:00:00'


# ########################## 判断闰年 ##########################
# def calc_year(year):
#     if year % 4 == 0:
#         if year % 100 == 0:
#             if year % 400 == 0:
#                 return 366
#             else:
#                 return 365
#         else:
#             return 366
#     else:
#         return 365
#
#
# days = calc_year(2023)
# print(days)
# ############################################################


# now_time1 = datetime.datetime.now()
# print(now_time1)
#
# now_time2 = str(now_time1)
# print(now_time2)
#
# now_time3 = datetime.datetime.strptime(now_time2, "%Y-%m-%d %H:%M:%S.%f")
# print(now_time3)

# import jsonpath
#
# item = {
#     "@context": "http://schema.org",
#     "@type": "BreadcrumbList",
#     "itemListElement": [
#         {
#             "@type": "ListItem", "position": 1, "item": {"@id": "https://www.spiegel.de/gutscheine/", "name": "Gutscheine"}
#         },
#         {
#             "@type": "ListItem", "position": 2, "item": {"@id": "https://www.spiegel.de/gutscheine/kategorien/online-kaufhaeuser", "name": "Online-Kaufhäuser"}
#         },
#         {
#             "@type": "ListItem", "position": 3, "item": {"@id": "https://www.spiegel.de/gutscheine/otto", "name": "OTTO"}
#         }
#     ]
# }
#
# deals = jsonpath.jsonpath(item, '$..deals')[0]

# ##########################  时间戳格式化  ##########################
date = time.localtime(1680278400)
print(time.strftime('%Y-%m-%d %H:%M:%S', date))

# print(datetime.datetime(2023, 3, 20, 12, 14, 44, 680152).strftime())


l1 = ['80', '316', '3152', '2084', '3854', '1680', '1726', '3046', '842', '2720', '198', '2028', '284', '2546', '186',
      '3777', '1358', '632', '4780', '2440']

l2 = ['222', '4354', '3152', '1896', '2624', '4419', '2480', '4618', '4590', '3046', '2388', '3030', '4571', '3624',
      '3974', '356', '354', '3950', '4376', '206', '284', '4038', '226', '412', '3951', '3936', '4470', '4608', '2772',
      '4443', '3290', '286', '1656', '3264', '3777', '1728', '3190', '4429', '1742', '1432', '4641', '3170', '4436',
      '3774', '4117', '3564', '3837', '3956', '2848', '3340', '4401', '236', '4100', '4508', '3354', '4044', '4291',
      '3840', '4459', '4382', '3604', '4511', '1306', '1704', '274', '4306', '1906', '3224', '4560', '4500', '4561',
      '1554', '4518', '4565', '564', '488', '4636', '4207', '4007', '4122', '2492', '1400', '1918', '1098', '4464',
      '3966', '2234', '4301', '322', '2404', '4473', '4603', '4239', '4309', '4034', '4583', '2012', '4397', '1450',
      '2928', '1082', '404', '366', '1662', '2672', '3256', '498', '1650', '2346', '2462', '1826', '480', '732', '2202',
      '1810', '718', '644', '3702', '3786', '3626', '764', '1976', '3973', '4151', '9', '2396', '1038', '4289', '2500',
      '1636', '180', '2560', '96', '4130', '3056', '2108', '3074', '3100', '3080', '2576', '784', '3831', '558', '2296',
      '1322', '4126', '4391', '4114', '318', '4290', '3943', '3828', '4465', '1368', '3839', '2680', '3852', '3932',
      '3288', '2886', '4194', '3874', '4046', '1264', '4089', '1416', '3020', '1968', '4083', '904', '3546']

for i in l1:
    if i in l2:
        print(i)

