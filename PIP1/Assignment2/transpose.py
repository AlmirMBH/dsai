"""
Exercise 5: Write a program that asks the user to enter a matrix and displays its transpose.
"""

# Functions
def get_matrix():
    matrix = []
    number_of_rows = get_number_of_rows()

    for i in range(number_of_rows):
        row_elements = input(f"Enter row {i + 1} as (space-separated values): ")
        matrix.append([element for element in row_elements.split()])

    return matrix


def get_number_of_rows():
    number = input("Enter the number of rows: ")
    while not number.isdigit():
        number = input("Enter the number of rows: ")

    return int(number)


def longest_row_count(matrix):
    # not all rows have to be equal
    longest_row_element_count = 0

    for index, row in enumerate(matrix):
        current_length = len(row)
        if current_length > longest_row_element_count:
            longest_row_element_count = current_length

    return longest_row_element_count


def transpose_matrix(matrix):
    transposed = []
    longest_row_element_count = longest_row_count(matrix)

    for i in range(longest_row_element_count):
        new_row = []
        for j in range(len(matrix)):
            try:
                new_row.append(matrix[j][i])
            except:
                new_row.append("")
        transposed.append(new_row)

    return transposed


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))



matrix = get_matrix()

print("\nYour matrix:")
print_matrix(matrix)

print("\nTransposed matrix:")
transposed_matrix = transpose_matrix(matrix)
print_matrix(transposed_matrix)
