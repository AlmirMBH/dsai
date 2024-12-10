"""
Create 3 new types of exceptions named AgeException, FirstNameException and IDException.
- Create a class Person that has 3 instance variables with following restrictions:
    • name - must be a string that only contains letters
    • age - must be a positive integer
    • ID - must be a positive 4-digit integer ABCD such that (A + B + C)%10 = D
- Test all of these requirements in the constructor of the Person class, and if any of them is not met, raise
one of the created exceptions.
- Ask the user to input name, age and ID for a person and try creating a new Person object with those variables.
- If an exception is raised, ask the user to input the variable that created the exception again.
- If there are no exceptions, print the person’s information and end the program.
"""

class FirstNameException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AgeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IDException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Person:
    def __init__(self, name, age, person_id):
        self.name = self.validate_name(name)
        self.age = self.validate_age(age)
        self.person_id = self.validate_id(person_id)


    @staticmethod
    def validate_name(name):
        if not name.isalpha():
            raise FirstNameException("Your name must meet the required criteria.")
        return name


    @staticmethod
    def validate_age(age):
        try:
            age = int(age)
            if age <= 0:
                raise AgeException("Your age must meet the required criteria.")
        except ValueError:
            raise AgeException("Your age must meet the required criteria.")
        return age


    @staticmethod
    def validate_id(person_id):
        try:
            person_id = int(person_id)
            if not (1000 <= person_id <= 9999):
                raise IDException("Your ID must meet the required criteria.")
            A, B, C, D = [int(digit) for digit in str(person_id)]
            if (A + B + C) % 10 != D:
                raise IDException("Your ID must meet the required criteria.")
        except ValueError:
            raise IDException("Your ID must meet the required criteria.")
        return person_id


    def __str__(self):
        return f"Person(Name: {self.name}, Age: {self.age}, ID: {self.person_id})"



if __name__ == "__main__":
    name = None
    age = None
    person_id = None

    while name is None:
        try:
            name = input("Enter your name (only letters allowed): ")
            Person.validate_name(name)
        except FirstNameException as exception:
            print(f"Error: {exception}")
            name = None


    while age is None:
        try:
            age = input("Enter your age (positive integer): ")
            Person.validate_age(age)
        except (AgeException, ValueError) as exception:
            print(f"Error: {exception}")
            age = None


    while person_id is None:
        try:
            person_id = input("Enter your 4-digit positive integer ID. For example, ABCD such that (A + B + C) % 10 = D: ")
            Person.validate_id(person_id)
        except (IDException, ValueError) as exception:
            print(f"Error: {exception}")
            person_id = None


    person = Person(name, age, person_id)
    print(person)
