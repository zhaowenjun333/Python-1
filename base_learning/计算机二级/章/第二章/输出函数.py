'''
a=input('请输入：')
print(a)
#eval:去掉最外层的引号
b=eval('1.2')
print(b,type(b))
'''

'''
#print(输出字符串模板.format(变量1，变量2，......，变量N))
#用于混合输出字符串与变量的值，其中输出字符串模板中使用{}表示一个槽位，每一个槽位对应.format()的一个变量}
m,n=10,20
print('整数{}和整数{}的差ui：{}'.format(m,n,m-n))
'''

#print()函数输出文本时会在最后增加一个换行，如果不希望在最后增加这个换行，
#或者希望输出文本后增加其他内容，可以对print()函数的end参数进行赋值。
#语法格式为：print(待输出的内容,end='增加的输出结尾')
a=10
print(a,end='.')
print(a,end='%')
print(a)