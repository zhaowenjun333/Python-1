import time
import asyncio


# 异步协程函数
# async def func():
#     print('我喜欢林非')
#     # 睡眠3秒钟
#     time.sleep(3)    # 让当前的线程处于阻塞当状态， CPU是不为我工作的
#     print('我真的喜欢林非')
#
#
# if __name__ == '__main__':
#     g = func()   # 此时的函数是异步协程函数  此时函数执行得到的是一个协程对象
#     # print(g)
#     # 结果：<coroutine object func at 0x000001FD88A75DC8>
#     asyncio.run(g)     # 协程程序运行需要asyncio模块的支持


# async def like1():
#     print('我喜欢林非')
#     # 睡眠3秒钟
#     # time.sleep(3)   # 当程序出现了同步操作的时候，异步就中断了
#     # await: 挂起任务
#     await asyncio.sleep(3)   # 异步操作的代码
#     print('我真的喜欢林非')
#
#
# async def like2():
#     print('我喜欢陈凡')
#     # 睡眠3秒钟
#     # time.sleep(2)
#     await asyncio.sleep(2)
#     print('我真的喜欢陈凡')
#
#
# async def like3():
#     print('我喜欢林非')
#     # 睡眠3秒钟
#     # time.sleep(4)
#     await asyncio.sleep(4)
#     print('我真的喜欢陈凡')
#
#
# if __name__ == '__main__':
#     f1 = like1()
#     f2 = like2()
#     f3 = like3()
#     tasks = [f1, f2, f3]
#
#     t1 = time.time()
#     # 一次性启动多个任务(协程)
#     asyncio.run(asyncio.wait(tasks))
#     t2 = time.time()
#     print(t2-t1)


async def like1():
    print('我喜欢林非')
    await asyncio.sleep(3)
    print('我真的喜欢林非')


async def like2():
    print('我喜欢陈凡')
    await asyncio.sleep(2)
    print('我真的喜欢陈凡')


async def like3():
    print('我喜欢林非')
    await asyncio.sleep(4)
    print('我真的喜欢陈凡')


async def main():
    # 第一种写法
    # f1 = like1()
    # await f1     # 异步协程的调用 ，await只能放在async里面
    # f2 = like2()
    # await f2
    # f3 = like3()
    # await f3
    # 一般await挂起操作放在协程对象前面
    # 第二种写法（推荐）
    tasks = [
      asyncio.create_task(like1()),     # asyncio.create_task() :用来包装成Task对象，Python3.8版本以后需要手动包装
      asyncio.create_task(like2()),
      asyncio.create_task(like2())
    ]
    # 挂起
    await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    # 一次性启动多个任务（协程）
    asyncio.run(main())
    t2 = time.time()
    print(t2-t1)


# input()  程序也是处于阻塞状态
# request.get(bilibili)  在网络上请求返回数据之前，程序也是出于阻塞状态
# 一般情况下，当程序处于 IO 操作的时候，线程都会出于阻塞状态

# 协程：当程序遇见了 IO 操作的时候，可以选择性的切换到其他任务上

# *************************  模板   ***************************************
# 爬虫领域的应用(伪代码)
# async def download(url):
#     print('准备开始下载')
#     await asyncio.sleep(2)    # 网络请求
#     print('下载完成')
#
#
# async def main():
#     urls = [
#         'http://www.baidu.com',
#         'http://www.bilibili.com',
#         'http://www.163.com'
#     ]
#     tasks = []
#     for url in urls:
#         d = download(url)
#         tasks.append(d)
#
#     await asyncio.wait(tasks)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())

