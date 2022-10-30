"""
一、请写出一段 Python 代码实现删除一个 list 里面的重复元素。
"""
# 1. 利用字典的 fromkeys 来自动过滤重复值；
# a = [1, 2, 3, 4, 5, 2, 3]
#
#
# def fun1(a):
#     b = {}
#     b = b.fromkeys(a)
#     print(b)
#     c = list(b.keys())
#     print(c)
#
#
# fun1(a)

# 2. 利用 集合set 的特性，元素是非重复的。
# a = [1, 2, 3, 4, 5, 2, 3]
#
#
# def fun1(a):
#     a = list(set(a))
#     print(a)
#
#
# fun1(a)


"""
二、统计如下 list 单词及其出现次数。
"""
# a = ['apple', 'banana', 'apple', 'tomato', 'orange', 'apple', 'banana', 'watermeton']

# dic = {}
# for key in a:
#     # get() 函数返回指定键的值
#     dic[key] = dic.get(key, 0) + 1
#     print(dic)
#
# print(dic)

# from collections import Counter
#
# a = ['apple', 'banana', 'apple', 'tomato', 'orange', 'apple', 'banana', 'watermeton']
# d = Counter(a)
#
# print(d)

"""
三、给列表中的字典排序：假设有如下 list 对象
alist=[{"name":"a", "age":20}, {"name":"b", "age":30}, {"name":"c", "age":25}]，将alist中的元素按照age从小到大排序。
"""
# alist = [{"name": "a", "age": 20}, {"name": "b", "age": 30}, {"name": "c", "age": 25}]
#
# alist.sort(key=lambda x: x['age'])
# print(alist)

"""
四、假设有如下两个 list：
a = ['a', 'b', 'c', 'd', 'e']，
b = [1, 2, 3, 4, 5]，
将 a 中的元素作为 key，b 中元素作为 value，将 a，b 合并为字典。
"""
a = ['a', 'b', 'c', 'd', 'e']
b = [1, 2, 3, 4, 5]

print(dict(list(zip(a, b))))
print(dict(zip(a, b)))


