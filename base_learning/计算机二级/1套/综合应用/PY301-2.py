# 以下代码为提示框架
# 请在...处使用一行或多行代码替换
#
# 注意：提示框架代码可以任意修改，以完成程序功能为准

f = open("命运.txt","r")
txt = f.read()

for ch in "\n":
    txt = txt.replace(ch,"")
d = {}
for ch in txt:
    d[ch] = d.get(ch,0)+1
ls = list(d.items())
ls.sort(key=lambda x:x[1], reverse=True) # 此行可以按照词频由高到低排序
for i in range(10):
    print(str(ls[i])[2],end="")

f.close()