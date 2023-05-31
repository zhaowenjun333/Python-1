# 从小到大排序
""" 快速排序 """


def quick_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    pivot = arr[0]
    left = []
    right = []

    for i in range(1, n):
        if arr[i] < pivot:
            left.append(arr[i])
        else:
            right.append(arr[i])
    return quick_sort(left) + [pivot] + quick_sort(right)


""" 选择排序 """
def find_smallest(arr):
    smallest = arr[0]
    smallest_id = 0
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_id = i
    return smallest_id


def selection_sort(arr):
    new_arr = []
    for i in range(len(arr)):
        # print(f'第{i}轮遍历')
        smallest_id = find_smallest(arr)
        # print(f'此轮最小的数为：{arr[smallest_id]}')
        new_arr.append(arr.pop(smallest_id))
        # print(f'次轮结束后arrr: {arr}')
        # print(f'此轮结束后new_arr: {new_arr}')
        # print('\n')
    return new_arr


"""冒泡排序"""


def bubble_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


"""插入排序"""


def insertion_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key
    return arr


"""二分法查找"""


# 左闭右闭
class Solution1:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:
                return mid
        return -1


# 左闭右开
class Solution2:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid
            else:
                return mid
        return -1


# MD5（不可逆）
from hashlib import md5

num = '1|1685019152000D#uqGdcw41pWeNXm'
parse_num = md5(num.encode()).hexdigest()
print(parse_num)

# BASE64
import base64

# 加密
a = str(base64.b64encode(b'123456'))
print(a[2:-1])
# 解密
b = 'MTIzNDU2'
print(base64.b64decode(b).decode())
# or
print(str(base64.b64decode(b), 'utf-8'))

# SHA加密（不可逆）
import hashlib

wd = '你好'
sha1 = hashlib.sha1(wd.encode(encoding='utf-8')).hexdigest()
print(sha1)


"""九九乘法表"""
def func_9():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f'{j}*{i}={i * j}', end=' ')
        print()


func_9()
