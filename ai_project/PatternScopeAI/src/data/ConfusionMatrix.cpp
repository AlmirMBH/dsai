#include "ConfusionMatrix.h"
#include <iomanip>
#include <cmath>

ConfusionMatrix::ConfusionMatrix(int numClassesCount) : numClasses(numClassesCount), totalSamples(0) {
    matrix.resize(numClasses, std::vector<int>(numClasses, 0));
}

/**
 * Clear all recorded predictions from memory.
 */
void ConfusionMatrix::reset() {
    for (auto& matrixRow : matrix) {
        std::fill(matrixRow.begin(), matrixRow.end(), 0);
    }
    totalSamples = 0;
}

/**
 * Record a single prediction by comparing the actual 
 * category to the guessed category.
 */
void ConfusionMatrix::addPrediction(int trueLabelValue, int predictedLabelValue) {
    if (trueLabelValue >= 0 && trueLabelValue < numClasses && predictedLabelValue >= 0 && predictedLabelValue < numClasses) {
        matrix[trueLabelValue][predictedLabelValue]++;
        totalSamples++;
    }
}

/**
 * Display the grid of correct and incorrect predictions 
 * in the console.
 */
void ConfusionMatrix::print(std::ostream& outputStream) const {
    for (int rowIndex = 0; rowIndex < numClasses; ++rowIndex) {
        for (int colIndex = 0; colIndex < numClasses; ++colIndex) {
            outputStream << std::setw(4) << matrix[rowIndex][colIndex];
        }
        outputStream << "\n";
    }
}

/**
 * Calculate the total percentage of correct guesses.
 */
double ConfusionMatrix::getAccuracy() const {
    if (totalSamples == 0) {
        return 0.0;
    }
    int correctPredictionsCount = 0;
    for (int classIndex = 0; classIndex < numClasses; ++classIndex) {
        correctPredictionsCount += matrix[classIndex][classIndex];
    }
    return static_cast<double>(correctPredictionsCount) / totalSamples;
}

/**
 * Calculate how many guesses for a specific category 
 * were actually correct. (Precision)
 */
double ConfusionMatrix::getPrecision(int targetClassIndex) const {
    // Total number of times the model guessed this category.
    int totalPredictedAsClassCount = 0;
    for (int rowIndex = 0; rowIndex < numClasses; ++rowIndex) {
        totalPredictedAsClassCount += matrix[rowIndex][targetClassIndex];
    }
    // Return what percentage of those guesses were right.
    return totalPredictedAsClassCount == 0 ? 0 : static_cast<double>(matrix[targetClassIndex][targetClassIndex]) / totalPredictedAsClassCount;
}

/**
 * Calculate how many actual patterns of a category 
 * the system successfully found. (Recall)
 */
double ConfusionMatrix::getRecall(int targetClassIndex) const {
    // Total number of actual patterns that belong to this category in the data.
    int totalActualClassCount = 0;
    for (int colIndex = 0; colIndex < numClasses; ++colIndex) {
        totalActualClassCount += matrix[targetClassIndex][colIndex];
    }
    // Return what percentage of the actual patterns were correctly identified.
    return totalActualClassCount == 0 ? 0 : static_cast<double>(matrix[targetClassIndex][targetClassIndex]) / totalActualClassCount;
}

/**
 * Combine precision and recall into a single quality score. (F1 Score)
 */
double ConfusionMatrix::getF1Score(int targetClassIndex) const {
    double precisionValue = getPrecision(targetClassIndex);
    double recallValue = getRecall(targetClassIndex);
    // Use a mathematical average (harmonic mean) to balance finding patterns with being accurate.
    return (precisionValue + recallValue == 0) ? 0 : 2.0 * (precisionValue * recallValue) / (precisionValue + recallValue);
}

/**
 * Save the recorded predictions to a text file.
 */
void ConfusionMatrix::save(std::ostream& outputStream) const {
    outputStream << numClasses << " " << totalSamples << "\n";
    for (const auto& matrixRow : matrix) {
        for (int cellValue : matrixRow) {
            outputStream << cellValue << " ";
        }
        outputStream << "\n";
    }
}

/**
 * Load recorded predictions from a text file.
 */
void ConfusionMatrix::load(std::istream& inputStream) {
    inputStream >> numClasses >> totalSamples;
    matrix.assign(numClasses, std::vector<int>(numClasses));
    for (int rowIndex = 0; rowIndex < numClasses; rowIndex++) {
        for (int colIndex = 0; colIndex < numClasses; colIndex++) {
            inputStream >> matrix[rowIndex][colIndex];
        }
    }
}
