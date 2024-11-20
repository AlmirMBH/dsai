"""
Attributes:
• name (string): The name of the animal.
• species (string): The species of the animal.
• age (integer): The age of the animal.
Methods:
Age: {age}".
• __str__(): Returns a string representation of the animal in the format "{name} ({species}),
"""

class Animal:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def age_info(self):
        return "Age: " + str(self.age)

    def __str__(self):
        return str(self.name) + " (" + str(self.species)+ ")"