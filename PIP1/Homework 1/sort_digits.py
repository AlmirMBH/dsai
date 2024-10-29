"""
Homework 1 1: Write a program that plays a simple game. The game is described as follows. User
enters a number. Then, the user tries to sort the digits of the number by repeatedly
reversing the order of the first 'n' digits of a number. Make sure to validate user input.
For example, if the user enters 52136, the output should be 12356. To get this output,
the user must go through the following steps:

Current state          Value of n    Resulting state
52136                       3           12536
12536                       4           35216
35216                       2           53216
"""

def reverse_digits(number, n_digits):
    number_str = str(number)
    if n_digits > len(number_str) or n_digits < 1:
        print("Invalid number! It must be between 1 and the length of the number: ")
        return number_str

    reversed_part = number_str[:n_digits][::-1] # first n elements, then reverse
    remaining_part = number_str[n_digits:] # skip first n elements, take the remaining

    return reversed_part + remaining_part


def check_if_sorted(number):
    n_digit_prompt = "Enter a valid number between 1 and the length of the number: "
    is_sorted = False

    while not is_sorted:
        print(f"Current state: {number}")
        n_digit = input(n_digit_prompt)

        if not n_digit.isdigit() or not (1 <= int(n_digit) <= len(str(number))):
            print("Invalid input! " + n_digit_prompt)
            continue

        n_digit = int(n_digit)
        number = reverse_digits(number, n_digit)

        if ''.join(sorted(str(number))) == str(number):
            is_sorted = True
            print(f"Sorted number: {number}")


positive_number_prompt = "Enter a valid positive integer: "
user_input = input(positive_number_prompt)

while not user_input.isdigit():
    user_input = input("Invalid input! " + positive_number_prompt)

number = int(user_input)
check_if_sorted(number)