"""
Exercise 3: Write a program that asks the user to enter two numbers and prints all numbers that
are not the multiple of 6 between them.
"""

def validate_input(prompt):
    number = input(prompt)
    while not number.isdigit():
        number = input("Invalid number! " + prompt)

    return int(number)

start = validate_input("Enter the first integer: ")
end = validate_input("Enter the second integer: ")

# Swap if start greater than end
if start > end:
    start, end = end, start

for number in range(start, end + 1):
    if number % 6 != 0:
        print(number)

