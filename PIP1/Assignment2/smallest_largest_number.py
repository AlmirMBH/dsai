"""
Loops 1: Write a program that asks the user to input 10 numbers, and finds the difference
between largest and the smallest number.
"""

input_range = 10
numbers = []

for i in range(input_range):
    input_valid = True
    while input_valid:
        try:
            number = float(input(f"Enter number {i + 1}: "))
            numbers.append(number)
            input_valid = False
        except ValueError:
            print("Invalid input. Please enter a valid number.")

print(f"The largest number is: {max(numbers)}\n"
      f"The smallest number is: {min(numbers)}\n"
      f"The difference between the largest and smallest number is: {max(numbers) - min(numbers)}")
