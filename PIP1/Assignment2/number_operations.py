import re

"""
Exercise 2: Write a program that asks the user to input two numbers, then asks the user which
mathematical operation to perform, and shows the result.
"""

def get_numbers():
    prompt = "Enter two numbers separated by a space, comma, or colon: "
    numbers = input(prompt)
    numbers = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)', numbers)

    while len(numbers) != 2:
        numbers = input("Invalid input. " + prompt)
        numbers = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)', numbers)

    num1, num2 = map(float, [num[0] for num in numbers])

    return {"num1": num1, "num2": num2}


def get_operation():
    prompt = "Select a mathematical operation: (+, -, *, /)"
    available_operations = ["+", "-", "*", "/"]
    operation = input(prompt)

    while operation not in available_operations:
        operation = input("Invalid operation! " + prompt)

    return operation


def calculate(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        else:
            return 0

numbers = get_numbers()
operation = get_operation()
result = calculate(numbers["num1"], numbers["num2"], operation)

print("Result:", result)
