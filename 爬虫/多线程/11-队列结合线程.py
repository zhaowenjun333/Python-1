from queue import Queue
import threading
import time


def set_value(q):
    num = 0
    while True:
        q.put(num)
        num += 1
        time.sleep(0.01)


def get_value(q):   # 获取数据
    while True:
        print(q.get())


if __name__ == '__main__':
    q = Queue(5)
    t1 = threading.Thread(target=set_value, args=(q, ))
    t2 = threading.Thread(target=get_value, args=(q, ))
    t1.start()
    t2.start()
