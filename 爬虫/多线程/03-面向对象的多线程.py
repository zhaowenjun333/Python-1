import threading
import time
from threading import Thread


class MyThread1(Thread):
    def run(self):
        for i in range(5):
            print(f'MyThread1----{i}')
            time.sleep(1)


class MyThread2(Thread):
    def run(self):
        for i in range(5):
            print(f'MyThread2----{i}')
            time.sleep(1)


if __name__ == '__main__':
    t1 = time.time()
    mt1 = MyThread1()
    mt2 = MyThread2()
    mt1.start()
    mt2.start()
    t2 = time.time()
    print(t2-t1)
