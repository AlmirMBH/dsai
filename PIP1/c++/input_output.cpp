#include <iostream>
#include <string>

int main() {
// TAKE INPUT
     int age;
     std::cout << "Enter your age: ";
     std::cin >> age; // Reads input from the user
     std::cout << "You are " << age << " years old.";

// IF-statement
     int score;
     std::cout << "Enter your score: ";
     std::cin >> score;
     if (score >= 90) {
         std::cout << "Grade: A" << std::endl;
     } else if (score >= 75) {
         std::cout << "Grade: B" << std::endl;
     } else {
         std::cout << "Grade: C" << std::endl;
     }

     return 0;
 }