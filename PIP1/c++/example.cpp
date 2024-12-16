#include <iostream>
#include <vector>

using namespace std;

// Commands to install C++ and compile the code
// pip install pybind11
// g++ -shared -fPIC -o example.so example.cpp
// g++ -shared -fPIC -std=c++11 -o example.so example.cpp

// Function overloading I
double area(double side) {
    return side * side;
}

double area(double length, double width) {
    return length * width;
}

// Function overloading II (templates to avoid specifying int and float)
template <typename T>
T surface(T length, T width) {
    return length * width;
}

// The compiler determines the correct return type based on the operation in decltype
template <typename T1, typename T2>
auto calculateArea(T1 length, T2 width) -> decltype(length * width)
{
    return length * width;
}


extern "C" {
    int add(int a, int b) {
        return a + b;
    }

    float divide(float a, float b) {
        return a / b;
    }

    void printNumbers(int n) {
        for (int i = 1; i <= n; ++i) {
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }

    // Loops
    void printVector() {
        std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8};
        for (auto num : numbers) {  // 'auto' deduces the type of 'num' as int
            std::cout << num << " ";
        }
        std::cout << std::endl;
    }

    void printWhile(int n) {
        int i = 0;
        while (i < n) {
            std::cout << "Value: " << i++ << std::endl;
        }
    }

    void printDoWhile(int n) {
        int i = 0; // `i` should be declared outside the loop
        do {
            std::cout << "Value: " << i++ << std::endl;
        } while (i < n);
    }

    // Pass by reference
    void printValue(int num) {
        std::cout << "Initial value: " << num << std::endl;
    }

    void modifyValue(int& num) { // Modify be reference
        num += 5;
        std::cout << "Modified value: " << num << std::endl;
    }

    void passByReference(int num) {
        printValue(num);
        modifyValue(num);
        printValue(num);
    }

    // Constants and pass by reference
    const int CONSTANT_VALUE = 10;
    const int CONSTANT_VALUE_TWO = 15;

    void printConstant() {
        std::cout << "Constant values: " << CONSTANT_VALUE << " " << CONSTANT_VALUE_TWO << std::endl;
    }

    void printMessage(const std::string& message) {
        std::cout << message << std::endl;
    }

    void message() {
        std::string message = "Hello, world!";
        printMessage(message); // Passing by constant reference
    }

    // Function overloading (functions must be declared above and they cannot be in the "extern C" - the same name)
    void functionOverloading() {
        std::cout << "Area of square: " << area(5) << std::endl;
        std::cout << "Area of rectangle: " << area(5.0, 10.0) << std::endl;
    }

    void functionTemplateOverloading() { // Uses function templates
        std::cout << "Area of square: " << surface(5, 5) << std::endl;
        std::cout << "Area of rectangle: " << surface(5.0, 10.0) << std::endl;
    }

    void calculateArea() {
        std::cout << "Area of square: " << calculateArea(5, 5) << std::endl;
        std::cout << "Area of rectangle: " << calculateArea(5.0, 10.2) << std::endl;
    }

    void declarations() {
        int a = 5;
        float b = 12.5;
        auto x = a; // variable declaration with type and assignment int x = 5
        decltype(b) y = 0.0f; // variable declaration with type and without the assignment float y = 0

        std::cout << "First: " << x << std::endl;
        std::cout << "Second: " << y << std::endl;
    }
}
