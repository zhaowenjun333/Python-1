import time
from threading import Thread


def sing():
    for i in range(3):
        print(f'林正在唱歌。。。。。{i}')
        time.sleep(1)


def dance():
    for i in range(3):
        print(f'林正在跳舞。。。。。{i}')
        time.sleep(1)


if __name__ == '__main__':
    # 一个主线程，两个子线程
    d1 = time.time()
    t1 = Thread(target=sing)
    t2 = Thread(target=dance)
    t1.start()
    t2.start()
    d2 = time.time()
    print(d2-d1)

