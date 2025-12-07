#include "KNN.h"

KNN::KNN(int k) : k(k) {}

void KNN::train(const Dataset& dataset) {
    trainingData.clear();
    for (size_t i = 0; i < dataset.size(); ++i) {
        trainingData.push_back(std::make_pair(dataset.getFeatures(i), dataset.getLabel(i)));
    }
}

int KNN::predict(const FeatureVector& features) {
    if (trainingData.empty()) {
        return -1;
    }
    
    std::vector<std::pair<double, int>> distances;
    for (const auto& pair : trainingData) {
        double dist = features.distance(pair.first);
        distances.push_back(std::make_pair(dist, pair.second));
    }
    
    std::sort(distances.begin(), distances.end());
    
    int kActual = std::min(k, static_cast<int>(distances.size()));
    std::vector<int> votes(10, 0);
    
    for (int i = 0; i < kActual; ++i) {
        int label = distances[i].second;
        if (label >= 0 && label < 10) {
            votes[label]++;
        }
    }
    
    int maxVotes = 0;
    int predictedLabel = 0;
    for (int i = 0; i < 10; ++i) {
        if (votes[i] > maxVotes) {
            maxVotes = votes[i];
            predictedLabel = i;
        }
    }
    
    return predictedLabel;
}

double KNN::getConfidence(const FeatureVector& features) {
    if (trainingData.empty()) {
        return 0.0;
    }
    
    std::vector<std::pair<double, int>> distances;
    for (const auto& pair : trainingData) {
        double dist = features.distance(pair.first);
        distances.push_back(std::make_pair(dist, pair.second));
    }
    
    std::sort(distances.begin(), distances.end());
    
    int kActual = std::min(k, static_cast<int>(distances.size()));
    std::vector<int> votes(10, 0);
    
    for (int i = 0; i < kActual; ++i) {
        int label = distances[i].second;
        if (label >= 0 && label < 10) {
            votes[label]++;
        }
    }
    
    int maxVotes = 0;
    for (int i = 0; i < 10; ++i) {
        if (votes[i] > maxVotes) {
            maxVotes = votes[i];
        }
    }
    
    return static_cast<double>(maxVotes) / kActual;
}

void KNN::addExample(const FeatureVector& features, int label) {
    trainingData.push_back(std::make_pair(features, label));
}

