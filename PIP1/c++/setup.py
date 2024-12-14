import ctypes

example = ctypes.CDLL('./example.so')
print(example.add(3, 5))  # Output: 8

example.divide.restype = ctypes.c_float  # Specify the return type
example.divide.argtypes = [ctypes.c_float, ctypes.c_float]  # Specify the argument types
print(example.divide(4.0, 2.0))  # Output: 2.0

print("\nFor loop")
# Set argument types
example.printNumbers.argtypes = [ctypes.c_int]
example.printNumbers(5)  # Output: 1 2 3 4 5

print("\nFor loop with type auto-detection")
example.printVector()

print("\nWhile")
example.printWhile(5)

print("\nDo-While")
example.printDoWhile(5)

print("\nPass by reference")
example.passByReference(10)

print("\nConstants")
example.printConstant()
example.message()

print("\nFunction overloading")
example.functionOverloading()
example.functionTemplateOverloading()
example.calculateArea()

print("\nVariable declarations via existing types")
example.declarations()
