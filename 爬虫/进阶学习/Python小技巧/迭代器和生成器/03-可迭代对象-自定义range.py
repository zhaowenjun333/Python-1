# 基于可迭代对象 & 迭代器实现： 自定义range
# 迭代器类
class IterRange(object):
    def __init__(self, num):
        self.num = num
        self.counter = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter == self.num:
            raise StopIteration   # 抛出错误，循环终止
        return self.counter


class Xrange(object):
    def __init__(self, max_num):
        self.max_num = max_num

    def __iter__(self):
        return IterRange(self.max_num)   # 返回迭代器对象


obj = Xrange(100)   # 可迭代对象
for item in obj:
    print(item)

