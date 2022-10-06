import time


def sing():
    for i in range(3):
        print(f'林正在唱歌。。。。。{i}')
        time.sleep(1)


def dance():
    for i in range(3):
        print(f'林正在跳舞。。。。。{i}')
        time.sleep(1)


if __name__ == '__main__':
    sing()
    dance()
