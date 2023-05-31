import numpy as np

my_list = [1, 2, 3, 4, 5]
my_array = np.array([1, 2, 3, 4, 5])

# 打印列表和数组
print(f'Python列表：{my_list}')
print(f'Numpy数组：{my_array}')
# 结果
# Python列表：[1, 2, 3, 4, 5]
# Numpy数组：[1 2 3 4 5]

# 访问列表和数组中的元素
print(f'列表第一个元素：{my_list[0]}')
print(f'数组第一个元素：{my_array[0]}')
# 结果
# 列表第一个元素：1
# 数组第一个元素：1

# 使用循环对列表和数组进行迭代
for element in my_list:
    print(f"Python列表的元素: {element}")

for element in my_array:
    print(f"NumPy数组的元素: {element}")
# 结果
# Python列表的元素: 1
# Python列表的元素: 2
# Python列表的元素: 3
# Python列表的元素: 4
# Python列表的元素: 5
# NumPy数组的元素: 1
# NumPy数组的元素: 2
# NumPy数组的元素: 3
# NumPy数组的元素: 4
# NumPy数组的元素: 5


# 使用内置函数和方法对列表和数组进行操作
print(f"列表的总和: {sum(my_list)}")
print(f"数组的总和: {np.sum(my_array)}")
# 结果
# 列表的总和: 15
# 数组的总和: 15
