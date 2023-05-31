"""
迭代器对象
● 有内置的__next__()方法的对象，执行该方法可以不依赖索引取值
● 有内置的__iter__()方法的对象，执行迭代器的__iter__()方法得到的依然是迭代器本身

"""
from collections.abc import Iterable, Iterator

li = [1, 2, 3, 4]
print(isinstance(li, Iterator))  # False

"""
iter()
可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
那我们可以通过iter()方法将可迭代的对象，转为迭代器。
"""
lis = iter(li)
print(type(lis))  # <class 'list_iterator'>
