#include <iostream>
using namespace std;

// References
// A reference in C++ is an alias for an existing variable, which means it does not create a new
// variable. It acts as another name for the same memory location. When you create a reference
// to a variable, you are essentially creating a second way to access and manipulate the same value
// stored in memory.
// A reference must be initialized at the time of
// declaration, and once it is initialized, it cannot be changed to refer to another variable.
// References are commonly used in functions to avoid copying data or to modify the original variable.

void increment(int &a) { // Pass by reference
    a++; // Modifies the original variable
    cout << "Inside function: " << a << endl;
}

int main() {
    int x = 10; // Original variable
    int &ref = x; // Reference to x
    // Modifying the reference affects the original variable
    ref += 5;
    cout << "After modifying ref:" << endl;
    cout << "Value of x: " << x << endl; // Outputs 15
    cout << "Value of ref: " << ref << endl; // Outputs 15
    // Modify the original variable directly
    x -= 3;
    cout << "\nAfter modifying x directly:" << endl;
    cout << "Value of x: " << x << endl; // Outputs 12
    cout << "Value of ref: " << ref << endl; // Outputs 12

    // Another example
    int num = 5;
    increment(num);
    cout << "Outside function: " << num << endl; // Original is changed

    return 0;
}