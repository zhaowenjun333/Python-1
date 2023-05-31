import random
import time
import timeit

'''快速排序'''
def quick_sort(arr):
    # 递归结束条件：如果序列长度小于等于1，则直接返回序列本身
    if len(arr) <= 1:
        return arr
    # 被选择的基准值，这里选取索引位的一个元素
    pivot = arr[0]
    # 初始化左、右子序列
    left = []
    right = []
    '''
    1. 从小到大排序
    2. 遍历序列中的元素，将小于基准值的放入左子序列，大于等于枢轴元素的放入右子序列
    '''
    for i in range(1, len(arr)):
        if arr[i] < pivot:
            left.append(arr[i])
        else:
            right.append(arr[i])
        # 递归排序左右子序列，将排好序的左子序列、基准值、排好序的右子序列合并成一个有序序列
    return quick_sort(left) + [pivot] + quick_sort(right)


'''冒泡排序函数'''
def bubble_sort(arr):
    print(f'排序前：{arr}')
    n = len(arr)
    for i in range(n):
        # 每次遍历只处理未排序的部分
        for j in range(0, n - i - 1):
            # 如果前一个元素比后一个元素打，则交换它们的位置
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    print(f'冒泡排序结果：{arr}')
    return arr


'''插入排序'''
def insertion_sort(arr):
    print(f'排序前：{arr}')
    # 遍历未排序部分的元素
    for i in range(1, len(arr)):
        # 当前要插入的元素
        key = arr[i]
        # 已排序部分的最后一个元素的下标
        j = i - 1

        # 将已排序部分中大于当前元素的元素向后移动
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # 将当前元素插入到正确位置
        arr[j + 1] = key
    print(f'插入排序结果：{arr}')
    return arr


'''希尔排序'''
def shell_sort(arr):
    print(f'排序前：{arr}')
    n = len(arr)
    gap = n // 2  # 初始间隔设定为数组长度的一半
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # 对间隔为gap的元素进行插入排序
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2  # 缩小间隔
    print(f'希尔排序结果：{arr}')
    return arr


if __name__ == '__main__':
    max_num = 100
    random_arr = [random.randint(1, max_num) for n in range(max_num)]
    print(f'排序前：{random_arr}')

    print('---' * 30)

    quick_sort_arr = quick_sort(random_arr)
    quick_sort_t = timeit.timeit(stmt=f"quick_sort({random_arr})", setup="from __main__ import quick_sort", number=1)
    print(f'快速排序结果：{quick_sort_arr}')
    print(f'快速排序时间：{quick_sort_t}')

    print('---' * 30)

    bubble_sort_t = timeit.timeit(stmt=f"bubble_sort({random_arr})", setup="from __main__ import bubble_sort", number=1)
    print(f'冒泡排序时间：{bubble_sort_t}')

    print('---' * 30)

    insetion_sort_t = timeit.timeit(stmt=f"insertion_sort({random_arr})", setup="from __main__ import insertion_sort", number=1)
    print(f'插入排序时间：{insetion_sort_t}')

    print('---' * 30)

    shell_sort_t = timeit.timeit(stmt=f"shell_sort({random_arr})", setup="from __main__ import shell_sort", number=1)
    print(f'希尔排序时间：{shell_sort_t}')
