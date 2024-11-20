from Animal import Animal

"""
Mammal (inherits from Animal):
Additional Attributes:
• has_fur (boolean): Indicates whether the mammal has fur.
• diet (string): The diet of the mammal (e.g., "Carnivore", "Herbivore", "Omnivore").
• average_lifespan (integer): The average lifespan of the mammal in years.
Additional Methods:
• years_left_to_live(current_year: int): Calculates and returns the estimated years left for the
mammal to live based on its average lifespan and current age.
• __str__(): Returns a string representation of a mammal.
"""

class Mammal(Animal):
    def __init__(self, name, species, age, has_fur, diet, average_lifespan):
        super().__init__(name, species, age)
        self.has_fur = has_fur
        self.diet = diet
        self.average_lifespan = average_lifespan


    def years_left_to_live(self):
        return self.average_lifespan - self.age


    def __str__(self):
        fur_status = "Has fur" if self.has_fur else "No fur"
        return (str(self.name)
                + " (" + str(self.species) +"), "
                + fur_status
                + ", Diet: " + str(self.diet)
                + ", Age: " + str(self.age) + " years")