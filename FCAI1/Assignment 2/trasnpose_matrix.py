import numpy as np

"""
Based on matrix M, create the transpose of the matrix.
"""

M = np.array([
    ["1", "2", "3"],
    ["1/3.6", "5", "23"],
    ["2^10.5", "42", "cos(80.841)"]
])

M_transposed = M.T

for row in M_transposed:
    print(", ".join(row))
