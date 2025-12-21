#include "KNN.h"
#include <algorithm>

void KNN::train(const Dataset& dataset) {
    trainingData.clear();
    for (size_t sampleIndex = 0; sampleIndex < dataset.size(); ++sampleIndex) {
        trainingData.push_back({dataset.getFeatures(sampleIndex), dataset.getLabel(sampleIndex)});
    }
}

void KNN::addExample(const FeatureVector& features, int label) {
    trainingData.push_back({features, label});
}

int KNN::predict(const FeatureVector& features) {
    if (trainingData.empty()) return -1;
    
    std::vector<std::pair<double, int>> distances;
    for (int dataIndex = 0; dataIndex < trainingData.size(); dataIndex++) {
        distances.push_back({features.distance(trainingData[dataIndex].first), trainingData[dataIndex].second});
    }
    std::sort(distances.begin(), distances.end());
    
    std::vector<int> votes(10, 0);
    int neighborsToCheck = std::min(k, (int)distances.size());
    for (int neighborIndex = 0; neighborIndex < neighborsToCheck; ++neighborIndex) {
        votes[distances[neighborIndex].second]++;
    }
    
    int bestClass = 0;
    for (int classIndex = 1; classIndex < 10; classIndex++) {
        if (votes[classIndex] > votes[bestClass]) bestClass = classIndex;
    }
    return bestClass;
}

double KNN::getConfidence(const FeatureVector& features) {
    if (trainingData.empty()) return 0.0;
    
    std::vector<std::pair<double, int>> distances;
    for (int dataIndex = 0; dataIndex < trainingData.size(); dataIndex++) {
        distances.push_back({features.distance(trainingData[dataIndex].first), trainingData[dataIndex].second});
    }
    std::sort(distances.begin(), distances.end());
    
    std::vector<int> votes(10, 0);
    int neighborsToCheck = std::min(k, (int)distances.size());
    int maxVotes = 0;
    for (int neighborIndex = 0; neighborIndex < neighborsToCheck; ++neighborIndex) {
        int label = distances[neighborIndex].second;
        votes[label]++;
        if (votes[label] > maxVotes) maxVotes = votes[label];
    }
    return (double)maxVotes / neighborsToCheck;
}

void KNN::save(std::ostream& outputStream) const {
    outputStream << k << " " << trainingData.size() << "\n";
    for (auto& dataPair : trainingData) {
        for (double featureValue : dataPair.first.getFeatures()) outputStream << featureValue << " ";
        outputStream << dataPair.second << "\n";
    }
}

void KNN::load(std::istream& inputStream) {
    size_t dataSize;
    inputStream >> k >> dataSize;
    trainingData.clear();
    for (size_t sampleIndex = 0; sampleIndex < dataSize; sampleIndex++) {
        std::vector<double> featureValues(784);
        for (int featureIndex = 0; featureIndex < 784; featureIndex++) inputStream >> featureValues[featureIndex];
        int label; inputStream >> label;
        trainingData.push_back({FeatureVector(featureValues), label});
    }
}
