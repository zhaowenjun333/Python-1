# 创建生成器函数
def func():
    yield 1
    yield 2


# 创建生成器对象（内部是根据生成器类generator创建的对象），生成器类的内部也声明了：__iter__、__next__方法
obj1 = func()
v1 = next(obj1)
print(v1)

v2 = next(obj1)
print(v2)

# v3 = next(obj1)
# print(v3)

obj2 = func()
for item in obj2:  # 首先会执行迭代器对象的__iter__一直去反复执行 next(对象)
    print(item)
# 按照迭代器的的规则来看，其实生成器也是一种特殊的迭代器类（生成器也是一种特殊的迭代器）


# 生成器推导式：与列表推导式类似，只不过生成器推导式使用小括号
# g = (x for x in range(5))
# # print(g)       # generator object
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# # 超出报错：StopIteration
# # print(next(g))
#
# for i in g:
#     print(i)


