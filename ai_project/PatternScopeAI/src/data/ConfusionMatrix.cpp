#include "ConfusionMatrix.h"
#include <iomanip>
#include <cmath>

ConfusionMatrix::ConfusionMatrix(int numClasses) : numClasses(numClasses), totalSamples(0) {
    matrix.resize(numClasses, std::vector<int>(numClasses, 0));
}

void ConfusionMatrix::reset() {
    for (auto& row : matrix) {
        std::fill(row.begin(), row.end(), 0);
    }
    totalSamples = 0;
}

void ConfusionMatrix::addPrediction(int trueLabel, int predictedLabel) {
    if (trueLabel >= 0 && trueLabel < numClasses && 
        predictedLabel >= 0 && predictedLabel < numClasses) {
        matrix[trueLabel][predictedLabel]++;
        totalSamples++;
    }
}

void ConfusionMatrix::print(std::ostream& os) const {
    os << "\nConfusion Matrix:\n";
    os << "     ";
    for (int i = 0; i < numClasses; ++i) {
        os << std::setw(4) << i;
    }
    os << "\n";
    
    for (int i = 0; i < numClasses; ++i) {
        os << std::setw(4) << i << " ";
        for (int j = 0; j < numClasses; ++j) {
            os << std::setw(4) << matrix[i][j];
        }
        os << "\n";
    }
}

double ConfusionMatrix::getAccuracy() const {
    if (totalSamples == 0) return 0.0;
    int correct = 0;
    for (int i = 0; i < numClasses; ++i) {
        correct += matrix[i][i];
    }
    return static_cast<double>(correct) / totalSamples;
}

double ConfusionMatrix::getPrecision(int classIndex) const {
    if (classIndex < 0 || classIndex >= numClasses) return 0.0;
    int predicted = 0;
    for (int i = 0; i < numClasses; ++i) {
        predicted += matrix[i][classIndex];
    }
    if (predicted == 0) return 0.0;
    return static_cast<double>(matrix[classIndex][classIndex]) / predicted;
}

double ConfusionMatrix::getRecall(int classIndex) const {
    if (classIndex < 0 || classIndex >= numClasses) return 0.0;
    int actual = 0;
    for (int j = 0; j < numClasses; ++j) {
        actual += matrix[classIndex][j];
    }
    if (actual == 0) return 0.0;
    return static_cast<double>(matrix[classIndex][classIndex]) / actual;
}

double ConfusionMatrix::getF1Score(int classIndex) const {
    double precision = getPrecision(classIndex);
    double recall = getRecall(classIndex);
    if (precision + recall == 0.0) return 0.0;
    return 2.0 * (precision * recall) / (precision + recall);
}

