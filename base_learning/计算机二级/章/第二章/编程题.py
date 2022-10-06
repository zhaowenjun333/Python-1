#获得用户输入的一个整数N，计算并输出N的32次方。

#方法一：pow(a,b)内置函数，a的b次方
""" 
import math
num=eval(input("请输入一个整数："))
print(math.pow(num,32)) 
"""
#方法二：循环
 
num=eval(input('请输入一个整数：'))
sum=1
i=1
while i<=32:
    sum=sum*num
    i += 1
print(sum)
