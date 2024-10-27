# Ascii conversion and length (strings immutable)
# The len is used for strings, lists, dictionaries, tuples, sets, bytes, bytearrays, arrays
print(ord("d"))
print(len("d"))

# Dictionary
print(len({"a":1, "b":2}))
print("a", "b", sep=", ", end="\n")

# Formatting
pi = 3.14159
print(f"My number is {pi:.2f}")

# List (mutable collection of objects)
list1 = [1, 2, 3, 4]
list1.append(5)
list1[1] = 8
# Changing list by elements value
list1.remove(8)

# Changing list by elements index
list1.pop(0)
del list1[1]

print(list1)

# List slicing
list2 = [100, 200, 300, 400, 500]
list2 = list2[::2]
list3 = list2[::-1]
print(list2)
print(list3)
# flush, file
# python 2 and 3 are not compatible