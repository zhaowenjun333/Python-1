

my_dict = {'a': 1, 'b': 2, 'c': 3}
keys = ['a', 'c']

# 方法一：列表推导式
values1 = [my_dict.get(key) for key in keys]
# print(values1)

# 方法二：高阶函数, (map效率不如列表推导式)
values2 = list(map(my_dict.get, keys))
# print(values2)

# 方法三：pip install pydash
from pydash import at
values3 = at(my_dict, 'a', 'c')
# print(values3)

# 方法四：pandas
import pandas as pd
s = pd.Series(my_dict)
print(s[['a', 'c']])
