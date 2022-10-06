ls = [("小黑",59),("小绿",58),("小王",52),("小许",62)]
#ls.sort(key=lambda x:x[1])
#print(ls)
#结果：[('小王', 52), ('小绿', 58), ('小黑', 59), ('小许', 62)]

ls.sort(key=lambda x:x[0])
print(ls)