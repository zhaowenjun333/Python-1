# 线程：执行单位，好比公司员工，必须要有，CPU调度线程
# 进程：资源单位，一个进程里至少要一个线程

# 启动每一个程序默认都会有一个主线程
# if __name__ == '__main__':
#     print('hello')

# 多线程
from threading import Thread


# def func():
#     for i in range(1000):
#         print('func', i)
#
#
# if __name__ == '__main__':
#     # 给新员工安排活儿，不影响自己本身的活儿
#     t = Thread(target=func())     # 创建线程类对象，并给线程安排任务
#     t.start()   # 多线程状态为可以开始工作状态，具体的执行时间由CPU决定
#     for i in range(1000):
#         print('main', i)


# class MyThread(Thread):
#     def run(self):  # 当线程被执行的时候，被执行的就是run()
#         for i in range(1000):
#             print('子线程', i)
#
#
# if __name__ == '__main__':
#     t = MyThread()
#     t.start()   # 开启线程，CPU默认执行run()
#
#     for i in range(1000):
#         print('主线程', i)


# 补充(传参)
def func(name):
    for i in range(1000):
        print(name, i)


if __name__ == '__main__':
    t1 = Thread(target=func, args=("周杰伦",))
    t1.start()

    t2 = Thread(target=func, args=("华晨宇",))
    t2.start()
