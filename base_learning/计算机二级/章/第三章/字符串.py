""" 
#单引号
print('这是一个单行字符串')
#双引号
print("这是一个单行字符串")
#输出含有双引号的字符串
print('这是一个单"行"字符串')
#输出含有单引号的字符串
print("这是一个单'行'字符串")
#输出多行字符串用三引号
print('''这是多行字符串第一行
这是第二行
这是第三行''') 
"""

 
#字符串索引
"""
a='多情却被无情恼'
print(a[-1])
print(a[3]) 
"""

#字符串的切片
b='春花秋月何时了，往事知多少'
#花-->月
print(b[1:4])
#空字符串
print(b[8:4])
#省略0,从春-->到月
print(b[:4])
#省略N-1,从知-->到最后
print(b[10:])
#注意：print()打印输出时没有''(引号)
#输出往事
print(b[8:-3])