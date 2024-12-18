#include <iostream>
#include <vector>
#include <limits>

/**
* Write a C++ program that allows the user to input a matrix of integers. The program should then:
- Compute the sum of all elements in the matrix.
- Find the largest element in the matrix.
- Transpose the matrix (swap rows and columns) and print the transposed matrix.
- Prints a new matrix where each element at a given position is the sum of the
  corresponding element in the original matrix and twice the element at the same
  position in the transposed matrix.
Important note: You should define functions for all of these subtasks
*/


std::vector<std::vector<int>> createMatrix(int rows, int cols) {
    // inner vector must be specified, rows inferred in the constructor (zeros)
    std::vector<std::vector<int>> matrix(rows, std::vector<int>(cols));
    std::cout << "Enter the elements of the matrix:\n";
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cin >> matrix[i][j];
        }
    }
    return matrix;
}


int sum(const std::vector<std::vector<int>>& matrix) {
    int sum = 0;
    for (const auto& row : matrix) { // auto recognize type
        for (int val : row) {
            sum += val;
        }
    }
    return sum;
}

int largestElement(const std::vector<std::vector<int>>& matrix) {
    int largest = std::numeric_limits<int>::min(); // initialize to the min int value
    for (const auto& row : matrix) { // auto recognize type
        for (int val : row) {
            if (val > largest) {
                largest = val;
            }
        }
    }
    return largest;
}


std::vector<std::vector<int>> transposeMatrix(const std::vector<std::vector<int>>& matrix) {
    int rows = matrix.size(), cols = matrix[0].size();
    std::vector<std::vector<int>> transposed(cols, std::vector<int>(rows)); // swap
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            transposed[j][i] = matrix[i][j];
        }
    }
    return transposed;
}


std::vector<std::vector<int>> createNewMatrix(const std::vector<std::vector<int>>& original, const std::vector<std::vector<int>>& transposed) {
    int rows = original.size(), cols = original[0].size();
    std::vector<std::vector<int>> newMatrix(rows, std::vector<int>(cols));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            newMatrix[i][j] = original[i][j] + 2 * transposed[i][j]; // 1o + 2t
        }
    }
    return newMatrix;
}

void printMatrix(const std::vector<std::vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int val : row) {
            std::cout << val << " ";
        }
        std::cout << "\n";
    }
}

int main() {
    int rows, cols;
    std::cout << "Enter the number of rows and columns: ";
    std::cin >> rows >> cols;
    auto matrix = createMatrix(rows, cols);
    auto transposed = transposeMatrix(matrix);
    auto newMatrix = createNewMatrix(matrix, transposed);
    std::cout << "Sum of matrix elements: " << sum(matrix) << "\n";
    std::cout << "Largest matrix element: " << largestElement(matrix) << "\n";
    std::cout << "Transposed matrix:\n";
    printMatrix(transposed);
    std::cout << "New matrix:\n";
    printMatrix(newMatrix);

    return 0;
}
