#include <iostream>
#include <string> // Library required for std::string
#include <vector>

int main() {
// Collections
// Vectors (dynamic memory management i.e. can be resized dynamically)
    std::vector<int> nums = {10, 20, 30, 40, 50};
    nums.push_back(60); // add to the last place
    nums.push_back(70);

    for (int i = 0; i < nums.size(); i++) {
        std::cout << "Element at index " << i << ": " << nums[i] << std::endl;
    }

    std::cout << "Element at position 2 is " << nums.at(2) << std::endl;
    std::cout << "Size of the vector " << nums.size() << std::endl;

    // Take user input
    std::vector<int> numbers;
    int n, input;
    std::cout << "Enter the number of elements: ";
    std::cin >> n;
    std::cout << "Enter " << n << " numbers: "; // Input elements from the user

    for (int i = 0; i < n; i++) {
        std::cin >> input;
        numbers.push_back(input);
    }

    std::cout << "You entered: ";

    for (int num : numbers) {
        std::cout << num << " ";
    }

    std::cout << std::endl;

    return 0;
 }