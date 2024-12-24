#include <iostream>
#include <string>


class Animal {
    protected:
        std::string name;

    public:
        Animal(std::string animalName) : name(animalName) {}

    virtual void speak() const {
        std::cout << "Some generic animal sound" << std::endl;
    }

    virtual ~Animal() = default;
};


class Cat : public Animal {
    public:
        Cat(std::string catName) : Animal(catName) {}

    void speak() const override {
        std::cout << name << " says Meow!" << std::endl;
    }

    // void ignore() const {
    // the "const" is kind of a promise
    // to the compiler that the method is read-only
    // it does not allow object to be modified
    void ignore() {
        std::cout << name << " is ignoring you." << std::endl;
    }
};


int main() {
    Animal* someAnimal = new Animal("GenericAnimal");
    someAnimal->speak();

    Cat* cat = new Cat("Tom");
    cat->speak();
    cat->ignore();

    // Destroy the used objects
    delete someAnimal;
    delete cat;
    return 0;
}
