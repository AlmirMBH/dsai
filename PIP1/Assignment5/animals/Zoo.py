from Animal import Animal
from Mammal import Mammal
from Bird import Bird

"""
Manages a list of animals and provides the following methods:
a) Operations:
• add_animal(animal: Animal): Adds an animal to the zoo if there is available space in the zoo
(zoo has limited capacity for birds and for mammals).
• remove_animal(animal: Animal): Removes an animal from the zoo.
b) Search and Filter:
• filter_by_type(animal_type: string): Filters and returns a list of animals by type (Mammal or
Bird).
• filter_by_diet(diet: string): Filters mammals by their diet.
• filter_by_age(age: int): Filters animals by their age.
• filter_by_endangered_status(): Filters birds by whether they are endangered.
c) Display:
• display_all_animals(): Displays all animals currently in the zoo.
• zoo_summary(): Displays the total number of animals, their types, and details of all animals
in the zoo.
d) File Operations:
• save_to_file(filename: string): Saves all animals to a simple text file.
• load_from_file(filename: string): Loads animals from a saved text file.
"""

class Zoo:
    def __init__(self, mammal_capacity=5, bird_capacity=5):
        self.mammals = []
        self.birds = []
        self.mammal_capacity = mammal_capacity
        self.bird_capacity = bird_capacity

    def add_animal(self, animal: Animal):
        if isinstance(animal, Mammal) and len(self.mammals) < self.mammal_capacity:
            self.mammals.append(animal)
        elif isinstance(animal, Bird) and len(self.birds) < self.bird_capacity:
            self.birds.append(animal)
        else:
            print("No space available for this animal.")


    def remove_animal(self, animal: Animal):
        if isinstance(animal, Mammal):
            if animal in self.mammals:
                self.mammals.remove(animal)
            else:
                print("Mammal not found in the zoo.")
        elif isinstance(animal, Bird):
            if animal in self.birds:
                self.birds.remove(animal)
            else:
                print("Bird not found in the zoo.")


    def filter_by_type(self, animal_type: str):
        if animal_type.lower() == "mammal":
            return self.mammals
        elif animal_type.lower() == "bird":
            return self.birds
        return []


    def filter_by_diet(self, diet: str):
        result = []
        for mammal in self.mammals:
            if mammal.diet.lower() == diet.lower():
                result.append(mammal)
        return result


    def filter_by_age(self, age: int):
        result = []
        for animal in self.mammals + self.birds:
            if animal.age == age:
                result.append(animal)
        return result


    def filter_by_endangered_status(self, wing_span_threshold: int):
        result = []
        for bird in self.birds:
            if bird.is_endangered(wing_span_threshold):
                result.append(bird)
        return result


    def display_all_animals(self, filename: str):
        print("\nAll Animals in the Zoo:")
        try:
            with open(filename, "r") as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("No animals found in the zoo file.")


    def zoo_summary(self, filename: str):
        total_animals = 0
        mammals = 0
        birds = 0

        try:
            with open(filename, "r") as file:
                for line in file:
                    total_animals += 1
                    if line.startswith("Mammal:"):
                        mammals += 1
                    elif line.startswith("Bird:"):
                        birds += 1
        except FileNotFoundError:
            print("No animals found in the zoo file.")
            return

        print("\nZoo Summary:"
              + "\nTotal Animals: " + str(total_animals)
              + "\nMammals: " + str(mammals)
              + "\nBirds: " + str(birds)
              +"\nDetails:")
        self.display_all_animals(filename)


    def save_to_file(self, filename: str):
        with open(filename, "a") as file:
            for mammal in self.mammals:
                file.write(
                    "Mammal: " + str(mammal.name) + ", "
                    + str(mammal.species) + ", "
                    + str(mammal.age) + ", "
                    + str(mammal.has_fur) + ", "
                    + str(mammal.diet) + ", "
                    + str(mammal.average_lifespan) + "\n")
            for bird in self.birds:
                file.write("Bird: " + str(bird.name) + ", "
                           + str(bird.species) + ", "
                           + str(bird.age) + ", "
                           + str(bird.wing_span) + ", "
                           + str(bird.can_fly) + "\n")
        print("Animals saved to " + str(filename) + ".")


    def load_from_file(self, filename: str):
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(", ")
                    if parts[0] == "Mammal":
                        name, species, age, has_fur, diet, lifespan = parts[1:]
                        self.add_animal(Mammal(name, species, int(age), bool(int(has_fur)), diet, int(lifespan)))
                    elif parts[0] == "Bird":
                        name, species, age, wingspan, can_fly = parts[1:]
                        self.add_animal(Bird(name, species, int(age), float(wingspan), bool(int(can_fly))))
            print("Animals loaded from " + str(filename) + ".")
            for animal in self.mammals + self.birds:
                print(animal.name)

        except FileNotFoundError:
            print("File " + str(filename) + " not found.")