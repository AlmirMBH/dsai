#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
/**
Write a C++ program that performs advanced matrix operations and simulates a two-phase pathfinding algorithm.
The program should:
1) Input Matrix Dimensions: Accept the number of rows and columns from the user.
2) Populate the Matrix: Allow the user to fill the matrix with integers representing terrain costs.
3) Find the Maximum and Minimum Terrain Costs: Calculate and print the maximum and minimum values in the matrix.
4) Pathfinding Simulation
Simulate a two-phase pathfinding algorithm in the matrix:
Phase 1: From Bottom-Left to Midpoint
- Start at the bottom-left corner (rows-1, 0) of the matrix.
- Move up or right at each step, choosing the cell with the minimum cost.
- Stop once you reach the midpoint of the top row (0, cols/2).
Phase 2: From Midpoint to Bottom-Right
- Continue from the midpoint (0, cols/2).
- Move down or right at each step, choosing the cell with the minimum cost.
- Stop once you reach the bottom-right corner (rows-1, cols-1).
5) Print the sequence of cells visited in the entire path (basically print the path taken).
6) Calculate and display the total cost of the path.
*/

pair<int, int> getUserMatrix() {
    int rows, cols;
    cout << "Enter the number of rows: ";
    cin >> rows;
    cout << "Enter the number of columns: ";
    cin >> cols;
    return {rows, cols};
}


vector<vector<int>> getMatrix(int rows, int cols) {
    vector<vector<int>> matrix(rows, vector<int>(cols));
    cout << "Enter matrix terrain costs e.g. for 2x2 enter 4 values. Press enter after each:\n";
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            cin >> matrix[i][j];
        }
    }
    return matrix;
}


void findMaxMinCost(const vector<vector<int>>& matrix, int& maxCost, int& minCost) {
    maxCost = matrix[0][0];
    minCost = matrix[0][0];
    for (const auto& row : matrix) { // auto-detect type
        for (int val : row) {
            if (val > maxCost) maxCost = val;
            if (val < minCost) minCost = val;
        }
    }
    cout << "Maximum Terrain Cost: " << maxCost << endl;
    cout << "Minimum Terrain Cost: " << minCost << endl;
}


vector<pair<int, int>> phase1Pathfinding(const vector<vector<int>>& matrix, int rows, int cols) {
    vector<pair<int, int>> path;
    int r = rows - 1;
    int c = 0;  // Start at bottom-left
    path.push_back({r, c});

    // Move to the midpoint of the top row
    while (r != 0 || c != cols / 2) {
        if (r > 0 && c < cols / 2) {
            if (matrix[r - 1][c] < matrix[r][c + 1]) {
                r--;
            } else {
                c++;
            }
        } else if (r > 0) {
            r--;
        } else if (c < cols / 2) {
            c++;
        }
        path.push_back({r, c}); // update path
    }

    return path;
}


vector<pair<int, int>> phase2Pathfinding(const vector<vector<int>>& matrix, int rows, int cols) {
    vector<pair<int, int>> path;
    int r = 0;
    int c = cols / 2;  // midpoint
    path.push_back({r, c}); // updatae path

    // Move to the bottom-right corner
    while (r != rows - 1 || c != cols - 1) {
        if (r < rows - 1 && c < cols - 1) {
            if (matrix[r + 1][c] < matrix[r][c + 1]) {
                r++;
            } else {
                c++;
            }
        } else if (r < rows - 1) {
            r++;
        } else if (c < cols - 1) {
            c++;
        }
        path.push_back({r, c}); // update path
    }
    return path;
}


int calculatePathCost(const vector<pair<int, int>>& path, const vector<vector<int>>& matrix) {
    int totalCost = 0;
    for (const auto& element : path) {
        totalCost += matrix[element.first][element.second];
    }
    return totalCost;
}


void displayMatrix(const vector<vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int val : row) {
            cout << val << " ";
        }
        cout << endl;
    }
}


int main() {
    int maxCost, minCost;
    auto [rows, cols] = getUserMatrix();
    vector<vector<int>> matrix = getMatrix(rows, cols);
    findMaxMinCost(matrix, maxCost, minCost);

    // Phase 1: From Bottom-Left to Midpoint
    vector<pair<int, int>> phase1Path = phase1Pathfinding(matrix, rows, cols);
    cout << "Phase 1 Path (Bottom-Left to Midpoint): ";
    for (const auto& cell : phase1Path) {
        cout << "(" << cell.first << ", " << cell.second << ") ";
    }
    cout << endl;

    // Phase 2: From Midpoint to Bottom-Right
    vector<pair<int, int>> phase2Path = phase2Pathfinding(matrix, rows, cols);
    cout << "Phase 2 Path (Midpoint to Bottom-Right): ";
    for (const auto& cell : phase2Path) {
        cout << "(" << cell.first << ", " << cell.second << ") ";
    }
    cout << endl;

    // Full path and total cost
    vector<pair<int, int>> fullPath = phase1Path; // include entire first path and then second from second element to the end
    fullPath.insert(fullPath.end(), phase2Path.begin() + 1, phase2Path.end());  // +1 because midpoint already included
    cout << "Full Path: ";
    for (const auto& cell : fullPath) {
        cout << "(" << cell.first << ", " << cell.second << ") ";
    }
    cout << endl;

    int totalCost = calculatePathCost(fullPath, matrix);
    cout << "Total Cost: " << totalCost << endl;

    displayMatrix(matrix);

    return 0;
}