"""
希尔排序（Shell Sort）是一种基于插入排序的排序算法，也被称为缩小增量排序。
它通过将待排序的数组分割成若干个子序列进行插入排序，逐步减小子序列的长度，最终完成整个数组的排序。
"""

def shell_sort(arr):
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
    return arr


# 测试
array = [9, 5, 1, 8, 3, 7, 4, 6, 2, 10]
sorted_array = shell_sort(array)
print(sorted_array)

# 打印结果
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
