import sys, gc


# 这个函数创建一个自己指向自己的列表
def create_cycle():
    lst = [8, 9, 10]
    lst.append(lst)


print("创建垃圾...")
for i in range(8):
    create_cycle()

print("我们来强制回收...")
n = gc.collect()
print("清理掉的无头尸体:", n)
print("没清理的垃圾:", gc.garbage)
