from Person import Person
from Student import Student

person = Person("Michael Jordan", 60)
student = Student("Almir Mustafic", 55, "20114")

print("Persons File:")
print(Person.read_file())

print("\nStudents File:")
print(Student.read_file())