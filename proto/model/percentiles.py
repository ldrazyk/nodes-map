import numpy as np

def get_percentiles(data, j):

    arr = np.array([row[j] for row in data])
    print(arr)
    
    return np.searchsorted(np.sort(arr), arr) / (len(arr) - 1) * 100

data = [
    [2, 3, 5, 7, 1],
    [0, 4, 8, 2, 9],
    [4, 5, 8, 3, 0],
    [9, 7, 4, 0, 2],
    [1, 5, 0, 3, 2]
]

print(get_percentiles(data, 0))