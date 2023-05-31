# 列表、元组、字典、集合、字符串：创建的对象都是可迭代对象

v1 = list([11, 22, 33, 44])
# v1 是一个可迭代对象，因为在列表中声明了一个__iter__ 方法并且返回一个迭代器对象
print(dir(v1))

if '__iter__' in dir(v1) and '__next__' not in dir(v1):
    print('v1是可迭代对象，不是迭代器')

v2 = v1.__iter__()
if '__iter__' in dir(v2) and '__next__' in dir(v2):
    print('v2是迭代器对象')
    print(v2.__next__())

