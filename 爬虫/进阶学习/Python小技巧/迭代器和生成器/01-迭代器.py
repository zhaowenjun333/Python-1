# from collections.abc import Iterable, Iterator
#
# print(isinstance('abc', Iterable))  # True
# print(isinstance([1, 2, 3, 4], Iterable))  # True
# print(isinstance(123, Iterable))  # False

# 元组
# mytuple = ("apple", "banana", "cherry")
# myit = iter(mytuple)
#
# print(next(myit))
# print(next(myit))
# print(next(myit))


# 字符串
# mystr = "banana"
# myit = iter(mystr)
#
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))
# print(next(myit))

# 遍历迭代器
# 迭代元组
# mytuple = ("apple", "banana", "cherry")
# for x in mytuple:
#     print(x)
#
# # 迭代字符串
# mystr = "banana"
# for x in mystr:
#     print(x)


# 创建迭代器类型
class IT(object):

    def __init__(self):
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter == 3:
            raise StopIteration()
        return self.counter


# # 根据实例化创建一个迭代器对象
obj1 = IT()
# print(IT)


# 执行方法一：
# v1 = obj1.__next__()
# v2 = obj1.__next__()
# v3 = obj1.__next__()   # 抛出异常

# 执行方法二：
v1 = next(obj1)
print(v1)

v2 = next(obj1)
print(v2)

v3 = next(obj1)
print(v3)
