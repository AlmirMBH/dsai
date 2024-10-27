"""
Problem 1: Ask the user to enter their name, student ID number and age. Then, display the following message:
Hi, I am <Name>, my student number is <student ID> and I am <age> years old.
I look forward to learning everything I can about Python
"""

name = input("Enter your name: ")

while not name.isalpha():
    print("Invalid input! Please enter letters only.")
    name = input("Enter your name: ")


student_id = input("Enter your student ID: ")
while not (student_id.lstrip('-').isdigit()):
    print("Invalid number!")
    student_id = input("Enter your student ID: ")


age = input("Enter your age: ")

while not (age.lstrip('-').isdigit()):
    print("Invalid number!")
    age = input("Enter your student ID: ")

print()
print("Hi, I am " + name + ", my student number is " + str(student_id) + " and I am " + str(age) + " years old. I look forward to learning everything I can about Python")


