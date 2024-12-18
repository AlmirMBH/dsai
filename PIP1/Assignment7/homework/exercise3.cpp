#include <iostream>

using namespace std;
/**
Write a C++ program that calculates the n-th Fibonacci number without using recursion.
The Fibonacci sequence is defined as follows:
- F(0) = 0
- F(1) = 1
- For n ≥ 2 F(n) = F(n-1) + F(n-2)
The program should:
- Accept an "integer n" as input from the user.
- Calculate and print the n-th Fibonacci number using an iterative approach (not recursion).
- Also, program should print all Fibonacci numbers which are smaller than n-th Fibonacci number.
*/

// e.g. 0 1 1 2 3 5 8 13
void fibonacci() {
    int n;
    cout << "Enter an integer n: ";
    cin >> n;

    if (n == 0) {
        cout << "F(0) = 0" << endl;
        return;
    }


    int prev = 0, curr = 1;
    cout << "Fibonacci numbers smaller than the input number F(" << n << "): " << prev << " ";

    while (curr < n) {
        cout << curr << " ";
        int next = prev + curr;
        prev = curr;
        curr = next;
    }
    cout << endl;
    cout << "F(" << n << ") = " << curr + prev << endl;
}


int main() {
    fibonacci();
    return 0;
}