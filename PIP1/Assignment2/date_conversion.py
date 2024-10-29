"""
Conditionals 2: Write a program that asks the user to enter two integers day and month . The value of
day should be between 1 and 31, and the value of month should be between 1 and 12.
If the input is valid, the program needs to print out the date in the following format:
day of monthName , where the monthName is the name of the month corresponding
to the value of the month variable.
"""

months = [
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
]

def validate_int(prompt, min_value, max_value):
    value = input(prompt)
    while not (value.isdigit() and min_value <= int(value) <= max_value):
        print(f"Invalid input! Please enter a number between {min_value} and {max_value}.")
        value = input(prompt)
    return int(value)

day = validate_int("Enter the day (1-31): ", 1, 31)
month = validate_int("Enter the month (1-12): ", 1, 12)

print(f"{day} of {months[month - 1]}")
