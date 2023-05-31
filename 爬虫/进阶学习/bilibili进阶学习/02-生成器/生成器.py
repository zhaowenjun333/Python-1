# 生成器     -->  迭代器的一种   ----  generator（生成器）

# 列表推导式
li = [i for i in range(1, 10)]
# print(li)

li_ = (i for i in range(1, 10))
# print(li_)

r1 = li_.__next__()
# print(r1)


# 生成器函数
def func1():
    # 返回1-10之间的元素
    for i in range(1, 10):
        yield i  # 返回函数结果不退出函数


# res = func1()  # 生成器对象
# # print(res)
# for i in res:
#     print(i)


# # 返回1-100之间的能被3整除的数
# def func2():
#     for i in range(1, 101):
#         if i % 3 == 0:
#             yield i
#
#
# generator = func2()
# for item in generator:
#     print(item)


# enumerate：索引和元组
# for i in enumerate([1, 55, 99, 'gean', 'man', '5.0']):
#     print(i)

# zip：打包
# for i in zip([1, 55, 99, 'gean', 'man', '5.0'],
#              ('a', 'b', 'c', 'd', 'e', 'f')):
#     print(i)

# 生成器函数
'''
自己定义一个生成器函数 {my_enumerate},
自己定义一个生成器函数 {my_zip},
'''


def my_enumerate():
    pass


def my_zip():
    pass
