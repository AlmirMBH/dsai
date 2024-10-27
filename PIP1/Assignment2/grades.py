"""
Exercise 3: Write a program that asks the user to enter points obtained in a course and displays
the grade. For the point range 100-95 the grade is 10, 94-85 for grade 9, 84-75 for
grade 8, 74-65 for grade 7, 64-55 for grade 6, no grade if below 55 points. If the user
enters points that are not in the range (100-0), appropriate message is printed out
and the program terminates
"""

def convert_points_into_grade(points):
    if 95 <= points: return 10
    elif 85 <= points: return 9
    elif 75 <= points: return 8
    elif 65 <= points: return 7
    elif 55 <= points: return 6
    elif points < 55: return None

prompt = "Enter points (0-100): "

points_input = input(prompt)

while not points_input.isdigit() or not (0 <= int(points_input) <= 100):
    prompt = "Invalid number! Please enter an integer between 0 and 100: "
    points_input = input(prompt)

grade = convert_points_into_grade(int(points_input))

if grade is not None:
    print(f"Your grade is: {grade}")
else:
    print("No grade for points below 55.")
