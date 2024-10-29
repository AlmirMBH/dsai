import numpy as np

"""
Using NumPy, create matrix M.
"""

M = np.array([
    ["1", "2", "3"],
    ["1/3.6", "5", "23"],
    ["2**10.5", "42", "cos(80.841)"]
])

for row in M:
    print(", ".join(row))
