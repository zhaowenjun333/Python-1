# 可迭代对象
# 如果一个类中有__iter__方法返回一个迭代器对象：则我们称这个类创建的对象为可迭代对象

# class Foo(object):
#     def __iter__(self):
#         return 迭代对象(生成器对象)

# obj = Foo()   # obj是可迭代对象

# 可迭代对象是可以使用for来进行循环，在循环的内部其实是先执行__iter__方法，
# 获取其迭代器对象，然后再在内部执行这个迭代器对象的next功能，逐步取值。

# for item.txt in obj:
#     pass


# 迭代器类
# class IT(object):
#     counter = 0
#
#     def __int__(self, counter):
#         self.counter = counter
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         self.counter += 1
#         if self.counter == 3:
#             raise StopIteration()
#         return self.counter
#
#
# class Foo(object):
#     def __iter__(self):
#         return IT()  # 返回迭代器对象
#
#
# # 以Foo创建的对象为可迭代对象
# obj = Foo()
# # 循环可迭代对象时，内部先执行 obj.__iter__ 并获取迭代器对象：
# #     for循环内部会不断执行迭代器对象的next方法
# for item.txt in obj:
#     print(item.txt)


# 可迭代对象实例
v1 = range(10)
print(dir(v1))
# v1: 可迭代对象
if '__iter__' in dir(v1):
    print(True)
# for i in dir(v1):
#     print(i)

v2 = v1.__iter__()  # 返回迭代器对象
print(dir(v2))
for i in range(10):
    print(v2.__next__())
    # print(next(v2))
