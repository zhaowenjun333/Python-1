# 精确模式

import jieba

a = '全国计算机等级考试Python科目'

ls = jieba.lcut(a)

print(ls)
# 结果：['全国', '计算机', '等级', '考试', 'Python', '科目']

#等价方式
l1 = jieba.cut(a)
print(l1)
# 返回一个可迭代对象
# 结果：<generator object Tokenizer.cut at 0x0000023BB6116430>
print(list(l1))
# 结果：['全国', '计算机', '等级', '考试', 'Python', '科目']