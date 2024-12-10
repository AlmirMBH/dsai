import pandas as pd

# Unlike csv library, pandas library requires the data to be stored in a dictionary, where the keys represent
# names of the columns, while values are lists that represent column data.
people={"Name":["Alice", "Bob", "Charlie"], "Age":[21, 22, 20]}

dataFrame = pd.DataFrame(people)
dataFrame.to_csv("people.csv", index=False)

dataFrame = pd.read_csv("people.csv")
people=dataFrame
print(people)