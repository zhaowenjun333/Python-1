""" 
a='Python'
#str.lower():小写
b=a.lower()
#str.upper():大写
c=a.upper()
print(b)
print(c) 
"""

#str.split():分隔
#不写其他分割方法默认按照空格分隔
"""
d='我，爱，Python'.split("，")
print(d)
"""

#str.count():统计
""" 
e='我爱Python,我爱Python编程'
print(e.count('P'))
print(e.count('编程')) 
"""
#str.replace():替换
""" 
f=e.replace('Python','Java')
print(f) 
"""

#str.center():居中并填充
""" 
g="我爱Python".center(25,'*')
print(g) """
#str.strip():去掉字符串左右字符
""" 
h=g.strip('*')
print(h)
"""

#str.join(item):讲item变量的每一个元素后增加一个str字符串
#注意：除了最后一个元素后面不加
j='*'.join('我爱Python')
print(j)
#输出：我*爱*P*y*t*h*o*n