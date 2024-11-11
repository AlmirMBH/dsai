class Person:

    numberOfPeople = 0

    def __init__(self, name, age):
        self._name = name
        self._age = age
        Person.numberOfPeople=Person.numberOfPeople+1


    def Greet(self):
        print("Hi, my name is "+self._name+" and I am "+str(self._age)+" old.")

class Student(Person):
    def __init__(self, name, age, id):
        super().__init__(name, age)
        self._id=id

    def Greet(self):
        print("Hi, my name is "+self._name+" and my student ID is "+str(self._id)+".")


class Teacher(Person):
    def __init__(self, name, age, title):
        super().__init__(name, age)
        self._title=title

    def Greet(self):
        print("Hi, my name is "+self._name+" and my title is "+self._title+".")


Bob=Teacher("Bob", 22, "Professor")
Alice=Student("Alice", 23, 2000)

lst=[]
lst.append(Bob)
lst.append(Alice)

for person in lst:
    person.Greet()