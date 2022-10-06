# 全模式（将字符串的所有分词可能均列出来，冗余性最大）

import jieba

ls = jieba.lcut('全国计算机等级考试Python科目', cut_all=True)

print(ls)
# 结果：['全国', '国计', '计算', '计算机', '算机', '等级', '考试', 'Python', '科目']