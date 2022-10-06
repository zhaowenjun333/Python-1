import threading
import time
from threading import Thread

num = 0


def task1():
    global num
    for i in range(10000000):
        num += 1
    print(f'task1 num={num}')


def task2():
    global num
    for i in range(10000000):
        num += 1
    print(f'task2 num={num}')


if __name__ == '__main__':
    t1 = time.time()
    d1 = Thread(target=task1)
    d2 = Thread(target=task2)
    d1.start()
    d2.start()
    print(f'main num={num}')
    t2 = time.time()

'''
1. 共享全局变量会发生资源竞争问题
2. 多线程共享是不安全的，CPU决定着程序的执行
'''
