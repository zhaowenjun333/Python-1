import random
import time


def bubble_sort(arr):
    """
    冒泡排序函数，将输入的数组 arr 排序后返回
    """
    n = len(arr)
    for i in range(n):
        # 每次遍历只处理未排序的部分
        for j in range(0, n-i-1):
            # 如果前一个元素比后一个元素打，则交换它们的位置
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


if __name__ == '__main__':
    t1 = time.time()
    max_num = 100
    random_arr = [random.randint(1, max_num) for n in range(max_num)]

    print(f'排序前: \n{random_arr}')
    print(f'排序后: \n{bubble_sort(random_arr)}')
    t2 = time.time()
    print(f'用时：{t2-t1}')
