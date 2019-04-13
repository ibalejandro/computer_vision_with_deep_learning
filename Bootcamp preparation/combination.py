import math

n = 6
x = 2
with_repetition = True

if not with_repetition:
    combination = math.factorial(n) / (math.factorial(x) * math.factorial(n - x))
else:
    combination = math.factorial(n + x - 1) / (math.factorial(x) * math.factorial(n - 1))
print(combination)
