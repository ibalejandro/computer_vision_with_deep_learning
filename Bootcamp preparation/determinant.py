import numpy as np

array = [[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]]

a = np.array(array)
det = np.linalg.det(a)
print(det)
