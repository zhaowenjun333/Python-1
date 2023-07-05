from timeit import timeit
import sys

sys.setrecursionlimit(5000)  # 设置递归深度限制为5000


# 普通递归求和
def digui_sum(n):
    if n == 1:
        return 1
    else:
        return n + digui_sum(n - 1)


# 尾递归求和
def wei_digui_sum(n, acc=0):
    if n == 0:
        return acc
    else:
        return wei_digui_sum(n - 1, acc + n)


# 循环求和
def xunhuan_sum(n):
    num = 0
    if n >= 1:
        for i in range(1, n + 1):
            num += i
    else:
        num += n
    print(f'循环求和结果：{num}')


# 列表求和
def list_sum(n):
    lst = [i for i in range(n + 1)]
    print(f'列表求和结果：{sum(lst)}')


if __name__ == '__main__':
    number = 1000

    # 普通递归
    digui_sum_result = digui_sum(number)
    digui_sum_t = timeit(stmt=f'digui_sum({number})', setup="from __main__ import digui_sum", number=1)
    print(f'普通递归求和结果：{digui_sum_result}')
    print(f'普通递归求和时间：{digui_sum_t}')  # 0.00016040000000000498

    print('---' * 20)

    # 尾递归
    wei_digui_sum_result = digui_sum(number)
    wei_digui_sum_t = timeit(stmt=f'wei_digui_sum({number})', setup="from __main__ import wei_digui_sum", number=1)
    print(f'尾递归求和结果：{wei_digui_sum_result}')
    print(f'尾递归求和时间：{wei_digui_sum_t}')  # 0.00016040000000000498

    print('---' * 20)

    # 循环
    xunhuan_sum_t = timeit(stmt=f'xunhuan_sum({number})', setup="from __main__ import xunhuan_sum", number=1)
    print(f'循环求和时间：{xunhuan_sum_t}')

    print('---' * 20)

    # 列表
    list_sum_t = timeit(stmt=f'list_sum({number})', setup="from __main__ import list_sum", number=1)
    print(f'列表求和时间：{xunhuan_sum_t}')

