from Zoo import Zoo
from Mammal import Mammal
from Bird import Bird

zoo = Zoo(mammal_capacity=5, bird_capacity=5)
mammal1 = Mammal("Lion", "Big Lion", 4, True, "Carnivore", 20)
mammal2 = Mammal("Lion", "Small Lion", 3, True, "Carnivore", 20)
mammal3 = Mammal("Tiger", "Big Tiger", 5, True, "Carnivore", 20)
mammal4 = Mammal("Tiger", "Small Tiger", 1, True, "Carnivore", 20)
mammal5 = Mammal("Wolf", "Big Wolf", 7, True, "Carnivore", 25)
mammal6 = Mammal("Wolf", "Small Wolf", 2, True, "Carnivore", 25)

bird1 = Bird("Hawk", "Fast Hawk", 2, 2.5, True)
bird2 = Bird("Hawk", "Slow Hawk", 3, 2.7, True)
bird3 = Bird("Hawk", "Big Hawk", 7, 2.8, True)
bird4 = Bird("Hawk", "Small Hawk", 1, 2.4, True)
bird5 = Bird("Ostrich", "Fast Hawk", 2, 2.5, True)

mammals = [mammal1, mammal2, mammal3, mammal4, mammal5, mammal6]
birds = [bird1, bird2, bird3, bird4, bird5]

for mammal in mammals:
    zoo.add_animal(mammal)

for bird in birds:
    zoo.add_animal(bird)

zoo.save_to_file("zoo.txt")
zoo.load_from_file("zoo.txt")
zoo.zoo_summary("zoo.txt")

print("\nFilter by age")
animals_by_age = zoo.filter_by_age(3)
for animal in animals_by_age:
    print(animal.name + ", age: " + str(animal.age))