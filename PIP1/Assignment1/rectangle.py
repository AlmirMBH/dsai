"""
Problem 3: Ask the user to enter the length, the width and the height of the rectangle and display its area and volume.
"""

# Length
length = input("Enter the length of the rectangle: ")

while not (length.lstrip('-').isdigit() or
           (length.count('.') == 1 and length.replace('.', '').lstrip('-').isdigit())):
    print("Invalid number!")
    length = input("Enter a valid integer or float: ")

length = float(length)

# Width
width = input("Enter the width of the rectangle: ")

while not (width.lstrip('-').isdigit() or
           (width.count('.') == 1 and width.replace('.', '').lstrip('-').isdigit())):
    print("Invalid number!")
    width = input("Enter a valid integer or float: ")

width = float(width)

# Height
height = input("Enter the width of the rectangle: ")

while not (height.lstrip('-').isdigit() or
           (height.count('.') == 1 and height.replace('.', '').lstrip('-').isdigit())):
    print("Invalid number!")
    height = input("Enter a valid integer or float: ")

height = float(height)


# Calculate area and volume
area = round(length * width, 2)
volume = round(length * width * height, 2)

# Display the results
print()
print("The area of the rectangle is: " + str(area))
print("The volume of the rectangular prism is: " + str(volume))