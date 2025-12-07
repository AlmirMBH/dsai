#include "Dataset.h"

void Dataset::add(const FeatureVector& features, int label) {
    data.push_back(std::make_pair(features, label));
}

const FeatureVector& Dataset::getFeatures(size_t index) const {
    return data[index].first;
}

int Dataset::getLabel(size_t index) const {
    return data[index].second;
}

std::vector<int> Dataset::getLabels() const {
    std::vector<int> labels;
    labels.reserve(data.size());
    for (const auto& pair : data) {
        labels.push_back(pair.second);
    }
    return labels;
}

void Dataset::clear() {
    data.clear();
}

