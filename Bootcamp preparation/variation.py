import math

n = 6
x = 2
with_repetition = True

stop_element = n - x + 1
if not with_repetition:
    variation = 1
    for i in range(n, stop_element - 1, -1):
        variation *= i
else:
    variation = math.pow(n, x)
print(variation)
