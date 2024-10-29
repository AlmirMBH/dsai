import numpy as np

"""
Based on matrix M, show third row, second column and element at (2, 1) of the matrix M;
"""

M = np.array([
    ["1", "2", "3"],
    ["1/3.6", "5", "23"],
    ["2**10.5", "42", "cos(80.841)"]
])

third_row = M[2]
second_column = M[:, 1]
element_at_2_1 = M[2, 1]

print("Third Row of the matrix M:")
print(third_row)

print("\nSecond Column of the matrix M:")
print(second_column)

print("\nElement at (2, 1) of the matrix M:")
print(element_at_2_1)
