# class Foo(object):
#     def __iter__(self):
#         yield 1
#         yield 2
#
#
# # 有yield返回生成器对象，生成器对象是特殊的迭代器
# obj = Foo()  # obj也是可迭代对象
#
# for item.txt in obj:
#     print(item.txt)

"""
基于可迭代对象 & 生成器 实现：自定义range
"""


class Xrange(object):
    def __init__(self, max_num):
        self.max_num = max_num

    def __iter__(self):
        counter = 0
        while counter < self.max_num:
            yield counter
            counter += 1


obj = Xrange(100)
for item in obj:
    print(item)
