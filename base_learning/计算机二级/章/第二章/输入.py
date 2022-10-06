#判断输入的整数是否在0~100之间
num=eval(input('请输入一个整数:'))
if num>100 or num<0:
    print('输入得数大于100或小于0')
else:
    print('您输入的是数在0到100之间')
