import time
from threading import Thread


def task():   # 子线程
    print('hello world')
    time.sleep(1)
    print('hello world')


if __name__ == '__main__':
    t1 = time.time()
    for i in range(5):  # 主线程
        # task()
        t = Thread(target=task)
        # t.setDaemon(True)  # 守护线程，主线程执行结束子线程
        t.start()  # 多线程状态为开始工作的状态，具体时间由cpu决定
        t.join()   # 子线程结束后在执行主线程
    print("我是主线程")
    t2 = time.time()
    print(t2-t1)
