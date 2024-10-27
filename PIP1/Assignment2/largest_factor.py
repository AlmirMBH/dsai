"""
Loops 2: Write a program that asks the user to enter a number and finds the largest factor of a
number, i.e. largest number that evenly divides given number.
"""

number = input("Enter a number greater than 1: ")

while not (number.isdigit() and int(number) > 1):
    print("Invalid input. Please enter a valid integer greater than 1.")
    number = input("Enter a number greater than 1: ")

number = int(number)

for i in range(number // 2, 0, -1):
    print(i)
    if number % i == 0:
        print(f"The largest factor of {number} is: {i}")
        break

