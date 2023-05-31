# 面试题（不允许使用for循环，循环列表中的数据）
dict_info = {
    'name': 'Gean',
    'age': 21,
    'gender': 'man'
}

iterator = dict_info.__iter__()   # 字典迭代器
while True:
    try:
        res = iterator.__next__()
    except StopIteration as se:
        break
    else:
        print(f'{res}: {dict_info[res]}')
