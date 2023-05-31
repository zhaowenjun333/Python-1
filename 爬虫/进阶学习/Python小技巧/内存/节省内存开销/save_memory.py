import os
import time
import psutil


class StudentA:
    # 节约型
    # __slots__ 指定 Student 类的实例只能有 name 和 age 两个属性。
    __slots__ = ['name', 'age']

    def __init__(self, name, age):
        self.name = name
        self.age = age


class StudentB:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def measure_time(func):
    start_time = time.time()
    result = func()
    end_time = time.time()
    print(f'Time elapsed: {end_time - start_time:.6f} seconds')
    return result


# 各创建10000人
# @measure_time
# def create_instance_without_slotsA(n=100000):
#     return [StudentA('Gean', 22) for i in range(n)]


@measure_time
def create_instance_without_slotsB(n=100000):
    return [StudentB('ChenFan', 22) for i in range(n)]


if __name__ == '__main__':
    create_instance_without_slotsA
    processA = psutil.Process(os.getpid())
    print('StudentA used memory: ', processA.memory_info().rss / 1024 / 1024, 'MB')

    create_instance_without_slotsB
    processB = psutil.Process(os.getpid())
    print('StudentB used memory: ', processB.memory_info().rss / 1024 / 1024, 'MB')



