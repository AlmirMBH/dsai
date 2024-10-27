import math

"""
Problem 4:
Ask the user to enter the radius of the sphere and display its volume. Use math library to get the value of π.
"""

radius = input("Enter the radius of the sphere: ")

while not (radius.lstrip('-').isdigit() or
           (radius.count('.') == 1 and radius.replace('.', '').lstrip('-').isdigit())) or float(radius) <= 0:
    print("Invalid number!")
    radius = input("Enter the radius of the sphere: ")

radius = float(radius)

volume = round((4/3) * math.pi * (radius ** 3), 2)

print()
print("The volume of the sphere is: " + str(volume))
