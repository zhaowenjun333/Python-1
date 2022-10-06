import time
from threading import Thread


def task():
    print('hello world')
    time.sleep(1)
    print('hello world')


if __name__ == '__main__':
    t1 = time.time()
    for i in range(5):
        # task()
        t = Thread(target=task)
        t.start()  # 多线程状态为开始工作的状态，具体时间由cpu决定
    t2 = time.time()
    print(t2-t1)
