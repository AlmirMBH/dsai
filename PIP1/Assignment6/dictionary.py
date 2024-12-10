#Method 1
person1 = {"Name": "Alice", "Age": 20}
print(person1)  # {'Name': 'Alice', 'Age': 20}

#Method 2
person2 = dict(Name="Bob", Age=21)
print(person2)  # {'Name': 'Bob', 'Age': 21}

keys = ["Name", "Age"]
values = ["Alice", "20", "Address"]
dct = dict(zip(keys, values))
print(dct)  # {'Name': 'Alice', 'Age': '20'}

person={"Name": "Alice", "Age": 20}
#Method 1
print(person["Name"])
#Method 2
print(person.get("Name"))  # getter