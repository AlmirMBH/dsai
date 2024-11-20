"""
Implement another class, which represents a student. A student is represented by
their name, age and id. In addition to being added to the persons.txt file, student's
information need to be added to a file named students.txt which contains information
about all students in the format name (id): age. It also has a static method called
read_file which returns the content of students.txt.
"""

from Person import Person

class Student(Person):
    def __init__(self, name, age, id):
        super().__init__(name, age) # reuse the person class' constructor
        self._student_id = id

        with open("students.txt", "a") as file:
            file.write(str(self._name) + " (" + str(self._student_id) + "): " + str(self._age)+ "\n")

    @staticmethod
    def read_file():
        try:
            with open("students.txt", "r") as file:
                return file.read()
        except FileNotFoundError:
            return "students.txt file not found."