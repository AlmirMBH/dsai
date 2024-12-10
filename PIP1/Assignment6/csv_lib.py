import csv

people=[["Name", "Age"], ["Alice", 21], ["Bob", 22], ["Charlie", 20]]

#mulitrow write
with open("people.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(people)

#singlerow write
with open("people.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    for row in people:
        writer.writerow(row)

# read from csv
with open("people.csv", mode="r", newline="") as file:
    reader=csv.reader(file)

    for row in reader:
        print(row)