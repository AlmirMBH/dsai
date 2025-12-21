#include "KNN.h"
#include <algorithm>

/**
 * Store all patterns from the dataset into memory. 
 * Use these patterns later to find the closest matches.
 */
void KNN::train(const Dataset& dataset) {
    trainingData.clear();
    for (size_t sampleIndex = 0; sampleIndex < dataset.size(); ++sampleIndex) {
        trainingData.push_back({dataset.getFeatures(sampleIndex), dataset.getLabel(sampleIndex)});
    }
}

/**
 * Add one new pattern to the memory during runtime.
 */
void KNN::addExample(const FeatureVector& features, int label) {
    trainingData.push_back({features, label});
}

/**
 * Find the closest patterns in memory to the new image. 
 * Return the most common category among the closest matches.
 */
int KNN::predict(const FeatureVector& features) {
    if (trainingData.empty()) {
        return -1;
    }
    
    std::vector<std::pair<double, int>> distances;
    for (int dataIndex = 0; dataIndex < (int)trainingData.size(); dataIndex++) {
        distances.push_back({features.distance(trainingData[dataIndex].first), trainingData[dataIndex].second});
    }
    std::sort(distances.begin(), distances.end());
    
    // Use 10 as the size because the system recognizes digits from 0 to 9.
    std::vector<int> votes(10, 0);
    int neighborsToCheck = std::min(k, (int)distances.size());
    for (int neighborIndex = 0; neighborIndex < neighborsToCheck; ++neighborIndex) {
        votes[distances[neighborIndex].second]++;
    }
    
    int bestClass = 0;
    for (int classIndex = 1; classIndex < 10; classIndex++) {
        if (votes[classIndex] > votes[bestClass]) {
            bestClass = classIndex;
        }
    }
    return bestClass;
}

/**
 * Calculate how certain the model is about its guess. 
 * Check how many of the closest matches belong to the same category.
 */
double KNN::getConfidence(const FeatureVector& features) {
    if (trainingData.empty()) {
        return 0.0;
    }
    
    std::vector<std::pair<double, int>> distances;
    for (int dataIndex = 0; dataIndex < (int)trainingData.size(); dataIndex++) {
        distances.push_back({features.distance(trainingData[dataIndex].first), trainingData[dataIndex].second});
    }
    std::sort(distances.begin(), distances.end());
    
    // Use 10 as the size because the system recognizes digits from 0 to 9.
    std::vector<int> votes(10, 0);
    int neighborsToCheck = std::min(k, (int)distances.size());
    int maxVotes = 0;
    for (int neighborIndex = 0; neighborIndex < neighborsToCheck; ++neighborIndex) {
        int label = distances[neighborIndex].second;
        votes[label]++;
        if (votes[label] > maxVotes) {
            maxVotes = votes[label];
        }
    }
    return (double)maxVotes / neighborsToCheck;
}

/**
 * Save all stored patterns from memory to a text file.
 */
void KNN::save(std::ostream& outputStream) const {
    outputStream << k << " " << trainingData.size() << "\n";
    for (auto& dataPair : trainingData) {
        for (double featureValue : dataPair.first.getFeatures()) {
            outputStream << featureValue << " ";
        }
        outputStream << dataPair.second << "\n";
    }
}

/**
 * Load patterns from a text file into memory.
 */
void KNN::load(std::istream& inputStream) {
    size_t dataSize;
    inputStream >> k >> dataSize;
    trainingData.clear();
    for (size_t sampleIndex = 0; sampleIndex < dataSize; sampleIndex++) {
        // Create a list for 784 numbers because each image is 28 pixels wide and 28 pixels tall.
        std::vector<double> featureValues(784);
        for (int featureIndex = 0; featureIndex < 784; featureIndex++) {
            inputStream >> featureValues[featureIndex];
        }
        int label; 
        inputStream >> label;
        trainingData.push_back({FeatureVector(featureValues), label});
    }
}
