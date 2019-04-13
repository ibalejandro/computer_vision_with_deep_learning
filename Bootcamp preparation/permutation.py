import math

n = 6
x = 2
with_repetition = True
element_repetitions = [3, 2]

if not with_repetition:
    permutation = math.factorial(n) / math.factorial(n - x)
else:
    norm_factor = 1
    for i in element_repetitions:
        norm_factor *= math.factorial(i)
    permutation = math.factorial(n) / norm_factor
print(permutation)
