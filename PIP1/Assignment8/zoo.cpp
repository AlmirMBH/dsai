#include <iostream>
#include <string>
#include <sstream>
#include <vector>


/**
 * Animal
 * Attributes:
 *   - name (string): The name of the animal.
 *   - species (string): The species of the animal.
 *   - age (integer): The age of the animal.
 * Methods:
 *   - string to_string() : Returns a string representation of the animal in the format: {name} ({species}), Age: {age}.
 *   - void display() : Displays the animal's details
*/
class Animal {
    protected:
        std::string name;
        std::string species;
        int age;

    public:
        Animal(std::string name, std::string species, int age)
//            : name(name), species(species), age(age) // Shorter way to assign values
            {
                this->name = name;
                this->species = species;
                this->age = age;
            }

    virtual std::string to_string()  {
        return name + " (" + species + "), Age: " + std::to_string(age);
    }

    virtual void display()  {
        std::cout << to_string() << std::endl;
    }

    virtual ~Animal() = default;
};


/**
 * Mammal (inherits from Animal)
 * Additional attributes:
 * - has_fur (boolean): Indicates whether the mammal has fur.
 * - diet (string): The diet of the mammal (e.g., "Carnivore", "Herbivore", "Omnivore").
 * - average_lifespan (integer): The average lifespan of the mammal in years.
 * Additional methods:
 * - int years_left_to_live(int current_year) : Calculates and returns the
 *   estimated years left for the mammal to live based on its average lifespan and current age.
 * - string to_string()  override: Returns a string representation of a mammal,
 *   including has_fur, diet, and average_lifespan.
 * - void display()  override: Displays the mammal’s details.
 */
class Mammal : public Animal {
    private:
        bool has_fur;
        std::string diet;
        int average_lifespan;

    public:
        Mammal(std::string name, std::string species, int age, bool has_fur, std::string diet, int average_lifespan)
            : Animal(name, species, age)
            {
                this->has_fur = has_fur;
                this->diet = diet;
                this->average_lifespan = average_lifespan;
            }


    int years_left_to_live()  { // we do not need the current year here
        int years_left = average_lifespan - age;
        return (years_left > 0) ? years_left : 0;
    }

    public:
        std::string get_diet() {
            return diet;
        }

    std::string to_string()  override {
        return Animal::to_string() + ", Fur: " + (has_fur ? "Yes" : "No") + ", Diet: " + diet + ", Average Lifespan: " + std::to_string(average_lifespan);
    }

    void display()  override {
        std::cout << to_string() << std::endl;
    }
};

/**
 * Bird (inherits from Animal)
 * Additional attributes:
 * - wing_span (float): The wingspan of the bird in meters.
 * - can_fly (boolean): Indicates whether the bird can fly.
 * Additional methods:
 * - bool is_endangered(float wing_span_threshold) : Returns true if the bird species is endangered, based on a wingspan threshold
 *   (species with a wingspan below the threshold are endangered).
 * - string to_string()  override: Returns a string representation of a bird, including wing_span and can_fly.
 * - void display()  override: Displays the bird’s details
 */
class Bird : public Animal {
    private:
        float wing_span;
        bool can_fly;

    public:
        Bird(std::string name, std::string species, int age, float wing_span, bool can_fly)
        : Animal(name, species, age)
        {
            this->wing_span = wing_span;
            this->can_fly = can_fly;
        }


    bool is_endangered(float wing_span_threshold)  {
        return wing_span < wing_span_threshold;
    }

    std::string to_string() override {
        return Animal::to_string() + ", Wingspan: " + std::to_string(wing_span) + "m, Can fly: " + (can_fly ? "Yes" : "No");
    }

    void display() override {
        std::cout << to_string() << std::endl;
    }
};

/**
 * Zoo Class:
 * Manages a collection of animals (both Mammal and Bird) and provides the following methods:
 * a) Operations:
 *    - void add_animal(Animal* animal): Adds an animal to the zoo if there is available space (assuming the zoo has limited capacity).
 * b) Search and Filter:
 *    - vector<Animal*> filter_by_diet(string diet): Filters mammals by their diet (e.g., "Carnivore", "Herbivore").
 *    - vector<Animal*> filter_by_age(int age): Filters animals by their age.
 * c) Display:
 *    - void display_all_animals(): Displays all animals currently in the zoo.
 *    - void zoo_summary(): Displays the total number of animals and remaining capacity.
 */
class Zoo {
    private:
        std::vector<Animal*> animals;
        int capacity;

    public:
        Zoo(int capacity) : capacity(capacity) {}

        void add_animal(Animal* animal) {
            if (animals.size() < capacity) {
                animals.push_back(animal);
            } else {
                std::cout << "No space for new animals!" << std::endl;
            }
        }


        std::vector<Animal*> filter_by_diet(std::string diet) {
            std::vector<Animal*> filtered_animals;
            for (Animal* animal : animals) {
                if (Mammal* mammal = dynamic_cast<Mammal*>(animal)) {
                    if (mammal->get_diet() == diet) {
                        filtered_animals.push_back(animal);
                    }
                }
            }
            return filtered_animals;
        }


        std::vector<Animal*> filter_by_age(int age) {
            std::vector<Animal*> filtered_animals;
            for (Animal* animal : animals) {
                if (animal->to_string().find(std::to_string(age)) != std::string::npos) {
                    filtered_animals.push_back(animal);
                }
            }
            return filtered_animals;
        }

        void display_all_animals() {
            for (Animal* animal : animals) {
                animal->display();
            }
        }

        void zoo_summary() {
            std::cout << "Total number of animals: " << animals.size() << std::endl;
            std::cout << "Remaining zoo capacity (space): " << capacity - animals.size() << std::endl;
        }
};

// Test all the classes and functionalities
int main() {
    Animal animal("Lion", "Cat", 5);
    animal.display();
    std::cout << std::endl;

    Mammal mammal("Tiger", "Cat", 4, true, "Carnivore", 15);
    mammal.display();
    std::cout << "Years left for " << mammal.to_string() << ": " << mammal.years_left_to_live() << std::endl;

    Bird bird("Eagle", "Bird", 3, 2.3, true);
    bird.display();
    float wing_span_threshold = 2.0;
    std::cout << "Is the " << bird.to_string() << " endangered? "
              << (bird.is_endangered(wing_span_threshold) ? "Yes" : "No") << std::endl;
    std::cout << std::endl;

    Zoo zoo(5);
    zoo.add_animal(&animal);
    zoo.add_animal(&mammal);
    zoo.add_animal(&bird);
    std::cout << "Animals in the zoo:" << std::endl;
    zoo.display_all_animals();
    std::cout << std::endl;
    zoo.zoo_summary();
    std::cout << std::endl;

    // By diet
    std::string diet = "Carnivore";
    std::vector<Animal*> filtered_by_diet = zoo.filter_by_diet(diet);
    std::cout << "Filtered by diet (" << diet << "):" << std::endl;
    for (Animal* animal : filtered_by_diet) {
        animal->display();
    }
    std::cout << std::endl;

    // By age
    int age = 3;
    std::vector<Animal*> filtered_by_age = zoo.filter_by_age(age);
    std::cout << "Filtered by age (" << age << "):" << std::endl;
    for (Animal* animal : filtered_by_age) {
        animal->display();
    }

    return 0;
}
