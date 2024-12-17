#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<int> nums = {10, 20, 30, 40, 50};
    nums.push_back(60); // add to the last place
    nums.push_back(70);

    for (int num : nums) {
        std::cout << num << " ";
    }

    // The above range-based loop is the same as the for below
    for (int i = 0; i < nums.size(); i++) {
        std::cout << nums.at(i) << " ";
    }

    std::cout << "Element at position 2 is " << nums.at(2) << std::endl;
    std::cout << "Size of the vector " << nums.size() << std::endl;

    return 0;
 }