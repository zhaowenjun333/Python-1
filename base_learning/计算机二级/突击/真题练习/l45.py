data = input() #姓名 年龄 性别
#定义初始总人数
n = 0
#定义初始总年龄
age = 0
#定义初始总男人数
man_num = 0
while data:
    if data == '\n':
        break
    n += 1
    ls = data.split()
    age += int(ls[2])
    if ls[1]== "男":
        man_num += 1
    data = input()
avg = age/n
print("平均年龄是{:.2f} 男性人数是{}".format(avg,man_num))