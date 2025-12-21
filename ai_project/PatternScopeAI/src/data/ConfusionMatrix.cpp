#include "ConfusionMatrix.h"
#include <iomanip>
#include <cmath>

ConfusionMatrix::ConfusionMatrix(int numClassesCount) : numClasses(numClassesCount), totalSamples(0) {
    matrix.resize(numClasses, std::vector<int>(numClasses, 0));
}

void ConfusionMatrix::reset() {
    for (auto& matrixRow : matrix) std::fill(matrixRow.begin(), matrixRow.end(), 0);
    totalSamples = 0;
}

void ConfusionMatrix::addPrediction(int trueLabelValue, int predictedLabelValue) {
    if (trueLabelValue >= 0 && trueLabelValue < numClasses && predictedLabelValue >= 0 && predictedLabelValue < numClasses) {
        matrix[trueLabelValue][predictedLabelValue]++;
        totalSamples++;
    }
}

void ConfusionMatrix::print(std::ostream& outputStream) const {
    for (int rowIndex = 0; rowIndex < numClasses; ++rowIndex) {
        for (int colIndex = 0; colIndex < numClasses; ++colIndex) outputStream << std::setw(4) << matrix[rowIndex][colIndex];
        outputStream << "\n";
    }
}

double ConfusionMatrix::getAccuracy() const {
    if (totalSamples == 0) return 0.0;
    int correctPredictionsCount = 0;
    for (int classIndex = 0; classIndex < numClasses; ++classIndex) correctPredictionsCount += matrix[classIndex][classIndex];
    return static_cast<double>(correctPredictionsCount) / totalSamples;
}

double ConfusionMatrix::getPrecision(int targetClassIndex) const {
    int totalPredictedAsClassCount = 0;
    for (int rowIndex = 0; rowIndex < numClasses; ++rowIndex) totalPredictedAsClassCount += matrix[rowIndex][targetClassIndex];
    return totalPredictedAsClassCount == 0 ? 0 : static_cast<double>(matrix[targetClassIndex][targetClassIndex]) / totalPredictedAsClassCount;
}

double ConfusionMatrix::getRecall(int targetClassIndex) const {
    int totalActualClassCount = 0;
    for (int colIndex = 0; colIndex < numClasses; ++colIndex) totalActualClassCount += matrix[targetClassIndex][colIndex];
    return totalActualClassCount == 0 ? 0 : static_cast<double>(matrix[targetClassIndex][targetClassIndex]) / totalActualClassCount;
}

double ConfusionMatrix::getF1Score(int targetClassIndex) const {
    double precisionValue = getPrecision(targetClassIndex);
    double recallValue = getRecall(targetClassIndex);
    return (precisionValue + recallValue == 0) ? 0 : 2.0 * (precisionValue * recallValue) / (precisionValue + recallValue);
}

void ConfusionMatrix::save(std::ostream& outputStream) const {
    outputStream << numClasses << " " << totalSamples << "\n";
    for (const auto& matrixRow : matrix) {
        for (int cellValue : matrixRow) outputStream << cellValue << " ";
        outputStream << "\n";
    }
}

void ConfusionMatrix::load(std::istream& inputStream) {
    inputStream >> numClasses >> totalSamples;
    matrix.assign(numClasses, std::vector<int>(numClasses));
    for (int rowIndex = 0; rowIndex < numClasses; rowIndex++) {
        for (int colIndex = 0; colIndex < numClasses; colIndex++) inputStream >> matrix[rowIndex][colIndex];
    }
}
