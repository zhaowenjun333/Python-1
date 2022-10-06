from queue import Queue

# maxsize: 最大值，可以存多少个数据，队列参数不写，大小跟内存有关系
q = Queue(5)  # 只能存5个
q.put(1)
q.put({'name': '林非'})
q.put([3, 4, 5])
q.put(2.3)
q.put(True)
q.put_nowait(5)   # 继续存，但会触发异常
print(q.qsize())  # 查看当前队列的大小
