""" #以读的方式打开命运.txt文件，用相对路径即可
f = open('命运.txt','r')
#一个字符一个字符的读取，用read
txt = f.read()
d = {}
#遍历字典，并统计字符
for i in txt:
    if i not in "，。？！《》【】、“”‘’：；——（）□\n":
        d[i] = d.get(i,0) + 1
#print(d)
ls = list(d.items())
ls.sort(key=lambda x:x[1],reverse=True)
print("{}:{}".format(ls[0][0],ls[0][1]))

#关闭文件
f.close() """


""" # 以下代码为提示框架
# 请在...处使用一行或多行代码替换
#
# 注意：提示框架代码可以任意修改，以完成程序功能为准
f = open('命运.txt','r')
txt = f.read()
d = {}
for i in txt:
    if i not in "\n":
        d[i] = d.get(i,0) + 1
ls = list(d.items())
ls.sort(key=lambda x:x[1], reverse=True) # 此行可以按照词频由高到低排序
for a in range(10):
    print(ls[a][0],end='')

f.close() """

f = open('命运.txt','r')
fi = open('命运-频次排序.txt','w')
txt = f.read()
d = {}
for i in txt:
    if i not in " \n":
        d[i] = d.get(i,0) + 1
ls = list(d.items())
ls.sort(key=lambda x:x[1], reverse=True) # 此行可以按照词频由高到低排序
s=""
for k in ls:
    s += "{}:{}".format(k[0],k[1]) + ","
fi.write(s[:-1])

f.close()
fi.close()
