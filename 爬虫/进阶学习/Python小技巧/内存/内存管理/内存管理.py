import sys
name = 'Gean'
print(sys.getrefcount(name))  # 打印4


'''
1. name变量
2. getrefcount：当name被传递给getrefcount函数的时候，函数的参数也指向了它。
3. Python解释器：为了执行这个脚本，Python解释器也保留了一个引用，直到脚本结束。只针对脚本全局变量。
4. 编译优化器：当执行脚本的时候，优化器会尝试优化字节码，所以也产生了一次引用。这个引用是临时的，很快就会消失。
'''