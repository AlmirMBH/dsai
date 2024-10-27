import math
from sympy import primerange

"""
Exercise 1
Declare the following variables:
• An integer variable named age that represents your current age.
• A float variable named height that reflects your height in meters (e.g., 1.75).
• A string variable named name that stores your name.
• A boolean variable named is_student that indicates whether you are currently a student (True) or not
(False).
After declaring these variables, your program should print their values. Use descriptive messages to explain each
output clearly, providing context for the information displayed.
example: name = "John" print("My name is", name + ".")
"""
age = 25
height = 1.75
name = "John"
is_student = True

print("My name is", name + ".")
print("I am", age, "years old.")
print("My height is", height, "meters.")
print("Am I a student?", is_student)


"""
Exercise 2
In this task, you will create a program that checks the temperature to determine if it is hot or cold.
Instructions:
Prompt the User: Ask the user to enter the current temperature in degrees Celsius. Use If-Else Statements: If the
temperature is 30 degrees or higher, print: "It’s hot outside." If the temperature is below 30 degrees, print: "It’s
cold outside."
Example Output:
If the user enters 32, the program should output: "It’s hot outside." If the user enters 20, the program should output:
"It’s cold outside."
"""
temperature = int(input("Enter the current temperature in degrees Celsius: "))

if temperature >= 30:
    print("It’s hot outside.")
else:
    print("It’s cold outside.")

"""
Exercise 3a
Calculate following expressions:
"""
result = 4.7 ** (12 / 7.4) + math.sqrt(5)
print("Task a: " + str(result))

"""
3b
"""
result = math.sin(math.pi / 6) + math.tan(math.pi * (math.e ** math.pi))
print(f"tan(π) * e^π: {result}")

"""
3c
"""
result = (3 + 5**8) * 5
print(f"The result of (3 + 5^8) * 5 is: {result}")

"""
3d
"""
result = math.floor(169 / 14)
print(f"The result of [169 / 14] is: {result}")


"""
Exercise 4
In this task, you will develop a program that prints the numbers from 1 up to a user-defined number, referred to as
N. The first step is to prompt the user to enter a positive integer. This input will serve as the upper limit for our
loop.
Once the user provides their input, we will implement a for loop that iterates from 1 to N. Within each iteration,
the loop will execute a simple command to print the current number.
For example, if the user enters the number 5, the program should produce the following output: 1 2 3 4 5
"""
N = 0
for _ in range(100):
    N = input("Enter a positive integer: ")

    if N.isdigit() and int(N) > 0:
        N = int(N)
        break

if N <= 0:
    print("No valid input received after several attempts.")
else:
    for number in range(1, N + 1):
        print(number, end=" ")

print("\n")


"""
Exercise 5
Complete the same task as in the previous example, but use a while loop instead.
"""
N = input("Enter a positive integer: ")

while not N.isdigit():
    print("That's not a valid number. Please enter a positive integer.")
    N = input("Enter a positive integer: ")

N = int(N)

for number in range(1, N + 1):
    print(number, end=" ")

print()


"""
Exercise 6
In this task, you will create a program that collects numbers from the user and stores them in a list until the user
decides to stop. Start by creating an empty list to store the numbers. Implement a while loop that will repeatedly
ask the user to enter a number.
Inside the loop, prompt the user to enter a number. Append the entered number to the list. Ask the user if they
want to add another number. If the user types "yes," the loop will continue; if they type "no," the loop will end.
After the user decides to stop, print the list of numbers.
"""
numbers = []

user_input = input("Enter a number: ")
numbers.append(int(user_input))

continue_input = input("Do you want to add another number? (yes/no): ").strip().lower()

while continue_input != "yes" and continue_input != "no":
    continue_input = input("Do you want to add another number? (yes/no): ").strip().lower()

    if continue_input != "yes" and continue_input != "no":
        print("Only 'yes' or 'no' allowed")

while continue_input == "yes":
    user_input = input("Enter a number: ")
    numbers.append(int(user_input)) # int validation required
    continue_input = input("Do you want to add another number? (yes/no): ").strip().lower()

print("You entered the following numbers:")
print(numbers)

print()




"""
Extra task
Print prime numbers
"""
nums = range(1,1000)

def is_prime(num):
    for x in range(2, num):
        if (num%2) == 0:
            return False
    return True

primes = list(filter(is_prime, nums))
print(primes)

primes = list(primerange(0, 1000))
print(primes)

