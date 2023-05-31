# 迭代器 （iterator）
# 可迭代对象 (iterable)
l1 = [1, 3, 5, 'Gean']

print(l1.__iter__())  # 可迭代对象
iterator = l1.__iter__()

# print(iterator.__next__())
# print(iterator.__next__())
# print(iterator.__next__())
# print(iterator.__next__())


flag = True
while flag:
    try:
        res = iterator.__next__()
    except StopIteration as se:
        flag = False
    else:
        print(res)

