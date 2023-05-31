# NumPy数组在内存中存储为连续的块，因此比Python列表更有效地使用内存；
#
# NumPy数组可以使用原地操作来修改其内容，这意味着它们可以在不创建新数组的情况下执行许多操作。

import numpy as np
import sys
# 创建一个包含10000个整数的Python列表
my_list = list(range(10000))

# 创建一个包含10000个整数的Numpy数组
my_array = np.array(range(10000))

# 查看Python列表和Numpy数组在内存中所占的空间
print(f'Python列表占用的内存：{sys.getsizeof(my_list)}')
print(f'Numpy数组所占用的内存：{my_array.nbytes}')
# 结果
# Python列表占用的内存：80056


