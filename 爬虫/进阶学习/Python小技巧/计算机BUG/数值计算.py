# 一
a = 1.2
b = 0.1

print(a-b)

# 二: 计算机的保留逻辑是，舍0存1。
a = 1.2
b = 0.1
c = a - b

if c >= 1.1:
    print(True)
else:
    print(False)


import decimal

a1 = 1.8
b1 = 0.1
c1 = a1 + b1
print(c1)

a2 = decimal.Decimal(f'{a1}')
b2 = decimal.Decimal(f'{b1}')
c2 = a2+b2
print(c2)


# 10/3
from fractions import Fraction

print(10/3)
print(Fraction(10, 3))
print(Fraction(10, 5))

