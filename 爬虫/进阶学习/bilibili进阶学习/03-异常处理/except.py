#
"""
03-异常处理（报错）
KeyError
ImportError
IndexError
"""

# age = int(input('请输入你的年龄：'))
# print(age)

'''
try:
    可能报错的代码语句    
except 错误类型1（as 别名）:
    如果出错就要执行的代码
except 错误类型2（as 别名）:
    如果出错就要执行的代码
else:
    若没有出错就会执行的代码
finally:
    无论是否报错都会执行的代码
raise:
    人为抛出一个异常类型
class xxxError(Exception):
    pass
'''

# while True:
#     try:
#         age = int(input('请输入你的年龄：'))
#     except ValueError:
#         print('请输入正确的数据类型')
#         continue   # 跳过本次循环
#     else:
#         print(age)
#         break

str1 = 'ahlkhdalkhdohnkcvhjkia'
# 用户输入索引的位置，然后打印该位置的字符
while True:
    try:
        locate = int(input('请输入索引位置：'))
    except ValueError:
        print('请输入正确的数据类型')
        continue   # 跳过本次循环
    try:
        res = str1[locate]
    except IndexError:
        print('索引越界了，请输入正确的索引范围')
        continue
    else:
        print(res)
        break
