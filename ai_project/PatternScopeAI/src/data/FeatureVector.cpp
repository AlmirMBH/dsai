#include "FeatureVector.h"
#include <cmath>
#include <algorithm>

FeatureVector::FeatureVector() {}

FeatureVector::FeatureVector(const std::vector<double>& initialFeatures) : features(initialFeatures) {}

FeatureVector::FeatureVector(size_t size) : features(size, 0.0) {}

double FeatureVector::get(size_t index) const {
    if (index < features.size()) {
        return features[index];
    }
    return 0.0;
}

void FeatureVector::set(size_t index, double value) {
    if (index < features.size()) {
        features[index] = value;
    }
}

void FeatureVector::add(double value) {
    features.push_back(value);
}

double FeatureVector::distance(const FeatureVector& other) const {
    if (features.size() != other.features.size()) {
        return 1e10;
    }
    
    double sum = 0.0;
    for (size_t featureIndex = 0; featureIndex < features.size(); ++featureIndex) {
        double diff = features[featureIndex] - other.features[featureIndex];
        sum += diff * diff;
    }
    return std::sqrt(sum);
}

void FeatureVector::save(std::ostream& outputStream) const {
    outputStream << features.size() << " ";
    for (double featureValue : features) {
        outputStream << featureValue << " ";
    }
    outputStream << "\n";
}

void FeatureVector::load(std::istream& inputStream) {
    size_t dataSize;
    if (!(inputStream >> dataSize)) {
        return;
    }
    features.resize(dataSize);
    for (size_t featureIndex = 0; featureIndex < dataSize; ++featureIndex) {
        inputStream >> features[featureIndex];
    }
}

