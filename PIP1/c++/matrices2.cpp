#include <iostream>
#include <vector>

using namespace std;

// Matrices
// Why Use References Here?
// Efficiency: Avoids copying rows and elements from the matrix, which could be expensive for larger matrices.
// Read-Only Guarantee: The use of const ensures that the data in the matrix is not accidentally modified while printing.

int main() {
    int rows, cols;
    // Take the size of the matrix from the user
    std::cout << "Enter the number of rows and columns: ";
    std::cin >> rows >> cols;
    std::vector<std::vector<int>> matrix(rows, std::vector<int>(cols)); // Declare a 2D vector (matrix)
    // Input elements for the matrix
    std::cout << "Enter elements of the matrix: " << std::endl;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            std::cin >> matrix[i][j];
        }
    }
    // Print the matrix using references
    std::cout << "You entered: " << std::endl;
    // Reference to each row
    for (const vector<int> &row : matrix) {
    { // Reference to each value in the row
        for (const int &val : row)
            std::cout << val << " ";
        }
    std::cout << std::endl;
    }

    // Using key word 'auto'
    std::cout << "You entered: " << std::endl;
    for (const auto &row : matrix) { // Auto deduces vector<int>, also it is read-only because of const
        for (const auto &val : row) { // Auto deduces int
            std::cout << val << " ";
        }
    std::cout << std::endl;
    }

    return 0;
}