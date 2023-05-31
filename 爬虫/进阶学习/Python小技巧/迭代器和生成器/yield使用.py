# yield：是一个生成器函数，返回的是一个迭代器

# yield 表达式
def square():
    for x in range(4):
        yield x ** 2
        square_gen = square()
        for y in square_gen:
            print(y)


def foo():
    print('Starting.....')

    while True:
        res = yield 4
        print("res:", res)


g = foo()
print("第一次调用执行结果：")
print(next(g))
print("*" * 100)
print("第二次调用执行结果：")
print(next(g))
print("*" * 100)
