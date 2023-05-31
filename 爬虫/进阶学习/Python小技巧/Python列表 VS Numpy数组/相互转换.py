
import numpy as np

# 一、Python列表转换为NumPy数组
my_list = [1, 2, 3, 4, 5]

# 将Python列表转换为NumPy数组
my_array = np.array(my_list)

# 输出转换后的NumPy数组
print(my_array)

# 二、NumPy数组转换为Python列表
new_list = my_array.tolist()
print(new_list)
