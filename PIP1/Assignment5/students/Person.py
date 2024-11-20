"""
Create a class representing a person. The class has protected attributes name and age.
In addition to initializing those attributes, the constructor needs to add a line
containing the person’s information into a file named persons.txt in the format name: age.
The class has a static method called read_file which returns the content of persons.txt.
"""

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

        with open("persons.txt", "a") as file:
            file.write(str(self._name) + ": " + str(self._age) + "\n")

    @staticmethod
    def read_file():
        try:
            with open("persons.txt", "r") as file:
                return file.read()
        except FileNotFoundError:
            return "persons.txt file not found."