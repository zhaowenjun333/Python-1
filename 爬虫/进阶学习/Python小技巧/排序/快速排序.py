import random
import time
import timeit


def quick_sort(arr):
    # 递归结束条件：如果序列长度小于等于1，则直接返回序列本身
    if len(arr) <= 1:
        return arr
    # 被选择的基准值，这里选取索引位的一个元素
    pivot = arr[0]
    # 初始化左、右子序列
    left = []
    right = []
    # 遍历序列中的元素，将小于基准值的放入左子序列，大于等于枢轴元素的放入右子序列
    for i in range(1, len(arr)):
        if arr[i] < pivot:
            left.append(arr[i])
        else:
            right.append(arr[i])
        # 递归排序左右子序列，将排好序的左子序列、基准值、排好序的右子序列合并成一个有序序列
    return quick_sort(left) + [pivot] + quick_sort(right)


if __name__ == '__main__':
    t1 = time.time()
    max_num = 100
    random_arr = [random.randint(1, max_num) for n in range(max_num)]

    print(f'排序前: \n{random_arr}')
    print(f'排序后: \n{quick_sort(random_arr)}')
    t2 = time.time()
    print(f'用时：{t2-t1}')

