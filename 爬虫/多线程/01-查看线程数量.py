import threading
import time
from threading import Thread


def task1():
    for i in range(5):
        print(f'task1...{i}')
        time.sleep(1)


def task2():
    for i in range(5):
        print(f'task2...{i}')
        time.sleep(1)


if __name__ == '__main__':
    t1 = time.time()
    d1 = Thread(target=task1)
    d2 = Thread(target=task2)
    d1.start()
    d2.start()
    # 查看当前的线程,返回当前运行中的Thread对象列表
    while True:
        print(threading.enumerate())   # 运行结果不固定，线程无序
        if len(threading.enumerate()) <= 1:
            break
        time.sleep(1)
    t2 = time.time()
    print(t2-t1)

