import numpy as np

"""
Define a function quadratic(M) that takes a NumPy 1D array and reshapes it into a square matrix if possible.
If reshaping is not possible, the function should do nothing.
"""

M = np.array([
    ["1", "2", "3"],
    ["1/3.6", "5", "23"],
    ["2**10.5", "42", "cos(80.841)"]
])


def quadratic(M):
    # Check if M is a 1D array
    if M.ndim != 1:
        print("Input must be a 1D array.")
        return None

    # Check if the length is a perfect square
    length = M.size
    sqrt_length = int(np.sqrt(length))

    if sqrt_length * sqrt_length == length:
        square_matrix = M.reshape(sqrt_length, sqrt_length)
        return square_matrix
    else:
        print("Reshaping not possible; input size is not a perfect square.")
        return None


square_matrix = quadratic(M)
print("\nReshaped Square Matrix:")
print(square_matrix)

M_invalid = np.array([1, 2, 3])
square_matrix_invalid = quadratic(M_invalid)
print("\nAttempt with an invalid size:")
print(square_matrix_invalid)