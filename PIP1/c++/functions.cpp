#include <iostream>
using namespace std;

// Functions
// If the function definition appears after the function call, a
// declaration (also known as a prototype) must be provided before the function call.
    int add(int a, int b);

    int main() {
        int x = 5, y = 10;
        int sum = add(x, y);
        cout << "Sum: " << sum << endl;
        return 0;
    }

    // Function definition
    int add(int a, int b) {
        return a + b;
    }