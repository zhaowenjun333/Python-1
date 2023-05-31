import re
a = "one,two,four,"
print(a.split(','))

b = a
print(re.split(r',', b))

# 过滤空字符串
c = a
print(list(filter(None, c.split(','))))
print(list(filter(None, re.split(r',', c))))
