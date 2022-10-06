
num = 0
li = [1, 2, 3]


def task():
    global num    # 是否全局变量的指向进行了修改（内存地址的改变）
    global li
    num += 100
    # li.append(4)   # 地址不变
    li = li + [5]  # 重新赋值地址改变


task()
print(num)
print(li)
