def get_num_of_sums(n):
    l = 1
    count = 0
    while ((l * (l + 1)) / 2) < n:
        a = (n - ((l * (l + 1)) / 2)) / (l + 1)
        if int(a) == a:
            count += 1
        l += 1
    return count


number = 15
print(get_num_of_sums(number))
