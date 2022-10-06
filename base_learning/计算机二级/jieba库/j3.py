# 搜索引擎模式

import jieba

ls = jieba.lcut_for_search('全国计算机等级考试Python科目')

print(ls)
# 结果：['全国', '计算', '算机', '计算机', '等级', '考试', 'Python', '科目']