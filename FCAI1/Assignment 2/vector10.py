import numpy as np

"""
Using NumPy, create a column vector of length 10 where the elements are the numbers from 1 to 10;
"""

column_vector = np.arange(1, 11).reshape(10, 1)

print(column_vector)
