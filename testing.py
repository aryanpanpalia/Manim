import numpy as np

a1 = np.array([1, 2, 3])
a2 = np.array([1.01, 1.99, 3])

def approx(array1, array2):
    for element1, element2 in zip(array1, array2):
        if not (element1 - 0.05 < element2 < element1 + 0.05):
            return False
    return True

print(approx(a1, a2))
