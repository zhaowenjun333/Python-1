import numpy as np

# 使用Numpy数组进行加法
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = a + b
print(c)
print(type(c))
# 结果
# [5 7 9]
# <class 'numpy.ndarray'>


# 使用Python列表进行加法
a = [1, 2, 3]
b = [4, 5, 6]
# print(a + b)
c = []

for i in range(len(a)):
    c.append(a[i] + b[i])
print(c)  # 输出 [5, 7, 9]
