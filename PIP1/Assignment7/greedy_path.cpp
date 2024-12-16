#include <iostream>
#include <vector>
#include <stdlib>
#include <ctime>

using namespace std;

// Function to print the matrix
void printMatrix(const vector<vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int val : row) {
            cout << val << "\t";
        }
        cout << endl;
    }
}

// Greedy pathfinding algorithm from bottom-left to top-right
void greedyPathfinding(const vector<vector<int>>& matrix) {
    int rows = matrix.size();
    int cols = matrix[0].size();

    // Start from bottom-left corner
    int row = rows - 1;
    int col = 0;

    // Variables to track the path
    vector<pair<int, int>> path;
    int totalCost = 0;

    // Greedy pathfinding
    while (row > 0 || col < cols - 1) {
        path.push_back({row, col});
        totalCost += matrix[row][col];

        // Decide whether to move up or right based on maximum cost
        if (row > 0 && (col == cols - 1 || matrix[row - 1][col] > matrix[row][col + 1])) {
            // Move up
            row--;
        } else if (col < cols - 1) {
            // Move right
            col++;
        }
    }

    // Add the top-right corner to the path
    path.push_back({0, cols - 1});
    totalCost += matrix[0][cols - 1];

    // Print the path and the total cost
    cout << "Path taken (from bottom-left to top-right):" << endl;
    for (const auto& p : path) {
        cout << "(" << p.first << ", " << p.second << ") -> ";
    }
    cout << "End" << endl;
    cout << "Total cost of the path: " << totalCost << endl;
}

int main() {
    srand(time(0)); // Seed for random number generation

    int rows = 5;
    int cols = 5;

    // Create a random matrix (for example, 5x5)
    vector<vector<int>> matrix(rows, vector<int>(cols));

    // Fill matrix with random values between 1 and 10
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = rand() % 10 + 1;
        }
    }

    // Print the matrix
    cout << "Generated matrix:" << endl;
    printMatrix(matrix);

    // Run the greedy pathfinding algorithm
    greedyPathfinding(matrix);

    return 0;
}
