import threading
import time
from threading import Thread


def task1():
    for i in range(5):
        print(f'task1...{i}')
        time.sleep(1)


if __name__ == '__main__':
    t1 = time.time()
    print(threading.enumerate(), '创建之前')
    d1 = Thread(target=task1)
    print(threading.enumerate(), '创建之后')
    d1.start()
    print(threading.enumerate(), '开启线程')
    t2 = time.time()
    print(t2-t1)
