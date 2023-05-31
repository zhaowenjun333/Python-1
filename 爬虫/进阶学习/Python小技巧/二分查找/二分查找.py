import timeit
# 方法一：
class Solution0:
    def search(self, nums: list[int], target: int) -> int:
        a = 0
        for i in range(len(nums)):
            if target == nums[i]:
                a = i
                break
            else:
                a = -1
        print(f'Solution0查询结果为: {a}')
        return a


nums1 = [-1, 0, 3, 5, 9, 12]
s0 = Solution0()
t01 = timeit.timeit(stmt=f's0.search({nums1}, {9})', setup='from __main__ import s0', number=1)
print(t01)
t02 = timeit.timeit(stmt=f's0.search({nums1}, {2})', setup='from __main__ import s0', number=1)
print(t02)

"""
题目：
给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target ，
写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。

示例1
输入: nums = [-1,0,3,5,9,12], target = 9
输出: 4
解释: 9 出现在 nums 中并且下标为 4

示例2
输入: nums = [-1,0,3,5,9,12], target = 2
输出: -1
解释: 2 不存在 nums 中因此返回 -1
"""


# 方法二（二分法）：
# （1）左闭右闭
class Solution1:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            middle = (left + right) // 2
            if nums[middle] < target:
                left = middle + 1
            elif nums[middle] > target:
                right = middle - 1
            else:
                return middle
        return -1


s1 = Solution1()
t11 = timeit.timeit(stmt=f's1.search({nums1}, {9})', setup='from __main__ import s1', number=1)
print(t11)
t12 = timeit.timeit(stmt=f's1.search({nums1}, {2})', setup='from __main__ import s1', number=1)
print(t12)

# （2）左闭右开
class Solution:
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
