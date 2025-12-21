#include "FeatureVector.h"
#include <cmath>
#include <algorithm>

FeatureVector::FeatureVector() {}

FeatureVector::FeatureVector(const std::vector<double>& f) : features(f) {}

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
    for (size_t i = 0; i < features.size(); ++i) {
        double diff = features[i] - other.features[i];
        sum += diff * diff;
    }
    return std::sqrt(sum);
}

void FeatureVector::save(std::ostream& os) const {
    size_t s = features.size();
    os.write(reinterpret_cast<const char*>(&s), sizeof(s));
    os.write(reinterpret_cast<const char*>(features.data()), s * sizeof(double));
}

void FeatureVector::load(std::istream& is) {
    size_t s;
    is.read(reinterpret_cast<char*>(&s), sizeof(s));
    features.resize(s);
    is.read(reinterpret_cast<char*>(features.data()), s * sizeof(double));
}

