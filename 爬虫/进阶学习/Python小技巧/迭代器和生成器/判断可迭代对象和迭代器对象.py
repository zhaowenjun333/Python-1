from collections.abc import Iterable, Iterator
"""
Iterable: 可迭代对象
Iterator: 迭代器对象
"""

# v1 = [11, 22, 33]  # 可迭代对象
# print(isinstance(v1, Iterable))  # True , 判断是可迭代：判断依据是是否有__iter__且返回迭代器对象
# print(isinstance(v1, Iterator))  # False , 判断是否是迭代器：判断依据是__iter__ 和 __next__。
#
# v2 = v1.__iter__()
# print(isinstance(v2, Iterable))  # True
# print(isinstance(v2, Iterator))  # True

import types

s = '123'
d = {'a': 123}
e = {'a', s, 123}

print(isinstance(s, types.GeneratorType))
print(isinstance(d, types.GeneratorType))
print(isinstance(e, types.GeneratorType))
print('-'*10)
print(isinstance(s, Iterable))
print(isinstance(d, Iterable))
print(isinstance(e, Iterable))
