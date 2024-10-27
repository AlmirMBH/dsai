import random

"""
Problem 5: Ask the user to enter a list of 5 names. Then, randomly select one of the names from the list and remove it.
Then, display the remaining four names as well as the removed name. Use random library to select the
random name for the removal.
"""

names = []

for i in range(5):
    name = input("Enter name " + str(i+1) + ": ")
    while not name.isalpha() or name in names:
        print("Invalid input! Only letters, no duplicate names!")
        name = input("Enter your name: ")
    names.append(name)

removed_name = random.choice(names)
names.remove(removed_name)

print("Removed name: " + removed_name)
print("Remaining names:", names)