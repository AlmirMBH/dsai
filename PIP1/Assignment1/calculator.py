"""
Problem 2: Let's create a simple calculator. First, ask the user to enter two floating point numbers. Then, display the sum,
the difference, the product and the quotient of entered numbers.
"""

number_1 = input("Enter a valid integer or float: ")

# We need to validate the input i.e. integers or decimals (no built-in function for floats),
# so we need to replace the '.' and check if all the characters are digits
while not (number_1.lstrip('-').isdigit() or
           (number_1.count('.') == 1 and number_1.replace('.', '').lstrip('-').isdigit())):
    print("Invalid number!")
    number_1 = input("Enter a valid integer or float: ")

number_1 = float(number_1)

# Allowed operators
valid_operators = ['+', '-', '*', '/']
operator = input("Enter the operator (+, -, *, /): ")

while operator not in valid_operators:
    print("Invalid operator! Please enter a valid operator.")
    operator = input("Enter the operator (+, -, *, /): ")


number_2 = input("Enter a valid integer or float: ")

while not (number_2.lstrip('-').isdigit() or
           (number_2.count('.') == 1 and number_1.replace('.', '').lstrip('-').isdigit())):
    print("Invalid number!")
    number_1 = input("Enter a valid integer or float: ")

number_2 = float(number_2)

result = 0

if operator == '+':
    result = number_1 + number_2
elif operator == '-':
    result = number_1 - number_2
elif operator == '*':
    result = number_1 * number_2
elif operator == '/':
    if number_2 != 0:
        result = number_1 / number_2
    else:
        result = 0


print("The result is: " + str(round(result, 2)))
