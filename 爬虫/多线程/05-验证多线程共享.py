import threading
import time
from threading import Thread

num = 100


def task1():
    global num
    num += 1
    print(f'task1 num={num}')


def task2():
    print(f'task2 num={num}')


if __name__ == '__main__':
    t1 = time.time()
    d1 = Thread(target=task1)
    d2 = Thread(target=task2)
    d1.start()
    d2.start()
    print(f'main num={num}')
    t2 = time.time()
