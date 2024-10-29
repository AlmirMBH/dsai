import numpy as np

"""
Based on matrix M, create the product of the matrix with the sum of its first column.
"""

M = np.array([
    [1, 2, 3],
    [1/3.6, 5, 23],
    [2**10.5, 42, np.cos(np.radians(80.841))]
])

first_column_sum = np.sum(M[:, 0])
result = M * first_column_sum

# Make the output readable (rounding)
np.set_printoptions(precision=4, suppress=True)

print("Original Matrix M:")
print(M)
print("\nSum of the First Column:")
print(first_column_sum)
print("\nResulting Matrix (M multiplied by the sum of its first column):")
print(result)
