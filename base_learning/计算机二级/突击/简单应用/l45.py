names=input("请输入各个同学行业名称，行业名称之间用空格间隔（回车结束输入）：")
ls = names.split()
d = {}
for i in ls:
    d[i] = d.get(i,0)+1
ls = list(d.items())
ls.sort(key=lambda x:x[1], reverse=True) # 按照数量排序
for k in ls:
    print("{}:{}".format(k[0],k[1]))