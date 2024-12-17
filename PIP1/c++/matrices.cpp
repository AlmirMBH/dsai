#include <iostream>
#include <string> // Library required for std::string
#include <vector>

int main() {
// Matrices (vector of vectors i.e. each vector is a row)
  std::vector<std::vector<int>> matrix1 = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9, 5}
    };

    for (int i = 0; i < matrix1.size(); i++) {
        for (int j = 0; j < matrix1.at(i).size(); j++) {
            std::cout << matrix1.at(i).at(j) << " ";
        }
        std::cout << std::endl;
    }

    // Initialize matrix with same numbers
    int m_rows = 3, m_cols = 3;
    std::vector<std::vector<int>> matrix2(m_rows, std::vector<int>(m_cols, 7));
    for (std::vector<int> row : matrix2) {
        for (int val : row) {
            std::cout << val << " ";
        }
    std::cout << std::endl;
    }



    // Take user input
    int rows, cols;
    std::cout << "Enter the number of rows and columns: ";
    std::cin >> rows >> cols;
    std::vector<std::vector<int>> matrix(rows, std::vector<int>(cols)); // Declare a 2D vector (matrix)
    std::cout << "Enter elements of the matrix: " << std::endl; // Input elements for the matrix
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            std::cin >> matrix.at(i).at(j);
        }
    }

    std::cout << "You entered: " << std::endl;
    for (std::vector<int> row : matrix) {
        for (int val : row) {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }

    return 0;
 }