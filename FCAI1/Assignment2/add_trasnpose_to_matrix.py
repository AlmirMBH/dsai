import numpy as np

"""
Based on matrix M, crate the matrix obtained by adding the transpose of the matrix to the original matrix;
"""

M = np.array([
    ["1", "2", "3"],
    ["1/3.6", "5", "23"],
    ["2^10.5", "42", "cos(80.841)"]
])

M_transpose = M.T
result = M + M_transpose

print("Original Matrix M:")
print(M)
print("\nTranspose of Matrix M:")
print(M_transpose)
print("\nResulting Matrix (M + M^T):")
print(result)
