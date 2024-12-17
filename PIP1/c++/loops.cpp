#include <iostream>
#include <string>

int main() {
// For Loop
     for (int i = 1; i <= 5; i++) {
         std::cout << "Iteration " << i << std::endl;
     }

// While Loop
     int i = 1;
     while (i <= 5) {
         std::cout << "Iteration " << i << std::endl;
         i++;
     }

// Do-While Loop
     int j = 6;
     do {
         std::cout << "Iteration " << j << std::endl;
         j--;
     } while (j <= 5 and i > 0);

     return 0;
 }