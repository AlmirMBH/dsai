#include "FeatureVector.h"
#include <cmath>
#include <algorithm>

FeatureVector::FeatureVector() {}

FeatureVector::FeatureVector(const std::vector<double>& f) : features(f) {}

FeatureVector::FeatureVector(size_t size) : features(size, 0.0) {}

/**
 * Retrieve a specific value from the list of numbers.
 */
double FeatureVector::get(size_t index) const {
    if (index < features.size()) {
        return features[index];
    }
    return 0.0;
}

/**
 * Set a specific value in the list of numbers.
 */
void FeatureVector::set(size_t index, double value) {
    if (index < features.size()) {
        features[index] = value;
    }
}

/**
 * Add a new value to the end of the list.
 */
void FeatureVector::add(double value) {
    features.push_back(value);
}

/**
 * Calculate how different two lists of numbers are.
 */
double FeatureVector::distance(const FeatureVector& other) const {
    if (features.size() != other.features.size()) {
        return 1e10;
    }
    
    double sum = 0.0;
    for (size_t i = 0; i < features.size(); ++i) {
        double diff = features[i] - other.features[i];
        sum += diff * diff;
    }
    return std::sqrt(sum);
}

/**
 * Save the list of numbers to a text file.
 */
void FeatureVector::save(std::ostream& os) const {
    os << features.size() << " ";
    for (double featureValue : features) {
        os << featureValue << " ";
    }
    os << "\n";
}

/**
 * Load a list of numbers from a text file.
 */
void FeatureVector::load(std::istream& is) {
    size_t dataSize;
    if (!(is >> dataSize)) {
        return;
    }
    features.resize(dataSize);
    for (size_t featureIndex = 0; featureIndex < dataSize; ++featureIndex) {
        is >> features[featureIndex];
    }
}

