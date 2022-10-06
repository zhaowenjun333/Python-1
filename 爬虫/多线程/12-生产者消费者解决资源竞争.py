import threading
import time
from queue import Queue

num = 0
q = Queue(2)
q.put(num)


def task(nums):
    for i in range(nums):
        numbers = q.get()
        numbers += 1
        q.put(numbers)  # 新值放入队列中


def task1(nums):
    for i in range(nums):
        numbers = q.get()
        numbers += 1
        q.put(numbers)  # 新值放入队列中


if __name__ == '__main__':
    nums = 100000
    t1 = threading.Thread(target=task, args=(nums, ))
    t2 = threading.Thread(target=task1, args=(nums, ))
    t1.start()
    t2.start()
    time.sleep(3)
    print(f'main---num={q.get()}')
