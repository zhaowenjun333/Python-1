import copy

# test = 'abc'
# print("=====赋值=====")
# b = test
# print(test)
# print(b)
# print(test is b)
# print(test == b)
# print(id(test))
# print(id(b))
# print("=====浅拷贝=====")
# b = copy.copy(test)
# print(test)
# print(b)
# print(test is b)
# print(test == b)
# print(id(test))
# print(id(b))
# print("=====深拷贝=====")
# b = copy.deepcopy(test)
# print(test)
# print(b)
# print(test is b)
# print(test == b)
# print(id(test))
# print(id(b))

list1 = [[1, 2], [30, 40]]
list2 = copy.copy(list1)
list3 = copy.deepcopy(list1)

list1.append(100)
print("list1:", list1, id(list1))
print("list2:", list2, id(list2))
print("list3:", list3, id(list3))
list1[0].append(3)
print("list1:", list1, id(list1))
print("list2:", list2, id(list2))
print("list3:", list3, id(list3))
list1[1] += (50, 60)
print("list1:", list1, id(list1))
print("list2:", list2, id(list2))
print("list3:", list3, id(list3))

# a = [[1, 2], (3, 1000)]
# b = copy.copy(a)
# print(id(a))
# print(id(b))


