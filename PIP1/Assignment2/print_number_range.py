"""
Write a program that asks the user to enter a series of numbers from the keyboard.
User can stop entering numbers by entering value -1. The program needs to calculate
and print out the average of all entered numbers that are between 20 and 50, as well
as print out how many numbers were out of [20, 50] range.
"""

prompt = "Enter a number between 20 and 50 or -1 to stop: "
avg_message = "\nThe average of numbers between 20 and 50 is: "
required_numbers_missing_message = "No numbers between 20 and 50 were entered."
out_of_range_numbers_message = "Total numbers out of the range [20, 50]: "
numbers = []
out_of_range_count = 0
num = 0

while num != -1:
    try:
        num = float(input(prompt))
        if 20 <= num <= 50: numbers.append(num)
        elif num != -1: out_of_range_count += 1
    except ValueError:
        print("Invalid input! " + prompt)

if numbers:
    average = sum(numbers) / len(numbers)
    print(avg_message + str(average))
else:
    print(required_numbers_missing_message)

print(out_of_range_numbers_message + str(out_of_range_count))
