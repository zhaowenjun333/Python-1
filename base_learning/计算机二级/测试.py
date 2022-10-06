# ls = ['my','44','py','45']

# ls.reverse()

# print(''.join(ls[-1::-1]))


# from turtle import *
# import turtle
# speed(6)
# penup()
# pencolor('black')
# goto(-20,130)
# fillcolor('red')
# begin_fill()
# pendown()
# setheading(16)
# circle(-50,-150)
# setheading(180)
# forward(60)
# end_fill()

# penup()
# pencolor('red')
# goto(-20,130)
# fillcolor('red')
# begin_fill()
# pendown()
# setheading(196)
# circle(120,-30)
# end_fill()

# penup()
# pencolor('yellow')
# goto(-39,118)
# fillcolor('yellow')
# begin_fill()
# pendown()
# setheading(20)
# circle(20,40)
# end_fill()
# forward(6)
# circle(-4,140)

# hideturtle()
# done()

# x = 4 + 3j
# y = 4 - 3j

# print(x+y)

# a = "Hello"
# print(len(a))

# a = 3.141593
# b = "*"
# print("{0:{2}>{1},}\n{0:{2}^{1},}\n{0:{2}<{1},}".format(a,20,b))


# a = 75
# if a>60:
#     print("Should Work Hard!")
# elif a>70:
#     print("Good")
# else:
#     print("Excellent")

# a = input("").split(",")
# print(a)
# x = 0
# while x:
#     print(a[x],end=" ")
#     x = x+1


# def maxcount():
#     a,b = 1000,99
#     for i in range(10):
#         a*=b+1
#         print("a:",a)
#         b*=a-1
#         print("b:",b)
#         return a
# print(maxcount())


# chinesetime = {'夜半': '子时','鸡鸣':'丑时','平旦':'寅时', '日出':'卯时','食时':'辰时','隅中':'已时', '日中':'午时','日映':'未时','哺时':'申时', '日入':'酋时','黄昏':'戌时','人定':'亥时',}
# time = chinesetime.pop('黄昏','失败')
# print(time)
# print(chinesetime)


# from numpy import size


# s = 'Hello World'
# # print(s[5::-2])
# print(len(s))

# import string

# y1='a'

# y2='asdf'

# print(y1 in string.printable, y2 in string.printable)




# def func(x =[],y=[6,7]):

#     x.append(8)

#     y. append(8)

#     return(x+y)

# a,b=[1,2],[3,4]

# t=func(x=a)
# print(t)
# t=func(y=b)
# print(t)
# print(func(),end=";")


# a=[12,34,56]

# b=[1,2,3,4]

# def displ(a):

#     print('res：',[a])
# b=a
# print(b)
# a.append([5,6])
# print(b)
# displ(b)

# def func(x =[],y=[6,7]):

#     x.append(8)
#     y.append(8)
#     return(x+y)

# a,b=[1,2],[3,4]

# t=func(x=a)
# t=func(y=b)
# print(func(),end=";")



# ls =["ab","44","cd","46"]
# # 方法一
# # print("".join(ls[-1::-1]))

# ls.reverse()
# # print(ls)
# print("".join(ls))


# ss =[2,3,6,9,7,1]

# for i in ss:
#     ss.remove(min(ss))
#     print(ss)
#     print(min(ss),end = ",")


# import random
# ls = ["a","b","c","d"]
# print(ls[int(random.random()*3)])


# L1 =['abc', ['123','456']]

# L2 = ['1','2','3']

# print(L1 > L2)



# txt=open("demo.txt","r")

# print(txt.read())

# txt.close()



# d = {"中国":1}
# print(list(d))
# print(list(d.items()))


# import time

# print(time.ctime())




d={'A':10,'B':2,'C':100,'D':9,'E':-10}

s=0

for i in d:

    if d[i]>2:

        continue
    print(d[i])
    s += d[i]

print(s)



