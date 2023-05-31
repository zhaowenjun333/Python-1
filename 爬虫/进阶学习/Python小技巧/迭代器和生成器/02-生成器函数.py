"""
生成器函数
当一个函数中包含yield关键字，那么这个函数就不再是一个普通的函数，
而是一个generator。调用函数就是创建了一个生成器对象。
其工作原理就是通过重复调用next()或者__next__()方法，直到捕获一个异常。
"""


# def yieldtest(number):
#     n = 0
#     # li = []
#     while n < number:
#         # li.append(n)
#         yield n
#         n += 1
#
#
# res = yieldtest(20)
# # print(res)  # generator object
# print(next(res))  # 0
# print(next(res))  # 1
# print(next(res))  # 2
# print(next(res))  # 3

"""
注意：
● yield返回一个值，并且记住这个返回值的位置，下次遇到next()调用时，
  代码从yield的下一条语句开始执行。与return的差别是，return也是返回一个值，
  但是直接结束函数。
"""


"""
实现斐波那契数列，除第一个和第二个数外，任何一个数都可以由前两个相加得到：
1，1，2，3，5，8，12，21，34.....
"""


def createNums():
    print("-----func start-----")
    a, b = 0, 1
    for i in range(5):
        # print(f'a：{a}\nb：{b}')
        yield b
        a, b = b, a + b
        print(f'a：{a}\nb：{b}')
        print('--'*10)
    print("-----func end-----")


g = createNums()
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))

for j in g:
    print(j)
