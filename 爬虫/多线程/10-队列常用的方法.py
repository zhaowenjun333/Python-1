from queue import Queue

q = Queue(5)  # 只能存5个
q.put(1)
q.put(2)
q.put(3)
print(f'队列大小---{q.qsize()}')  # 查看当前队列的大小
print(q.get())
print(f'队列大小---{q.qsize()}')
# print(q.get())
# print(f'队列大小---{q.qsize()}')
# print(q.get())
# print(f'队列大小---{q.qsize()}')
print(q.full())   # 返回bool类型，False，判断队列是否满了
print(q.empty())  # 判断队列是否为空，False
