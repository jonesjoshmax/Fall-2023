import numpy as np

a = np.array([[1, 1, 1],
              [2, 2, 2],
              [3, 3, 3]])
b = np.array([[4],
              [5],
              [6]])
c = np.array([4, 5, 6])

print(np.dot(a, b), np.dot(a, c))
