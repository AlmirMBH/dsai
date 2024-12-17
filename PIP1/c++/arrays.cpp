#include <iostream>
#include <string>

int main() {
// Collections
// Arrays (static, fixed in size, elemnts of the same type)
    int nums[5] = {10, 20, 30, 40, 50};

    for (int i = 0; i < 5; i++) {
        std::cout << "Element at index " << i << ": " << nums[i] << std::endl;
    }

    // Take user input
    int integers[5];
    std::cout << "Enter 5 numbers: " << std::endl;
    for (int i = 0; i < 5; i++) {
        std::cin >> integers[i];
    }
    std::cout << "You entered: ";

    for (int i = 0; i < 5; i++) {
        std::cout << integers[i] << " ";
    }

    std::cout << std::endl;

    return 0;
 }