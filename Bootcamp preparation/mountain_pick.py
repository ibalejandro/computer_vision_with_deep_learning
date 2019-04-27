def find_mountain_pick(path):
    max_val = path[0]
    mountain_pick = 0
    for i in range(1, len(path)):
        if path[i] > max_val:
            max_val = path[i]
            mountain_pick = i
    return mountain_pick


def binary_search(path, left, right):
    if left == right:
        return left
    elif right - left == 1:
        index = left
        if path[left] < path[right]:
            index = right
        return index
    else:
        middle = (left + right) // 2
        if path[middle] - path[middle - 1] < 0:
            return binary_search(path, left, middle - 1)
        elif path[middle] - path[middle + 1] < 0:
            return binary_search(path, middle + 1, right)
        else:
            return middle


def find_mountain_pick_binary_search(path):
    return binary_search(path, 0, len(path) - 1)


mountain_path = [1, 2, 3, 5, 4, 3, 2, 1, 0]
print("Brute force: {}".format(find_mountain_pick(mountain_path)))
print("Binary search: {}".format(find_mountain_pick_binary_search(mountain_path)))
