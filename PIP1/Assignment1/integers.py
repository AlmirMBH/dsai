"""
Problem 6: Ask the user to enter two integers. Then, swap their values and display them.
"""
integer1 = input("Enter the first integer: ")

while not (integer1.lstrip('-').isdigit()):
    print("Invalid number!")
    integer1 = input("Enter the first integer: ")

integer2 = input("Enter the second integer: ")

while not (integer2.lstrip('-').isdigit()):
    print("Invalid number!")
    integer2 = input("Enter the first integer: ")

# Swap the values
integer1, integer2 = integer2, integer1

print()
print("First integer:", integer1)
print("Second integer:", integer2)
