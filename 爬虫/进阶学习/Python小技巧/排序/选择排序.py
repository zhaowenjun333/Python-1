""" 选择排序 """
def find_smallest(arr):
    smallest = arr[0]
    smallest_id = 0
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_id = i
    return smallest_id

def selection_sort(arr):
    new_arr = []
    for i in range(len(arr)):
        # print(f'第{i}轮遍历')
        smallest_id = find_smallest(arr)
        # print(f'此轮最小的数为：{arr[smallest_id]}')
        new_arr.append(arr.pop(smallest_id))
        # print(f'次轮结束后arrr: {arr}')
        # print(f'此轮结束后new_arr: {new_arr}')
        # print('\n')
    return new_arr


if __name__ == '__main__':
    array = [1, 5, 6, 2, 8, 7, 9, 4]
    newArr = selection_sort(array)
    print(newArr)
