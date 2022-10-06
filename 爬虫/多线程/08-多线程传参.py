import threading
import time
from threading import Thread

num = 0


def task1(nums):
    global num
    # 上锁
    mutex.acquire()
    mutex.acquire()
    for i in range(nums):
        num += 1
    mutex.release()  # 解锁
    mutex.release()  # 解锁
    print(f'task1 num={num}')


def task2(nums):
    global num
    # 上锁
    mutex.acquire()
    mutex.acquire()
    for i in range(nums):
        num += 1
    mutex.release()  # 解锁
    mutex.release()  # 解锁
    print(f'task2 num={num}')


if __name__ == '__main__':
    t1 = time.time()
    # 创建一把锁
    mutex = threading.RLock()   # 可加重复锁
    # mutex = threading.Lock()
    nums = 1000000
    # 传参必须以元祖形式
    d1 = Thread(target=task1, args=(nums,))
    d2 = Thread(target=task2, args=(nums,))
    d1.start()
    # d1.join()    # 等待子线程结束
    d2.start()
    # d2.join()
    time.sleep(2)
    print(f'main num={num}')
    t2 = time.time()


