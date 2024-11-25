"""
This file contains the most important things covered in lectures. Some of the code from labs should also be revised.
See the following code in Assignments 2, 3, 4, 5 and Homework 1 in this repository.


ASCII FUNCTIONS
ord('A') = 65
chr(65) = 'A'

STRINGS
len, lower, upper, strip, replace e.g. string.lower()
sep, end in print e.g. print('cat', end="|")
flush, file in print function
s = "hello"   s[0] = "H"   // error, not possible, use replace()
print(s*5) prints "hello" 5 times

FLOATS
pi = 3.14259
formatting e.g. print(f"{pi:.2f}") = 3.14

LISTS FUNCTIONS
append
remove e.g. list.remove(6) removes by value, not index
pop  removes an element by index and returns the removed element
del  removes an element by index and does not return the removed element
list[start:stop:step] starting index, end index, step e.g. 2 would return every other element starting from the 1st
list = [10, 20, 30, 40, 50]
print(list[1:4]) = 20, 30, 40
print(list[::2]) = 10, 30, 50
print(list[::-1]) = 50, 40, 30, 20, 10

len() is used for strings, lists, tuples, dictionaries and sets

FOR LOOP
for i in range(start:stop:step)
Example
for i in range(1, 6, 1):
    print(i) # 1, 2, 3, 4, 5

If no variable is required, just looping, '_' can be used instead of i
for _ in range(start:stop:step)

INLINE FOR LOOP
result = [i for i in range(5)]  // This method is known as list comprehension
print(result)  // [0, 1, 2, 3, 4]

result = [i for i in range(5) if i % 2 == 0]
print(result)  // [0, 2, 4]

GENERATORS (YIELD)
Yield is a keyword that turns a function into a generator. It allows for lazy evaluation, producing values one at a time.
When a generator function calls yield, it temporarily pauses and saves its state. Subsequent calls to the generator
resume execution from where it left off.

def simple_generator():
    for i in range(5):
        print(f"Generating {i}")
        yield i

gen = simple_generator()
print(next(gen))
print(next(gen))

LAMBDA FUNCTIONS
A lambda function is a small, anonymous function defined with the lambda keyword.
It is often used for short, single-use functions. Syntax: lambda arguments: expression
A typical example of usage of lambda function in sorting lists (provides sorting condition).

# Lambda function that adds 2 numbers
add = lambda x, y: x + y
print(add(3, 4))  # Output: 7

sorted() sorts in ascending order (can be multiple criteria), but you can change this with the reverse argument
lambda is recursive and returns elements on index 1 of the sub-arrays e.g. 5, 2, 7
it can also return 2 data sets, so that sorting is done based on two criteria, see sorted_data2
data = [["apple", 5, "A"], ["cherry", 2, "B"], ["banana", 7, "C"]]
print(data)
sorted_data = sorted(data, key = lambda element: element[1], reverse=True)
sorted_data2 = sorted(data, key = lambda element: (element[1], element[2]))
print(sorted_data_2)

DICTIONARY
dictionary1 = {"key1": value1, "key2": value2}
dictionary2 = dict("key1": value1, "key2": value2)

Convert lists to a dictionary
keys = ["name", "age", "city"]
values = ["Jordan", 33, "Sarajevo"]
dictionary = dict(zip(keys, values))

keys = ["names", "ages", "cities"]
values = [["Jordan", "Pippen", "Rodman"], [33, 34, 35], ["Sarajevo", "Chicago", "Detroit"]]
dictionary = dict(zip(keys, values))

pairs = [("name": "Jordan"), ("age": 33), ("city": "Sarajevo")]
dictionary = dict(zip(pairs)) # zip = merge

List of tuples to dictionary
pairs = [("name", "Jordan"), ("age", 33), ("city", "Sarajevo")] # tuples
dictionary = dict(pairs)

Access dictionary element when you do not know if the key exists and assign default value
pairs = [("name", "Jordan"), ("age", 33), ("city", "Sarajevo")] # tuples
dictionary = dict(pairs)
print(dictionary.get("xyz", "Almir"))

EXCEPTIONS
class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def risky_operation(value):
    if value < 0:
        raise CustomError("Value cannot be negative!")
    return value ** 2

try:
    result = risky_operation(-5)
    print(f"Result: {result}")
except CustomError as e:
    print(f"Caught an error: {e}")

FILE OPERATIONS
File Modes:
- Reading ('r'): Opens a file for reading. If the file doesn’t exist, it raises an error.
- Writing ('w'): Opens a file for writing. If the file exists, it will be overwritten. If not, a new file is created.
- Appending ('a'): Opens a file to add content at the end without deleting existing data.
- Updating ('r+', 'w+', 'a+'): Allows both reading and writing.
File Types:
- Text files ('t' mode, default): Store data as readable text, with each line ending in a newline character (\n). Used for most files that
contain readable characters.
- Binary files ('b' mode): Store data in raw binary format, suitable for non-text data like images, videos, or executable files.
Data is read and written as byte streams.
Examples:
- open('file.txt', 'rt') opens a text file for reading,
- open('file.bin', 'wb') opens a binary file for writing.

file = file.open("fileName.txt", "a")
file.write("text")
file.close()

with open("fileName", "mode") as file
    file.write("text")
    # no need to close

file.read()
line = file.readline()
line.strip() # remove new line characters
file.readlines()

CSV (import csv module)
with open("fileName", "mode") as file
    writer = csv.writer("file")
    writer.writerows("text")

csv.reader("fileName") # iterable
csv.DictReader("fileName") # iterable and returns each row as dictionary

(import pandas as pd)
df = pd.DataFrame(data)
df.to_csv("fileName", index=False) # false for writing in file
df.to_dict("fileName") # DataFrame to dictionary
pandas.read_csv("fileName")

2D CHARTS
import matplotlib.pyplot as plt
import numpy as np

n = np.arrange(1, 101)
x = np.sin(n)
y = np.cos(n)

plt.style.use('dark_background') # only if you want dark background, otherwise white
plt.figure(figsize=(10, 6))
plt.plot(n, x, label='x = sin(n)', color='blue', linestyle='-')
plt.plot(n, y, label='y = cos(n)', color='red', linestyle='--')

# Add labels and title
plt.xlabel('n')
plt.ylabel('Function Values')
plt.title('Plot of x = sin(n) and y = cos(n)')

plt.legend()
plt.grid()
plt.show()

PIE CHART
import matplotlib.pyplot as plt

labels = ['A', 'B', 'C', 'D']
sizes = [15, 30, 45, 10]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

autopct='%1.1f%%': Displays percentages on the pie chart.
The format '%1.1f%%' means one digit before and one digit after the decimal point (e.g., 25.0%)
startangle=90: Rotates the pie chart so the first slice starts at 90 degrees (top of the circle).

SCATTER PLOT
import numpy as np
import matplotlib.pyplot as plt

# Generate 100 random points for x and y
x = np.random.randn(100)
y = np.random.randn(100)

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot points with different colors based on the condition
plt.scatter(x[x > 0], y[x > 0], color='blue', label='x > 0')
plt.scatter(x[x <= 0], y[x <= 0], color='red', label='x ≤ 0')

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot of Random Points with Normal Distribution')
plt.legend()
plt.grid()
plt.show()

Decomposition: Breaking a large problem into smaller, manageable parts.
Abstraction: Hiding the complexity by focusing on high-level steps, not implementation details

FUNCTION DOCS
def someFunction():
    add documentation notes here (use docstrings (triple quotes) like the docstring at the beginning of this file)

read function documentation
print(someFunction.__doc__)
help(someFunction)

GLOBALS
if you want to change a value of the variable that is not instanced in the function
you have to use 'global' before the name of the variable
Use globals only for: configuration constants, shared state across functions and similar stuff that should be global

RACE CONDITION
A race condition occurs when two or more processes or threads access shared resources
simultaneously, and the outcome depends on the timing or order of their execution.
This can lead to unpredictable or incorrect behavior in a program.

NESTED FUNCTIONS
If you have a function defined inside another function (a nested function), the inner function can access
variables from the outer function’s scope.
If you want to modify a variable from the outer function within the inner function, you need to declare that
variable as "nonlocal".
Nested functions can only be invoked from within their parent function.

PASSING PARAMETERS
In Python, all arguments are passed by object reference, which means that the
function receives a reference to the original object, not a copy of the object itself.
However, the behavior can vary depending on the type of the object being passed.
MUTABLE ARGUMENTS:If you pass a mutable object (like a list or a dictionary) to a function and modify it
inside the function, the changes will affect the original object.
IMMUTABLE ARGUMENTS: If you pass an immutable object (like an integer, string, or tuple) and
attempt to modify it, function will create a new local object instead of
modifying the original one. This will not affect the original object.

DEFAULT FUNCTION PARAMETERS
The parameters with default values must be written after the parameters without them.
def someFunction(par1, par2, par3="John")

RECURSIONS
Recursion is a process where a function calls itself to solve smaller instances of a problem.
Use recursions to: simplify code, divide complex problem into smaller ones and simplify algorithms
Be aware that recursions: might cause performance issues, stack overflow, memory consumption
Characteristics of recursions
Base case: The condition that stops recursion (prevents infinite recursion).
Recursive case: The part where the function calls itself with a modified argument, moving toward the base case.

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
print(factorial(5))  // 5 * 4 * 3 * 2

def factorial(n):
    return n * factorial(n - 1) if n > 0 else 1

ITERATION INSTEAD OF RECURSION
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
print(factorial(5))  // 5 * 4 * 3 * 2

MAIN
Checks if the script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()

MODULES
A module is a file containing Python code (functions, variables, classes) that can be imported
and used in other Python scripts.
Modules are used for: modularity, reusability and maintainability

MODULE IMPORT
Imports everything from the module
import moduleName
Imports specific functions, variables, or classes from the module
from moduleName import functionName

COMMON MODULES
File handling
os: Interact with the operating system
shutil: High-level file operations (e.g., copying, moving files)
pathlib: Object-oriented approach to working with file paths

Data handling and processing
csv: Handle CSV (Comma Separated Values) files
json: Parse and create JSON (JavaScript Object Notation) data
pickle: Serialize and deserialize Python objects
sqlite3: Interface with SQLite databases

Math and science
math: Provides basic mathematical functions like sqrt(), pow(), etc.
statistics: Perform statistical calculations (e.g., mean, median)
random: Generate random numbers and perform random operations
numpy: Advanced numerical operations on arrays and matrices

Web Development
requests: HTTP library for sending requests to web servers (e.g., GET, POST)
flask: Lightweight framework for building web applications
django: Full-featured web framework for creating complex web apps
urllib: Module for working with URLs (e.g., fetching data from the web)

Date and Time Handling
datetime: Work with dates, times, and time intervals
time: Functions to manipulate time (e.g., sleep, time stamps)
calendar: Access calendar-related functions and data

System Operations and Utilities
sys: Provides access to system-specific parameters and functions.
subprocess: Run system commands and interact with processes.
argparse: Handle command-line arguments.
logging: Record and log events in your application

Testing and Debugging
unittest: Framework for writing and running tests.
pytest: More advanced testing framework for simple and scalable test cases.
pdb: Python’s built-in debugger for troubleshooting code.

Networking
socket: Provides low-level networking interfaces (e.g., for TCP/UDP connections).
asyncio: Write concurrent code for networking and I/O-bound tasks

Core Machine Learning Libraries
scikit-learn: Classification, regression, clustering, dimensionality reduction
tensorflow: Efficient computation on both CPUs and GPUs
keras: Simplifies building and training deep learning models
pytorch: Deep learning framework known for flexibility and dynamic computation graphs.

OBJECT-ORIENTED PROGRAMMING
A programming paradigm that uses "objects" to structure code, combining data (attributes) and behaviors (methods).
The goal is to simplify complex programs by organizing related data and functions together.
It emphasizes reusability, modularity and flexibility.

PILLARS OF OOP
ENCAPSULATION is the bundling of variables (data) and methods (functions) that operate on the data into a
single unit called an object. Hides internal details and protects data by bundling it with methods that operate on it.
Data ABSTRACTION is the concept of hiding the internal details of an object and exposing only the necessary
functionalities.
INHERITANCE is the process by which one class (subclass) inherits the properties and methods
of another class (superclass).
POLYMORPHISM allows objects to be treated as instances of their parent class, enabling a
single interface to represent different underlying forms (data types).

CLASS EXTENSION
class Person:
    def __init__(self, name, age):
            self._name = name
            self._age = age

    def greet(self):
        return "Hello, " + self._name + "!"

    def __str__(self):
        return f"Person (name={self._name}, age={self._age})"

class Student(Person):
    def __init__(self, name, age, id, school):
        super().__init__(name, age)
        self._id = id
        self._school = school

Example (see student instance below)
Encapsulation: info for the created student is encapsulated in the instance
Abstraction: methods and properties related with Person class are in this class and nowhere else (encapsulated)
Polymorphism: instance of the Student class is of type Student but also Person
Inheritance: method greet is called on the Student instance, but it is actually inherited from the Person class
student = Student("James", 22, 20079, "CWRU")
print(student.greet())  // method greet inherited

ACCESS CONTROL LEVELS (applies to both methods and properties)
Global variables not possible in python classes, only static ones
person = Person("Almir", "Mustafic")
public or static variables
person.name       def getName()

protected
person._name      def _getName()

private
person.__name     def __getName()

METHODS
Static methods might require first parameter to be e.g. cls, which might be used instead of 'self' or 'this'
in some languages. If you do not need to use the 'cls' to refer to sth within the class, you can omit it
@staticmethod - annotation used above static class methods e.g.
@staticmethod
def calculateNumbers(cls)

OVERLOADING
Whenever e.g. '==' is used somewhere in the code, function __eq__ will be called as well
# __eq__ binary ==
# __ne__ binary !=

ENUM (ENUMERATED)
class Colors:
    red = (255, 0, 0)
    green = (0, 255, 0)

    nameToColor = {
    "red": red,
    "green": green
    }

    @staticmethod
    def getColor(color):
        return Colors.nameToColor.get(color)

PROPERTY (SETTER)
Bear in mind that the setter MUST have an annotation and a getter, and they all MUST have the same name.
In addition, setter name is called like e.g. person.name() but person.name due to @property annotation

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def setName(self, name):
        self._name = name

OPERATORS
Two commonly used operators for mathematical operations are @ and *, each serving distinct purposes.
The @ Operator: designed for matrix multiplication and indicates the intention of performing linear algebra operations.
The * Operator: used for element-wise multiplication or other multiplication operations, and it can be
overloaded to provide custom behavior in user-defined classes
"""


# Code examples
# Multiplication table
rows = 11
cols = 10
print(" " * 4, end="") # space before row headers to align it with the table
for j in range(1, cols + 1):
    print(f"{j:4}", end="") # print 4 spaces and then the column title
print("\n " + "-" * (cols * 5)) # separate the table header

for i in range(1, rows):
    print(f"{i:2} |", end="")  # print 2 spaces and then row title
    for j in range(1, cols + 1):
        print(f"{i*j:4}", end="")  # print 4 spaces and then the product of two numbers
    print()


# OOP
class Person:
    def __init__(self, name, age):
            self._name = name
            self._age = age

    def greet(self):
        return "Hello, " + self._name + "!"

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    def __str__(self):
        return f"Person (name={self._name}, age={self._age})"

class Student(Person):
    def __init__(self, name, age, id, school):
        super().__init__(name, age)
        self._id = id
        self._school = school

student = Student("James", 22, 20079, "CWRU")
print(student.greet())
print(student)

result = [i for i in range(5) if i % 2 == 0]
print(result)