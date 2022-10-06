import copy

list1 = [[1, 2], (30, 40)]
list2 = copy.deepcopy(list1)

list1.append(100)
print("list1:", list1)
print("list2:", list2)

list1[0].append(3)
print("list1:", list1)
print("list2:", list2)

list1[1] += (50, 60)
print("list1:", list1)
print("list2:", list2)

list1: [[1, 2], (30, 40), 100]
list2: [[1, 2], (30, 40)]
list1: [[1, 2, 3], (30, 40), 100]
list2: [[1, 2], (30, 40)]
list1: [[1, 2, 3], (30, 40, 50, 60), 100]
list2: [[1, 2], (30, 40)]
